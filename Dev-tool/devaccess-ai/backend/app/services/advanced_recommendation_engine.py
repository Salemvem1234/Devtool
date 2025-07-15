"""
Advanced Recommendation Engine with Experience-Level Tailoring
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, desc
import structlog

from app.models.user import User
from app.models.software import Software, SoftwareCategory
from app.models.account import DevAccount
from app.models.user_profiling import (
    UserProfile, ExperienceLevelEnum, DomainInterestEnum,
    UserBehavioralEvent, RecommendationInteraction,
    calculate_profile_completeness
)
from app.models.enhanced_models import ToolRecommendation
from app.core.config import settings

logger = structlog.get_logger()


class AdvancedRecommendationEngine:
    """Advanced AI-powered recommendation engine with experience-level tailoring"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        
        # Experience-level specific recommendation strategies
        self.experience_strategies = {
            ExperienceLevelEnum.NEWBIE: self._get_newbie_recommendations,
            ExperienceLevelEnum.INTERMEDIATE: self._get_intermediate_recommendations,
            ExperienceLevelEnum.EXPERIENCED: self._get_experienced_recommendations,
            ExperienceLevelEnum.EXPERT: self._get_expert_recommendations
        }
        
        # Tool recommendations by experience level
        self.experience_tool_preferences = {
            ExperienceLevelEnum.NEWBIE: {
                "hosting": {
                    "preferred": ["vercel", "netlify", "surge"],
                    "reasoning": "Easy deployment with minimal configuration",
                    "avoid": ["aws_ec2", "digital_ocean", "linode"]
                },
                "database": {
                    "preferred": ["supabase", "firebase", "airtable"],
                    "reasoning": "Backend-as-a-service with simple setup",
                    "avoid": ["postgresql", "mongodb", "redis"]
                },
                "auth": {
                    "preferred": ["auth0", "firebase_auth", "supabase_auth"],
                    "reasoning": "Managed authentication with good documentation",
                    "avoid": ["custom_jwt", "passport"]
                },
                "ide": {
                    "preferred": ["vscode", "replit", "codepen"],
                    "reasoning": "Beginner-friendly with extensive extensions",
                    "avoid": ["vim", "emacs"]
                }
            },
            ExperienceLevelEnum.INTERMEDIATE: {
                "hosting": {
                    "preferred": ["vercel", "netlify", "railway", "render"],
                    "reasoning": "Good balance of ease and flexibility",
                    "avoid": []
                },
                "database": {
                    "preferred": ["supabase", "planetscale", "mongodb_atlas"],
                    "reasoning": "Managed services with more control options",
                    "avoid": []
                },
                "ci_cd": {
                    "preferred": ["github_actions", "vercel", "netlify"],
                    "reasoning": "Integrated CI/CD with learning opportunities",
                    "avoid": ["jenkins", "teamcity"]
                },
                "monitoring": {
                    "preferred": ["sentry", "logflare", "betterstack"],
                    "reasoning": "Easy to set up with good learning value",
                    "avoid": []
                }
            },
            ExperienceLevelEnum.EXPERIENCED: {
                "hosting": {
                    "preferred": ["railway", "render", "fly_io", "aws", "gcp"],
                    "reasoning": "Professional-grade with good free tiers",
                    "avoid": []
                },
                "database": {
                    "preferred": ["planetscale", "supabase", "mongodb_atlas", "cockroachdb"],
                    "reasoning": "Enterprise-ready with advanced features",
                    "avoid": []
                },
                "monitoring": {
                    "preferred": ["sentry", "datadog", "newrelic", "honeycomb"],
                    "reasoning": "Professional monitoring and observability",
                    "avoid": []
                },
                "infrastructure": {
                    "preferred": ["terraform", "pulumi", "aws_cdk"],
                    "reasoning": "Infrastructure as code capabilities",
                    "avoid": []
                }
            },
            ExperienceLevelEnum.EXPERT: {
                "hosting": {
                    "preferred": ["aws", "gcp", "azure", "kubernetes"],
                    "reasoning": "Full control and enterprise capabilities",
                    "avoid": []
                },
                "database": {
                    "preferred": ["planetscale", "cockroachdb", "mongodb_atlas", "aws_rds"],
                    "reasoning": "High-performance and scalable solutions",
                    "avoid": []
                },
                "security": {
                    "preferred": ["snyk", "checkmarx", "sonarqube"],
                    "reasoning": "Advanced security and code analysis",
                    "avoid": []
                },
                "observability": {
                    "preferred": ["datadog", "newrelic", "splunk", "elastic"],
                    "reasoning": "Enterprise observability platforms",
                    "avoid": []
                }
            }
        }

    async def generate_experience_tailored_recommendations(
        self, 
        user: User, 
        limit: int = 10,
        context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Generate recommendations tailored to user's experience level"""
        
        # Get user profile
        profile = await self._get_user_profile(user)
        if not profile:
            return await self._generate_default_recommendations(user, limit)
        
        # Update profile completeness
        completeness = calculate_profile_completeness(profile)
        profile.profile_completeness_score = completeness
        await self.db.commit()
        
        # Get experience-specific recommendations
        experience_level = profile.experience_level
        if experience_level in self.experience_strategies:
            recommendations = await self.experience_strategies[experience_level](profile, limit, context)
        else:
            recommendations = await self._get_intermediate_recommendations(profile, limit, context)
        
        # Apply collaborative filtering
        collaborative_recs = await self._apply_collaborative_filtering(profile, recommendations)
        
        # Apply content-based filtering
        content_recs = await self._apply_content_based_filtering(profile, collaborative_recs)
        
        # Score and rank final recommendations
        final_recs = await self._score_and_rank_recommendations(profile, content_recs)
        
        # Track recommendation generation
        await self._track_recommendation_event(profile, "recommendations_generated", {
            "experience_level": experience_level.value,
            "count": len(final_recs),
            "context": context
        })
        
        return final_recs[:limit]

    async def _get_newbie_recommendations(
        self, 
        profile: UserProfile, 
        limit: int, 
        context: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate recommendations for newbie developers"""
        
        recommendations = []
        preferences = self.experience_tool_preferences[ExperienceLevelEnum.NEWBIE]
        
        # Prioritize categories based on common newbie needs
        priority_categories = ["hosting", "database", "auth", "ide"]
        
        for category in priority_categories:
            if category in preferences:
                category_prefs = preferences[category]
                
                for tool_name in category_prefs["preferred"][:2]:  # Top 2 per category
                    software = await self._get_software_by_name(tool_name)
                    if software and await self._user_doesnt_have_tool(profile.user_id, software.id):
                        
                        # Enhanced reasoning for newbies
                        reasoning = self._generate_newbie_reasoning(
                            software, 
                            category,
                            category_prefs["reasoning"]
                        )
                        
                        recommendations.append({
                            "software": software,
                            "confidence_score": 0.85,  # High confidence for beginner-friendly tools
                            "recommendation_type": "experience_tailored",
                            "experience_level": "newbie",
                            "reasoning": reasoning,
                            "category": category,
                            "beginner_friendly": True,
                            "setup_complexity": "simple",
                            "learning_resources": await self._get_learning_resources(software)
                        })
        
        return recommendations

    async def _get_intermediate_recommendations(
        self, 
        profile: UserProfile, 
        limit: int, 
        context: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate recommendations for intermediate developers"""
        
        recommendations = []
        preferences = self.experience_tool_preferences[ExperienceLevelEnum.INTERMEDIATE]
        
        # Mix of categories for growing skills
        priority_categories = ["hosting", "database", "ci_cd", "monitoring"]
        
        for category in priority_categories:
            if category in preferences:
                category_prefs = preferences[category]
                
                for tool_name in category_prefs["preferred"][:3]:  # Top 3 per category
                    software = await self._get_software_by_name(tool_name)
                    if software and await self._user_doesnt_have_tool(profile.user_id, software.id):
                        
                        reasoning = self._generate_intermediate_reasoning(
                            software,
                            category,
                            category_prefs["reasoning"],
                            profile
                        )
                        
                        recommendations.append({
                            "software": software,
                            "confidence_score": 0.75,
                            "recommendation_type": "experience_tailored",
                            "experience_level": "intermediate",
                            "reasoning": reasoning,
                            "category": category,
                            "growth_opportunity": True,
                            "setup_complexity": "balanced",
                            "skill_development": await self._get_skill_development_info(software)
                        })
        
        return recommendations

    async def _get_experienced_recommendations(
        self, 
        profile: UserProfile, 
        limit: int, 
        context: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate recommendations for experienced developers"""
        
        recommendations = []
        preferences = self.experience_tool_preferences[ExperienceLevelEnum.EXPERIENCED]
        
        # Professional-grade tools and services
        priority_categories = ["hosting", "database", "monitoring", "infrastructure"]
        
        for category in priority_categories:
            if category in preferences:
                category_prefs = preferences[category]
                
                for tool_name in category_prefs["preferred"][:3]:
                    software = await self._get_software_by_name(tool_name)
                    if software and await self._user_doesnt_have_tool(profile.user_id, software.id):
                        
                        reasoning = self._generate_experienced_reasoning(
                            software,
                            category,
                            category_prefs["reasoning"],
                            profile
                        )
                        
                        recommendations.append({
                            "software": software,
                            "confidence_score": 0.80,
                            "recommendation_type": "experience_tailored",
                            "experience_level": "experienced",
                            "reasoning": reasoning,
                            "category": category,
                            "professional_grade": True,
                            "setup_complexity": "advanced",
                            "enterprise_features": await self._get_enterprise_features(software)
                        })
        
        return recommendations

    async def _get_expert_recommendations(
        self, 
        profile: UserProfile, 
        limit: int, 
        context: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate recommendations for expert developers"""
        
        recommendations = []
        preferences = self.experience_tool_preferences[ExperienceLevelEnum.EXPERT]
        
        # Enterprise and architecture-focused tools
        priority_categories = ["hosting", "database", "security", "observability"]
        
        for category in priority_categories:
            if category in preferences:
                category_prefs = preferences[category]
                
                for tool_name in category_prefs["preferred"][:4]:  # More options for experts
                    software = await self._get_software_by_name(tool_name)
                    if software and await self._user_doesnt_have_tool(profile.user_id, software.id):
                        
                        reasoning = self._generate_expert_reasoning(
                            software,
                            category,
                            category_prefs["reasoning"],
                            profile
                        )
                        
                        recommendations.append({
                            "software": software,
                            "confidence_score": 0.70,  # Lower confidence, experts know what they want
                            "recommendation_type": "experience_tailored",
                            "experience_level": "expert",
                            "reasoning": reasoning,
                            "category": category,
                            "enterprise_grade": True,
                            "setup_complexity": "expert",
                            "architectural_benefits": await self._get_architectural_benefits(software)
                        })
        
        return recommendations

    def _generate_newbie_reasoning(self, software: Software, category: str, base_reasoning: str) -> str:
        """Generate beginner-friendly reasoning"""
        return f"Perfect for beginners! {software.display_name or software.name} is {base_reasoning.lower()}. " \
               f"It offers excellent documentation, helpful tutorials, and a supportive community. " \
               f"You can get started in minutes without complex configuration."

    def _generate_intermediate_reasoning(self, software: Software, category: str, base_reasoning: str, profile: UserProfile) -> str:
        """Generate intermediate-level reasoning"""
        primary_lang = profile.primary_languages[0] if profile.primary_languages else "your preferred language"
        return f"Great for growing your skills! {software.display_name or software.name} provides {base_reasoning.lower()}. " \
               f"It works well with {primary_lang} and offers room to explore more advanced features as you learn. " \
               f"This tool will help you build more complex projects while keeping things manageable."

    def _generate_experienced_reasoning(self, software: Software, category: str, base_reasoning: str, profile: UserProfile) -> str:
        """Generate experienced-level reasoning"""
        return f"Recommended for professional development. {software.display_name or software.name} offers {base_reasoning.lower()}. " \
               f"It provides the reliability and advanced features you need for production applications, " \
               f"with excellent integration capabilities and professional support options."

    def _generate_expert_reasoning(self, software: Software, category: str, base_reasoning: str, profile: UserProfile) -> str:
        """Generate expert-level reasoning"""
        return f"Enterprise-grade solution. {software.display_name or software.name} delivers {base_reasoning.lower()}. " \
               f"Designed for complex architectures and high-scale applications, it offers deep customization, " \
               f"advanced security features, and the flexibility needed for sophisticated implementations."

    async def _apply_collaborative_filtering(self, profile: UserProfile, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply collaborative filtering based on similar users"""
        
        # Find users with similar profiles
        similar_users = await self._find_similar_users(profile)
        
        if not similar_users:
            return recommendations
        
        # Get tools used by similar users
        similar_user_tools = await self._get_tools_used_by_similar_users(similar_users)
        
        # Boost recommendations that similar users liked
        for rec in recommendations:
            software_id = rec["software"].id
            if software_id in similar_user_tools:
                usage_count = similar_user_tools[software_id]
                boost = min(0.2, usage_count * 0.05)  # Max 20% boost
                rec["confidence_score"] += boost
                rec["collaborative_signal"] = f"{usage_count} similar developers use this tool"
        
        return recommendations

    async def _apply_content_based_filtering(self, profile: UserProfile, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply content-based filtering based on user preferences"""
        
        for rec in recommendations:
            software = rec["software"]
            
            # Boost based on language match
            if profile.primary_languages and software.tags:
                language_match = any(lang.lower() in [tag.lower() for tag in software.tags] 
                                   for lang in profile.primary_languages)
                if language_match:
                    rec["confidence_score"] += 0.15
                    rec["language_match"] = True
            
            # Boost based on domain interest
            if profile.domain_interests and software.category:
                domain_keywords = {
                    DomainInterestEnum.WEB_DEVELOPMENT: ["web", "frontend", "backend", "api"],
                    DomainInterestEnum.MOBILE_DEVELOPMENT: ["mobile", "ios", "android", "react native"],
                    DomainInterestEnum.AI_ML: ["ai", "ml", "machine learning", "neural"],
                    DomainInterestEnum.DEVOPS: ["devops", "deployment", "ci", "cd", "infrastructure"]
                }
                
                for domain in profile.domain_interests:
                    if domain in domain_keywords:
                        keywords = domain_keywords[domain]
                        if any(keyword in software.category.name.lower() for keyword in keywords):
                            rec["confidence_score"] += 0.1
                            rec["domain_match"] = domain.value
            
            # Adjust based on complexity preference
            if profile.complexity_preference:
                if profile.complexity_preference == "simple" and rec.get("setup_complexity") == "simple":
                    rec["confidence_score"] += 0.1
                elif profile.complexity_preference == "advanced" and rec.get("setup_complexity") in ["advanced", "expert"]:
                    rec["confidence_score"] += 0.1
        
        return recommendations

    async def _score_and_rank_recommendations(self, profile: UserProfile, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Final scoring and ranking of recommendations"""
        
        for rec in recommendations:
            software = rec["software"]
            
            # Factor in software quality metrics
            if software.success_rate and software.success_rate > 80:
                rec["confidence_score"] += 0.05
            
            if software.popularity_score and software.popularity_score > 70:
                rec["confidence_score"] += 0.05
            
            # Penalize if user has shown disinterest in category
            if profile.least_used_categories:
                software_category = software.category.name.lower() if software.category else ""
                if any(category.lower() in software_category for category in profile.least_used_categories):
                    rec["confidence_score"] -= 0.15
            
            # Ensure confidence score stays within bounds
            rec["confidence_score"] = max(0.0, min(1.0, rec["confidence_score"]))
        
        # Sort by confidence score
        return sorted(recommendations, key=lambda x: x["confidence_score"], reverse=True)

    async def _find_similar_users(self, profile: UserProfile) -> List[int]:
        """Find users with similar profiles"""
        
        # Simple similarity based on experience level and primary languages
        result = await self.db.execute(
            select(UserProfile.user_id).where(
                and_(
                    UserProfile.experience_level == profile.experience_level,
                    UserProfile.user_id != profile.user_id,
                    UserProfile.primary_languages.isnot(None)
                )
            ).limit(50)
        )
        
        return [row[0] for row in result.fetchall()]

    async def _get_tools_used_by_similar_users(self, user_ids: List[int]) -> Dict[int, int]:
        """Get tools used by similar users with usage counts"""
        
        result = await self.db.execute(
            select(DevAccount.software_id, func.count(DevAccount.software_id))
            .where(DevAccount.user_id.in_(user_ids))
            .group_by(DevAccount.software_id)
        )
        
        return {software_id: count for software_id, count in result.fetchall()}

    async def _get_user_profile(self, user: User) -> Optional[UserProfile]:
        """Get user profile"""
        result = await self.db.execute(
            select(UserProfile).where(UserProfile.user_id == user.id)
        )
        return result.scalar_one_or_none()

    async def _get_software_by_name(self, name: str) -> Optional[Software]:
        """Get software by name"""
        result = await self.db.execute(
            select(Software).where(Software.name.ilike(f"%{name}%"))
        )
        return result.scalar_one_or_none()

    async def _user_doesnt_have_tool(self, user_id: int, software_id: int) -> bool:
        """Check if user doesn't already have this tool"""
        result = await self.db.execute(
            select(DevAccount).where(
                and_(
                    DevAccount.user_id == user_id,
                    DevAccount.software_id == software_id
                )
            )
        )
        return result.scalar_one_or_none() is None

    async def _get_learning_resources(self, software: Software) -> List[Dict[str, str]]:
        """Get learning resources for beginners"""
        # Placeholder - would integrate with actual learning resource database
        return [
            {"type": "documentation", "url": software.documentation_url or software.website_url},
            {"type": "getting_started", "url": f"{software.website_url}/docs/getting-started"},
        ]

    async def _get_skill_development_info(self, software: Software) -> Dict[str, Any]:
        """Get skill development information for intermediate users"""
        return {
            "skills_learned": ["configuration", "integration", "best_practices"],
            "next_level_tools": [],
            "career_relevance": "high"
        }

    async def _get_enterprise_features(self, software: Software) -> List[str]:
        """Get enterprise features for experienced users"""
        return ["advanced_security", "team_collaboration", "enterprise_support", "sla_guarantees"]

    async def _get_architectural_benefits(self, software: Software) -> List[str]:
        """Get architectural benefits for expert users"""
        return ["scalability", "performance", "security", "integration_flexibility"]

    async def _generate_default_recommendations(self, user: User, limit: int) -> List[Dict[str, Any]]:
        """Generate default recommendations when no profile exists"""
        
        # Return popular tools across categories
        result = await self.db.execute(
            select(Software)
            .where(
                and_(
                    Software.is_active == True,
                    Software.has_free_tier == True,
                    Software.popularity_score >= 60
                )
            )
            .order_by(desc(Software.popularity_score))
            .limit(limit)
        )
        
        softwares = result.scalars().all()
        
        return [
            {
                "software": software,
                "confidence_score": 0.5,
                "recommendation_type": "popular",
                "reasoning": "Popular tool in the developer community with a generous free tier"
            }
            for software in softwares
        ]

    async def _track_recommendation_event(self, profile: UserProfile, event_type: str, event_data: Dict[str, Any]):
        """Track recommendation-related events"""
        
        event = UserBehavioralEvent(
            user_profile_id=profile.id,
            event_type=event_type,
            event_category="recommendations",
            event_data=event_data,
            timestamp=datetime.utcnow()
        )
        
        self.db.add(event)
        await self.db.commit()
