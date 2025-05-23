from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlalchemy
from sqlalchemy import create_engine, inspect
import pandas as pd
import google.generativeai as genai

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
        'database': os.getenv('DB_NAME') or st.secrets["DB_NAME"]
    }
except Exception as e:
    DB_CONFIG = {
        'user': '',
        'password': '',
        'host': '',
        'port': '3306',
        'database': ''
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

# Streamlit UI
st.set_page_config(page_title="Database Conversational AI")
st.header("Ask Your Database Anything")

# Add connection type selector
connection_type = st.radio(
    "Choose connection method:",
    ["Enter Database Credentials", "Use Saved Configuration"],
    help="Select how you want to connect to your database"
)

# Database connection inputs
if connection_type == "Enter Database Credentials":
    st.info("⚠️ Make sure your database is accessible from the internet if you're using this deployed app.")
    
    db_type = st.selectbox("Database Type", ["mysql", "postgresql", "sqlite"])
    db_user = st.text_input("Username")
    db_password = st.text_input("Password", type="password")
    db_host = st.text_input("Host")
    db_port = st.text_input("Port", "3306" if db_type == "mysql" else "5432" if db_type == "postgresql" else "")
    db_name = st.text_input("Database Name")
    
    # Show connection string example
    if db_type == "mysql":
        st.info(f"Connection string format: mysql+pymysql://username:password@host:3306/database")
    elif db_type == "postgresql":
        st.info(f"Connection string format: postgresql+psycopg2://username:password@host:5432/database")
    
    # Add SSL option for secure connection
    use_ssl = st.checkbox("Use SSL Connection", value=True)
else:
    if not any(DB_CONFIG.values()):
        st.error("⚠️ No saved configuration found. Please configure the database credentials in the app secrets or use manual entry.")
        st.stop()
    else:
        db_type = "mysql"  # Since we're using MySQL
        db_user = DB_CONFIG['user']
        db_password = DB_CONFIG['password']
        db_host = DB_CONFIG['host']
        db_port = DB_CONFIG['port']
        db_name = DB_CONFIG['database']
        use_ssl = True
        st.success("✅ Using saved database configuration")

        # Display current configuration (without sensitive data)
        st.info(f"""Current Configuration:
        - Host: {db_host}
        - Port: {db_port}
        - Database: {db_name}
        - User: {db_user}
        """)

conn_status = st.empty()
schema_prompt = ""

if st.button("Connect to Database"):
    try:
        if db_type == "sqlite":
            engine = create_engine(f"sqlite:///{db_name}")
        elif db_type == "mysql":
            # Using pymysql driver with SSL if enabled
            connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            if use_ssl:
                connection_string += "?ssl=true"
            engine = create_engine(connection_string)
        elif db_type == "postgresql":
            # Using psycopg2 driver with SSL if enabled
            connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            if use_ssl:
                connection_string += "?sslmode=require"
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
        if "Can't connect to MySQL server" in str(e):
            st.error("⚠️ Make sure your database server:")
            st.error("1. Is accessible from the internet")
            st.error("2. Has the correct firewall rules to allow incoming connections")
            st.error("3. Has the user's IP whitelisted")
            st.error("\nNote: 'localhost' will not work in cloud deployment. You need a publicly accessible database.")

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