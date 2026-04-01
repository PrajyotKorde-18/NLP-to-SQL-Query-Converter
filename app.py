import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent

load_dotenv()
st.set_page_config(page_title="NL2SQL Assistant", layout="wide")

# Premium UI Styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 100%);
        color: #f0f0f0;
    }
    .stChatFloatingInputContainer {
        bottom: 20px;
    }
    div[data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #333;
    }
    .stMarkdown p {
        font-size: 1.1rem;
        line-height: 1.6;
    }
    /* Style Chat bubbles */
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Text-to-SQL Assistant")
st.markdown("##### Chat with your Database in plain English")

with st.sidebar:
    st.header("Configuration")
    
    provider = st.radio("Select Provider", ["Google Gemini", "Groq"], index=1)
    
    if provider == "Google Gemini":
        google_keys_raw = os.getenv("GOOGLE_API_KEY", "")
        api_key = st.text_input("Google AI API Key(s)", value=google_keys_raw, type="password", help="You can provide multiple keys separated by commas for rotation.")
        model_name = "gemini-3-flash-preview"
        st.info("Using gemini-3-flash-preview")
        
        # Display number of keys detected
        keys_list = [k.strip() for k in api_key.split(",") if k.strip()]
        if len(keys_list) > 1:
            st.info(f"🔄 Rotating between {len(keys_list)} Google API keys.")
    else:
        groq_keys_raw = os.getenv("GROQ_API_KEY", "")
        api_key = st.text_input("Groq API Key(s)", value=groq_keys_raw, type="password", help="You can provide multiple keys separated by commas for rotation.")
        
        model_name = "llama-3.3-70b-versatile"
        st.info("Using llama-3.3-70b-versatile")
        
        # Display number of keys detected
        keys_list = [k.strip() for k in api_key.split(",") if k.strip()]
        if len(keys_list) > 1:
            st.info(f"🔄 Rotating between {len(keys_list)} Groq API keys.")
    
    st.markdown("---")
    st.markdown("### System Architecture")
    st.write("**Mode:** Schema-Grounded RAG (NL2SQL)")
    allow_write = st.checkbox("Enable Write Access (Danger)", value=False, help="Allows creating/dropping tables and databases via NL.")
    st.caption("This system uses dynamic schema retrieval to ground the LLM in your database structure.")
    
    st.markdown("---")
    st.markdown("### Database Info")
    host = st.text_input("Host", value='localhost')
    port = st.text_input("Port", value='3306')
    username = st.text_input("Username", value='root')
    password = st.text_input("Password", value='root', type='password')
    database_schema = st.text_input("Database (Optional)", value='text_to_sql', help="Leave empty to connect to the server and create a new database.")
    
    if database_schema:
        st.info(f"Connecting to Database: {username}@{host}/{database_schema}")
        engine_str = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_schema}"
    else:
        st.info(f"Connecting to Server (No Database selected): {username}@{host}:{port}")
        # Default to 'mysql' database to allow administrative commands like CREATE DATABASE
        engine_str = f"mysql+pymysql://{username}:{password}@{host}:{port}/mysql"
        
    try:
        db = SQLDatabase.from_uri(engine_str)
        tables = db.get_usable_table_names()
        st.success("✓ Connection established.")
        if database_schema:
            st.write("Available Tables:")
            for t in tables:
                st.write(f"- {t}")
    except Exception as e:
        st.error(f"Error communicating with DB: {e}")
        db = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question about your database (e.g. How many products are there?)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not api_key:
        st.error(f"Please enter your {provider} Key in the sidebar.")
    elif db is None:
        st.error("Database connection not ready.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Executing agent..."):
                current_keys = [k.strip() for k in api_key.split(",") if k.strip()]
                success = False
                
                for i, key in enumerate(current_keys):
                    try:
                        # Use selected model with broad safety settings for free tier compatibility
                        if provider == "Google Gemini":
                            llm = ChatGoogleGenerativeAI(
                                model=model_name, 
                                api_key=key,
                                safety_settings={
                                    "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                                    "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                                    "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                                    "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
                                }
                            )
                        else:
                            llm = ChatGroq(
                                model_name=model_name,
                                groq_api_key=key,
                                temperature=0
                            )
                        
                        # This toolkit provides Schema-Grounded generation
                        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
                        
                        # Dynamic System Prompt based on Write Access
                        write_policy = "DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database."
                        if allow_write:
                            write_policy = "You are AUTHORED to fulfill CREATE, DROP, and DELETE requests for tables or databases if the user asks. Proceed with caution."

                        sql_prefix = f"""You are a strict SQL Database agent. 
You can interact with a SQL database using the provided tools.
You are AUTHORED to fully manage the database including:
- Creating new databases (CREATE DATABASE ...)
- Creating tables (CREATE TABLE ...)
- Inserting data (INSERT INTO ...)
- Querying data (SELECT ...)

{write_policy}

IMPORTANT: 
- ALWAYS look at the tables first using 'sql_db_list_tables'.
- If the current connection is to the server (no specific database selected), you are free to create a new database.
- You MUST only use the exact tool format provided. Do not use tags like <function> or invent your own syntax.
- If you create a new database, notify the user that they should update the 'Database' field in the sidebar to work within it."""
                        system_message = sql_prefix.format(dialect=db.dialect, top_k=5)
                        
                        # Create agent
                        agent_executor = create_react_agent(llm, toolkit.get_tools(), prompt=system_message)
                        
                        events = agent_executor.stream(
                            {"messages": [("user", prompt)]},
                            stream_mode="values",
                        )
                        
                        final_response = ""
                        for event in events:
                            msg = event["messages"][-1]
                            if hasattr(msg, "content"):
                                content = msg.content
                                if isinstance(content, list):
                                    final_response = "".join([str(p.get("text", "")) if isinstance(p, dict) else str(p) for p in content])
                                else:
                                    final_response = content
                        
                        if isinstance(final_response, str):
                            st.markdown(final_response)
                            st.session_state.messages.append({"role": "assistant", "content": final_response})
                        else:
                            st.write(final_response)
                            st.session_state.messages.append({"role": "assistant", "content": str(final_response)})
                        
                        success = True
                        break # Success! Exit key loop
                        
                    except Exception as e:
                        # Log error for this key
                        error_str = str(e)
                        if "rate_limit" in error_str.lower() or "limit_reached" in error_str.lower() or "429" in error_str:
                            if i < len(current_keys) - 1:
                                st.warning(f"⚠️ API Key {i+1} reached rate limit. Switching to key {i+2}...")
                                continue # Try next key
                            else:
                                st.error(f"❌ All {len(current_keys)} API keys have reached their rate limits.")
                        else:
                            st.error(f"Error: {e}")
                            break # Non-rate-limit error, don't retry with other keys
