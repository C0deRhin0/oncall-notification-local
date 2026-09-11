import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///oncall.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

    APP_TIMEZONE = os.environ.get("APP_TIMEZONE", "Asia/Manila")

    GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS", "")
    GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")

    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "")
    TWILIO_SMS_SENDER_ID = os.environ.get("TWILIO_SMS_SENDER_ID", TWILIO_PHONE_NUMBER)

    CLICKSEND_USERNAME = os.environ.get("CLICKSEND_USERNAME", "")
    CLICKSEND_API_KEY = os.environ.get("CLICKSEND_API_KEY", "")
    CLICKSEND_SENDER_ID = os.environ.get("CLICKSEND_SENDER_ID", "")

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

    AUTO_APPROVE_SCHEDULE = os.environ.get("AUTO_APPROVE_SCHEDULE", "false").lower() == "true"
    INCIDENT_COOLDOWN_MINUTES = int(os.environ.get("INCIDENT_COOLDOWN_MINUTES", "5"))
    POLL_INTERVAL_SECONDS = int(os.environ.get("POLL_INTERVAL_SECONDS", "30"))

    @classmethod
    def validate_required_settings(cls):
        missing = [
            name
            for name in ("SECRET_KEY", "ADMIN_USERNAME", "ADMIN_PASSWORD")
            if not getattr(cls, name)
        ]
        if missing:
            raise RuntimeError(
                "Required configuration is missing: "
                f"{', '.join(missing)}. Set these environment variables before starting the app."
            )
