"""
Recommendation endpoints for AI-powered tool suggestions
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.services.recommendation_service import RecommendationService
import structlog

logger = structlog.get_logger()

router = APIRouter()


class ProjectContext(BaseModel):
    """Project context for generating recommendations"""
    type: str = "web_app"  # web_app, mobile_app, api_service, etc.
    languages: List[str] = []
    frameworks: List[str] = []
    requirements: List[str] = []  # hosting, database, auth, etc.
    description: Optional[str] = None


class DeveloperProfileUpdate(BaseModel):
    """Model for updating developer profile"""
    primary_languages: Optional[List[str]] = None
    frameworks: Optional[List[str]] = None
    cloud_preferences: Optional[List[str]] = None
    project_types: Optional[List[str]] = None
    experience_level: Optional[str] = None
    team_size: Optional[str] = None
    preferred_tools: Optional[List[str]] = None
    avoided_tools: Optional[List[str]] = None


class RecommendationFeedback(BaseModel):
    """Model for recommendation feedback"""
    action: str  # accepted, dismissed, rated
    feedback: Optional[str] = None


@router.get("/personalized")
async def get_personalized_recommendations(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get personalized tool recommendations for the user"""
    
    try:
        recommendation_service = RecommendationService(db)
        recommendations = await recommendation_service.generate_personalized_recommendations(
            user=current_user,
            limit=limit
        )
        
        # Format response
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
                "reasoning": rec.get("reasoning", ""),
                "popularity_score": software.popularity_score
            })
        
        return {
            "recommendations": formatted_recs,
            "total": len(formatted_recs)
        }
        
    except Exception as e:
        logger.error("Failed to get personalized recommendations", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get recommendations")


@router.post("/project-based")
async def get_project_based_recommendations(
    project_context: ProjectContext,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get recommendations based on specific project requirements"""
    
    try:
        recommendation_service = RecommendationService(db)
        recommendations = await recommendation_service.generate_project_based_recommendations(
            user=current_user,
            project_context=project_context.dict()
        )
        
        # Format response
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
                "reasoning": rec.get("reasoning", ""),
                "project_context": rec.get("project_context")
            })
        
        return {
            "recommendations": formatted_recs,
            "project_context": project_context.dict(),
            "total": len(formatted_recs)
        }
        
    except Exception as e:
        logger.error("Failed to get project-based recommendations", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get project recommendations")


@router.get("/category/{category}")
async def get_category_recommendations(
    category: str,
    limit: int = 5,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get recommendations for a specific category"""
    
    try:
        recommendation_service = RecommendationService(db)
        recommendations = await recommendation_service.get_category_recommendations(
            user=current_user,
            category=category,
            limit=limit
        )
        
        # Format response
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
                "reasoning": rec.get("reasoning", ""),
                "popularity_score": software.popularity_score
            })
        
        return {
            "category": category,
            "recommendations": formatted_recs,
            "total": len(formatted_recs)
        }
        
    except Exception as e:
        logger.error("Failed to get category recommendations", error=str(e), category=category)
        raise HTTPException(status_code=500, detail="Failed to get category recommendations")


@router.get("/profile")
async def get_developer_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's developer profile"""
    
    try:
        recommendation_service = RecommendationService(db)
        profile = await recommendation_service._get_or_create_developer_profile(current_user)
        
        return {
            "id": profile.id,
            "primary_languages": profile.primary_languages,
            "frameworks": profile.frameworks,
            "cloud_preferences": profile.cloud_preferences,
            "project_types": profile.project_types,
            "experience_level": profile.experience_level,
            "team_size": profile.team_size,
            "most_used_categories": profile.most_used_categories,
            "preferred_tools": profile.preferred_tools,
            "avoided_tools": profile.avoided_tools,
            "total_accounts_created": profile.total_accounts_created,
            "success_rate": profile.success_rate,
            "created_at": profile.created_at,
            "updated_at": profile.updated_at
        }
        
    except Exception as e:
        logger.error("Failed to get developer profile", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get developer profile")


@router.put("/profile")
async def update_developer_profile(
    profile_update: DeveloperProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update user's developer profile"""
    
    try:
        recommendation_service = RecommendationService(db)
        
        # Filter out None values
        update_data = {k: v for k, v in profile_update.dict().items() if v is not None}
        
        profile = await recommendation_service.update_developer_profile(
            user=current_user,
            profile_data=update_data
        )
        
        return {
            "message": "Developer profile updated successfully",
            "profile": {
                "id": profile.id,
                "primary_languages": profile.primary_languages,
                "frameworks": profile.frameworks,
                "cloud_preferences": profile.cloud_preferences,
                "experience_level": profile.experience_level,
                "team_size": profile.team_size,
                "updated_at": profile.updated_at
            }
        }
        
    except Exception as e:
        logger.error("Failed to update developer profile", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to update developer profile")


@router.post("/feedback/{recommendation_id}")
async def provide_recommendation_feedback(
    recommendation_id: int,
    feedback: RecommendationFeedback,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Provide feedback on a recommendation"""
    
    try:
        recommendation_service = RecommendationService(db)
        
        await recommendation_service.track_recommendation_feedback(
            user=current_user,
            recommendation_id=recommendation_id,
            action=feedback.action,
            feedback=feedback.feedback
        )
        
        return {"message": "Feedback recorded successfully"}
        
    except Exception as e:
        logger.error("Failed to record feedback", error=str(e), recommendation_id=recommendation_id)
        raise HTTPException(status_code=500, detail="Failed to record feedback")


@router.get("/analytics")
async def get_recommendation_analytics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get analytics on recommendation performance"""
    
    try:
        recommendation_service = RecommendationService(db)
        analytics = await recommendation_service.get_recommendation_analytics(current_user)
        
        return analytics
        
    except Exception as e:
        logger.error("Failed to get recommendation analytics", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get analytics")
