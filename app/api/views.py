from flask import jsonify, request
from app.todo.models import Todo
from . import api_blueprint
from app import db
from sqlalchemy.exc import IntegrityError
from app.auth_api.views import required_token

@api_blueprint.route('/ping', methods=["GET", "POST"])
def ping():
    return "pong"

@api_blueprint.route('/todos', methods=['GET'])
def todos_list():
    todos = Todo.query.all()
    todo_list = [todo.as_dict() for todo in todos]
    return jsonify({'todos': todo_list})

@api_blueprint.route('/todos/<int:todo_id>', methods=['GET'])
def todos_get(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify(errorMessage="Requested todo item has not been found"), 404

    return jsonify(todo.as_dict()), 200

@api_blueprint.route('/todos', methods=['POST'])
@required_token
def create_todos():
    try:
        data = request.get_json()
        new_todo = Todo(title=data['title'], complete=data.get('complete', False))
        db.session.add(new_todo)
        db.session.commit()

        todo_dict = new_todo.as_dict()

        return jsonify(todo_dict), 200

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'IntegrityError: Duplicate entry'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_blueprint.route('/todos/<int:todo_id>', methods=['PUT'])
@required_token
def update_todos(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    data = request.get_json()
    todo.title = data.get('title', todo.title)
    todo.complete = data.get('complete', todo.complete)

    db.session.commit()

    todo_dict = todo.as_dict()

    return jsonify(todo_dict), 200

@api_blueprint.route('/todos/<int:todo_id>', methods=['DELETE'])
@required_token
def delete_todos(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    todo_dict = todo.as_dict()

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message': 'Todo deleted', 'deleted_todo': todo_dict})
