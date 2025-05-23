from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlalchemy
from sqlalchemy import create_engine, inspect
import pandas as pd

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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

# Database connection inputs
db_type = st.selectbox("Database Type", ["mysql", "postgresql", "sqlite"])
db_user = st.text_input("Username")
db_password = st.text_input("Password", type="password")
db_host = st.text_input("Host", "localhost")
db_port = st.text_input("Port", "3306" if db_type == "mysql" else "5432" if db_type == "postgresql" else "")
db_name = st.text_input("Database Name")

conn_status = st.empty()
schema_prompt = ""

if st.button("Connect to Database"):
    try:
        if db_type == "sqlite":
            engine = create_engine(f"sqlite:///{db_name}")
        elif db_type == "mysql":
            # Using pymysql driver
            engine = create_engine(
                f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            )
        elif db_type == "postgresql":
            engine = create_engine(
                f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            )
        
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
        
        Examples:
        Q: How many students in Data Science?
        A: SELECT COUNT(*) FROM student WHERE class = 'Data Science'
        
        Q: Show students with marks > 80 in CS?
        A: SELECT s.name, m.marks 
           FROM student s 
           INNER JOIN marks m ON s.id = m.student_id 
           WHERE m.marks > 80 AND s.class = 'CS'
        """
        
        st.session_state.base_prompt = base_prompt
        
    except ModuleNotFoundError as e:
        missing_module = str(e).split("'")[1]
        conn_status.error(f"❌ Missing driver: Install required package with:\n`pip install {missing_module}`")
    except Exception as e:
        conn_status.error(f"❌ Connection failed: {e}")

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