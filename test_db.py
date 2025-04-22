from sqlalchemy import create_engine, text
import urllib

# --- Connection String Setup ---
driver_name = "ODBC Driver 17 for SQL Server"
quoted_driver = urllib.parse.quote_plus(driver_name)
DATABASE_URL = f"mssql+pyodbc://sa:s7t4iJgb4t7Fd0ILx5u10zT@localhost\\SQL_STEFANO/TEST_STEFANO?driver={quoted_driver}"

print(f"Attempting to connect with URL: {DATABASE_URL}")
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Option 1: Change alias AND remove semicolon (Most likely to work)
        query = text("SELECT GETDATE() AS db_time") # Changed alias, removed ;

        # Option 2: Just remove semicolon
        # query = text("SELECT GETDATE() AS current_time") # Removed ;

        # Option 3: Simplest query (remove alias and semicolon)
        # query = text("SELECT GETDATE()")

        print(f"Executing query: {query}") # See what's being sent
        result = conn.execute(query)
        print("✅ Connection and Execution successful!")
        for row in result:
            # Access using the NEW alias if you changed it (or index 0 if removed)
            print("Current time from DB:", row.db_time) # Use 'db_time' if using Option 1
            # Or: print("Current time from DB:", row.current_time) # If using Option 2
            # Or: print("Current time from DB:", row[0]) # If using Option 3
except Exception as e:
    print("❌ Operation failed:", e)