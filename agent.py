import json
from typing import Any

from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL
from schemas import (
    PatientSearchRequest,
    InsuranceEligibilityRequest,
    AppointmentSlotRequest,
    BookAppointmentRequest,
)
from tools import (
    search_patient,
    check_insurance_eligibility,
    find_available_slots,
    book_appointment,
)
from audit import audit_log


# -------------------------------------------------------------------
# OpenAI Client (OpenRouter compatible)
# -------------------------------------------------------------------
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)


# -------------------------------------------------------------------
# Tool Definitions
# -------------------------------------------------------------------
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_patient",
            "description": "Search for a patient by name",
            "parameters": PatientSearchRequest.model_json_schema(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_insurance_eligibility",
            "description": "Check insurance eligibility for a patient",
            "parameters": InsuranceEligibilityRequest.model_json_schema(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_available_slots",
            "description": "Find available appointment slots",
            "parameters": AppointmentSlotRequest.model_json_schema(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "Book an appointment",
            "parameters": BookAppointmentRequest.model_json_schema(),
        },
    },
]


# -------------------------------------------------------------------
# System Prompt (Workflow-guided for OSS models)
# -------------------------------------------------------------------
SYSTEM_PROMPT = """
You are a healthcare workflow orchestration agent.

WORKFLOW POLICY:
- If a patient name is mentioned, call `search_patient` first
- After patient identification, check insurance eligibility
- Before booking, find available slots
- Use tools for ALL actions

STRICT RULES:
- NO medical advice
- NO diagnosis
- NO free-text answers
- ONLY tool calls
"""


# -------------------------------------------------------------------
# Core Agent
# -------------------------------------------------------------------
def run_agent(user_input: str, dry_run: bool = True) -> dict[str, Any]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            extra_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "Clinical Appointment Agent",
            },
        )

        assistant_msg = response.choices[0].message

        # -----------------------------------------------------------
        # If model refuses to call a tool
        # -----------------------------------------------------------
        if not assistant_msg.tool_calls:
            audit_log(
                "REFUSAL",
                {"input": user_input, "reason": assistant_msg.content},
            )
            return {
                "status": "REFUSED",
                "reason": "Model could not determine a safe tool call",
            }

        tool_call = assistant_msg.tool_calls[0]
        tool_name = tool_call.function.name

        try:
            tool_args = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError:
            return {"status": "ERROR", "reason": "Invalid JSON arguments"}

        audit_log(
            "TOOL_CALL",
            {"tool": tool_name, "arguments": tool_args, "dry_run": dry_run},
        )

        if dry_run:
            return {
                "status": "DRY_RUN",
                "tool": tool_name,
                "arguments": tool_args,
            }

        # -----------------------------------------------------------
        # Execute tool with schema validation
        # -----------------------------------------------------------
        try:
            if tool_name == "search_patient":
                req = PatientSearchRequest(**tool_args)
                result = search_patient(req)

            elif tool_name == "check_insurance_eligibility":
                req = InsuranceEligibilityRequest(**tool_args)
                result = check_insurance_eligibility(req)

            elif tool_name == "find_available_slots":
                req = AppointmentSlotRequest(**tool_args)
                result = find_available_slots(req)

            elif tool_name == "book_appointment":
                req = BookAppointmentRequest(**tool_args)
                result = book_appointment(req)

            else:
                return {"status": "ERROR", "reason": "Unknown tool"}

        except Exception as e:
            audit_log(
                "VALIDATION_ERROR",
                {"tool": tool_name, "error": str(e)},
            )
            return {"status": "ERROR", "reason": "Tool execution failed"}

        # -----------------------------------------------------------
        # Normalize tool output (single OR list)
        # -----------------------------------------------------------
        # -----------------------------------------------------------
# Normalize tool output (single OR list)  ✅ FIX
# -----------------------------------------------------------
        if isinstance(result, list):
            tool_content = json.dumps(
                [json.loads(r.model_dump_json()) for r in result]
            )
        else:
            tool_content = result.model_dump_json()



        # -----------------------------------------------------------
        # Append messages in CORRECT order
        # -----------------------------------------------------------
        messages.append(assistant_msg)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_content,
            }
        )

        # -----------------------------------------------------------
        # Final step
        # -----------------------------------------------------------
        if tool_name == "book_appointment":
            audit_log("FINAL_OUTPUT", result.model_dump())
            return result.model_dump()
