"""
NLP endpoints for intent recognition and request processing
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.nlp_service import NLPService
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

logger = structlog.get_logger()

router = APIRouter()


class IntentRequest(BaseModel):
    """Request model for intent recognition"""
    text: str
    context: Optional[Dict[str, Any]] = None


class IntentResponse(BaseModel):
    """Response model for intent recognition"""
    intent: str
    confidence: float
    entities: Dict[str, Any]
    software_suggestions: List[Dict[str, Any]]
    action_plan: List[str]


class SoftwareSuggestionRequest(BaseModel):
    """Request model for software suggestions"""
    query: str
    category: Optional[str] = None
    limit: int = 10


class SoftwareSuggestionResponse(BaseModel):
    """Response model for software suggestions"""
    suggestions: List[Dict[str, Any]]
    total_found: int


@router.post("/parse-intent", response_model=IntentResponse)
async def parse_user_intent(
    request: IntentRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Parse user intent from natural language request
    
    Examples:
    - "I need an account for Cursor"
    - "Get me a free tier for a CI/CD tool"
    - "I want to try out a new database service"
    """
    try:
        nlp_service = NLPService(db)
        result = await nlp_service.parse_intent(request.text, request.context)
        
        logger.info(
            "Intent parsed successfully",
            text=request.text,
            intent=result["intent"],
            confidence=result["confidence"]
        )
        
        return IntentResponse(**result)
        
    except Exception as e:
        logger.error("Failed to parse intent", error=str(e), text=request.text)
        raise HTTPException(status_code=500, detail="Failed to parse intent")


@router.post("/suggest-software", response_model=SoftwareSuggestionResponse)
async def suggest_software(
    request: SoftwareSuggestionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Suggest software based on user query and preferences
    """
    try:
        nlp_service = NLPService(db)
        suggestions = await nlp_service.suggest_software(
            query=request.query,
            category=request.category,
            limit=request.limit
        )
        
        logger.info(
            "Software suggestions generated",
            query=request.query,
            category=request.category,
            suggestions_count=len(suggestions)
        )
        
        return SoftwareSuggestionResponse(
            suggestions=suggestions,
            total_found=len(suggestions)
        )
        
    except Exception as e:
        logger.error("Failed to suggest software", error=str(e), query=request.query)
        raise HTTPException(status_code=500, detail="Failed to suggest software")


@router.get("/categories")
async def get_software_categories(db: AsyncSession = Depends(get_db)):
    """Get all available software categories"""
    try:
        nlp_service = NLPService(db)
        categories = await nlp_service.get_categories()
        
        return {"categories": categories}
        
    except Exception as e:
        logger.error("Failed to get categories", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get categories")


@router.post("/validate-request")
async def validate_automation_request(
    request: IntentRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Validate if a user request can be automated
    """
    try:
        nlp_service = NLPService(db)
        validation = await nlp_service.validate_automation_request(request.text)
        
        return {
            "can_automate": validation["can_automate"],
            "confidence": validation["confidence"],
            "requirements": validation["requirements"],
            "warnings": validation.get("warnings", []),
            "estimated_success_rate": validation.get("estimated_success_rate", 0)
        }
        
    except Exception as e:
        logger.error("Failed to validate request", error=str(e), text=request.text)
        raise HTTPException(status_code=500, detail="Failed to validate request")
