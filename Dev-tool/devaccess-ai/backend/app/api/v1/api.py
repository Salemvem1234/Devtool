"""
Main API router for DevAccess AI v1
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, software, accounts, automation, nlp, recommendations, monitoring, onboarding

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(software.router, prefix="/software", tags=["software"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(automation.router, prefix="/automation", tags=["automation"])
api_router.include_router(nlp.router, prefix="/nlp", tags=["nlp"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])
api_router.include_router(onboarding.router, prefix="/onboarding", tags=["onboarding"])
