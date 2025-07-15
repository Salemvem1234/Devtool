"""
Automation endpoints for task management
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
from app.services.automation_service import automation_service

router = APIRouter()

@router.post("/create-account")
async def create_account(software_name: str, email_domain: str = None, usage_context: str = None) -> JSONResponse:
    """Create account using automation"""
    result = await automation_service.create_account(software_name, email_domain, usage_context)

    if result.status == "success":
        return JSONResponse(
            status_code=200,
            content={"status": "success", "data": result}
        )
    else:
        raise HTTPException(
            status_code=400,
            detail=result.error_message
        )
