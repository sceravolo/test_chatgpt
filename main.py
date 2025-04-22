# main.py
import os
from dotenv import load_dotenv

# ---> Load .env file at the very start <---
# Ensure this runs before importing modules that need the variables
load_dotenv()

# Now import other modules
from fastapi import FastAPI
from pydantic import BaseModel
from app.mcp_handler import handle_conversation # Imports mcp_handler, which imports db

app = FastAPI()

class ChatRequest(BaseModel):
    user_input: str

@app.post("/chat")
async def chat(request: ChatRequest):
    response_text = await handle_conversation(request.user_input)
    return {"response": response_text}

# Optional: Add a check during startup (outside request handling)
# db_url_check = os.getenv("DATABASE_URL")
# if not db_url_check:
#     print("WARNING: DATABASE_URL not found after load_dotenv in main.py!")
# else:
#     print("DATABASE_URL loaded successfully in main.py.")