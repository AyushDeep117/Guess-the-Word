from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)

from services.auth_service import (
    validate_registration,
    username_exists,
    create_user,
    authenticate_user,
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
    
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = authenticate_user(username, password)

        if user is None:
            flash("Invalid username or password.", "error")
            return render_template("login.html")

        session.clear()

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]

        return redirect(url_for("home"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.", "success")

    return redirect(url_for("auth.login"))


    