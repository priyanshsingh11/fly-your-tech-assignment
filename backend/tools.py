import json
import os
from langchain.tools import tool
from utils import get_company_info_retriever

@tool
def company_info_tool(query: str):
    """
    Use this tool to answer questions about Fly Your Tech company details like 
    address, email, phone, services, and pricing.
    """
    retriever = get_company_info_retriever()
    docs = retriever.invoke(query)
    return "\n".join([doc.page_content for doc in docs])

@tool
def get_all_leads(dummy_input: str = ""):
    """
    Retrieves a list of all current business leads from the database. 
    Use this when the user asks for a general overview of leads or 'who' are the leads.
    """
    BASE_DIR = os.path.dirname(__file__)
    try:
        with open(os.path.join(BASE_DIR, "leads.json"), "r") as f:
            leads = json.load(f)
        return json.dumps(leads, indent=2)
    except Exception as e:
        return f"Error reading leads: {e}"

@tool
def get_lead_details(name: str):
    """
    Retrieves specific details about a lead by their name.
    Use this when the user asks about a specific person (e.g., 'What is Alice interested in?').
    """
    BASE_DIR = os.path.dirname(__file__)
    try:
        with open(os.path.join(BASE_DIR, "leads.json"), "r") as f:
            leads = json.load(f)
        # Simple fuzzy match / exact match find
        for lead in leads:
            if name.lower() in lead["name"].lower():
                return json.dumps(lead, indent=2)
        return f"No lead found matching the name '{name}'."
    except Exception as e:
        return f"Error searching leads: {e}"

@tool
def schedule_meeting(details: str):
    """
    Schedules a meeting or sends an email based on the user's request.
    This is a dummy tool and returns a confirmation message.
    """
    # In a real scenario, this would call an API like Google Calendar or SendGrid
    return f"Action confirmed: '{details}' has been scheduled successfully."

# List of tools to be used by the agent
tools = [company_info_tool, get_all_leads, get_lead_details, schedule_meeting]
