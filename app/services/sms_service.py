import logging
from flask import current_app
from twilio.rest import Client
from app import db
from app.models import NotificationLog

logger = logging.getLogger(__name__)

MAX_SMS_LENGTH = 160


def send_sms(incident, engineer):
    """Send a Twilio SMS to the engineer. Returns message_sid or None."""
    body = _build_sms_body(incident)

    try:
        client = Client(
            current_app.config["TWILIO_ACCOUNT_SID"],
            current_app.config["TWILIO_AUTH_TOKEN"],
        )
        msg = client.messages.create(
            to=engineer.phone,
            from_=current_app.config["TWILIO_PHONE_NUMBER"],
            body=body,
        )
        log = NotificationLog(
            incident_id=incident.id,
            engineer_id=engineer.id,
            type="sms",
            status="sent",
            twilio_sid=msg.sid,
            notes=f"SMS sent to {engineer.phone}",
        )
        db.session.add(log)
        db.session.commit()
        logger.info(f"[sms_service] SMS sent → SID={msg.sid} engineer={engineer.name}")
        return msg.sid
    except Exception as e:
        logger.error(f"[sms_service] Failed to send SMS to {engineer.name}: {e}")
        try:
            log = NotificationLog(
                incident_id=incident.id,
                engineer_id=engineer.id,
                type="sms",
                status="failed",
                notes=str(e),
            )
            db.session.add(log)
            db.session.commit()
        except Exception:
            pass
        return None


def _build_sms_body(incident):
    template = current_app.config["SMS_TEMPLATE"]
    company = current_app.config["COMPANY_NAME"]
    subject = incident.email_subject or "Unknown"
    snippet = incident.body_snippet or ""

    # Assemble without snippet first to measure fixed length
    fixed = template.format(
        company_name=company,
        email_subject=subject,
        email_body_snippet="",
    )
    budget = MAX_SMS_LENGTH - len(fixed)
    if budget < 0:
        budget = 0
    snippet = snippet[:budget]

    body = template.format(
        company_name=company,
        email_subject=subject,
        email_body_snippet=snippet,
    )
    if len(body) > MAX_SMS_LENGTH:
        body = body[:MAX_SMS_LENGTH]
    return body
