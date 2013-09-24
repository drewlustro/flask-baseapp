from flask import Blueprint, render_template, g, session, flash,\
    redirect, url_for, request, send_from_directory
from app.models import User
from app.forms import LoginForm, SignupForm
from app.lib import filters
import os
from app import application

controller = Blueprint("default", __name__, url_prefix="")


@controller.route("/")
def index():
    return render_template('default/index.html')


@controller.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    next = None
    if g.user:
        return redirect(url_for(".index"))

    if form.validate_on_submit():
        u = User.login(form.email.data, form.password.data)
        if u:
            g.user = u
            session['user_id'] = g.user.id
            flash("Welcome back")
            return redirect(url_for(".index"))
        else:
            next = request.form.get('next', None)
            flash("Invalid e-mail address or password please try again.")

    if not next:
        next = request.args.get('next', None)
    return render_template("default/login.html", form=form)


@controller.route("/signup", methods=['GET', 'POST'])
def signup():
    if g.user:
        return redirect(url_for(".index"))

    form = SignupForm(csrf_enabled=False)
    if form.validate_on_submit():
        u = User.create(passwd=form.password.data,
                        email=form.email.data)
        if u:
            g.user = u
            session['user_id'] = g.user.id
            return redirect(url_for(".index"))
        else:
            flash("An account already exists with that username.")

    return render_template("default/signup.html", form=form)


@controller.route('/img/<name>.<ext>')
def img(name, ext):
    mimetype = "image/png"
    if ext == "jpg" or ext == "jpeg":
        mimetype = "image/jpeg"
    elif ext == "gif":
        mimetype = "image/gif"
    return send_from_directory(os.path.join(application.root_path, 'img'),
                               name + '.' + ext, mimetype=mimetype)

@controller.route('/fonts/<name>.<ext>')
def fonts(name, ext):
    return send_from_directory(os.path.join(application.root_path, 'fonts'),
                               name + '.' + ext)


@controller.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(application.root_path, 'static'),
                               'favicon.ico', mimetype='image/x-icon')


@controller.route("/logout")
def logout():
    session.pop("user_id", None)
    g.user = None
    return redirect(url_for(".index"))
