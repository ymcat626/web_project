import json
from .session import session
from ..utils import (
    log,
    redirect,
    http_response,
    json_response,
)
from ..models.todo import Todo


def all(request):
    todo_list = Todo.all()
    todos = [t.json() for t in todo_list]
    return json_response(todos)


def add(request):
    form = request.json()
    todo = Todo.new(form)
    return json_response(todo)


def delete(request):
    todo_id = int(request.query.get('id'))
    t = Todo.delete(todo_id)
    return json_response(t)


def update(request):
    form = request.form()
    todo_id = int(form.get('id'))
    t = Todo.update(todo_id, form)
    return json_response(t)


route_dict = {
    'api/todo/all': all,
    'api/todo/add': add,
    'api/todo/delete': delete,
    'api/todo/update': update,
}
