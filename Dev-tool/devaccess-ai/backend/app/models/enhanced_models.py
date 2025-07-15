"""
Enhanced models for comprehensive DevAccess AI features
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.core.database import Base


class AlertTypeEnum(PyEnum):
    """Alert type enumeration"""
    USAGE_WARNING = "usage_warning"
    QUOTA_EXCEEDED = "quota_exceeded"
    EXPIRY_REMINDER = "expiry_reminder"
    ACCOUNT_SUSPENDED = "account_suspended"
    API_KEY_ROTATED = "api_key_rotated"
    FREE_TIER_UPGRADED = "free_tier_upgraded"


class ProjectTypeEnum(PyEnum):
    """Project type enumeration for recommendations"""
    WEB_APP = "web_app"
    MOBILE_APP = "mobile_app"
    API_SERVICE = "api_service"
    DESKTOP_APP = "desktop_app"
    DATA_PIPELINE = "data_pipeline"
    MACHINE_LEARNING = "machine_learning"
    DEVOPS = "devops"
    MICROSERVICES = "microservices"


class UsageMetric(Base):
    """Model for tracking free tier usage metrics"""
    
    __tablename__ = "usage_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    dev_account_id = Column(Integer, ForeignKey("dev_accounts.id"), nullable=False)
    
    # Metric information
    metric_name = Column(String(100), nullable=False)  # e.g., "api_calls", "storage_gb", "build_minutes"
    current_usage = Column(Float, default=0.0)
    limit_value = Column(Float, nullable=True)
    unit = Column(String(50), nullable=True)  # e.g., "requests", "GB", "minutes"
    
    # Percentage and status
    usage_percentage = Column(Float, default=0.0)
    is_critical = Column(Boolean, default=False)  # > 90%
    is_warning = Column(Boolean, default=False)   # > 75%
    
    # Tracking metadata
    last_updated = Column(DateTime, default=datetime.utcnow)
    last_checked = Column(DateTime, default=datetime.utcnow)
    check_frequency_hours = Column(Integer, default=24)
    
    # Data source
    data_source = Column(String(100), nullable=True)  # "api", "scraping", "manual"
    raw_data = Column(JSON, nullable=True)
    
    # Relationships
    dev_account = relationship("DevAccount", back_populates="usage_metrics")
    alerts = relationship("UsageAlert", back_populates="usage_metric", cascade="all, delete-orphan")


class UsageAlert(Base):
    """Model for usage alerts and notifications"""
    
    __tablename__ = "usage_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dev_account_id = Column(Integer, ForeignKey("dev_accounts.id"), nullable=False)
    usage_metric_id = Column(Integer, ForeignKey("usage_metrics.id"), nullable=True)
    
    # Alert information
    alert_type = Column(Enum(AlertTypeEnum), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(20), default="info")  # info, warning, critical
    
    # Status
    is_read = Column(Boolean, default=False)
    is_resolved = Column(Boolean, default=False)
    auto_generated = Column(Boolean, default=True)
    
    # Actions and recommendations
    recommended_actions = Column(JSON, nullable=True)
    action_taken = Column(String(100), nullable=True)
    
    # Timing
    triggered_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User")
    dev_account = relationship("DevAccount")
    usage_metric = relationship("UsageMetric", back_populates="alerts")


class APICredential(Base):
    """Model for storing extracted API keys and tokens"""
    
    __tablename__ = "api_credentials"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    dev_account_id = Column(Integer, ForeignKey("dev_accounts.id"), nullable=False)
    
    # Credential information
    credential_type = Column(String(50), nullable=False)  # "api_key", "token", "secret", "webhook_url"
    credential_name = Column(String(100), nullable=True)  # e.g., "Production API Key", "Webhook Secret"
    encrypted_value = Column(String(1000), nullable=False)  # Encrypted credential
    
    # Metadata
    scope = Column(String(200), nullable=True)  # Permissions/scope
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    usage_count = Column(Integer, default=0)
    last_used = Column(DateTime, nullable=True)
    
    # Extraction metadata
    extracted_from = Column(String(200), nullable=True)  # "dashboard", "email", "api_response"
    extraction_method = Column(String(100), nullable=True)  # "scraping", "email_parsing", "api"
    
    # Security
    last_rotated = Column(DateTime, nullable=True)
    rotation_frequency_days = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    dev_account = relationship("DevAccount", back_populates="api_credentials")


class DeveloperProfile(Base):
    """Enhanced developer profile for personalized recommendations"""
    
    __tablename__ = "developer_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # Technical profile
    primary_languages = Column(JSON, nullable=True)  # ["Python", "JavaScript", "Go"]
    frameworks = Column(JSON, nullable=True)  # ["React", "FastAPI", "Django"]
    cloud_preferences = Column(JSON, nullable=True)  # ["AWS", "Vercel", "Netlify"]
    project_types = Column(JSON, nullable=True)  # Project types they work on
    
    # Experience level
    experience_level = Column(String(20), default="intermediate")  # beginner, intermediate, expert
    team_size = Column(String(20), nullable=True)  # solo, small_team, large_team
    
    # Usage patterns
    most_used_categories = Column(JSON, nullable=True)
    preferred_tools = Column(JSON, nullable=True)
    avoided_tools = Column(JSON, nullable=True)  # Tools they don't want recommended
    
    # Preferences
    notification_preferences = Column(JSON, nullable=True)
    alert_thresholds = Column(JSON, nullable=True)  # Custom alert thresholds
    automation_preferences = Column(JSON, nullable=True)
    
    # Analytics
    total_accounts_created = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    avg_setup_time_minutes = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="developer_profile", uselist=False)
    tool_recommendations = relationship("ToolRecommendation", back_populates="developer_profile")


class ToolRecommendation(Base):
    """Model for AI-powered tool recommendations"""
    
    __tablename__ = "tool_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    developer_profile_id = Column(Integer, ForeignKey("developer_profiles.id"), nullable=False)
    software_id = Column(Integer, ForeignKey("software.id"), nullable=False)
    
    # Recommendation details
    recommendation_type = Column(String(50), nullable=False)  # "personalized", "trending", "stack_based"
    confidence_score = Column(Float, default=0.0)  # 0.0 to 1.0
    ranking = Column(Integer, default=0)
    
    # Context
    project_context = Column(JSON, nullable=True)  # What project/stack this is recommended for
    reasoning = Column(Text, nullable=True)  # Why this tool is recommended
    alternatives = Column(JSON, nullable=True)  # Alternative tools
    
    # User feedback
    user_rating = Column(Integer, nullable=True)  # 1-5 stars
    user_feedback = Column(Text, nullable=True)
    was_used = Column(Boolean, default=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    dismissed = Column(Boolean, default=False)
    dismissed_reason = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    developer_profile = relationship("DeveloperProfile", back_populates="tool_recommendations")
    software = relationship("Software")


class TeamWorkspace(Base):
    """Model for team collaboration features"""
    
    __tablename__ = "team_workspaces"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Team information
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    invite_code = Column(String(50), unique=True, nullable=False)
    
    # Settings
    settings = Column(JSON, nullable=True)  # Team-wide settings
    shared_categories = Column(JSON, nullable=True)  # Which categories to share
    
    # Security
    require_approval = Column(Boolean, default=False)
    max_members = Column(Integer, default=10)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    memberships = relationship("TeamMembership", back_populates="team", cascade="all, delete-orphan")
    shared_accounts = relationship("SharedAccount", back_populates="team", cascade="all, delete-orphan")


class TeamMembership(Base):
    """Model for team membership and roles"""
    
    __tablename__ = "team_memberships"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("team_workspaces.id"), nullable=False)
    
    # Role and permissions
    role = Column(String(20), default="member")  # owner, admin, member, viewer
    permissions = Column(JSON, nullable=True)  # Granular permissions
    
    # Status
    is_active = Column(Boolean, default=True)
    invited_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    inviter = relationship("User", foreign_keys=[invited_by])
    team = relationship("TeamWorkspace", back_populates="memberships")


class SharedAccount(Base):
    """Model for securely sharing account access within teams"""
    
    __tablename__ = "shared_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    dev_account_id = Column(Integer, ForeignKey("dev_accounts.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("team_workspaces.id"), nullable=False)
    shared_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Sharing configuration
    access_level = Column(String(20), default="view")  # view, use, admin
    allowed_roles = Column(JSON, nullable=True)  # Which team roles can access
    
    # Security
    requires_approval = Column(Boolean, default=False)
    max_concurrent_users = Column(Integer, default=1)
    session_timeout_minutes = Column(Integer, default=60)
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    last_accessed = Column(DateTime, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    dev_account = relationship("DevAccount")
    team = relationship("TeamWorkspace", back_populates="shared_accounts")
    sharer = relationship("User")


class IntegrationConfig(Base):
    """Model for IDE, CLI, and workflow integrations"""
    
    __tablename__ = "integration_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Integration details
    integration_type = Column(String(50), nullable=False)  # "vscode", "cli", "github_actions", "slack"
    integration_name = Column(String(100), nullable=False)
    
    # Configuration
    config_data = Column(JSON, nullable=False)  # Integration-specific configuration
    encrypted_tokens = Column(JSON, nullable=True)  # Encrypted access tokens
    
    # Status
    is_active = Column(Boolean, default=True)
    last_sync = Column(DateTime, nullable=True)
    sync_status = Column(String(20), default="pending")  # pending, active, error
    
    # Error handling
    last_error = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")


# Update existing models with new relationships
def enhance_existing_models():
    """Add new relationships to existing models"""
    pass
