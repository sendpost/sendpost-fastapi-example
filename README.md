# SendPost FastAPI Example

This example demonstrates how to send emails using SendPost in a FastAPI application.

## Prerequisites

- Python 3.8 or higher
- A SendPost Sub-Account API Key

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file:
```env
SENDPOST_API_KEY=your_sub_account_api_key
SENDPOST_FROM_EMAIL=hello@playwithsendpost.io
SENDPOST_FROM_NAME=SendPost
```

3. Update `.env` with your SendPost Sub-Account API Key

## Run

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The server will start on `http://localhost:8000`

## Usage

Send a POST request to `http://localhost:8000/api/send-email`:

```bash
curl -X POST http://localhost:8000/api/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "to": "recipient@example.com",
    "subject": "Test Email",
    "htmlBody": "<h1>Hello World!</h1>"
  }'
```

## API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Notes

- Make sure your sender email domain is verified in your SendPost account
- The example uses Pydantic models for request validation
- The email service is async and uses dependency injection patterns
