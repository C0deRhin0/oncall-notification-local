from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Incident, NotificationLog, Engineer

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    incidents = (
        Incident.query.order_by(Incident.triggered_at.desc()).limit(50).all()
    )
    active_count = Incident.query.filter_by(status="active").count()
    resolved_count = Incident.query.filter_by(status="resolved").count()
    engineer_count = Engineer.query.count()
    oncall_count = Engineer.query.filter_by(is_oncall=True).count()

    return render_template(
        "dashboard.html",
        incidents=incidents,
        active_count=active_count,
        resolved_count=resolved_count,
        engineer_count=engineer_count,
        oncall_count=oncall_count,
    )
