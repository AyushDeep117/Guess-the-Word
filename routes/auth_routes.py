from flask import Blueprint, render_template, request, redirect, url_for, flash

from services.auth_service import (
    validate_registration,
    username_exists,
    create_user,
)


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        is_valid, error_message = validate_registration(
            username,
            password,
        )

        if not is_valid:
            flash(error_message, "error")
            return render_template("register.html")

        if username_exists(username):
            flash("Username already exists.", "error")
            return render_template("register.html")

        create_user(username, password)

        flash("Registration successful. Please log in.", "success")

        return redirect(url_for("auth.register"))


    return render_template("register.html")