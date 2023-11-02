import os
from datetime import datetime

from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

from data import posts

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'

db = SQLAlchemy(app)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    feedback_text = db.Column(db.Text)

    def __init__(self, name, feedback_text):
        self.name = name
        self.feedback_text = feedback_text


class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    feedback_text = TextAreaField('Feedback', validators=[DataRequired()])
    submit = SubmitField('Send')


with app.app_context():
    db.create_all()


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


if __name__ == '__main__':
    app.run(debug=True)
