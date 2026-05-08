# Call-Analysis-Platform

AI-powered system for analyzing banking customer support calls. This platform automatically transcribes audio calls, classifies customer intents, and routes inquiries to the appropriate department based on urgency and type.

## Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Django UI      │─────▶│  FastAPI Backend │─────▶│  AI Models      │
│  (Port 8080)    │      │  (Port 8000)      │      │  (Whisper + BERT)│
└─────────────────┘      └──────────────────┘      └─────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │  SQLite Database │
                        └──────────────────┘
```

## Features

- **Speech-to-Text**: Converts audio calls to text using OpenAI Whisper
- **Intent Classification**: Classifies customer intent using DistilBERT (77 banking intents)
- **Smart Routing**: Routes calls to appropriate department (account, cards, fraud, technical_support)
- **Urgency Detection**: Prioritizes high-urgency issues (fraud, compromised credentials)
- **Web Dashboard**: Upload audio files and view analysis results

## Intent Categories (77 total)

The model recognizes intents across these domains:
- **Account**: Refunds, transfers, balance issues, top-ups
- **Cards**: Card activation, delivery, payments, PIN issues
- **Fraud**: Unauthorized transactions, lost/stolen cards
- **Technical Support**: Identity verification, passcode recovery
- **General**: Currency support, country availability

## Quick Start

### Prerequisites

- Python 3.9+
- CUDA-capable GPU (recommended for faster inference)

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

**Option 1: Run both services manually**

```bash
# Terminal 1: Start FastAPI (Port 8000)
cd fastapi_backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start Django (Port 8080)
cd django_app/NLPBackend
python manage.py migrate
python manage.py runserver 8080
```

**Option 2: Using script**

```bash
python run.py
```

### Access the Application

- Web UI: http://localhost:8080
- API Docs: http://localhost:8000/docs

## API Usage

### Analyze Call

```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@call_recording.wav"
```

**Response:**
```json
{
  "transcript": "Hello, I need to report a suspicious transaction...",
  "intent": "card_payment_not_recognised",
  "confidence": 0.94,
  "urgency": "high",
  "department": "fraud"
}
```

## Project Structure

```
Call-Analysis-Platform/
├── fastapi_backend/          # FastAPI service
│   ├── main.py               # Application entry point
│   └── app/
│       ├── routes.py         # API endpoints
│       └── services/         # Business logic
│           ├── STT.py        # Whisper speech-to-text
│           ├── intent.py     # BERT intent classifier
│           └── rules.py     # Routing rules engine
├── django_app/               # Django web frontend
│   └── NLPBackend/
│       ├── api/              # Django app
│       │   ├── models.py    # CallAnalysis model
│       │   ├── views.py     # Upload & dashboard views
│       │   └── templates/   # HTML templates
│       └── NLPBackend/      # Django project settings
├── AI_Module/                # AI models
│   └── models/
│       ├── distilbert-banking77/  # Trained BERT model
│       └── routing_rules.json     # Intent-to-department mapping
└── notebooks/                # Jupyter notebooks for analysis
```

## Models

### Intent Classifier
- **Model**: DistilBERT fine-tuned on Banking77 dataset
- **Classes**: 77 banking-specific intents
- **Input**: Text (call transcript)
- **Output**: Intent label + confidence score

### Routing Rules
- Maps each intent to urgency level (high/medium/low)
- Maps each intent to target department

## Configuration

### FastAPI Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STT_MODEL` | base | Whisper model size (tiny/base/small/medium/large) |
| `DEVICE` | auto | CPU or CUDA for inference |

### Django Settings

Edit `django_app/NLPBackend/NLPBackend/settings.py`:
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Add your domain/IP
- `SECRET_KEY`: Generate new key for production

## Development

### Running Tests

```bash
# Django tests
cd django_app/NLPBackend
python manage.py test

# API tests
pytest fastapi_backend/
```

### Adding New Intents

1. Fine-tune the BERT model on new intent data
2. Add intent mapping in `AI_Module/models/routing_rules.json`
3. Redeploy the model

## Tech Stack

- **Backend**: FastAPI, Django 6.0
- **AI/ML**: PyTorch, Transformers, Whisper
- **Database**: SQLite (development)
- **Frontend**: Bootstrap 5, HTML/CSS
- **NLP**: NLTK, DistilBERT

## License

MIT License