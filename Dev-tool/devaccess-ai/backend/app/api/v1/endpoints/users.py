"""
User management endpoints
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_users():
    """List users (admin only)"""
    return {"message": "User endpoints - to be implemented"}
