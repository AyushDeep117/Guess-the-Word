from flask import (
    Blueprint,
    render_template,
    request,
)

from utils.auth import admin_required

from services.report_service import (
    get_daily_report,
    get_user_report,
    get_all_users,
)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@admin_required
def dashboard():
    return render_template("admin_dashboard.html")


@admin_bp.route("/reports/daily")
@admin_required
def daily_report():

    report_date = request.args.get("date")

    if not report_date:
        from datetime import date
        report_date = date.today().isoformat()

    report = get_daily_report(report_date)

    return render_template(
        "daily_report.html",
        report=report,
    )


@admin_bp.route("/reports/user")
@admin_required
def user_report():

    users = get_all_users()

    selected_user_id = request.args.get(
        "user_id",
        type=int,
    )

    report = []

    selected_user = None

    if selected_user_id:

        report = get_user_report(
            selected_user_id
        )

        selected_user = next(
            (
                user
                for user in users
                if user["id"] == selected_user_id
            ),
            None,
        )

    return render_template(
        "user_report.html",
        users=users,
        report=report,
        selected_user=selected_user,
    )