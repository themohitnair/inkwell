"""Email generation service using Groq API."""

import json
from groq import Groq

from app.config import settings
from app.models import EmailRequest, EmailResponse
from app.prompts import get_prompt, IMPROVE_PROMPT


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

        if request.recipient_name:
            parts.append(f"- Recipient name: {request.recipient_name}")

        if request.sender_name:
            parts.append(f"- Sign off with: {request.sender_name}")

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
                body=data.get("body", content),
            )
        except json.JSONDecodeError:
            return EmailResponse(subject="Generated Email", body=content)

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

    async def improve(self, subject: str, body: str) -> EmailResponse:
        """Improve an existing email.

        Args:
            subject: Current email subject.
            body: Current email body.

        Returns:
            Improved email with subject and body.
        """
        prompt = f"Improve this email:\n\nSubject: {subject}\n\nBody:\n{body}"

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": IMPROVE_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1024,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        return self.parse_response(content)


# Default service instance
email_service = EmailService()
