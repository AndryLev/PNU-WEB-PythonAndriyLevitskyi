from flask import render_template,  redirect, url_for
from app import db
from .forms import TodoForm
from .models import Todo
from . import todo_blueprint


@todo_blueprint.route('/todo', methods=['POST', 'GET'])
def todo():
    todo_list = Todo.query.all()
    form = TodoForm()
    return render_template("todo/todo.html", todo_list=todo_list, form=form)


@todo_blueprint.route("/add", methods=["POST"])
def todo_add():
    form = TodoForm()
    if form.validate_on_submit():
        title = form.title.data
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for(".todo"))


@todo_blueprint.route("/update/<int:todo_id>")
def todo_update(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for(".todo"))


@todo_blueprint.route("/delete/<int:todo_id>")
def todo_delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for(".todo"))