"""Pydantic models for request/response schemas."""

from pydantic import BaseModel, Field
from enum import Enum


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


class EmailRequest(BaseModel):
    """Request model for email generation."""

    incoming_email: str = Field(default="", description="Email being replied to")
    recipient_name: str = Field(default="", description="Name of the recipient")
    is_cold_email: bool = Field(default=False, description="Whether this is a cold email")
    tone: int = Field(default=50, ge=0, le=100, description="Tone slider value (0=formal, 100=casual)")
    length: int = Field(default=50, ge=0, le=100, description="Length slider value (0=brief, 100=detailed)")
    custom_instructions: str = Field(default="", description="Additional instructions")

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


class EmailResponse(BaseModel):
    """Response model for generated email."""

    subject: str = Field(description="Email subject line")
    body: str = Field(description="Email body content")


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str = Field(description="Error message")
    detail: str | None = Field(default=None, description="Detailed error information")
