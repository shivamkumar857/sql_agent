from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlalchemy
from sqlalchemy import create_engine, inspect
import pandas as pd
import google.generativeai as genai

# Configure page
st.set_page_config(page_title="Database Conversational AI", layout="wide")

# Sidebar for database information and tips
with st.sidebar:
    st.title("Database Connection Guide")
    st.markdown("""
    ### MySQL Users
    For MySQL connections, use one of these free services:
    1. [PlanetScale](https://planetscale.com/) (Recommended)
    2. [Railway.app](https://railway.app)
    3. [AWS RDS](https://aws.amazon.com/rds/)
    
    ### PostgreSQL Users
    For PostgreSQL, you can use:
    1. [Render](https://render.com) (Recommended)
    2. [Railway.app](https://railway.app)
    3. [ElephantSQL](https://www.elephantsql.com/)
    
    ### Connection Tips
    - Never use 'localhost' in cloud deployment
    - Enable SSL for secure connections
    - Use strong passwords
    - Keep your credentials secure
    """)

# Configure Gemini AI
try:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets["GOOGLE_API_KEY"]
    if not GOOGLE_API_KEY:
        st.error("⚠️ Google API Key is not configured. Please set it in the secrets.")
    else:
        genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error("⚠️ Error accessing Google API Key. Please check your secrets configuration.")

# Database configuration from secrets (for development/testing)
try:
    DB_CONFIG = {
        'user': os.getenv('DB_USER') or st.secrets["DB_USER"],
        'password': os.getenv('DB_PASSWORD') or st.secrets["DB_PASSWORD"],
        'host': os.getenv('DB_HOST') or st.secrets["DB_HOST"],
        'port': os.getenv('DB_PORT') or st.secrets["DB_PORT"],
        'database': os.getenv('DB_NAME') or st.secrets["DB_NAME"],
        'db_type': os.getenv('DB_TYPE') or st.secrets.get("DB_TYPE", "postgresql")
    }
except Exception as e:
    DB_CONFIG = {
        'user': '',
        'password': '',
        'host': '',
        'port': '5432',
        'database': '',
        'db_type': 'postgresql'
    }
    st.warning("⚠️ No database configuration found in secrets. Please enter database credentials manually.")

def get_db_schema(engine):
    inspector = inspect(engine)
    schema = []
    
    for table_name in inspector.get_table_names():
        columns = []
        for column in inspector.get_columns(table_name):
            columns.append(f"{column['name']} ({column['type']})")
        schema.append(f"Table '{table_name}' has columns: {', '.join(columns)}")
        
        # Add foreign key information
        fks = inspector.get_foreign_keys(table_name)
        if fks:
            fk_info = []
            for fk in fks:
                fk_info.append(
                    f"Foreign key {fk['constrained_columns']} references {fk['referred_table']}({fk['referred_columns']})"
                )
            schema.append(f"  Relationships: {'; '.join(fk_info)}")
    
    return "\n".join(schema)

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    response = model.generate_content([prompt, question])
    return response.text.strip().replace('```sql', '').replace('```', '')

def execute_query(query, engine):
    try:
        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.text(query))
            rows = result.fetchall()
            return rows if len(rows) > 0 else None
    except Exception as e:
        print(f"Database error: {e}")
        return None

def create_connection_string(db_type, user, password, host, port, database, use_ssl=True):
    """Create a database connection string based on the database type."""
    if db_type == "postgresql":
        conn_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        if use_ssl:
            conn_string += "?sslmode=require"
    elif db_type == "mysql":
        conn_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        if use_ssl:
            conn_string += "?ssl=true"
    else:  # sqlite
        conn_string = f"sqlite:///{database}"
    return conn_string

# Main UI
st.title("Ask Your Database Anything")
st.markdown("---")

# Add connection type selector
connection_type = st.radio(
    "Choose connection method:",
    ["Enter Database Credentials", "Use Saved Configuration"],
    help="Select how you want to connect to your database"
)

# Database connection inputs
if connection_type == "Enter Database Credentials":
    st.info("⚠️ Make sure your database is accessible from the internet if you're using this deployed app.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        db_type = st.selectbox(
            "Database Type", 
            ["mysql", "postgresql"],
            help="Choose your database type. For MySQL, we recommend PlanetScale. For PostgreSQL, we recommend Render."
        )
        db_user = st.text_input("Username")
        db_password = st.text_input("Password", type="password")
    
    with col2:
        db_host = st.text_input("Host")
        db_port = st.text_input("Port", "3306" if db_type == "mysql" else "5432")
        db_name = st.text_input("Database Name")
    
    # Show connection string example
    if db_type == "mysql":
        st.info("""
        ### MySQL Connection Guide
        1. Get a free database from [PlanetScale](https://planetscale.com)
        2. Use the connection details provided by PlanetScale
        3. Format: `mysql+pymysql://username:password@host:3306/database`
        """)
    else:
        st.info("""
        ### PostgreSQL Connection Guide
        1. Get a free database from [Render](https://render.com)
        2. Use the connection details provided by Render
        3. Format: `postgresql://username:password@host:5432/database`
        """)
    
    # Add SSL option for secure connection
    use_ssl = st.checkbox("Use SSL Connection", value=True)
else:
    if not any(DB_CONFIG.values()):
        st.error("⚠️ No saved configuration found. Please configure the database credentials in the app secrets or use manual entry.")
        st.stop()
    else:
        db_type = DB_CONFIG['db_type']
        db_user = DB_CONFIG['user']
        db_password = DB_CONFIG['password']
        db_host = DB_CONFIG['host']
        db_port = DB_CONFIG['port']
        db_name = DB_CONFIG['database']
        use_ssl = True
        st.success("✅ Using saved database configuration")

        # Display current configuration (without sensitive data)
        st.info(f"""Current Configuration:
        - Type: {db_type}
        - Host: {db_host}
        - Port: {db_port}
        - Database: {db_name}
        - User: {db_user}
        """)

conn_status = st.empty()
schema_prompt = ""

if st.button("Connect to Database"):
    try:
        connection_string = create_connection_string(
            db_type, db_user, db_password, db_host, db_port, db_name, use_ssl
        )
        engine = create_engine(connection_string)
        
        # Test connection
        with engine.connect() as conn:
            pass
        
        schema_prompt = get_db_schema(engine)
        conn_status.success("✅ Connected successfully!")
        
        # Store engine in session state
        st.session_state.engine = engine
        
        # Generate dynamic prompt
        base_prompt = f"""You are a SQL expert that converts English to SQL. Database schema:
        {schema_prompt}
        
        Rules:
        1. Use ONLY existing tables/columns
        2. Prefer INNER JOINs over subqueries
        3. Use table aliases for joins
        4. Handle ambiguous columns with table prefixes
        5. Return only valid SQL without markdown
        6. If no results found, query should still be valid
        """
        
        st.session_state.base_prompt = base_prompt
        
    except ModuleNotFoundError as e:
        missing_module = str(e).split("'")[1]
        conn_status.error(f"❌ Missing driver: Install required package with:\n`pip install {missing_module}`")
    except Exception as e:
        conn_status.error(f"❌ Connection failed: {e}")
        if "Can't connect to MySQL server" in str(e) or "could not connect to server" in str(e):
            st.error("⚠️ Database Connection Error:")
            st.error("1. Check if your database is accessible from the internet")
            st.error("2. Verify your connection credentials")
            st.error("3. Make sure the database service is running")
            if "localhost" in str(e):
                st.warning("""
                ⚠️ You're using 'localhost' which won't work in cloud deployment.
                
                For MySQL, use one of these free services:
                - [PlanetScale](https://planetscale.com)
                - [Railway.app](https://railway.app)
                
                For PostgreSQL, use:
                - [Render](https://render.com)
                - [ElephantSQL](https://www.elephantsql.com)
                """)

st.markdown("---")
question = st.text_input("Ask your question:")
if st.button("Generate Query") and 'engine' in st.session_state:
    try:
        response = get_gemini_response(question, st.session_state.base_prompt)
        st.code(f"Generated SQL:\n{response}")
        
        # Execute query
        result = execute_query(response, st.session_state.engine)
        
        if result is None:
            st.warning("No results found")
        else:
            # Display as table
            with st.session_state.engine.connect() as conn:
                df = pd.read_sql(response, conn)
                st.dataframe(df)
                
    except Exception as e:
        st.error(f"Error: {str(e)}")