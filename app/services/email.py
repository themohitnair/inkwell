"""Email generation service using Groq API."""

import json
from groq import Groq

from app.config import settings
from app.models import EmailRequest, EmailResponse
from app.prompts import get_prompt


class EmailService:
    """Service for generating emails using Groq API."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        """Initialize the email service.

        Args:
            api_key: Groq API key. Defaults to settings.
            model: Model to use. Defaults to settings.
        """
        self.api_key = api_key or settings.groq_api_key
        self.model = model or settings.groq_model
        self._client: Groq | None = None

    @property
    def client(self) -> Groq:
        """Lazy-loaded Groq client."""
        if self._client is None:
            if not self.api_key:
                raise ValueError("GROQ_API_KEY not configured")
            self._client = Groq(api_key=self.api_key)
        return self._client

    def build_prompt(self, request: EmailRequest) -> str:
        """Build the prompt for email generation.

        Args:
            request: Email generation request.

        Returns:
            Formatted prompt string.
        """
        parts = ["Generate an email with the following specifications:"]
        parts.append(f"\n- Tone: {request.tone_description}")
        parts.append(f"- Length: {request.length_description}")
        parts.append(f"- Politeness: {request.politeness_description}")
        parts.append(f"- Call-to-action: {request.cta_description}")

        if request.urgency_description:
            parts.append(f"- Urgency: {request.urgency_description}")

        if request.use_lists:
            parts.append("- Format: Use bullet points (with dashes -) and numbered lists where appropriate to organize information clearly")

        parts.append(f"- Salutation: {request.salutation_description}")
        parts.append(f"- Sign-off: {request.sign_off_description}")

        if request.recipient_name:
            parts.append(f"- Recipient name: {request.recipient_name}")

        if request.sender_name:
            parts.append(f"- Sender name (for signature): {request.sender_name}")

        if request.incoming_email:
            parts.append(
                f"\n- This is a REPLY to the following email:\n```\n{request.incoming_email}\n```"
            )

        if request.custom_instructions:
            parts.append(f"\n- Additional instructions: {request.custom_instructions}")

        return "\n".join(parts)

    def parse_response(self, content: str) -> EmailResponse:
        """Parse the JSON response into EmailResponse.

        Args:
            content: JSON response from LLM.

        Returns:
            Parsed email response.
        """
        try:
            data = json.loads(content)
            return EmailResponse(
                subject=data.get("subject", "Generated Email"),
                subject_variants=data.get("subject_variants", []),
                body=data.get("body", content),
            )
        except json.JSONDecodeError:
            return EmailResponse(subject="Generated Email", subject_variants=[], body=content)

    async def generate(self, request: EmailRequest) -> EmailResponse:
        """Generate an email based on the request.

        Args:
            request: Email generation parameters.

        Returns:
            Generated email with subject and body.

        Raises:
            ValueError: If API key not configured.
            Exception: If API call fails.
        """
        prompt = self.build_prompt(request)

        system_prompt = get_prompt(request.preset)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=request.temperature_float,
            max_tokens=1024,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        return self.parse_response(content)


# Default service instance
email_service = EmailService()
