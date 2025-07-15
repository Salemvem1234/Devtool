"""
NLP Service for DevAccess AI - Intelligent request understanding
"""
import re
import spacy
from typing import Dict, List, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.software import Software, SoftwareCategory
from app.core.config import settings
import structlog

logger = structlog.get_logger()


class NLPService:
    """Natural Language Processing service for intent recognition and entity extraction"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.nlp = None
        self._load_model()
        
        # Define intent patterns and keywords
        self.intent_patterns = {
            "create_account": [
                r"(?i).*(?:create|make|set up|get|need).*(?:account|access)",
                r"(?i).*(?:sign up|register).*(?:for|to)",
                r"(?i).*(?:account|access).*(?:for|to)",
                r"(?i).*(?:trial|demo|test).*(?:account|access)",
            ],
            "get_free_tier": [
                r"(?i).*(?:free|trial|demo).*(?:tier|plan|version)",
                r"(?i).*(?:free|gratis).*(?:access|account)",
                r"(?i).*(?:try|test).*(?:free|gratis)",
            ],
            "find_software": [
                r"(?i).*(?:find|search|look for|recommend).*(?:tool|software|service)",
                r"(?i).*(?:what|which).*(?:tool|software|service)",
                r"(?i).*(?:best|good|popular).*(?:tool|software|service)",
            ],
            "category_request": [
                r"(?i).*(?:database|db).*(?:tool|software|service)",
                r"(?i).*(?:ci/cd|deployment|build).*(?:tool|software|service)",
                r"(?i).*(?:ide|editor|development).*(?:tool|software|environment)",
                r"(?i).*(?:cloud|hosting|server).*(?:service|platform)",
                r"(?i).*(?:api|service|endpoint).*(?:tool|platform)",
            ]
        }
        
        # Software name patterns and aliases
        self.software_aliases = {
            "cursor": ["cursor", "cursor ai", "cursor ide"],
            "github": ["github", "gh", "git hub"],
            "gitlab": ["gitlab", "git lab"],
            "vercel": ["vercel", "zeit"],
            "netlify": ["netlify"],
            "heroku": ["heroku"],
            "aws": ["aws", "amazon web services", "amazon aws"],
            "gcp": ["gcp", "google cloud", "google cloud platform"],
            "azure": ["azure", "microsoft azure"],
            "mongodb": ["mongodb", "mongo", "mongo db"],
            "postgresql": ["postgresql", "postgres", "pg"],
            "mysql": ["mysql"],
            "redis": ["redis"],
            "docker": ["docker"],
            "kubernetes": ["kubernetes", "k8s"],
            "jenkins": ["jenkins"],
            "travis": ["travis", "travis ci"],
            "circleci": ["circleci", "circle ci"],
        }
        
        # Category mappings
        self.category_keywords = {
            "ide": ["ide", "editor", "development environment", "code editor"],
            "database": ["database", "db", "data storage", "mongodb", "postgresql", "mysql"],
            "ci_cd": ["ci/cd", "continuous integration", "deployment", "build", "pipeline"],
            "cloud_service": ["cloud", "hosting", "server", "infrastructure"],
            "api_service": ["api", "service", "endpoint", "rest", "graphql"],
            "testing": ["testing", "test", "qa", "quality assurance"],
            "monitoring": ["monitoring", "observability", "logging", "metrics"],
            "security": ["security", "auth", "authentication", "authorization"]
        }

    def _load_model(self):
        """Load spaCy NLP model"""
        try:
            self.nlp = spacy.load(settings.SPACY_MODEL)
            logger.info(f"Loaded spaCy model: {settings.SPACY_MODEL}")
        except OSError:
            logger.warning(f"Could not load {settings.SPACY_MODEL}, using basic English model")
            self.nlp = spacy.load("en_core_web_sm")

    async def parse_intent(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Parse user intent from natural language text"""
        
        # Normalize text
        text_lower = text.lower().strip()
        
        # Extract intent
        intent = self._classify_intent(text_lower)
        
        # Extract entities
        entities = await self._extract_entities(text)
        
        # Get software suggestions based on entities
        software_suggestions = await self._get_software_suggestions(entities, intent)
        
        # Generate action plan
        action_plan = self._generate_action_plan(intent, entities, software_suggestions)
        
        # Calculate confidence
        confidence = self._calculate_confidence(intent, entities, text)
        
        return {
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
            "software_suggestions": software_suggestions,
            "action_plan": action_plan
        }

    def _classify_intent(self, text: str) -> str:
        """Classify the user intent from text"""
        
        # Check each intent pattern
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return intent
        
        # Default fallback
        if any(keyword in text for keyword in ["account", "access", "sign up", "register"]):
            return "create_account"
        elif any(keyword in text for keyword in ["find", "search", "recommend", "suggest"]):
            return "find_software"
        else:
            return "general_inquiry"

    async def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities from text using NLP and pattern matching"""
        
        entities = {
            "software_names": [],
            "categories": [],
            "keywords": [],
            "requirements": []
        }
        
        # Use spaCy for named entity recognition
        doc = self.nlp(text)
        
        # Extract software names using aliases
        text_lower = text.lower()
        for software, aliases in self.software_aliases.items():
            for alias in aliases:
                if alias in text_lower:
                    entities["software_names"].append({
                        "name": software,
                        "matched_alias": alias,
                        "confidence": 0.9
                    })
        
        # Extract categories
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    entities["categories"].append({
                        "category": category,
                        "matched_keyword": keyword,
                        "confidence": 0.8
                    })
        
        # Extract general keywords and requirements
        keywords = []
        requirements = []
        
        # Free tier indicators
        if any(term in text_lower for term in ["free", "trial", "demo", "gratis"]):
            requirements.append("free_tier")
        
        # Urgency indicators
        if any(term in text_lower for term in ["quickly", "fast", "immediately", "asap"]):
            requirements.append("quick_setup")
        
        # No verification preferences
        if any(term in text_lower for term in ["no verification", "skip verification", "without phone"]):
            requirements.append("no_verification")
        
        entities["keywords"] = keywords
        entities["requirements"] = requirements
        
        return entities

    async def _get_software_suggestions(self, entities: Dict[str, Any], intent: str) -> List[Dict[str, Any]]:
        """Get software suggestions based on extracted entities"""
        
        suggestions = []
        
        # If specific software names were mentioned
        if entities["software_names"]:
            for software_entity in entities["software_names"]:
                try:
                    result = await self.db.execute(
                        select(Software).where(
                            Software.name.ilike(f"%{software_entity['name']}%")
                        ).limit(1)
                    )
                    software = result.scalar_one_or_none()
                    
                    if software:
                        suggestions.append({
                            "id": software.id,
                            "name": software.name,
                            "display_name": software.display_name,
                            "description": software.description,
                            "has_free_tier": software.has_free_tier,
                            "automation_supported": software.automation_supported,
                            "confidence": software_entity["confidence"]
                        })
                except Exception as e:
                    logger.error(f"Error fetching software: {e}")
        
        # If categories were mentioned
        if entities["categories"] and not suggestions:
            for category_entity in entities["categories"]:
                try:
                    result = await self.db.execute(
                        select(Software)
                        .join(SoftwareCategory)
                        .where(SoftwareCategory.name.ilike(f"%{category_entity['category']}%"))
                        .where(Software.is_active == True)
                        .where(Software.has_free_tier == True)
                        .limit(5)
                    )
                    softwares = result.scalars().all()
                    
                    for software in softwares:
                        suggestions.append({
                            "id": software.id,
                            "name": software.name,
                            "display_name": software.display_name,
                            "description": software.description,
                            "has_free_tier": software.has_free_tier,
                            "automation_supported": software.automation_supported,
                            "confidence": category_entity["confidence"]
                        })
                except Exception as e:
                    logger.error(f"Error fetching category software: {e}")
        
        return suggestions

    def _generate_action_plan(self, intent: str, entities: Dict[str, Any], suggestions: List[Dict[str, Any]]) -> List[str]:
        """Generate step-by-step action plan based on intent and entities"""
        
        plan = []
        
        if intent == "create_account":
            if suggestions:
                plan.append(f"1. Generate temporary email address")
                plan.append(f"2. Generate secure password")
                plan.append(f"3. Navigate to {suggestions[0]['name']} signup page")
                plan.append(f"4. Fill registration form automatically")
                if suggestions[0].get("requires_verification", True):
                    plan.append(f"5. Monitor email for verification link")
                    plan.append(f"6. Complete email verification")
                plan.append(f"7. Store credentials securely")
                plan.append(f"8. Provide access information to user")
            else:
                plan.append("1. Please specify which software you need access to")
                plan.append("2. I'll help create an account once you provide the software name")
        
        elif intent == "find_software":
            plan.append("1. Search software database based on your requirements")
            plan.append("2. Filter by category and free tier availability")
            plan.append("3. Present ranked suggestions")
            plan.append("4. Offer to create accounts for selected software")
        
        elif intent == "get_free_tier":
            plan.append("1. Identify software with available free tiers")
            plan.append("2. Check automation compatibility")
            plan.append("3. Proceed with account creation for free tier access")
        
        else:
            plan.append("1. Clarify your specific needs")
            plan.append("2. Provide relevant software suggestions")
            plan.append("3. Offer to automate account creation")
        
        return plan

    def _calculate_confidence(self, intent: str, entities: Dict[str, Any], text: str) -> float:
        """Calculate confidence score for the parsed intent"""
        
        confidence = 0.5  # Base confidence
        
        # Boost confidence if specific entities were found
        if entities["software_names"]:
            confidence += 0.3
        
        if entities["categories"]:
            confidence += 0.2
        
        # Boost confidence for clear intent patterns
        if intent != "general_inquiry":
            confidence += 0.2
        
        # Adjust based on text clarity and length
        if len(text.split()) >= 5:  # Reasonable length
            confidence += 0.1
        
        return min(confidence, 1.0)

    async def suggest_software(self, query: str, category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Suggest software based on query and category"""
        
        suggestions = []
        
        try:
            # Build query
            sql_query = select(Software).where(Software.is_active == True)
            
            if category:
                sql_query = sql_query.join(SoftwareCategory).where(
                    SoftwareCategory.name.ilike(f"%{category}%")
                )
            
            if query:
                sql_query = sql_query.where(
                    Software.name.ilike(f"%{query}%") |
                    Software.description.ilike(f"%{query}%")
                )
            
            sql_query = sql_query.limit(limit)
            
            result = await self.db.execute(sql_query)
            softwares = result.scalars().all()
            
            for software in softwares:
                suggestions.append({
                    "id": software.id,
                    "name": software.name,
                    "display_name": software.display_name,
                    "description": software.description,
                    "category": software.category.name if software.category else None,
                    "has_free_tier": software.has_free_tier,
                    "automation_supported": software.automation_supported,
                    "website_url": software.website_url,
                    "popularity_score": software.popularity_score
                })
        
        except Exception as e:
            logger.error(f"Error suggesting software: {e}")
        
        return suggestions

    async def get_categories(self) -> List[Dict[str, Any]]:
        """Get all available software categories"""
        
        categories = []
        
        try:
            result = await self.db.execute(select(SoftwareCategory))
            category_records = result.scalars().all()
            
            for category in category_records:
                categories.append({
                    "id": category.id,
                    "name": category.name,
                    "description": category.description
                })
        
        except Exception as e:
            logger.error(f"Error fetching categories: {e}")
        
        return categories

    async def validate_automation_request(self, text: str) -> Dict[str, Any]:
        """Validate if a request can be automated"""
        
        entities = await self._extract_entities(text)
        
        # Check if we have enough information
        can_automate = bool(entities["software_names"] or entities["categories"])
        
        # Calculate confidence
        confidence = 0.7 if entities["software_names"] else 0.5 if entities["categories"] else 0.2
        
        # Define requirements
        requirements = ["temporary_email", "secure_password"]
        
        if "no_verification" not in entities["requirements"]:
            requirements.append("email_verification")
        
        warnings = []
        if not entities["software_names"]:
            warnings.append("No specific software mentioned - will suggest options")
        
        return {
            "can_automate": can_automate,
            "confidence": confidence,
            "requirements": requirements,
            "warnings": warnings,
            "estimated_success_rate": 85 if can_automate else 0
        }
