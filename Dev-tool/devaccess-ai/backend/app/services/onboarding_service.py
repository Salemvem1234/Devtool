"""
User Onboarding Service - Collecting the Right Data for Personalization
"""
from datetime import datetime
from typing import Dict, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog

from app.models.user import User
from app.models.user_profiling import (
    UserProfile, ExperienceLevelEnum, DomainInterestEnum, ProjectGoalEnum,
    OnboardingResponse, UserBehavioralEvent, calculate_profile_completeness
)
from app.core.config import settings

logger = structlog.get_logger()


class OnboardingService:
    """Service for managing user onboarding and profile creation"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        
        # Define the onboarding flow questions
        self.onboarding_questions = {
            "v1": [
                {
                    "step": 1,
                    "question_id": "experience_level",
                    "question_text": "What best describes your development experience level?",
                    "response_type": "single_choice",
                    "required": True,
                    "options": [
                        {
                            "value": "newbie",
                            "label": "Newbie/Beginner",
                            "description": "Just starting out, learning the basics"
                        },
                        {
                            "value": "intermediate", 
                            "label": "Intermediate",
                            "description": "Comfortable with fundamentals, building small projects"
                        },
                        {
                            "value": "experienced",
                            "label": "Experienced/Professional", 
                            "description": "Working professionally, comfortable with complex stacks"
                        },
                        {
                            "value": "expert",
                            "label": "Expert/Architect",
                            "description": "Leading teams, designing complex systems"
                        }
                    ]
                },
                {
                    "step": 2,
                    "question_id": "primary_languages",
                    "question_text": "Which programming languages do you primarily work with?",
                    "response_type": "multi_select",
                    "required": True,
                    "max_selections": 5,
                    "options": [
                        {"value": "javascript", "label": "JavaScript"},
                        {"value": "typescript", "label": "TypeScript"},
                        {"value": "python", "label": "Python"},
                        {"value": "java", "label": "Java"},
                        {"value": "csharp", "label": "C#"},
                        {"value": "go", "label": "Go"},
                        {"value": "rust", "label": "Rust"},
                        {"value": "php", "label": "PHP"},
                        {"value": "ruby", "label": "Ruby"},
                        {"value": "cpp", "label": "C++"},
                        {"value": "swift", "label": "Swift"},
                        {"value": "kotlin", "label": "Kotlin"},
                        {"value": "dart", "label": "Dart"},
                        {"value": "other", "label": "Other"}
                    ]
                },
                {
                    "step": 3,
                    "question_id": "domain_interests",
                    "question_text": "What types of applications or domains are you most interested in building?",
                    "response_type": "multi_select",
                    "required": True,
                    "max_selections": 4,
                    "options": [
                        {"value": "web_development", "label": "Web Development"},
                        {"value": "mobile_development", "label": "Mobile Development"},
                        {"value": "ai_ml", "label": "AI/Machine Learning"},
                        {"value": "data_science", "label": "Data Science"},
                        {"value": "game_development", "label": "Game Development"},
                        {"value": "devops", "label": "DevOps"},
                        {"value": "cybersecurity", "label": "Cybersecurity"},
                        {"value": "iot", "label": "IoT"},
                        {"value": "blockchain", "label": "Blockchain/Web3"},
                        {"value": "backend_services", "label": "Backend Services"},
                        {"value": "frontend_ui_ux", "label": "Frontend/UI/UX"},
                        {"value": "desktop_apps", "label": "Desktop Applications"}
                    ]
                },
                {
                    "step": 4,
                    "question_id": "preferred_stacks",
                    "question_text": "Are there any specific technology stacks or ecosystems you prefer?",
                    "response_type": "multi_select",
                    "required": False,
                    "max_selections": 5,
                    "options": [
                        {"value": "mern", "label": "MERN (MongoDB, Express, React, Node.js)"},
                        {"value": "mean", "label": "MEAN (MongoDB, Express, Angular, Node.js)"},
                        {"value": "jamstack", "label": "JAMstack (JavaScript, APIs, Markup)"},
                        {"value": "serverless", "label": "Serverless Architecture"},
                        {"value": "kubernetes", "label": "Kubernetes/Containerization"},
                        {"value": "aws_ecosystem", "label": "AWS Ecosystem"},
                        {"value": "azure_ecosystem", "label": "Azure Ecosystem"},
                        {"value": "gcp_ecosystem", "label": "Google Cloud Platform"},
                        {"value": "react_native", "label": "React Native"},
                        {"value": "flutter", "label": "Flutter"},
                        {"value": "django", "label": "Django"},
                        {"value": "rails", "label": "Ruby on Rails"},
                        {"value": "spring", "label": "Spring (Java)"},
                        {"value": "dotnet", "label": ".NET"}
                    ]
                },
                {
                    "step": 5,
                    "question_id": "tool_categories",
                    "question_text": "Which categories of development tools are you most likely to need free access to?",
                    "response_type": "multi_select",
                    "required": True,
                    "max_selections": 6,
                    "options": [
                        {"value": "hosting", "label": "Web Hosting & Deployment"},
                        {"value": "databases", "label": "Databases (SQL/NoSQL)"},
                        {"value": "ci_cd", "label": "CI/CD & Build Tools"},
                        {"value": "monitoring", "label": "Monitoring & Analytics"},
                        {"value": "authentication", "label": "Authentication Services"},
                        {"value": "api_tools", "label": "API Development & Testing"},
                        {"value": "storage", "label": "File Storage & CDN"},
                        {"value": "communication", "label": "Email & Communication"},
                        {"value": "ide", "label": "IDEs & Code Editors"},
                        {"value": "version_control", "label": "Version Control"},
                        {"value": "security", "label": "Security & Code Analysis"},
                        {"value": "ai_services", "label": "AI/ML Services"}
                    ]
                },
                {
                    "step": 6,
                    "question_id": "project_goals",
                    "question_text": "What best describes your current project goals?",
                    "response_type": "multi_select",
                    "required": False,
                    "max_selections": 3,
                    "options": [
                        {"value": "learning", "label": "Learning new technologies"},
                        {"value": "personal_project", "label": "Building personal projects"},
                        {"value": "portfolio", "label": "Creating portfolio pieces"},
                        {"value": "startup", "label": "Working on a startup idea"},
                        {"value": "freelance", "label": "Freelance client work"},
                        {"value": "enterprise", "label": "Enterprise/corporate development"},
                        {"value": "open_source", "label": "Contributing to open source"},
                        {"value": "experimentation", "label": "Experimenting with new tools"}
                    ]
                },
                {
                    "step": 7,
                    "question_id": "project_description",
                    "question_text": "Briefly describe your current project goals or what you're trying to achieve (optional):",
                    "response_type": "text_area",
                    "required": False,
                    "placeholder": "e.g., 'Building a real-time chat application', 'Learning serverless architecture', 'Setting up CI/CD for my open-source project'"
                },
                {
                    "step": 8,
                    "question_id": "preferences",
                    "question_text": "Help us personalize your experience:",
                    "response_type": "preference_matrix",
                    "required": False,
                    "sub_questions": [
                        {
                            "id": "team_size",
                            "text": "Team size:",
                            "type": "single_choice",
                            "options": [
                                {"value": "solo", "label": "Solo developer"},
                                {"value": "small_team", "label": "Small team (2-5 people)"},
                                {"value": "large_team", "label": "Large team (6+ people)"}
                            ]
                        },
                        {
                            "id": "complexity_preference",
                            "text": "Tool complexity preference:",
                            "type": "single_choice",
                            "options": [
                                {"value": "simple", "label": "Simple & easy to use"},
                                {"value": "balanced", "label": "Balanced features & complexity"},
                                {"value": "advanced", "label": "Advanced features & control"}
                            ]
                        },
                        {
                            "id": "learning_style",
                            "text": "Preferred learning style:",
                            "type": "single_choice",
                            "options": [
                                {"value": "hands_on", "label": "Hands-on experimentation"},
                                {"value": "documentation", "label": "Reading documentation"},
                                {"value": "video", "label": "Video tutorials"},
                                {"value": "community", "label": "Community support"}
                            ]
                        }
                    ]
                }
            ]
        }

    async def start_onboarding(self, user: User) -> Dict[str, Any]:
        """Start the onboarding process for a new user"""
        
        # Check if user already has a profile
        existing_profile = await self._get_user_profile(user)
        if existing_profile and existing_profile.onboarding_completed_at:
            return {
                "status": "already_completed",
                "message": "User has already completed onboarding",
                "profile_id": existing_profile.id
            }
        
        # Create or get existing profile
        if not existing_profile:
            profile = UserProfile(
                user_id=user.id,
                experience_level=ExperienceLevelEnum.INTERMEDIATE,  # Default, will be updated
                profile_created_at=datetime.utcnow()
            )
            self.db.add(profile)
            await self.db.commit()
            await self.db.refresh(profile)
        else:
            profile = existing_profile
        
        # Get first question
        first_question = self.onboarding_questions["v1"][0]
        
        # Track onboarding start
        await self._track_behavioral_event(
            profile, 
            "onboarding_started", 
            {"flow_version": "v1", "step": 1}
        )
        
        return {
            "status": "started",
            "profile_id": profile.id,
            "current_step": 1,
            "total_steps": len(self.onboarding_questions["v1"]),
            "question": first_question,
            "flow_version": "v1"
        }

    async def submit_onboarding_response(
        self, 
        user: User, 
        step: int, 
        question_id: str, 
        response_data: Any,
        time_to_answer: Optional[float] = None,
        confidence_level: Optional[str] = None
    ) -> Dict[str, Any]:
        """Submit a response to an onboarding question"""
        
        profile = await self._get_user_profile(user)
        if not profile:
            raise ValueError("User profile not found")
        
        # Validate step and question
        questions = self.onboarding_questions["v1"]
        if step < 1 or step > len(questions):
            raise ValueError(f"Invalid step: {step}")
        
        question = questions[step - 1]
        if question["question_id"] != question_id:
            raise ValueError(f"Question ID mismatch: {question_id}")
        
        # Validate response
        self._validate_response(question, response_data)
        
        # Store the response
        onboarding_response = OnboardingResponse(
            user_profile_id=profile.id,
            flow_version="v1",
            step_number=step,
            question_id=question_id,
            question_text=question["question_text"],
            response_type=question["response_type"],
            response_data=response_data,
            time_to_answer_seconds=time_to_answer,
            confidence_level=confidence_level,
            completed_at=datetime.utcnow()
        )
        
        self.db.add(onboarding_response)
        
        # Update profile based on the response
        await self._update_profile_from_response(profile, question_id, response_data)
        
        # Track behavioral event
        await self._track_behavioral_event(
            profile,
            "onboarding_response",
            {
                "step": step,
                "question_id": question_id,
                "response_type": question["response_type"],
                "time_to_answer": time_to_answer
            }
        )
        
        # Check if onboarding is complete
        if step >= len(questions):
            await self._complete_onboarding(profile)
            
            return {
                "status": "completed",
                "message": "Onboarding completed successfully!",
                "profile_completeness": calculate_profile_completeness(profile),
                "next_action": "generate_recommendations"
            }
        
        # Get next question
        next_question = questions[step]
        
        await self.db.commit()
        
        return {
            "status": "continue",
            "current_step": step + 1,
            "total_steps": len(questions),
            "question": next_question,
            "progress_percentage": ((step) / len(questions)) * 100
        }

    async def skip_onboarding_step(self, user: User, step: int, question_id: str) -> Dict[str, Any]:
        """Skip an optional onboarding step"""
        
        profile = await self._get_user_profile(user)
        if not profile:
            raise ValueError("User profile not found")
        
        questions = self.onboarding_questions["v1"]
        question = questions[step - 1]
        
        if question["required"]:
            raise ValueError("Cannot skip required question")
        
        # Store skipped response
        onboarding_response = OnboardingResponse(
            user_profile_id=profile.id,
            flow_version="v1",
            step_number=step,
            question_id=question_id,
            question_text=question["question_text"],
            response_type=question["response_type"],
            response_data=None,
            skipped=True,
            completed_at=datetime.utcnow()
        )
        
        self.db.add(onboarding_response)
        
        # Track skip event
        await self._track_behavioral_event(
            profile,
            "onboarding_skipped",
            {"step": step, "question_id": question_id}
        )
        
        # Continue to next question or complete
        if step >= len(questions):
            await self._complete_onboarding(profile)
            return {
                "status": "completed",
                "message": "Onboarding completed!",
                "profile_completeness": calculate_profile_completeness(profile)
            }
        
        next_question = questions[step]
        await self.db.commit()
        
        return {
            "status": "continue",
            "current_step": step + 1,
            "total_steps": len(questions),
            "question": next_question
        }

    async def get_onboarding_progress(self, user: User) -> Dict[str, Any]:
        """Get current onboarding progress for a user"""
        
        profile = await self._get_user_profile(user)
        if not profile:
            return {"status": "not_started"}
        
        if profile.onboarding_completed_at:
            return {
                "status": "completed",
                "completed_at": profile.onboarding_completed_at,
                "profile_completeness": calculate_profile_completeness(profile)
            }
        
        # Get completed responses
        from sqlalchemy import select, func
        result = await self.db.execute(
            select(func.count(OnboardingResponse.id))
            .where(OnboardingResponse.user_profile_id == profile.id)
        )
        completed_steps = result.scalar() or 0
        
        total_steps = len(self.onboarding_questions["v1"])
        
        return {
            "status": "in_progress",
            "completed_steps": completed_steps,
            "total_steps": total_steps,
            "progress_percentage": (completed_steps / total_steps) * 100,
            "current_step": completed_steps + 1 if completed_steps < total_steps else total_steps
        }

    def _validate_response(self, question: Dict[str, Any], response_data: Any) -> None:
        """Validate a response against question requirements"""
        
        if question["required"] and (response_data is None or response_data == ""):
            raise ValueError("Response is required for this question")
        
        response_type = question["response_type"]
        
        if response_type == "single_choice":
            if not isinstance(response_data, str):
                raise ValueError("Single choice response must be a string")
            valid_values = [opt["value"] for opt in question["options"]]
            if response_data not in valid_values:
                raise ValueError(f"Invalid choice: {response_data}")
        
        elif response_type == "multi_select":
            if not isinstance(response_data, list):
                raise ValueError("Multi-select response must be a list")
            max_selections = question.get("max_selections", len(question["options"]))
            if len(response_data) > max_selections:
                raise ValueError(f"Too many selections (max {max_selections})")
            valid_values = [opt["value"] for opt in question["options"]]
            for value in response_data:
                if value not in valid_values:
                    raise ValueError(f"Invalid choice: {value}")
        
        elif response_type == "text_area":
            if response_data and not isinstance(response_data, str):
                raise ValueError("Text area response must be a string")
        
        elif response_type == "preference_matrix":
            if not isinstance(response_data, dict):
                raise ValueError("Preference matrix response must be a dictionary")

    async def _update_profile_from_response(self, profile: UserProfile, question_id: str, response_data: Any) -> None:
        """Update user profile based on onboarding response"""
        
        if question_id == "experience_level":
            profile.experience_level = ExperienceLevelEnum(response_data)
        
        elif question_id == "primary_languages":
            profile.primary_languages = response_data
        
        elif question_id == "domain_interests":
            profile.domain_interests = response_data
            if response_data:
                profile.primary_domain = DomainInterestEnum(response_data[0])
        
        elif question_id == "preferred_stacks":
            profile.preferred_stacks = response_data
        
        elif question_id == "tool_categories":
            profile.needed_tool_categories = response_data
        
        elif question_id == "project_goals":
            profile.project_goals = response_data
        
        elif question_id == "project_description":
            profile.current_project_description = response_data
        
        elif question_id == "preferences":
            if isinstance(response_data, dict):
                profile.team_size = response_data.get("team_size")
                profile.complexity_preference = response_data.get("complexity_preference")
                profile.learning_style = response_data.get("learning_style")
        
        # Update profile completeness
        profile.profile_completeness_score = calculate_profile_completeness(profile)
        profile.last_updated = datetime.utcnow()

    async def _complete_onboarding(self, profile: UserProfile) -> None:
        """Mark onboarding as completed and perform final setup"""
        
        profile.onboarding_completed_at = datetime.utcnow()
        profile.profile_completeness_score = calculate_profile_completeness(profile)
        
        # Track completion event
        await self._track_behavioral_event(
            profile,
            "onboarding_completed",
            {
                "profile_completeness": profile.profile_completeness_score,
                "experience_level": profile.experience_level.value if profile.experience_level else None
            }
        )

    async def _get_user_profile(self, user: User) -> Optional[UserProfile]:
        """Get user profile"""
        result = await self.db.execute(
            select(UserProfile).where(UserProfile.user_id == user.id)
        )
        return result.scalar_one_or_none()

    async def _track_behavioral_event(self, profile: UserProfile, event_type: str, event_data: Dict[str, Any]) -> None:
        """Track a behavioral event"""
        
        event = UserBehavioralEvent(
            user_profile_id=profile.id,
            event_type=event_type,
            event_category="onboarding",
            event_data=event_data,
            timestamp=datetime.utcnow()
        )
        
        self.db.add(event)
