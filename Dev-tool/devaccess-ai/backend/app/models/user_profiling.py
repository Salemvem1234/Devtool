"""
Advanced User Profiling Models for DevAccess AI
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.core.database import Base


class ExperienceLevelEnum(PyEnum):
    """Developer experience level enumeration"""
    NEWBIE = "newbie"           # Just starting out, learning the basics
    INTERMEDIATE = "intermediate"  # Comfortable with fundamentals, building small projects
    EXPERIENCED = "experienced"   # Working professionally, comfortable with complex stacks
    EXPERT = "expert"           # Leading teams, designing complex systems


class DomainInterestEnum(PyEnum):
    """Development domain interest enumeration"""
    WEB_DEVELOPMENT = "web_development"
    MOBILE_DEVELOPMENT = "mobile_development"
    AI_ML = "ai_ml"
    DATA_SCIENCE = "data_science"
    GAME_DEVELOPMENT = "game_development"
    DEVOPS = "devops"
    CYBERSECURITY = "cybersecurity"
    IOT = "iot"
    BLOCKCHAIN = "blockchain"
    BACKEND_SERVICES = "backend_services"
    FRONTEND_UI_UX = "frontend_ui_ux"
    DESKTOP_APPS = "desktop_apps"
    EMBEDDED_SYSTEMS = "embedded_systems"


class ProjectGoalEnum(PyEnum):
    """Current project goal enumeration"""
    LEARNING = "learning"
    PERSONAL_PROJECT = "personal_project"
    STARTUP = "startup"
    FREELANCE = "freelance"
    ENTERPRISE = "enterprise"
    OPEN_SOURCE = "open_source"
    PORTFOLIO = "portfolio"
    EXPERIMENTATION = "experimentation"


class UserProfile(Base):
    """Comprehensive user profile for personalized recommendations"""
    
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # === EXPLICIT DATA COLLECTION ===
    
    # Experience Level (Critical for recommendations)
    experience_level = Column(Enum(ExperienceLevelEnum), nullable=False)
    years_of_experience = Column(Integer, nullable=True)  # Optional numeric supplement
    
    # Primary Programming Languages
    primary_languages = Column(JSON, nullable=True)  # ["Python", "JavaScript", "TypeScript"]
    secondary_languages = Column(JSON, nullable=True)  # Languages they're learning or occasionally use
    
    # Preferred Tech Stacks/Ecosystems
    preferred_stacks = Column(JSON, nullable=True)  # ["MERN", "JAMstack", "Serverless", "AWS Ecosystem"]
    cloud_platforms = Column(JSON, nullable=True)  # ["AWS", "GCP", "Azure", "Vercel", "Netlify"]
    
    # Areas of Interest/Domain
    domain_interests = Column(JSON, nullable=True)  # Array of DomainInterestEnum values
    primary_domain = Column(Enum(DomainInterestEnum), nullable=True)
    
    # Current Project Goals
    current_project_description = Column(Text, nullable=True)  # Free text description
    project_goals = Column(JSON, nullable=True)  # Array of ProjectGoalEnum values
    current_tech_stack = Column(JSON, nullable=True)  # What they're currently using
    
    # Tool Categories They Need
    needed_tool_categories = Column(JSON, nullable=True)  # ["databases", "hosting", "ci_cd", "monitoring"]
    
    # Learning Preferences
    learning_style = Column(String(50), nullable=True)  # "hands_on", "documentation", "video", "community"
    complexity_preference = Column(String(50), nullable=True)  # "simple", "balanced", "advanced"
    
    # Team Context
    team_size = Column(String(20), nullable=True)  # "solo", "small_team", "large_team"
    team_role = Column(String(50), nullable=True)  # "individual_contributor", "lead", "architect", "manager"
    
    # Budget/Cost Sensitivity
    budget_preference = Column(String(20), default="free_first")  # "free_only", "free_first", "cost_conscious", "value_focused"
    
    # === IMPLICIT DATA COLLECTION ===
    
    # Tool Request Patterns
    total_tools_requested = Column(Integer, default=0)
    successful_setups = Column(Integer, default=0)
    abandoned_setups = Column(Integer, default=0)
    
    # Category Preferences (learned from behavior)
    most_requested_categories = Column(JSON, nullable=True)  # Frequency count of categories
    least_used_categories = Column(JSON, nullable=True)
    
    # Usage Patterns
    avg_session_duration_minutes = Column(Float, nullable=True)
    most_active_time_of_day = Column(String(20), nullable=True)  # "morning", "afternoon", "evening", "night"
    frequency_of_use = Column(String(20), nullable=True)  # "daily", "weekly", "monthly", "sporadic"
    
    # Tool Lifecycle Behavior
    avg_tool_usage_duration_days = Column(Float, nullable=True)  # How long they keep accounts active
    tool_deletion_rate = Column(Float, default=0.0)  # Percentage of tools they delete
    
    # Search and Discovery Patterns
    common_search_terms = Column(JSON, nullable=True)  # Most frequent search queries
    discovery_method_preference = Column(String(50), nullable=True)  # "search", "browse", "recommendations"
    
    # Feature Usage Patterns
    most_used_features = Column(JSON, nullable=True)  # Which DevAccess AI features they use most
    feature_adoption_speed = Column(String(20), nullable=True)  # "early_adopter", "steady", "cautious"
    
    # Recommendation Interaction
    recommendation_acceptance_rate = Column(Float, default=0.0)  # How often they accept recommendations
    feedback_frequency = Column(Float, default=0.0)  # How often they provide feedback
    
    # === COMPUTED INSIGHTS ===
    
    # AI-Generated Profile Insights
    developer_archetype = Column(String(50), nullable=True)  # "full_stack_generalist", "frontend_specialist", etc.
    skill_trajectory = Column(String(50), nullable=True)  # "rapid_learner", "steady_growth", "specialized_expert"
    tool_adoption_pattern = Column(String(50), nullable=True)  # "early_adopter", "mainstream", "conservative"
    
    # Recommendation Confidence
    profile_completeness_score = Column(Float, default=0.0)  # 0-1 score of how complete the profile is
    recommendation_confidence = Column(Float, default=0.0)  # How confident we are in recommendations
    
    # Personalization Effectiveness
    personalization_score = Column(Float, default=0.0)  # How well personalized their experience is
    satisfaction_indicators = Column(JSON, nullable=True)  # Various satisfaction metrics
    
    # === TIMESTAMPS ===
    
    profile_created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_activity = Column(DateTime, nullable=True)
    onboarding_completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="user_profile")
    behavioral_events = relationship("UserBehavioralEvent", back_populates="user_profile", cascade="all, delete-orphan")
    recommendation_interactions = relationship("RecommendationInteraction", back_populates="user_profile", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, experience={self.experience_level.value if self.experience_level else 'None'}, domain={self.primary_domain.value if self.primary_domain else 'None'})>"


class UserBehavioralEvent(Base):
    """Track user behavioral events for implicit profiling"""
    
    __tablename__ = "user_behavioral_events"
    
    id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    
    # Event Details
    event_type = Column(String(50), nullable=False)  # "tool_request", "search", "feature_use", "login", etc.
    event_category = Column(String(50), nullable=True)  # "engagement", "conversion", "retention"
    event_data = Column(JSON, nullable=True)  # Flexible event-specific data
    
    # Context
    session_id = Column(String(100), nullable=True)
    page_path = Column(String(200), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    # Timing
    duration_seconds = Column(Float, nullable=True)  # How long the event took
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user_profile = relationship("UserProfile", back_populates="behavioral_events")


class RecommendationInteraction(Base):
    """Track how users interact with recommendations"""
    
    __tablename__ = "recommendation_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    recommendation_id = Column(Integer, ForeignKey("tool_recommendations.id"), nullable=False)
    
    # Interaction Details
    interaction_type = Column(String(50), nullable=False)  # "viewed", "clicked", "dismissed", "saved", "used"
    interaction_data = Column(JSON, nullable=True)  # Additional interaction context
    
    # Timing
    time_to_interaction_seconds = Column(Float, nullable=True)  # Time from show to interaction
    interaction_duration_seconds = Column(Float, nullable=True)
    
    # Outcome
    led_to_account_creation = Column(Boolean, default=False)
    led_to_long_term_usage = Column(Boolean, default=False)
    
    # Feedback
    explicit_rating = Column(Integer, nullable=True)  # 1-5 stars if provided
    implicit_satisfaction_score = Column(Float, nullable=True)  # Computed from behavior
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user_profile = relationship("UserProfile", back_populates="recommendation_interactions")
    recommendation = relationship("ToolRecommendation")


class OnboardingResponse(Base):
    """Store structured onboarding responses for analysis"""
    
    __tablename__ = "onboarding_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    
    # Onboarding Flow Tracking
    flow_version = Column(String(20), default="v1")
    step_number = Column(Integer, nullable=False)
    question_id = Column(String(100), nullable=False)
    
    # Response Data
    question_text = Column(Text, nullable=False)
    response_type = Column(String(50), nullable=False)  # "multiple_choice", "text", "multi_select", "scale"
    response_data = Column(JSON, nullable=False)  # The actual response
    
    # Metadata
    time_to_answer_seconds = Column(Float, nullable=True)
    skipped = Column(Boolean, default=False)
    confidence_level = Column(String(20), nullable=True)  # "very_sure", "somewhat_sure", "unsure"
    
    # Completion Tracking
    completed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user_profile = relationship("UserProfile")


class ProfileInsight(Base):
    """AI-generated insights about user profiles"""
    
    __tablename__ = "profile_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    
    # Insight Details
    insight_type = Column(String(50), nullable=False)  # "skill_assessment", "recommendation_improvement", "learning_path"
    insight_category = Column(String(50), nullable=True)  # "strengths", "gaps", "opportunities"
    
    # Content
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    confidence_score = Column(Float, nullable=False)  # 0-1 confidence in this insight
    
    # Supporting Data
    supporting_evidence = Column(JSON, nullable=True)  # Data that led to this insight
    recommended_actions = Column(JSON, nullable=True)  # Suggested actions based on insight
    
    # Status
    is_active = Column(Boolean, default=True)
    user_acknowledged = Column(Boolean, default=False)
    user_feedback = Column(Text, nullable=True)
    
    # Timing
    generated_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    user_profile = relationship("UserProfile")


# Helper function to calculate profile completeness
def calculate_profile_completeness(profile: UserProfile) -> float:
    """Calculate how complete a user profile is (0-1 scale)"""
    
    completeness_factors = {
        'experience_level': 0.15,  # Critical for recommendations
        'primary_languages': 0.15,  # Critical for recommendations
        'domain_interests': 0.10,
        'preferred_stacks': 0.10,
        'current_project_description': 0.08,
        'needed_tool_categories': 0.08,
        'team_size': 0.05,
        'learning_style': 0.05,
        'complexity_preference': 0.05,
        'budget_preference': 0.05,
        'years_of_experience': 0.04,
        'secondary_languages': 0.04,
        'cloud_platforms': 0.03,
        'project_goals': 0.03
    }
    
    score = 0.0
    
    for field, weight in completeness_factors.items():
        value = getattr(profile, field, None)
        if value is not None and value != [] and value != "":
            score += weight
    
    return min(score, 1.0)
