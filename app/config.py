import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
    SQLALCHEMY_DATABASE_URI = "sqlite:///oncall.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

    APP_TIMEZONE = os.environ.get("APP_TIMEZONE", "Asia/Manila")

    GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS", "")
    GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")

    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "")

    COMPANY_NAME = os.environ.get("COMPANY_NAME", "Nebulynx")
    TTS_TEMPLATE = os.environ.get(
        "TTS_TEMPLATE",
        "This is an automated oncall notification from {company_name}. "
        "A network incident has been reported. "
        "Incident reference: {email_subject}. "
        "Details: {email_body_snippet}. "
        "Please respond immediately. A follow-up text message will follow this call.",
    )
    SMS_TEMPLATE = os.environ.get(
        "SMS_TEMPLATE",
        "[ONCALL ALERT] {company_name} | Incident: {email_subject} | {email_body_snippet} | Respond immediately.",
    )

    AUTO_APPROVE_SCHEDULE = os.environ.get("AUTO_APPROVE_SCHEDULE", "true").lower() == "true"
    INCIDENT_COOLDOWN_MINUTES = int(os.environ.get("INCIDENT_COOLDOWN_MINUTES", "5"))
    POLL_INTERVAL_SECONDS = int(os.environ.get("POLL_INTERVAL_SECONDS", "30"))
