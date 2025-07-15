"""
Automation models for tracking tasks and results
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.core.database import Base


class TaskStatusEnum(PyEnum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class AutomationMethodEnum(PyEnum):
    """Automation method enumeration"""
    SELENIUM = "selenium"
    PLAYWRIGHT = "playwright"
    API = "api"
    HYBRID = "hybrid"


class AutomationTask(Base):
    """Model for tracking automation tasks"""
    
    __tablename__ = "automation_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    software_id = Column(Integer, ForeignKey("software.id"), nullable=False)
    
    # Task information
    task_type = Column(String(50), nullable=False)  # 'account_creation', 'verification', etc.
    method = Column(Enum(AutomationMethodEnum), nullable=False)
    status = Column(Enum(TaskStatusEnum), default=TaskStatusEnum.PENDING)
    
    # Request details
    user_request = Column(Text, nullable=True)  # Original user request/intent
    parsed_intent = Column(JSON, nullable=True)  # NLP parsed intent and entities
    
    # Execution details
    execution_plan = Column(JSON, nullable=True)  # Step-by-step execution plan
    current_step = Column(Integer, default=0)
    total_steps = Column(Integer, default=0)
    
    # Credentials and configuration
    generated_email = Column(String(255), nullable=True)
    email_provider = Column(String(100), nullable=True)
    automation_config = Column(JSON, nullable=True)  # Configuration used for automation
    
    # Results and monitoring
    success = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)
    execution_log = Column(Text, nullable=True)  # Detailed execution log
    screenshots = Column(JSON, nullable=True)  # Array of screenshot URLs/paths
    
    # Performance metrics
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="automation_tasks")
    software = relationship("Software", back_populates="automation_tasks")
    created_account = relationship("DevAccount", back_populates="automation_task", uselist=False)
    results = relationship("AutomationResult", back_populates="task", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<AutomationTask(id={self.id}, software='{self.software.name if self.software else 'Unknown'}', status='{self.status.value}')>"


class AutomationResult(Base):
    """Model for storing detailed automation results and artifacts"""
    
    __tablename__ = "automation_results"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key
    task_id = Column(Integer, ForeignKey("automation_tasks.id"), nullable=False)
    
    # Result details
    step_number = Column(Integer, nullable=False)
    step_name = Column(String(200), nullable=False)
    step_status = Column(Enum(TaskStatusEnum), nullable=False)
    
    # Step execution details
    action_performed = Column(String(500), nullable=True)
    selector_used = Column(String(500), nullable=True)
    input_data = Column(JSON, nullable=True)
    
    # Results
    success = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)
    screenshot_path = Column(String(500), nullable=True)
    page_source = Column(Text, nullable=True)
    
    # Performance
    execution_time_ms = Column(Integer, nullable=True)
    
    # Timestamps
    executed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    task = relationship("AutomationTask", back_populates="results")
    
    def __repr__(self):
        return f"<AutomationResult(id={self.id}, task_id={self.task_id}, step='{self.step_name}', status='{self.step_status.value}')>"
