import os
import logging
import datetime
import asyncio
import google.cloud.logging
from google.cloud import datastore
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from mcp.server.fastmcp import FastMCP 

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext

# --- 1. Setup Logging ---
try:
    cloud_logging_client = google.cloud.logging.Client()
    cloud_logging_client.setup_logging()
except Exception:
    logging.basicConfig(level=logging.INFO)

load_dotenv()
model_name = os.getenv("MODEL", "gemini-2.5-flash")

# --- 2. Database Setup ---
db = datastore.Client() 

mcp = FastMCP("CareerTools")

# ================= 3. TOOLS (Updated for Career Focus) =================

@mcp.tool()
def save_job_opportunity(title: str, company: str, location: str) -> str:
    """Saves a new job or internship listing to the career tracker."""
    try:
        key = db.key('JobOpportunity')
        job = datastore.Entity(key=key)
        job.update({
            'title': title, 
            'company': company,
            'location': location,
            'status': 'Interested', 
            'created_at': datetime.datetime.now()
        })
        db.put(job)
        return f"Success: Saved {title} at {company} to your career tracker."
    except Exception as e:
        return f"Database Error: {str(e)}"

@mcp.tool()
def list_career_goals() -> str:
    """Lists all saved job opportunities and application statuses."""
    try:
        query = db.query(kind='JobOpportunity')
        jobs = list(query.fetch())
        if not jobs: return "Your career tracker is empty."
        
        res = ["🚀 Professional Opportunities:"]
        for j in jobs:
            res.append(f"• {j.get('title')} @ {j.get('company')} ({j.get('status')})")
        return "\n".join(res)
    except Exception as e:
        return f"Database Error: {str(e)}"

@mcp.tool()
def log_networking_contact(name: str, role: str, notes: str) -> str:
    """Saves details about a professional contact or recruiter."""
    try:
        key = db.key('Networking')
        contact = datastore.Entity(key=key)
        contact.update({
            'name': name,
            'role': role,
            'notes': notes,
            'added_at': datetime.datetime.now()
        })
        db.put(contact)
        return f"Success: Added {name} ({role}) to your networking list."
    except Exception as e:
        return f"Database Error: {str(e)}"

@mcp.tool()
def update_job_status(job_id_str: str, new_status: str) -> str:
    """Updates the status of an application (e.g., 'Applied', 'Interviewing')."""
    try:
        numeric_id = int(''.join(filter(str.isdigit, job_id_str)))
        key = db.key('JobOpportunity', numeric_id)
        job = db.get(key)
        if job:
            job['status'] = new_status
            db.put(job)
            return f"Status for {job['title']} updated to {new_status}."
        return f"ID {numeric_id} not found."
    except Exception as e:
        return f"Error: {str(e)}"

# ================= 4. AGENTS (Updated Instructions) =================

def add_prompt_to_state(tool_context: ToolContext, prompt: str):
    tool_context.state["PROMPT"] = prompt
    return {"status": "ok"}

def career_instruction(ctx):
    user_prompt = ctx.state.get("PROMPT", "Introduce yourself.")
    return f"""
You are a Professional Career Executive Assistant.
Your goal is to help the user manage their job search and networking.
Be professional, organized, and helpful.
Request to process: {user_prompt}
"""

def root_instruction(ctx):
    raw_input = ctx.state.get("user_input", "Hello")
    return f"""
1. Save this career request: {raw_input} using 'add_prompt_to_state'.
2. Hand off control to the 'workflow' agent.
"""

workspace_agent = Agent(
    name="career_specialist",
    model=model_name,
    instruction=career_instruction,
    tools=[save_job_opportunity, list_career_goals, log_networking_contact, update_job_status]
)

workflow = SequentialAgent(
    name="workflow",
    sub_agents=[workspace_agent]
)

root_agent = Agent(
    name="root",
    model=model_name,
    instruction=root_instruction,
    tools=[add_prompt_to_state],
    sub_agents=[workflow]
)

# ================= 5. API (Path adjusted) =================

app = FastAPI()

class UserRequest(BaseModel):
    prompt: str

@app.post("/api/v1/career/chat")
async def chat(request: UserRequest):
    try:
        final_reply = ""
        async for event in root_agent.run_async({"user_input": request.prompt}):
            if hasattr(event, 'text') and event.text:
                final_reply = event.text

        return {
            "status": "success",
            "reply": final_reply if final_reply else "Career task processed."
        }
    except Exception as e:
        logging.error(f"Chat Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)