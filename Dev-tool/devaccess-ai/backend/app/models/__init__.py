"""
Database models for DevAccess AI
"""
from app.core.database import Base
from .user import User
from .software import Software, SoftwareCategory
from .account import DevAccount
from .automation import AutomationTask, AutomationResult
from .enhanced_models import (
    UsageMetric, UsageAlert, APICredential, DeveloperProfile,
    ToolRecommendation, TeamWorkspace, TeamMembership, SharedAccount,
    IntegrationConfig, AlertTypeEnum, ProjectTypeEnum
)
from .user_profiling import (
    UserProfile, ExperienceLevelEnum, DomainInterestEnum, ProjectGoalEnum,
    UserBehavioralEvent, RecommendationInteraction, OnboardingResponse,
    ProfileInsight, calculate_profile_completeness
)

__all__ = [
    "Base",
    "User", 
    "Software",
    "SoftwareCategory",
    "DevAccount",
    "AutomationTask",
    "AutomationResult",
    "UsageMetric",
    "UsageAlert",
    "APICredential",
    "DeveloperProfile",
    "ToolRecommendation",
    "TeamWorkspace",
    "TeamMembership",
    "SharedAccount",
    "IntegrationConfig",
    "AlertTypeEnum",
    "ProjectTypeEnum",
    "UserProfile",
    "ExperienceLevelEnum",
    "DomainInterestEnum",
    "ProjectGoalEnum",
    "UserBehavioralEvent",
    "RecommendationInteraction",
    "OnboardingResponse",
    "ProfileInsight",
    "calculate_profile_completeness"
]
