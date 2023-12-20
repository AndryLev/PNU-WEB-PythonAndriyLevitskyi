import os
from datetime import datetime

from flask import render_template, request

from .data import posts
from . import portfolio_blueprint

@portfolio_blueprint.route('/')
def home():
    return render_template("portfolio/home.html")


@portfolio_blueprint.route('/about')
def about():
    return render_template("portfolio/about.html")


@portfolio_blueprint.context_processor
def inject_data():
    os_name = os.name
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return dict(os_name=os_name, user_agent=user_agent, current_time=current_time)


@portfolio_blueprint.route('/skill/')
@portfolio_blueprint.route('/skill/<int:idx>')
def skill(idx=None):
    if idx is not None:
        return render_template("portfolio/skill.html", posts=posts, idx=idx)
    else:
        return render_template("portfolio/skills.html", posts=posts)