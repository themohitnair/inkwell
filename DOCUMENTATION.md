# Inkwell - Project Documentation

## 1. Problem Statement

Crafting professional emails is a time-consuming and often challenging task that many professionals struggle with daily. Key pain points include:

- **Writer's Block**: Difficulty initiating emails, especially for sensitive topics like job applications, cold outreach, or negotiations
- **Tone Inconsistency**: Maintaining appropriate formality levels across different recipients (executives, clients, colleagues)
- **Language Barriers**: Non-native speakers struggle to compose emails in languages required for international business
- **Spam Triggers**: Unknowingly using phrases that trigger spam filters, reducing email deliverability
- **Context Switching**: Adjusting communication style across different industries (legal, technical, sales) requires mental overhead
- **Response Crafting**: Formulating appropriate replies (acceptance, decline, counter-offer) while maintaining professionalism

These challenges lead to reduced productivity, communication delays, and potential misunderstandings in professional settings.

---

## 2. Objective

Inkwell aims to be an **AI-powered email drafting assistant** that:

1. **Generates contextually appropriate emails** based on user-specified parameters (tone, length, urgency, purpose)
2. **Supports 12 languages** for international communication needs
3. **Adapts to audience and industry** with specialized vocabulary and formality levels
4. **Provides spam detection** to ensure high email deliverability
5. **Offers alternative subject lines** for A/B testing and optimization
6. **Enables reply generation** with appropriate response types (accept, decline, counter-offer, etc.)
7. **Delivers a seamless user experience** through a modern, responsive web interface with real-time generation

---

## 3. Architecture

### 3.1 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT (BROWSER)                               │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         Tailwind CSS + HTMX                           │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐   │  │
│  │  │   Email Form    │  │  Result Display │  │  Spam Score Panel   │   │  │
│  │  │  (Parameters)   │  │  (Typewriter)   │  │  (Visual Feedback)  │   │  │
│  │  └────────┬────────┘  └────────▲────────┘  └──────────▲──────────┘   │  │
│  └───────────┼────────────────────┼──────────────────────┼──────────────┘  │
└──────────────┼────────────────────┼──────────────────────┼──────────────────┘
               │ HTMX POST          │ HTML Partial         │
               ▼                    │                      │
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FASTAPI SERVER                                    │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                          Routes Layer                                 │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐   │  │
│  │  │   GET /         │  │  POST /generate │  │  POST /api/generate │   │  │
│  │  │   (Render UI)   │  │  (HTML Response)│  │  (JSON API)         │   │  │
│  │  └─────────────────┘  └────────┬────────┘  └──────────┬──────────┘   │  │
│  └────────────────────────────────┼──────────────────────┼──────────────┘  │
│                                   │                      │                  │
│  ┌────────────────────────────────▼──────────────────────▼──────────────┐  │
│  │                        EmailService                                   │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐   │  │
│  │  │  build_prompt() │  │   generate()    │  │  parse_response()   │   │  │
│  │  │  (Prompt Eng.)  │  │  (API Call)     │  │  (JSON Extraction)  │   │  │
│  │  └─────────────────┘  └────────┬────────┘  └─────────────────────┘   │  │
│  └────────────────────────────────┼─────────────────────────────────────┘  │
│                                   │                                         │
│  ┌────────────────────────────────▼─────────────────────────────────────┐  │
│  │                      Models & Validation                              │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐   │  │
│  │  │  EmailRequest   │  │  EmailResponse  │  │  Spam Detection     │   │  │
│  │  │  (Pydantic)     │  │  (Pydantic)     │  │  (Trigger Analysis) │   │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
               │
               │ HTTPS API Call
               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            GROQ API                                         │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    llama-3.3-70b-versatile                            │  │
│  │                    (Large Language Model)                             │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Request Flow Diagram

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  User    │    │  HTMX    │    │ FastAPI  │    │ Email    │    │  Groq    │
│  Input   │    │  Form    │    │ Routes   │    │ Service  │    │  API     │
└────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘
     │               │               │               │               │
     │ Fill Form     │               │               │               │
     ├──────────────►│               │               │               │
     │               │               │               │               │
     │               │ POST /generate│               │               │
     │               ├──────────────►│               │               │
     │               │               │               │               │
     │               │               │ Validate      │               │
     │               │               ├──────────────►│               │
     │               │               │               │               │
     │               │               │               │ Build Prompt  │
     │               │               │               ├───────────────┤
     │               │               │               │               │
     │               │               │               │ API Request   │
     │               │               │               ├──────────────►│
     │               │               │               │               │
     │               │               │               │ JSON Response │
     │               │               │               │◄──────────────┤
     │               │               │               │               │
     │               │               │ EmailResponse │               │
     │               │               │◄──────────────┤               │
     │               │               │               │               │
     │               │ HTML Partial  │               │               │
     │               │◄──────────────┤               │               │
     │               │               │               │               │
     │ Display Result│               │               │               │
     │◄──────────────┤               │               │               │
     │               │               │               │               │
```

### 3.3 Component Architecture

```
inkwell/
├── app/
│   ├── config.py          ─────► Environment Configuration (Pydantic Settings)
│   ├── main.py            ─────► Application Factory (FastAPI Instance)
│   ├── models.py          ─────► Data Models + Enums + Spam Detection
│   ├── prompts.py         ─────► System Prompts for Email Presets
│   ├── routes.py          ─────► HTTP Endpoints (/, /generate, /api/generate)
│   └── services/
│       └── email.py       ─────► Core Business Logic (Prompt Building + API)
├── templates/
│   ├── index.html         ─────► Main UI (Form + Layout)
│   └── partials/
│       ├── result.html    ─────► Email Result Component
│       └── error.html     ─────► Error Display Component
└── run.py                 ─────► Entry Point (Uvicorn Server)
```

---

## 4. Technology Stack

### 4.1 Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | >=3.11 | Runtime environment |
| **FastAPI** | >=0.115.0 | Async web framework for API endpoints |
| **Uvicorn** | >=0.32.0 | ASGI server for production deployment |
| **Pydantic** | >=2.12.0 | Data validation and settings management |
| **Jinja2** | >=3.1.0 | Server-side HTML templating |

### 4.2 Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **HTMX** | 2.0.4 | Lightweight AJAX for dynamic interactions |
| **Tailwind CSS** | Latest (CDN) | Utility-first CSS framework |
| **Custom JS** | - | Typewriter effect, clipboard, shortcuts |

### 4.3 AI/ML

| Technology | Version | Purpose |
|------------|---------|---------|
| **Groq SDK** | >=0.37.0 | API client for LLM access |
| **Llama 3.3 70B** | - | Large language model for email generation |

### 4.4 DevOps & Tooling

| Technology | Purpose |
|------------|---------|
| **uv** | Fast Python package manager |
| **python-dotenv** | Environment variable management |
| **python-multipart** | Form data parsing |

### 4.5 Technology Stack Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   HTMX      │  │  Tailwind   │  │  Jinja2 Templates       │  │
│  │   2.0.4     │  │    CSS      │  │  (Server-Side Render)   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    FastAPI >=0.115.0                        ││
│  │  ┌───────────────┐  ┌───────────────┐  ┌─────────────────┐ ││
│  │  │    Routes     │  │   Services    │  │     Models      │ ││
│  │  │  (Endpoints)  │  │ (Email Logic) │  │   (Pydantic)    │ ││
│  │  └───────────────┘  └───────────────┘  └─────────────────┘ ││
│  └─────────────────────────────────────────────────────────────┘│
│                        Uvicorn ASGI Server                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        EXTERNAL SERVICES                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      Groq API                                ││
│  │              llama-3.3-70b-versatile Model                   ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Output

### 5.1 Email Response Structure

The application generates emails with the following output structure:

```json
{
  "subject": "Meeting Request: Q1 Strategy Discussion",
  "subject_variants": [
    "Quick Sync on Q1 Priorities",
    "Let's Align on Q1 Goals"
  ],
  "body": "Dear Mr. Johnson,\n\nI hope this message finds you well...",
  "spam_score": 15,
  "spam_warnings": []
}
```

### 5.2 Output Components

| Field | Type | Description |
|-------|------|-------------|
| `subject` | string | Primary email subject line |
| `subject_variants` | string[] | 2 alternative subject lines for A/B testing |
| `body` | string | Complete email body with formatting |
| `spam_score` | integer (0-100) | Spam likelihood score |
| `spam_warnings` | string[] | Detected spam triggers (if any) |

### 5.3 Computed Properties

| Property | Calculation | Example |
|----------|-------------|---------|
| `word_count` | Words in body | 156 |
| `read_time_display` | word_count / 200 wpm | "1 min read" |
| `read_time_seconds` | (word_count / 200) * 60 | 47 |

### 5.4 Sample Output Screenshot Representation

```
┌─────────────────────────────────────────────────────────────────┐
│  GENERATED EMAIL                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Subject: Meeting Request: Q1 Strategy Discussion    [Copy]     │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  Dear Mr. Johnson,                                              │
│                                                                 │
│  I hope this message finds you well. I am writing to request   │
│  a brief meeting to discuss our Q1 strategic priorities and    │
│  ensure alignment across our teams.                            │
│                                                                 │
│  Would you be available for a 30-minute call next week? I am   │
│  flexible with timing and happy to work around your schedule.  │
│                                                                 │
│  Best regards,                                                  │
│  Sarah Chen                                                     │
│                                                                 │
│                                                    [Copy Body]  │
├─────────────────────────────────────────────────────────────────┤
│  Alternative Subjects:                                          │
│  • Quick Sync on Q1 Priorities                                  │
│  • Let's Align on Q1 Goals                                      │
├─────────────────────────────────────────────────────────────────┤
│  Spam Score: ████░░░░░░ 15/100 (Low Risk)                      │
│  Word Count: 87 words | Read Time: ~30 sec                      │
└─────────────────────────────────────────────────────────────────┘
```

### 5.5 Spam Score Interpretation

| Score Range | Risk Level | Visual Indicator |
|-------------|------------|------------------|
| 0-30 | Low | Green |
| 31-60 | Medium | Yellow |
| 61-100 | High | Red |

---

## Summary

Inkwell is a full-stack AI email assistant that combines modern web technologies (FastAPI, HTMX, Tailwind) with advanced LLM capabilities (Groq/Llama 3.3) to solve the universal challenge of professional email composition. The architecture emphasizes simplicity, performance, and user experience while providing extensive customization options for diverse communication needs.
