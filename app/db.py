# app/db.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv # ---> REMOVE load_dotenv from here <---
import os
import sys # For exiting if config is missing

# load_dotenv() # ---> REMOVE load_dotenv from here <---

# This code now runs when db.py is imported by mcp_handler,
# which happens AFTER main.py has already called load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# ---> Add Validation <---
if DATABASE_URL is None:
    print("FATAL ERROR: DATABASE_URL environment variable not set or .env not loaded correctly.")
    # Optionally provide more specific guidance
    print("Ensure .env file exists and load_dotenv() is called correctly in main.py before imports.")
    sys.exit("Database configuration missing.") # Exit if DB URL is essential

print("--- app/db.py: DATABASE_URL loaded:", DATABASE_URL[:30] + "...") # Print prefix for confirmation, avoid logging full creds

# Engine creation should now succeed if DATABASE_URL is valid
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"FATAL ERROR: Failed to create SQLAlchemy engine: {e}")
    print(f"Check the format and content of your DATABASE_URL: {DATABASE_URL[:30] + '...'}")
    sys.exit("Database engine creation failed.")


def execute_sql_query(query: str):
    # Use a try-except block specifically around connection/execution
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            # Convert rows to dictionaries for easier handling/serialization
            # Use _mapping attribute for RowProxy objects from text() queries
            return [row._mapping for row in result]
    except Exception as e:
        print(f"Error during SQL execution in db.py: {e}")
        # Return a more structured error, maybe just the error string
        return [{"error": str(e)}] # Keep the previous error return format if the agent expects it