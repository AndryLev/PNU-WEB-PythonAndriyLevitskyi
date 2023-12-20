from flask import render_template, redirect, url_for, flash
from app import db
from .forms import FeedbackForm
from .models import Feedback
from . import feedback_blueprint

@feedback_blueprint.route('/index', methods=['GET', 'POST'])
def index():
    form = FeedbackForm()

    if form.validate_on_submit():
        name = form.name.data
        feedback_text = form.feedback_text.data

        feedback = Feedback(name=name, feedback_text=feedback_text)
        db.session.add(feedback)
        db.session.commit()

        flash('Feedback successfully saved', 'success')
        return redirect(url_for('.index'))

    feedbacks = Feedback.query.all()
    return render_template('feedback/index.html', form=form, feedbacks=feedbacks)