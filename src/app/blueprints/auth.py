from flask import (
    Blueprint,
    request,
    render_template,
    url_for,
    redirect,
)
from flask_login import (
    login_required,
    logout_user,
)

from ..forms.auth import (
    RegistrationForm,
    LoginForm,
)

blueprint = Blueprint('auth', __name__, template_folder='templates')


@blueprint.get("/sign-up/")
def get_signup_form():
    form = RegistrationForm(request.form)
    return render_template("auth/sign-up.html", form=form)


@blueprint.post("/sign-up/")
def sign_up():
    form = RegistrationForm(request.form)

    if form.validate_on_submit():
        return redirect(url_for("shows.get_shows"))
    return render_template("auth/sign-up.html", form=form), 400


@blueprint.get("/login/")
def get_login_page():
    form = LoginForm(request.form)
    return render_template("auth/login.html", form=form)


@blueprint.post("/login/")
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        return redirect(url_for("shows.get_shows"))
    else:
        return render_template("auth/login.html", form=form), 401


@blueprint.get("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.get_login_page"))
