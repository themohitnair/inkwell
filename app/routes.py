"""API routes for the application."""

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.models import EmailRequest
from app.services import EmailService

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Service instance - can be replaced with dependency injection
email_service = EmailService()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main page."""
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/generate", response_class=HTMLResponse)
async def generate_email(
    request: Request,
    preset: str = Form("general"),
    incoming_email: str = Form(""),
    recipient_name: str = Form(""),
    sender_name: str = Form(""),
    tone: int = Form(50),
    length: int = Form(50),
    temperature: int = Form(70),
    custom_instructions: str = Form(""),
    urgency: int = Form(0),
    cta_strength: int = Form(50),
    politeness: int = Form(50),
    salutation_style: str = Form("standard"),
    sign_off_style: str = Form("professional"),
    language: str = Form("english"),
    audience_type: str = Form("general"),
    purpose: str = Form("general"),
    keywords_to_include: str = Form(""),
    response_type: str = Form("none"),
    industry: str = Form("general"),
    recipient_relationship: str = Form("unknown"),
    include_attachment_reference: bool = Form(False),
):
    """Generate an email based on form input."""
    email_request = EmailRequest(
        preset=preset,
        incoming_email=incoming_email,
        recipient_name=recipient_name,
        sender_name=sender_name,
        tone=tone,
        length=length,
        temperature=temperature,
        custom_instructions=custom_instructions,
        urgency=urgency,
        cta_strength=cta_strength,
        politeness=politeness,
        salutation_style=salutation_style,
        sign_off_style=sign_off_style,
        language=language,
        audience_type=audience_type,
        purpose=purpose,
        keywords_to_include=keywords_to_include,
        response_type=response_type,
        industry=industry,
        recipient_relationship=recipient_relationship,
        include_attachment_reference=include_attachment_reference,
    )

    try:
        result = await email_service.generate(email_request)
        return templates.TemplateResponse(
            "partials/result.html",
            {
                "request": request,
                "subject": result.subject,
                "subject_variants": result.subject_variants,
                "body": result.body,
                "word_count": result.word_count,
                "read_time": result.read_time_display,
                "spam_score": result.spam_score,
                "spam_warnings": result.spam_warnings,
            },
        )
    except ValueError as e:
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "error": str(e)},
        )
    except Exception as e:
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "error": f"Failed to generate email: {str(e)}"},
        )


# JSON API endpoints for programmatic access
api_router = APIRouter(prefix="/api", tags=["api"])


@api_router.post("/generate")
async def api_generate_email(email_request: EmailRequest):
    """Generate an email via JSON API."""
    try:
        result = await email_service.generate(email_request)
        return result
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e))
