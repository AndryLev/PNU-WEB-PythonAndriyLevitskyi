import os
from datetime import datetime, timedelta
from flask import render_template, request, redirect, url_for, flash, session, make_response
from app.data import posts
from app import app, db
from app.forms import FeedbackForm, LoginForm
import json

from app.models import Feedback


def _get_credentials_filepath(filename="data/users.json", ):
    parent_dir = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(parent_dir, filename)
    return filepath


with open(_get_credentials_filepath(), 'r') as f:
    users = json.load(f)


# @app.route('/login')
# def login():
#     return render_template("login.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        remember = bool(request.form.get("remember"))

        if name in users and users[name] == password:
            session["username"] = name
            if remember:

                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=730)
            else:

                app.permanent_session_lifetime = timedelta(minutes=25)
            flash('Login successful', 'success')
            return redirect(url_for("info"))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for("login"))

    return render_template("login.html", form=form)


@app.route('/login/user', methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        if name in users and users[name] == password:
            session["username"] = name
            return redirect(url_for("info"))
    return redirect(url_for("login"))


@app.route('/info', methods=["GET", "POST"])
def info():
    user = session.get('username')

    user_cookies = request.cookies
    if user:
        if request.method == "POST":
            return render_template("info.html", username=user, user_cookies=user_cookies)
        return render_template("info.html", username=user, user_cookies=user_cookies)
    else:
        return redirect(url_for("login"))


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop('username', None)
    return redirect(url_for("login"))


@app.route('/add_cookie', methods=["POST"])
def add_cookie():
    user = session.get('username')

    if user:
        key = request.form.get('key')
        value = request.form.get('value')
        expiration = request.form.get('expiration')

        if key and value and expiration:
            expiration = int(expiration)
            expiration_time = datetime.now() + timedelta(seconds=expiration)

            response = make_response(redirect(url_for("info")))

            response.set_cookie(key, value, expires=expiration_time)

            return response
        else:
            return "Error: Invalid input for adding a cookie"
    else:
        return redirect(url_for("login"))
    pass


@app.route('/delete_cookie', methods=["POST"])
def delete_cookie():
    user = session.get('username')

    if user:
        key_to_delete = request.form.get('delete_key')

        if key_to_delete:

            response = make_response(redirect(url_for("info")))
            response.delete_cookie(key_to_delete)

            return response
        else:
            return "Error: Invalid input for deleting a cookie"
    else:
        return redirect(url_for("login"))


@app.route('/delete_all_cookies', methods=["POST"])
def delete_all_cookies():
    user = session.get('username')

    if user:

        response = make_response(redirect(url_for("info")))

        for key in request.cookies.keys():
            response.delete_cookie(key)

        return response
    else:
        return redirect(url_for("login"))
    pass


@app.route('/change_password', methods=['POST'])
def change_password():
    user = session.get('username')

    if user:
        new_password = request.form.get('new_password')

        if new_password:
            users[user] = new_password
            return redirect(url_for("info"))

    return redirect(url_for("login"))


@app.route('/index', methods=['GET', 'POST'])
def index():
    form = FeedbackForm()

    if form.validate_on_submit():
        name = form.name.data
        feedback_text = form.feedback_text.data

        feedback = Feedback(name=name, feedback_text=feedback_text)
        db.session.add(feedback)
        db.session.commit()

        flash('Feedback successfully saved', 'success')
        return redirect(url_for('index'))

    feedbacks = Feedback.query.all()
    return render_template('index.html', form=form, feedbacks=feedbacks)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.context_processor
def inject_data():
    os_name = os.name
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return dict(os_name=os_name, user_agent=user_agent, current_time=current_time)


@app.route('/skill/')
@app.route('/skill/<int:idx>')
def skill(idx=None):
    if idx is not None:
        return render_template("skill.html", posts=posts, idx=idx)
    else:
        return render_template("skills.html", posts=posts)
