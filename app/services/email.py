"""Email generation service using Groq API."""

from groq import Groq

from app.config import settings
from app.models import EmailRequest, EmailResponse


SYSTEM_PROMPT = """You are an expert email writer. Generate professional emails based on the given parameters.
Always respond in this exact format:
SUBJECT: [Your subject line here]
---
[Your email body here]

Do not include any other text or explanation outside this format."""


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

        if request.is_cold_email:
            parts.append("- Type: Cold email (first contact, no prior relationship)")
        else:
            parts.append("- Type: Regular email")

        if request.recipient_name:
            parts.append(f"- Recipient name: {request.recipient_name}")

        if request.incoming_email:
            parts.append(
                f"\n- This is a REPLY to the following email:\n```\n{request.incoming_email}\n```"
            )
        else:
            parts.append("\n- This is a NEW email (not a reply)")

        if request.custom_instructions:
            parts.append(f"\n- Additional instructions: {request.custom_instructions}")

        return "\n".join(parts)

    def parse_response(self, content: str) -> EmailResponse:
        """Parse the LLM response into subject and body.

        Args:
            content: Raw response from LLM.

        Returns:
            Parsed email response.
        """
        if "SUBJECT:" in content and "---" in content:
            parts = content.split("---", 1)
            subject = parts[0].replace("SUBJECT:", "").strip()
            body = parts[1].strip() if len(parts) > 1 else ""
            return EmailResponse(subject=subject, body=body)

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

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        content = response.choices[0].message.content
        return self.parse_response(content)


# Default service instance
email_service = EmailService()
