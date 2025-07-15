"""
DevAccount model for storing created developer accounts
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.core.database import Base


class AccountStatusEnum(PyEnum):
    """Account status enumeration"""
    PENDING = "pending"
    ACTIVE = "active"
    VERIFICATION_REQUIRED = "verification_required"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    FAILED = "failed"


class DevAccount(Base):
    """Model for storing created developer accounts"""
    
    __tablename__ = "dev_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    software_id = Column(Integer, ForeignKey("software.id"), nullable=False)
    
    # Account credentials (encrypted)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(500), nullable=False)  # Encrypted password
    username = Column(String(200), nullable=True)
    
    # Account information
    account_id = Column(String(200), nullable=True)  # External account ID if available
    account_url = Column(String(500), nullable=True)  # Direct link to account/dashboard
    
    # Status and verification
    status = Column(Enum(AccountStatusEnum), default=AccountStatusEnum.PENDING)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(500), nullable=True)
    verification_expires_at = Column(DateTime, nullable=True)
    
    # Free tier information
    free_tier_expires_at = Column(DateTime, nullable=True)
    usage_statistics = Column(Text, nullable=True)  # JSON string with usage data
    
    # Automation metadata
    creation_method = Column(String(50), nullable=True)  # 'automation', 'api', 'manual'
    automation_task_id = Column(Integer, ForeignKey("automation_tasks.id"), nullable=True)
    
    # Additional metadata
    notes = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)  # JSON array of user-defined tags
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_accessed = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="dev_accounts")
    software = relationship("Software", back_populates="dev_accounts")
    automation_task = relationship("AutomationTask", back_populates="created_account")
    usage_metrics = relationship("UsageMetric", back_populates="dev_account", cascade="all, delete-orphan")
    api_credentials = relationship("APICredential", back_populates="dev_account", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<DevAccount(id={self.id}, software='{self.software.name if self.software else 'Unknown'}', email='{self.email}', status='{self.status.value}')>"
