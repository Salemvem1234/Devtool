"""
AI-Powered Recommendation Service - Personalized tool recommendations
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, desc
import httpx
import structlog

from app.models.user import User
from app.models.software import Software, SoftwareCategory
from app.models.account import DevAccount
from app.models.enhanced_models import (
    DeveloperProfile, ToolRecommendation, ProjectTypeEnum,
    UsageMetric, APICredential
)
from app.core.config import settings

logger = structlog.get_logger()


class RecommendationService:
    """AI-powered service for generating personalized tool recommendations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        
        # Stack-based recommendations mapping
        self.stack_recommendations = {
            "react": {
                "hosting": ["vercel", "netlify", "surge"],
                "backend": ["supabase", "firebase", "railway"],
                "database": ["supabase", "planetscale", "mongodb"],
                "auth": ["auth0", "supabase", "firebase"],
                "analytics": ["posthog", "mixpanel", "amplitude"]
            },
            "vue": {
                "hosting": ["netlify", "vercel", "surge"],
                "backend": ["supabase", "firebase", "railway"],
                "database": ["supabase", "planetscale", "mongodb"],
                "analytics": ["posthog", "mixpanel"]
            },
            "python": {
                "hosting": ["railway", "render", "heroku"],
                "database": ["supabase", "planetscale", "mongodb"],
                "monitoring": ["sentry", "datadog", "newrelic"],
                "storage": ["cloudinary", "aws", "supabase"]
            },
            "nodejs": {
                "hosting": ["vercel", "railway", "render"],
                "database": ["supabase", "planetscale", "mongodb"],
                "monitoring": ["sentry", "datadog"],
                "api": ["postman", "insomnia", "rapidapi"]
            },
            "mobile": {
                "backend": ["supabase", "firebase", "appwrite"],
                "analytics": ["mixpanel", "amplitude", "firebase"],
                "auth": ["auth0", "firebase", "supabase"],
                "push": ["onesignal", "pusher", "firebase"]
            }
        }

    async def generate_personalized_recommendations(self, user: User, limit: int = 10) -> List[Dict[str, Any]]:
        """Generate personalized recommendations for a user"""
        
        # Get or create developer profile
        profile = await self._get_or_create_developer_profile(user)
        
        # Get user's existing accounts to avoid duplicates
        existing_accounts = await self._get_user_software_ids(user.id)
        
        recommendations = []
        
        # 1. Stack-based recommendations
        stack_recs = await self._generate_stack_based_recommendations(profile, existing_accounts)
        recommendations.extend(stack_recs)
        
        # 2. Usage pattern recommendations
        usage_recs = await self._generate_usage_pattern_recommendations(profile, existing_accounts)
        recommendations.extend(usage_recs)
        
        # 3. Trending tools recommendations
        trending_recs = await self._generate_trending_recommendations(existing_accounts)
        recommendations.extend(trending_recs)
        
        # 4. Complementary tools recommendations
        complementary_recs = await self._generate_complementary_recommendations(profile, existing_accounts)
        recommendations.extend(complementary_recs)
        
        # Score and rank recommendations
        scored_recommendations = await self._score_recommendations(recommendations, profile)
        
        # Remove duplicates and limit results
        unique_recommendations = self._deduplicate_recommendations(scored_recommendations)
        
        # Store recommendations for feedback learning
        await self._store_recommendations(profile, unique_recommendations[:limit])
        
        return unique_recommendations[:limit]

    async def generate_project_based_recommendations(self, user: User, project_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations based on specific project requirements"""
        
        profile = await self._get_or_create_developer_profile(user)
        existing_accounts = await self._get_user_software_ids(user.id)
        
        recommendations = []
        
        # Extract project details
        project_type = project_context.get("type", "web_app")
        languages = project_context.get("languages", [])
        frameworks = project_context.get("frameworks", [])
        requirements = project_context.get("requirements", [])
        
        # Generate stack-specific recommendations
        for lang in languages:
            if lang.lower() in self.stack_recommendations:
                stack = self.stack_recommendations[lang.lower()]
                
                for category, tools in stack.items():
                    if category in requirements or not requirements:
                        for tool_name in tools:
                            if await self._software_exists(tool_name):
                                software = await self._get_software_by_name(tool_name)
                                if software and software.id not in existing_accounts:
                                    recommendations.append({
                                        "software": software,
                                        "confidence_score": 0.8,
                                        "recommendation_type": "project_based",
                                        "reasoning": f"Recommended for {lang} {project_type} projects",
                                        "project_context": project_context
                                    })
        
        # Score and rank
        scored_recs = await self._score_recommendations(recommendations, profile)
        
        return scored_recs[:10]

    async def get_category_recommendations(self, user: User, category: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recommendations for a specific category"""
        
        profile = await self._get_or_create_developer_profile(user)
        existing_accounts = await self._get_user_software_ids(user.id)
        
        # Get software in the specified category
        result = await self.db.execute(
            select(Software)
            .join(SoftwareCategory)
            .where(
                and_(
                    SoftwareCategory.name.ilike(f"%{category}%"),
                    Software.is_active == True,
                    Software.has_free_tier == True,
                    ~Software.id.in_(existing_accounts) if existing_accounts else True
                )
            )
            .order_by(desc(Software.popularity_score))
            .limit(limit * 2)  # Get more to allow for filtering
        )
        softwares = result.scalars().all()
        
        recommendations = []
        for software in softwares:
            recommendations.append({
                "software": software,
                "confidence_score": min(software.popularity_score / 100, 1.0),
                "recommendation_type": "category_based",
                "reasoning": f"Popular {category} tool with free tier"
            })
        
        return recommendations[:limit]

    async def _get_or_create_developer_profile(self, user: User) -> DeveloperProfile:
        """Get existing developer profile or create a new one"""
        
        result = await self.db.execute(
            select(DeveloperProfile).where(DeveloperProfile.user_id == user.id)
        )
        profile = result.scalar_one_or_none()
        
        if not profile:
            profile = DeveloperProfile(
                user_id=user.id,
                experience_level="intermediate",
                primary_languages=[],
                frameworks=[],
                cloud_preferences=[],
                project_types=[],
                most_used_categories=[],
                preferred_tools=[],
                avoided_tools=[]
            )
            self.db.add(profile)
            await self.db.commit()
            await self.db.refresh(profile)
        
        return profile

    async def _get_user_software_ids(self, user_id: int) -> List[int]:
        """Get list of software IDs user already has accounts for"""
        
        result = await self.db.execute(
            select(DevAccount.software_id).where(DevAccount.user_id == user_id)
        )
        return [row[0] for row in result.fetchall()]

    async def _generate_stack_based_recommendations(self, profile: DeveloperProfile, existing_accounts: List[int]) -> List[Dict[str, Any]]:
        """Generate recommendations based on user's tech stack"""
        
        recommendations = []
        
        # Use primary languages to suggest complementary tools
        languages = profile.primary_languages or []
        frameworks = profile.frameworks or []
        
        for lang in languages:
            if lang.lower() in self.stack_recommendations:
                stack = self.stack_recommendations[lang.lower()]
                
                for category, tools in stack.items():
                    for tool_name in tools[:2]:  # Top 2 per category
                        software = await self._get_software_by_name(tool_name)
                        if software and software.id not in existing_accounts:
                            recommendations.append({
                                "software": software,
                                "confidence_score": 0.7,
                                "recommendation_type": "stack_based",
                                "reasoning": f"Complements your {lang} stack"
                            })
        
        return recommendations

    async def _generate_usage_pattern_recommendations(self, profile: DeveloperProfile, existing_accounts: List[int]) -> List[Dict[str, Any]]:
        """Generate recommendations based on usage patterns"""
        
        recommendations = []
        
        # Analyze most used categories
        most_used = profile.most_used_categories or []
        
        if most_used:
            # Find popular tools in most used categories
            for category in most_used[:3]:  # Top 3 categories
                result = await self.db.execute(
                    select(Software)
                    .join(SoftwareCategory)
                    .where(
                        and_(
                            SoftwareCategory.name.ilike(f"%{category}%"),
                            Software.is_active == True,
                            Software.has_free_tier == True,
                            ~Software.id.in_(existing_accounts) if existing_accounts else True
                        )
                    )
                    .order_by(desc(Software.popularity_score))
                    .limit(2)
                )
                softwares = result.scalars().all()
                
                for software in softwares:
                    recommendations.append({
                        "software": software,
                        "confidence_score": 0.6,
                        "recommendation_type": "usage_pattern",
                        "reasoning": f"Based on your frequent use of {category} tools"
                    })
        
        return recommendations

    async def _generate_trending_recommendations(self, existing_accounts: List[int]) -> List[Dict[str, Any]]:
        """Generate recommendations based on trending tools"""
        
        # Get tools with high popularity scores that are trending
        result = await self.db.execute(
            select(Software)
            .where(
                and_(
                    Software.is_active == True,
                    Software.has_free_tier == True,
                    Software.popularity_score >= 70,
                    ~Software.id.in_(existing_accounts) if existing_accounts else True
                )
            )
            .order_by(desc(Software.popularity_score))
            .limit(5)
        )
        softwares = result.scalars().all()
        
        recommendations = []
        for software in softwares:
            recommendations.append({
                "software": software,
                "confidence_score": 0.5,
                "recommendation_type": "trending",
                "reasoning": "Popular trending tool in the developer community"
            })
        
        return recommendations

    async def _generate_complementary_recommendations(self, profile: DeveloperProfile, existing_accounts: List[int]) -> List[Dict[str, Any]]:
        """Generate recommendations for tools that complement existing ones"""
        
        recommendations = []
        
        # Get user's existing software
        if existing_accounts:
            result = await self.db.execute(
                select(Software)
                .where(Software.id.in_(existing_accounts))
            )
            existing_software = result.scalars().all()
            
            # Define complementary relationships
            complementary_map = {
                "vercel": ["supabase", "planetscale", "sentry"],
                "netlify": ["supabase", "firebase", "auth0"],
                "heroku": ["postgresql", "redis", "sentry"],
                "supabase": ["vercel", "netlify", "cloudinary"],
                "react": ["vercel", "netlify", "supabase"],
            }
            
            for software in existing_software:
                complements = complementary_map.get(software.name.lower(), [])
                
                for complement_name in complements:
                    complement_software = await self._get_software_by_name(complement_name)
                    if complement_software and complement_software.id not in existing_accounts:
                        recommendations.append({
                            "software": complement_software,
                            "confidence_score": 0.65,
                            "recommendation_type": "complementary",
                            "reasoning": f"Works well with your existing {software.name} setup"
                        })
        
        return recommendations

    async def _score_recommendations(self, recommendations: List[Dict[str, Any]], profile: DeveloperProfile) -> List[Dict[str, Any]]:
        """Score and rank recommendations based on multiple factors"""
        
        for rec in recommendations:
            software = rec["software"]
            base_score = rec["confidence_score"]
            
            # Adjust score based on various factors
            score_adjustments = 0
            
            # Free tier quality (automation support, success rate)
            if software.automation_supported:
                score_adjustments += 0.1
            
            if software.success_rate and software.success_rate >= 80:
                score_adjustments += 0.1
            
            # User preferences
            preferred_tools = profile.preferred_tools or []
            avoided_tools = profile.avoided_tools or []
            
            if software.name.lower() in [t.lower() for t in preferred_tools]:
                score_adjustments += 0.2
            
            if software.name.lower() in [t.lower() for t in avoided_tools]:
                score_adjustments -= 0.3
            
            # Experience level matching
            if profile.experience_level == "beginner" and software.tags:
                if "beginner-friendly" in software.tags:
                    score_adjustments += 0.1
            
            # Final score calculation
            final_score = min(base_score + score_adjustments, 1.0)
            rec["confidence_score"] = final_score
        
        # Sort by confidence score
        return sorted(recommendations, key=lambda x: x["confidence_score"], reverse=True)

    def _deduplicate_recommendations(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate recommendations"""
        
        seen_software_ids = set()
        unique_recs = []
        
        for rec in recommendations:
            software_id = rec["software"].id
            if software_id not in seen_software_ids:
                seen_software_ids.add(software_id)
                unique_recs.append(rec)
        
        return unique_recs

    async def _store_recommendations(self, profile: DeveloperProfile, recommendations: List[Dict[str, Any]]):
        """Store recommendations for tracking and feedback learning"""
        
        # Clean up old recommendations
        await self.db.execute(
            select(ToolRecommendation).where(
                and_(
                    ToolRecommendation.developer_profile_id == profile.id,
                    ToolRecommendation.created_at < datetime.utcnow() - timedelta(days=30)
                )
            )
        )
        
        # Store new recommendations
        for i, rec in enumerate(recommendations):
            tool_rec = ToolRecommendation(
                developer_profile_id=profile.id,
                software_id=rec["software"].id,
                recommendation_type=rec["recommendation_type"],
                confidence_score=rec["confidence_score"],
                ranking=i + 1,
                reasoning=rec.get("reasoning"),
                project_context=rec.get("project_context"),
                expires_at=datetime.utcnow() + timedelta(days=30)
            )
            self.db.add(tool_rec)
        
        await self.db.commit()

    async def _software_exists(self, name: str) -> bool:
        """Check if software exists in database"""
        
        result = await self.db.execute(
            select(Software).where(Software.name.ilike(f"%{name}%"))
        )
        return result.scalar_one_or_none() is not None

    async def _get_software_by_name(self, name: str) -> Optional[Software]:
        """Get software by name"""
        
        result = await self.db.execute(
            select(Software).where(Software.name.ilike(f"%{name}%"))
        )
        return result.scalar_one_or_none()

    async def update_developer_profile(self, user: User, profile_data: Dict[str, Any]) -> DeveloperProfile:
        """Update developer profile with new information"""
        
        profile = await self._get_or_create_developer_profile(user)
        
        # Update fields if provided
        if "primary_languages" in profile_data:
            profile.primary_languages = profile_data["primary_languages"]
        
        if "frameworks" in profile_data:
            profile.frameworks = profile_data["frameworks"]
        
        if "cloud_preferences" in profile_data:
            profile.cloud_preferences = profile_data["cloud_preferences"]
        
        if "project_types" in profile_data:
            profile.project_types = profile_data["project_types"]
        
        if "experience_level" in profile_data:
            profile.experience_level = profile_data["experience_level"]
        
        if "team_size" in profile_data:
            profile.team_size = profile_data["team_size"]
        
        if "preferred_tools" in profile_data:
            profile.preferred_tools = profile_data["preferred_tools"]
        
        if "avoided_tools" in profile_data:
            profile.avoided_tools = profile_data["avoided_tools"]
        
        profile.updated_at = datetime.utcnow()
        
        await self.db.commit()
        return profile

    async def track_recommendation_feedback(self, user: User, recommendation_id: int, action: str, feedback: Optional[str] = None):
        """Track user feedback on recommendations"""
        
        result = await self.db.execute(
            select(ToolRecommendation).where(ToolRecommendation.id == recommendation_id)
        )
        recommendation = result.scalar_one_or_none()
        
        if recommendation:
            if action == "accepted":
                recommendation.was_used = True
                recommendation.user_rating = 5
            elif action == "dismissed":
                recommendation.dismissed = True
                recommendation.dismissed_reason = feedback
            elif action == "rated":
                # Assume feedback contains rating
                try:
                    rating = int(feedback)
                    recommendation.user_rating = max(1, min(5, rating))
                except (ValueError, TypeError):
                    pass
            
            recommendation.user_feedback = feedback
            await self.db.commit()

    async def get_recommendation_analytics(self, user: User) -> Dict[str, Any]:
        """Get analytics on recommendation performance"""
        
        profile = await self._get_or_create_developer_profile(user)
        
        result = await self.db.execute(
            select(ToolRecommendation).where(
                ToolRecommendation.developer_profile_id == profile.id
            )
        )
        recommendations = result.scalars().all()
        
        analytics = {
            "total_recommendations": len(recommendations),
            "accepted_count": len([r for r in recommendations if r.was_used]),
            "dismissed_count": len([r for r in recommendations if r.dismissed]),
            "average_rating": 0,
            "recommendation_types": {},
            "top_categories": [],
            "success_rate": 0
        }
        
        if recommendations:
            # Calculate averages
            rated_recs = [r for r in recommendations if r.user_rating]
            if rated_recs:
                analytics["average_rating"] = sum(r.user_rating for r in rated_recs) / len(rated_recs)
            
            # Calculate success rate
            total_with_feedback = len([r for r in recommendations if r.was_used or r.dismissed])
            if total_with_feedback > 0:
                analytics["success_rate"] = analytics["accepted_count"] / total_with_feedback
            
            # Recommendation type distribution
            for rec in recommendations:
                rec_type = rec.recommendation_type
                analytics["recommendation_types"][rec_type] = analytics["recommendation_types"].get(rec_type, 0) + 1
        
        return analytics
