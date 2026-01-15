from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import os
from services.email_service import SendPostEmailService

load_dotenv()

app = FastAPI(title="SendPost Email API")

email_service = SendPostEmailService()

class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    htmlBody: str
    textBody: str = None

@app.get("/")
def read_root():
    return {"message": "SendPost FastAPI Example API"}

@app.post("/api/send-email")
async def send_email(request: EmailRequest):
    result = await email_service.send_email(
        to=request.to,
        subject=request.subject,
        html_body=request.htmlBody,
        text_body=request.textBody
    )
    
    if result['success']:
        return {
            'success': True,
            'messageId': result['message_id']
        }
    else:
        raise HTTPException(status_code=500, detail=result['error'])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
