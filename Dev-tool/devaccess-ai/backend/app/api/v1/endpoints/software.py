"""
Software management endpoints
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_software():
    """List available software"""
    return {"message": "Software endpoints - to be implemented"}
