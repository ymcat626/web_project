# coding: utf-8
import time

from web006.todo import Todo
from web006.utils import (
    log,
    template,
    redirect,
    http_response,
)


def index(request):
    todo_list = Todo.all()
    body = template('simple_todo_index.html', todos=todo_list)
    return http_response(body)


def edit(request):
    todo_id = int(request.query.get('id', -1))
    todo = Todo.find_by(id=todo_id)
    body = template('simple_todo_edit.html', todo=todo)
    return http_response(body)


def add(request):
    form = request.form()
    todo = Todo.new(form)
    todo.save()
    return redirect('/')


def update(request):
    if request.method == 'POST':
        form = request.form()
        # ValueError: invalid literal for int() with base 10: ''
        todo_id = int(request.query.get('id', -1))
        log('debug update todo id :', todo_id)
        todo = Todo.find_by(id=todo_id)
        if todo is not None:
            todo.task = form.get('task', todo.task)
            todo.update_time = int(time.time())
            log('debug update todo task:', todo.task)
            todo.save()
    return redirect('/')


def delete(request):
    todo_id = int(request.query.get('id', -1))
    todo = Todo.find_by(id=todo_id)
    todo.remove()
    return redirect('/')


route_dict = {
    '/': index,
    '/add': add,
    '/update': update,
    '/edit': edit,
    '/delete': delete,
}