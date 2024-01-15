from flask import url_for
from app import db
from app.todo.models import Todo
from .base_test import BaseTest

class TodoTest(BaseTest):
    def test_todo_create(self):
        '''Тестує можливість добавлення нової задачі.'''
        data = {
            'title': 'flask tests',
        }
        with self.client:
            response = self.client.post(url_for('todo.todo_add'), data=data,
                                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            todo = Todo.query.filter_by(title='flask tests').first()
            self.assertIsNotNone(todo)

    def test_get_all_todo(self):
        '''Тестує коректність виводу усіх задач '''
        todo1 = Todo(title='todo_1', complete=False)
        db.session.add_all([todo1])

        response = self.client.get(url_for('todo.todo'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(bytes(f"{todo1.title}", 'utf-8'), response.data)
        self.assertEqual(Todo.query.count(), 1)

    def test_update_todo_complete(self):
        '''Тестує коректність оновлення статусу задачі'''
        todo1 = Todo(title='todo1', complete=False)
        db.session.add(todo1)
        with self.client:
            response = self.client.get(url_for('todo.todo_update', todo_id=1), follow_redirects=True)
            updated_todo = Todo.query.filter_by(id=1).first()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(updated_todo.complete)

    def test_delete_todo(self):
        '''Тестує видалення задачі'''
        todo1 = Todo(title="todo1", complete=False)
        db.session.add(todo1)

        with self.client:
            response = self.client.get(url_for("todo.todo_delete", todo_id=1), follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            deleted_todo = Todo.query.filter_by(id=1).first()
            self.assertIsNone(deleted_todo)
            self.assertFalse(Todo.query.filter_by(id=1).first())