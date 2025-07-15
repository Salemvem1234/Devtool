"""
User Onboarding API endpoints for collecting profile data
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.services.onboarding_service import OnboardingService
from app.services.advanced_recommendation_engine import AdvancedRecommendationEngine
import structlog

logger = structlog.get_logger()

router = APIRouter()


class OnboardingResponse(BaseModel):
    """Model for onboarding response submission"""
    step: int
    question_id: str
    response_data: Any
    time_to_answer: Optional[float] = None
    confidence_level: Optional[str] = None


class SkipRequest(BaseModel):
    """Model for skipping onboarding steps"""
    step: int
    question_id: str


@router.post("/start")
async def start_onboarding(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Start the user onboarding process"""
    
    try:
        onboarding_service = OnboardingService(db)
        result = await onboarding_service.start_onboarding(current_user)
        
        logger.info(
            "Onboarding started",
            user_id=current_user.id,
            status=result["status"]
        )
        
        return result
        
    except Exception as e:
        logger.error("Failed to start onboarding", error=str(e), user_id=current_user.id)
        raise HTTPException(status_code=500, detail="Failed to start onboarding")


@router.post("/submit")
async def submit_onboarding_response(
    response: OnboardingResponse,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit a response to an onboarding question"""
    
    try:
        onboarding_service = OnboardingService(db)
        result = await onboarding_service.submit_onboarding_response(
            user=current_user,
            step=response.step,
            question_id=response.question_id,
            response_data=response.response_data,
            time_to_answer=response.time_to_answer,
            confidence_level=response.confidence_level
        )
        
        logger.info(
            "Onboarding response submitted",
            user_id=current_user.id,
            step=response.step,
            question_id=response.question_id,
            status=result["status"]
        )
        
        return result
        
    except ValueError as e:
        logger.warning("Invalid onboarding response", error=str(e), user_id=current_user.id)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Failed to submit onboarding response", error=str(e), user_id=current_user.id)
        raise HTTPException(status_code=500, detail="Failed to submit response")


@router.post("/skip")
async def skip_onboarding_step(
    skip_request: SkipRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Skip an optional onboarding step"""
    
    try:
        onboarding_service = OnboardingService(db)
        result = await onboarding_service.skip_onboarding_step(
            user=current_user,
            step=skip_request.step,
            question_id=skip_request.question_id
        )
        
        logger.info(
            "Onboarding step skipped",
            user_id=current_user.id,
            step=skip_request.step,
            question_id=skip_request.question_id
        )
        
        return result
        
    except ValueError as e:
        logger.warning("Cannot skip onboarding step", error=str(e), user_id=current_user.id)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Failed to skip onboarding step", error=str(e), user_id=current_user.id)
        raise HTTPException(status_code=500, detail="Failed to skip step")


@router.get("/progress")
async def get_onboarding_progress(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current onboarding progress for the user"""
    
    try:
        onboarding_service = OnboardingService(db)
        progress = await onboarding_service.get_onboarding_progress(current_user)
        
        return progress
        
    except Exception as e:
        logger.error("Failed to get onboarding progress", error=str(e), user_id=current_user.id)
        raise HTTPException(status_code=500, detail="Failed to get progress")


@router.get("/questions")
async def get_onboarding_questions(
    current_user: User = Depends(get_current_user)
):
    """Get all onboarding questions (for preview or reference)"""
    
    try:
        onboarding_service = OnboardingService(None)  # No DB needed for questions
        questions = onboarding_service.onboarding_questions["v1"]
        
        return {
            "flow_version": "v1",
            "total_steps": len(questions),
            "questions": questions
        }
        
    except Exception as e:
        logger.error("Failed to get onboarding questions", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get questions")


@router.post("/complete")
async def complete_onboarding_and_get_recommendations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Complete onboarding and get initial personalized recommendations"""
    
    try:
        # Check onboarding status
        onboarding_service = OnboardingService(db)
        progress = await onboarding_service.get_onboarding_progress(current_user)
        
        if progress["status"] != "completed":
            raise HTTPException(
                status_code=400, 
                detail="Onboarding must be completed first"
            )
        
        # Generate initial recommendations
        recommendation_engine = AdvancedRecommendationEngine(db)
        recommendations = await recommendation_engine.generate_experience_tailored_recommendations(
            user=current_user,
            limit=8,
            context={"source": "onboarding_completion"}
        )
        
        # Format recommendations for response
        formatted_recs = []
        for rec in recommendations:
            software = rec["software"]
            formatted_recs.append({
                "id": software.id,
                "name": software.name,
                "display_name": software.display_name,
                "description": software.description,
                "category": software.category.name if software.category else None,
                "website_url": software.website_url,
                "has_free_tier": software.has_free_tier,
                "automation_supported": software.automation_supported,
                "confidence_score": rec["confidence_score"],
                "recommendation_type": rec["recommendation_type"],
                "experience_level": rec.get("experience_level"),
                "reasoning": rec.get("reasoning", ""),
                "setup_complexity": rec.get("setup_complexity"),
                "beginner_friendly": rec.get("beginner_friendly", False),
                "learning_resources": rec.get("learning_resources", [])
            })
        
        logger.info(
            "Onboarding completed with recommendations",
            user_id=current_user.id,
            recommendations_count=len(formatted_recs)
        )
        
        return {
            "status": "completed",
            "message": "Onboarding completed! Here are your personalized recommendations.",
            "profile_completeness": progress.get("profile_completeness", 0),
            "initial_recommendations": formatted_recs,
            "recommendation_count": len(formatted_recs),
            "next_steps": [
                "Review your personalized recommendations",
                "Select tools you'd like to try",
                "Let DevAccess AI create accounts for you",
                "Start building your projects!"
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to complete onboarding", error=str(e), user_id=current_user.id)
        raise HTTPException(status_code=500, detail="Failed to complete onboarding")


@router.get("/profile-summary")
async def get_profile_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a summary of the user's profile after onboarding"""
    
    try:
        from sqlalchemy import select
        from app.models.user_profiling import UserProfile
        
        result = await db.execute(
            select(UserProfile).where(UserProfile.user_id == current_user.id)
        )
        profile = result.scalar_one_or_none()
        
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Create a comprehensive profile summary
        summary = {
            "experience_level": profile.experience_level.value if profile.experience_level else None,
            "years_of_experience": profile.years_of_experience,
            "primary_languages": profile.primary_languages or [],
            "domain_interests": profile.domain_interests or [],
            "primary_domain": profile.primary_domain.value if profile.primary_domain else None,
            "preferred_stacks": profile.preferred_stacks or [],
            "needed_tool_categories": profile.needed_tool_categories or [],
            "project_goals": profile.project_goals or [],
            "current_project_description": profile.current_project_description,
            "team_size": profile.team_size,
            "complexity_preference": profile.complexity_preference,
            "learning_style": profile.learning_style,
            "profile_completeness_score": profile.profile_completeness_score,
            "onboarding_completed_at": profile.onboarding_completed_at,
            "created_at": profile.profile_created_at
        }
        
        # Add some insights
        insights = []
        
        if profile.experience_level:
            level_insights = {
                "newbie": "Perfect for getting started with beginner-friendly tools!",
                "intermediate": "Great balance of learning and building with flexible tools.",
                "experienced": "Ready for professional-grade tools and advanced features.",
                "expert": "Access to enterprise-level tools and architectural solutions."
            }
            insights.append(level_insights.get(profile.experience_level.value, ""))
        
        if profile.primary_languages:
            insights.append(f"Specializes in {', '.join(profile.primary_languages[:3])}")
        
        if profile.domain_interests:
            insights.append(f"Interested in {', '.join(profile.domain_interests[:2])}")
        
        return {
            "profile": summary,
            "insights": insights,
            "recommendation_readiness": profile.profile_completeness_score >= 0.6
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get profile summary", error=str(e), user_id=current_user.id)
        raise HTTPException(status_code=500, detail="Failed to get profile summary")
