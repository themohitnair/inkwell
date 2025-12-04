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


class EmailResponse(BaseModel):
    """Response model for generated email."""

    subject: str = Field(description="Primary email subject line")
    subject_variants: list[str] = Field(default_factory=list, description="Alternative subject line options")
    body: str = Field(description="Email body content")


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str = Field(description="Error message")
    detail: str | None = Field(default=None, description="Detailed error information")
