"""Pydantic models for request/response schemas."""

from pydantic import BaseModel, Field
from enum import Enum

from app.prompts import EmailPreset


class ToneLevel(str, Enum):
    """Email tone levels."""

    VERY_FORMAL = "very_formal"
    FORMAL = "formal"
    NEUTRAL = "neutral"
    FRIENDLY = "friendly"
    CASUAL = "casual"


class LengthLevel(str, Enum):
    """Email length levels."""

    VERY_BRIEF = "very_brief"
    CONCISE = "concise"
    MODERATE = "moderate"
    DETAILED = "detailed"
    COMPREHENSIVE = "comprehensive"


class UrgencyLevel(str, Enum):
    """Email urgency levels."""

    NONE = "none"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class CTAStrength(str, Enum):
    """Call-to-action strength levels."""

    SUBTLE = "subtle"
    GENTLE = "gentle"
    MODERATE = "moderate"
    DIRECT = "direct"
    STRONG = "strong"


class PolitenessLevel(str, Enum):
    """Politeness levels."""

    BLUNT = "blunt"
    DIRECT = "direct"
    POLITE = "polite"
    VERY_POLITE = "very_polite"
    DEFERENTIAL = "deferential"


class SalutationStyle(str, Enum):
    """Salutation/greeting styles."""

    NONE = "none"
    FORMAL = "formal"  # Dear Mr./Ms. X
    STANDARD = "standard"  # Dear X
    FRIENDLY = "friendly"  # Hi X
    CASUAL = "casual"  # Hey X


class SignOffStyle(str, Enum):
    """Sign-off styles."""

    NONE = "none"
    FORMAL = "formal"  # Sincerely / Respectfully
    PROFESSIONAL = "professional"  # Best regards / Kind regards
    FRIENDLY = "friendly"  # Best / Thanks
    CASUAL = "casual"  # Cheers / Take care
    WARM = "warm"  # Warm regards / Warmly


class Language(str, Enum):
    """Supported languages for email generation."""

    ENGLISH = "english"
    SPANISH = "spanish"
    FRENCH = "french"
    GERMAN = "german"
    ITALIAN = "italian"
    PORTUGUESE = "portuguese"
    DUTCH = "dutch"
    JAPANESE = "japanese"
    CHINESE = "chinese"
    KOREAN = "korean"
    HINDI = "hindi"
    ARABIC = "arabic"


class AudienceType(str, Enum):
    """Who the email is addressed to."""

    GENERAL = "general"
    MANAGER = "manager"
    EXECUTIVE = "executive"
    PEER = "peer"
    SUBORDINATE = "subordinate"
    CLIENT = "client"
    VENDOR = "vendor"
    RECRUITER = "recruiter"
    PROFESSOR = "professor"
    STUDENT = "student"


class PurposeTag(str, Enum):
    """Primary intent of the email."""

    GENERAL = "general"
    REQUEST = "request"
    INFORM = "inform"
    PERSUADE = "persuade"
    THANK = "thank"
    APOLOGIZE = "apologize"
    NEGOTIATE = "negotiate"
    DECLINE = "decline"
    INTRODUCE = "introduce"
    FOLLOW_UP = "follow_up"


class ResponseType(str, Enum):
    """Type of response for reply emails."""

    NONE = "none"
    ACCEPT = "accept"
    DECLINE = "decline"
    COUNTER_OFFER = "counter_offer"
    REQUEST_CLARIFICATION = "request_clarification"
    ACKNOWLEDGE = "acknowledge"
    DEFER = "defer"


class IndustryContext(str, Enum):
    """Industry context for appropriate jargon and conventions."""

    GENERAL = "general"
    TECH = "tech"
    FINANCE = "finance"
    LEGAL = "legal"
    MEDICAL = "medical"
    ACADEMIC = "academic"
    SALES = "sales"
    HR = "hr"
    MARKETING = "marketing"
    CONSULTING = "consulting"


class RecipientRelationship(str, Enum):
    """Relationship with the recipient."""

    UNKNOWN = "unknown"
    FIRST_CONTACT = "first_contact"
    NEW_ACQUAINTANCE = "new_acquaintance"
    ESTABLISHED = "established"
    CLOSE_COLLEAGUE = "close_colleague"
    INTERNAL = "internal"
    EXTERNAL = "external"


class EmailRequest(BaseModel):
    """Request model for email generation."""

    preset: EmailPreset = Field(default=EmailPreset.GENERAL, description="Email type preset")
    incoming_email: str = Field(default="", description="Email being replied to")
    recipient_name: str = Field(default="", description="Name of the recipient")
    sender_name: str = Field(default="", description="Sender's name for signature")
    tone: int = Field(default=50, ge=0, le=100, description="Tone slider value (0=formal, 100=casual)")
    length: int = Field(default=50, ge=0, le=100, description="Length slider value (0=brief, 100=detailed)")
    temperature: int = Field(default=70, ge=0, le=100, description="Creativity slider (0=precise, 100=creative)")
    use_lists: bool = Field(default=False, description="Use bullet points and numbered lists")
    custom_instructions: str = Field(default="", description="Additional instructions")
    urgency: int = Field(default=0, ge=0, le=100, description="Urgency slider (0=none, 100=critical)")
    cta_strength: int = Field(default=50, ge=0, le=100, description="CTA strength slider (0=subtle, 100=strong)")
    politeness: int = Field(default=50, ge=0, le=100, description="Politeness slider (0=blunt, 100=deferential)")
    salutation_style: SalutationStyle = Field(default=SalutationStyle.STANDARD, description="Greeting style")
    sign_off_style: SignOffStyle = Field(default=SignOffStyle.PROFESSIONAL, description="Sign-off style")
    language: Language = Field(default=Language.ENGLISH, description="Language for email generation")
    audience_type: AudienceType = Field(default=AudienceType.GENERAL, description="Who the email is addressed to")
    purpose: PurposeTag = Field(default=PurposeTag.GENERAL, description="Primary intent of the email")
    keywords_to_include: str = Field(default="", description="Comma-separated keywords to include")
    response_type: ResponseType = Field(default=ResponseType.NONE, description="Type of response for replies")
    industry: IndustryContext = Field(default=IndustryContext.GENERAL, description="Industry context")
    recipient_relationship: RecipientRelationship = Field(default=RecipientRelationship.UNKNOWN, description="Relationship with recipient")
    include_attachment_reference: bool = Field(default=False, description="Include attachment reference")

    @property
    def temperature_float(self) -> float:
        """Convert slider value to 0.0-1.0 range."""
        return self.temperature / 100.0

    @property
    def tone_level(self) -> ToneLevel:
        """Convert numeric tone to level."""
        if self.tone < 20:
            return ToneLevel.VERY_FORMAL
        elif self.tone < 40:
            return ToneLevel.FORMAL
        elif self.tone < 60:
            return ToneLevel.NEUTRAL
        elif self.tone < 80:
            return ToneLevel.FRIENDLY
        return ToneLevel.CASUAL

    @property
    def length_level(self) -> LengthLevel:
        """Convert numeric length to level."""
        if self.length < 20:
            return LengthLevel.VERY_BRIEF
        elif self.length < 40:
            return LengthLevel.CONCISE
        elif self.length < 60:
            return LengthLevel.MODERATE
        elif self.length < 80:
            return LengthLevel.DETAILED
        return LengthLevel.COMPREHENSIVE

    @property
    def tone_description(self) -> str:
        """Get human-readable tone description for prompt."""
        descriptions = {
            ToneLevel.VERY_FORMAL: "very formal and professional",
            ToneLevel.FORMAL: "formal but approachable",
            ToneLevel.NEUTRAL: "balanced and neutral",
            ToneLevel.FRIENDLY: "friendly and conversational",
            ToneLevel.CASUAL: "casual and relaxed",
        }
        return descriptions[self.tone_level]

    @property
    def length_description(self) -> str:
        """Get human-readable length description for prompt."""
        descriptions = {
            LengthLevel.VERY_BRIEF: "very brief (2-3 sentences)",
            LengthLevel.CONCISE: "concise (1 short paragraph)",
            LengthLevel.MODERATE: "moderate (2-3 paragraphs)",
            LengthLevel.DETAILED: "detailed (3-4 paragraphs)",
            LengthLevel.COMPREHENSIVE: "comprehensive and thorough (4+ paragraphs)",
        }
        return descriptions[self.length_level]

    @property
    def urgency_level(self) -> UrgencyLevel:
        """Convert numeric urgency to level."""
        if self.urgency < 20:
            return UrgencyLevel.NONE
        elif self.urgency < 40:
            return UrgencyLevel.LOW
        elif self.urgency < 60:
            return UrgencyLevel.MODERATE
        elif self.urgency < 80:
            return UrgencyLevel.HIGH
        return UrgencyLevel.CRITICAL

    @property
    def urgency_description(self) -> str | None:
        """Get human-readable urgency description for prompt."""
        descriptions = {
            UrgencyLevel.NONE: None,
            UrgencyLevel.LOW: "slightly time-sensitive, gently mention timing",
            UrgencyLevel.MODERATE: "moderately urgent, clearly convey time importance",
            UrgencyLevel.HIGH: "high urgency, emphasize immediate attention needed",
            UrgencyLevel.CRITICAL: "critical urgency, strongly emphasize this is time-critical and requires immediate action",
        }
        return descriptions[self.urgency_level]

    @property
    def cta_strength_level(self) -> CTAStrength:
        """Convert numeric CTA strength to level."""
        if self.cta_strength < 20:
            return CTAStrength.SUBTLE
        elif self.cta_strength < 40:
            return CTAStrength.GENTLE
        elif self.cta_strength < 60:
            return CTAStrength.MODERATE
        elif self.cta_strength < 80:
            return CTAStrength.DIRECT
        return CTAStrength.STRONG

    @property
    def cta_description(self) -> str:
        """Get human-readable CTA strength description for prompt."""
        descriptions = {
            CTAStrength.SUBTLE: "subtle and implied call-to-action, no direct ask",
            CTAStrength.GENTLE: "gentle suggestion, soft ask",
            CTAStrength.MODERATE: "clear but polite call-to-action",
            CTAStrength.DIRECT: "direct and explicit call-to-action",
            CTAStrength.STRONG: "strong, assertive call-to-action with clear expectation of response",
        }
        return descriptions[self.cta_strength_level]

    @property
    def politeness_level(self) -> PolitenessLevel:
        """Convert numeric politeness to level."""
        if self.politeness < 20:
            return PolitenessLevel.BLUNT
        elif self.politeness < 40:
            return PolitenessLevel.DIRECT
        elif self.politeness < 60:
            return PolitenessLevel.POLITE
        elif self.politeness < 80:
            return PolitenessLevel.VERY_POLITE
        return PolitenessLevel.DEFERENTIAL

    @property
    def politeness_description(self) -> str:
        """Get human-readable politeness description for prompt."""
        descriptions = {
            PolitenessLevel.BLUNT: "blunt and straightforward, minimal pleasantries",
            PolitenessLevel.DIRECT: "direct but not rude, minimal softening language",
            PolitenessLevel.POLITE: "polite with appropriate courtesies",
            PolitenessLevel.VERY_POLITE: "very polite with extra courtesies and softening language",
            PolitenessLevel.DEFERENTIAL: "highly deferential, very respectful with formal courtesies",
        }
        return descriptions[self.politeness_level]

    @property
    def salutation_description(self) -> str | None:
        """Get salutation instruction for prompt."""
        descriptions = {
            SalutationStyle.NONE: "Do not include any greeting/salutation",
            SalutationStyle.FORMAL: "Use formal salutation (Dear Mr./Ms./Dr. [Name])",
            SalutationStyle.STANDARD: "Use standard salutation (Dear [Name])",
            SalutationStyle.FRIENDLY: "Use friendly salutation (Hi [Name] or Hello [Name])",
            SalutationStyle.CASUAL: "Use casual salutation (Hey [Name])",
        }
        return descriptions[self.salutation_style]

    @property
    def sign_off_description(self) -> str | None:
        """Get sign-off instruction for prompt."""
        descriptions = {
            SignOffStyle.NONE: "Do not include any sign-off or closing",
            SignOffStyle.FORMAL: "Use formal sign-off (Sincerely, Respectfully, Yours faithfully)",
            SignOffStyle.PROFESSIONAL: "Use professional sign-off (Best regards, Kind regards)",
            SignOffStyle.FRIENDLY: "Use friendly sign-off (Best, Thanks, Thank you)",
            SignOffStyle.CASUAL: "Use casual sign-off (Cheers, Take care, Talk soon)",
            SignOffStyle.WARM: "Use warm sign-off (Warm regards, Warmly, With appreciation)",
        }
        return descriptions[self.sign_off_style]

    @property
    def language_description(self) -> str:
        """Get language instruction for prompt."""
        language_names = {
            Language.ENGLISH: "English",
            Language.SPANISH: "Spanish",
            Language.FRENCH: "French",
            Language.GERMAN: "German",
            Language.ITALIAN: "Italian",
            Language.PORTUGUESE: "Portuguese",
            Language.DUTCH: "Dutch",
            Language.JAPANESE: "Japanese",
            Language.CHINESE: "Chinese (Simplified)",
            Language.KOREAN: "Korean",
            Language.HINDI: "Hindi",
            Language.ARABIC: "Arabic",
        }
        return language_names[self.language]

    @property
    def audience_description(self) -> str | None:
        """Get audience type description for prompt."""
        if self.audience_type == AudienceType.GENERAL:
            return None
        descriptions = {
            AudienceType.GENERAL: None,
            AudienceType.MANAGER: "writing to a manager/supervisor - be respectful of their time and position",
            AudienceType.EXECUTIVE: "writing to an executive/C-level - be concise, focus on impact and outcomes",
            AudienceType.PEER: "writing to a peer/colleague - maintain professional but collegial tone",
            AudienceType.SUBORDINATE: "writing to a subordinate/team member - be clear and supportive",
            AudienceType.CLIENT: "writing to a client - be professional, service-oriented, and solution-focused",
            AudienceType.VENDOR: "writing to a vendor/supplier - be clear about requirements and expectations",
            AudienceType.RECRUITER: "writing to a recruiter - highlight relevant qualifications professionally",
            AudienceType.PROFESSOR: "writing to a professor/academic - be respectful and scholarly",
            AudienceType.STUDENT: "writing to a student - be clear, helpful, and encouraging",
        }
        return descriptions[self.audience_type]

    @property
    def purpose_description(self) -> str | None:
        """Get purpose tag description for prompt."""
        if self.purpose == PurposeTag.GENERAL:
            return None
        descriptions = {
            PurposeTag.GENERAL: None,
            PurposeTag.REQUEST: "primary purpose is to request something - be clear about what you need",
            PurposeTag.INFORM: "primary purpose is to inform/update - focus on clarity and key information",
            PurposeTag.PERSUADE: "primary purpose is to persuade - use compelling arguments and benefits",
            PurposeTag.THANK: "primary purpose is to thank - be sincere and specific about gratitude",
            PurposeTag.APOLOGIZE: "primary purpose is to apologize - be sincere, take responsibility, offer resolution",
            PurposeTag.NEGOTIATE: "primary purpose is to negotiate - be diplomatic, present options, seek win-win",
            PurposeTag.DECLINE: "primary purpose is to decline - be polite but firm, offer alternatives if possible",
            PurposeTag.INTRODUCE: "primary purpose is to introduce yourself/someone - be memorable and establish relevance",
            PurposeTag.FOLLOW_UP: "primary purpose is to follow up - reference previous interaction, add value",
        }
        return descriptions[self.purpose]

    @property
    def response_type_description(self) -> str | None:
        """Get response type description for prompt."""
        if self.response_type == ResponseType.NONE:
            return None
        descriptions = {
            ResponseType.NONE: None,
            ResponseType.ACCEPT: "this is an acceptance response - confirm clearly and express appreciation",
            ResponseType.DECLINE: "this is a decline response - be polite but clear, offer alternatives if appropriate",
            ResponseType.COUNTER_OFFER: "this is a counter-offer response - acknowledge original, present alternative professionally",
            ResponseType.REQUEST_CLARIFICATION: "this is a clarification request - be specific about what needs clarification",
            ResponseType.ACKNOWLEDGE: "this is an acknowledgment response - confirm receipt and next steps if any",
            ResponseType.DEFER: "this is a deferral response - explain timeline and commit to follow-up",
        }
        return descriptions[self.response_type]

    @property
    def industry_description(self) -> str | None:
        """Get industry context description for prompt."""
        if self.industry == IndustryContext.GENERAL:
            return None
        descriptions = {
            IndustryContext.GENERAL: None,
            IndustryContext.TECH: "tech/software industry context - can use technical terms appropriately",
            IndustryContext.FINANCE: "finance/banking industry context - use financial terminology appropriately",
            IndustryContext.LEGAL: "legal industry context - be precise, use legal terminology carefully",
            IndustryContext.MEDICAL: "medical/healthcare industry context - use medical terminology appropriately",
            IndustryContext.ACADEMIC: "academic/research context - use scholarly tone and terminology",
            IndustryContext.SALES: "sales context - focus on value proposition and relationship building",
            IndustryContext.HR: "HR/people operations context - be professional and policy-aware",
            IndustryContext.MARKETING: "marketing context - be creative and brand-conscious",
            IndustryContext.CONSULTING: "consulting context - be advisory and solution-oriented",
        }
        return descriptions[self.industry]

    @property
    def relationship_description(self) -> str | None:
        """Get recipient relationship description for prompt."""
        if self.recipient_relationship == RecipientRelationship.UNKNOWN:
            return None
        descriptions = {
            RecipientRelationship.UNKNOWN: None,
            RecipientRelationship.FIRST_CONTACT: "this is first contact - introduce context and establish relevance",
            RecipientRelationship.NEW_ACQUAINTANCE: "recently met - reference how you connected",
            RecipientRelationship.ESTABLISHED: "established relationship - can be more direct",
            RecipientRelationship.CLOSE_COLLEAGUE: "close colleague - can be more informal while professional",
            RecipientRelationship.INTERNAL: "internal communication - can assume shared context",
            RecipientRelationship.EXTERNAL: "external communication - be more formal and explanatory",
        }
        return descriptions[self.recipient_relationship]


class EmailResponse(BaseModel):
    """Response model for generated email."""

    subject: str = Field(description="Primary email subject line")
    subject_variants: list[str] = Field(default_factory=list, description="Alternative subject line options")
    body: str = Field(description="Email body content")
    spam_score: int = Field(default=0, ge=0, le=100, description="Spam likelihood score (0=safe, 100=likely spam)")
    spam_warnings: list[str] = Field(default_factory=list, description="Spam trigger warnings")

    @property
    def word_count(self) -> int:
        """Count words in the email body."""
        return len(self.body.split())

    @property
    def read_time_seconds(self) -> int:
        """Estimate read time in seconds (average 200 words per minute)."""
        return max(1, (self.word_count * 60) // 200)

    @property
    def read_time_display(self) -> str:
        """Human-readable read time."""
        seconds = self.read_time_seconds
        if seconds < 60:
            return f"~{seconds} sec read"
        minutes = seconds // 60
        return f"~{minutes} min read"


def calculate_spam_score(subject: str, body: str) -> tuple[int, list[str]]:
    """Calculate spam likelihood score and return warnings.

    Returns:
        Tuple of (score 0-100, list of warning messages)
    """
    score = 0
    warnings = []

    text = (subject + " " + body).lower()
    subject_lower = subject.lower()

    # Spam trigger words/phrases
    spam_triggers = {
        # High risk (10 points each)
        "high": [
            "act now", "limited time", "urgent", "immediate action",
            "click here", "click below", "buy now", "order now",
            "free money", "cash bonus", "winner", "you won",
            "congratulations", "100% free", "risk free", "no obligation",
            "double your", "earn extra", "make money fast",
        ],
        # Medium risk (5 points each)
        "medium": [
            "special offer", "exclusive deal", "discount", "save big",
            "lowest price", "best price", "cheap", "bargain",
            "guarantee", "no questions asked", "satisfaction guaranteed",
            "call now", "apply now", "sign up free", "subscribe now",
            "dear friend", "dear customer",
        ],
        # Low risk (2 points each)
        "low": [
            "free", "bonus", "offer", "deal", "promo",
            "!!!", "???", "all caps", "$$$",
        ],
    }

    for trigger in spam_triggers["high"]:
        if trigger in text:
            score += 10
            warnings.append(f"High-risk phrase: '{trigger}'")

    for trigger in spam_triggers["medium"]:
        if trigger in text:
            score += 5
            warnings.append(f"Medium-risk phrase: '{trigger}'")

    for trigger in spam_triggers["low"]:
        if trigger in text:
            score += 2

    # Check for excessive capitalization
    upper_ratio = sum(1 for c in subject if c.isupper()) / max(len(subject), 1)
    if upper_ratio > 0.5 and len(subject) > 5:
        score += 15
        warnings.append("Excessive capitals in subject line")

    # Check for excessive punctuation
    if subject.count("!") > 1:
        score += 10
        warnings.append("Multiple exclamation marks in subject")

    if "!!!" in text or "???" in text:
        score += 10
        warnings.append("Excessive punctuation detected")

    # Check for suspicious patterns
    if subject_lower.startswith("re:") and not body:
        score += 5
        warnings.append("Empty reply email")

    if subject_lower.startswith("fw:") or subject_lower.startswith("fwd:"):
        score += 3

    # Check for URL density
    url_count = text.count("http://") + text.count("https://") + text.count("www.")
    if url_count > 3:
        score += 10
        warnings.append(f"High URL density ({url_count} links)")

    # Cap at 100
    score = min(score, 100)

    return score, warnings


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str = Field(description="Error message")
    detail: str | None = Field(default=None, description="Detailed error information")
