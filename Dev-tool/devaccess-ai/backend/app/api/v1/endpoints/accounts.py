"""
Account management endpoints
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_accounts():
    """List user's created accounts"""
    return {"message": "Account endpoints - to be implemented"}
