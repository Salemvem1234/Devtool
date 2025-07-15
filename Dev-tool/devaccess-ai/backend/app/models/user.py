"""
User model for DevAccess AI
"""
from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    """User model for authentication and profile management"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile information
    full_name = Column(String(255), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    
    # Preferences
    preferred_email_domain = Column(String(100), nullable=True)
    auto_create_accounts = Column(Boolean, default=True)
    notification_preferences = Column(Text, nullable=True)  # JSON string
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    dev_accounts = relationship("DevAccount", back_populates="user", cascade="all, delete-orphan")
    automation_tasks = relationship("AutomationTask", back_populates="user", cascade="all, delete-orphan")
    developer_profile = relationship("DeveloperProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    user_profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    usage_alerts = relationship("UsageAlert", back_populates="user", cascade="all, delete-orphan")
    team_memberships = relationship("TeamMembership", back_populates="user", cascade="all, delete-orphan")
    integration_configs = relationship("IntegrationConfig", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
