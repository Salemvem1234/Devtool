"""
Software models for DevAccess AI - Development tools registry
"""
from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.core.database import Base


class SoftwareCategoryEnum(PyEnum):
    """Software category enumeration"""
    IDE = "ide"
    CI_CD = "ci_cd"
    DATABASE = "database"
    CLOUD_SERVICE = "cloud_service"
    API_SERVICE = "api_service"
    TESTING = "testing"
    MONITORING = "monitoring"
    ANALYTICS = "analytics"
    SECURITY = "security"
    DEPLOYMENT = "deployment"
    STORAGE = "storage"
    CDN = "cdn"
    EMAIL = "email"
    AUTHENTICATION = "authentication"
    PAYMENT = "payment"
    OTHER = "other"


class SoftwareCategory(Base):
    """Software category model"""
    
    __tablename__ = "software_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    icon_url = Column(String(500), nullable=True)
    
    # Relationships
    software = relationship("Software", back_populates="category")
    
    def __repr__(self):
        return f"<SoftwareCategory(id={self.id}, name='{self.name}')>"


class Software(Base):
    """Software/Development tool model"""
    
    __tablename__ = "software"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    display_name = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    
    # Basic information
    website_url = Column(String(500), nullable=False)
    signup_url = Column(String(500), nullable=True)
    documentation_url = Column(String(500), nullable=True)
    logo_url = Column(String(500), nullable=True)
    
    # Category
    category_id = Column(Integer, ForeignKey("software_categories.id"), nullable=False)
    tags = Column(JSON, nullable=True)  # Array of tags
    
    # Free tier information
    has_free_tier = Column(Boolean, default=False)
    free_tier_description = Column(Text, nullable=True)
    free_tier_limitations = Column(JSON, nullable=True)  # JSON object with limitations
    trial_duration_days = Column(Integer, nullable=True)
    
    # Automation information
    automation_supported = Column(Boolean, default=False)
    signup_automation_config = Column(JSON, nullable=True)  # Automation configuration
    requires_verification = Column(Boolean, default=True)
    requires_phone = Column(Boolean, default=False)
    has_captcha = Column(Boolean, default=False)
    
    # API information
    has_public_api = Column(Boolean, default=False)
    api_signup_endpoint = Column(String(500), nullable=True)
    api_documentation_url = Column(String(500), nullable=True)
    
    # Status and metrics
    is_active = Column(Boolean, default=True)
    popularity_score = Column(Integer, default=0)
    success_rate = Column(Integer, default=0)  # Automation success rate percentage
    last_verified = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship("SoftwareCategory", back_populates="software")
    dev_accounts = relationship("DevAccount", back_populates="software")
    automation_tasks = relationship("AutomationTask", back_populates="software")
    
    def __repr__(self):
        return f"<Software(id={self.id}, name='{self.name}', category='{self.category.name if self.category else 'Unknown'}')>"
