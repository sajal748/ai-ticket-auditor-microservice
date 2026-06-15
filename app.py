import time
from fastapi import FastAPI
from ollama import chat
from pydantic import BaseModel, Field
from typing import Literal

# Initialize the FastAPI Web Server Application
app = FastAPI(title="Internal AI Ticket Auditor")

# 1. Define the input the website portal will send to this API
class TicketInput(BaseModel):
    user_text: str
    selected_category: str
    selected_sub_category: str

# 2. Define the structured output the AI will return
class TicketAudit(BaseModel):
    is_dropdown_correct: bool = Field(description="True if description matches dropdowns, False otherwise.")
    correct_category: str = Field(description="The correct Category based on text.")
    correct_sub_category: str = Field(description="The correct Sub-Category based on text.")
    audit_reasoning: str = Field(description="1-sentence explanation of the mismatch or match.")

# 3. Create the API web endpoint that your website portal will talk to
@app.post("/audit")
def audit_ticket(ticket: TicketInput):
    start_time = time.time()
    
    prompt = f"""
    The user raised a ticket.
    Dropdown Selected Category: {ticket.selected_category}
    Dropdown Selected Sub-Category: {ticket.selected_sub_category}
    
    User Written Text Description: "{ticket.user_text}"
    
    Analyze if the text description matches the dropdown items they selected.
    """

    try:
        response = chat(
            model='llama3.2:3b',
            messages=[{'role': 'user', 'content': prompt}],
            format=TicketAudit.model_json_schema(),
            options={'temperature': 0}
        )

        latency = time.time() - start_time
        validated_audit = TicketAudit.model_validate_json(response.message.content)
        
        # This sends the clean JSON response back over the web network
        return {
            "status": "success",
            "latency_seconds": round(latency, 2),
            "audit": validated_audit.model_dump()
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}