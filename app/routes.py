from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from . import db
from .models import Todo

main = Blueprint('main', __name__)

@main.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@main.route('/add', methods=['POST'])
def add():
    title = request.json.get('title')
    if title:
        todo = Todo(title=title)
        db.session.add(todo)
        db.session.commit()
        return jsonify({'id': todo.id, 'title': todo.title}), 201
    return jsonify({'error': 'Title is required'}), 400

@main.route('/delete/<int:todo_id>', methods=['DELETE'])
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'result': 'Todo deleted'})
    return jsonify({'error': 'Todo not found'}), 404
