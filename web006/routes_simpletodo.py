# coding: utf-8
from web006.todo import Todo
from web006.utils import (
    log,
    template,
)


def http_response(body):
    headers = 'HTTP/1.1 200 OK\r\n\r\n'
    r = headers + body
    return r.encode(encoding='utf-8')


def index(request):
    todo_list = Todo.all()
    body = template('simple_todo_index.html', todos=todo_list)
    return http_response(body)


def edit(request):
    pass


def add(request):
    pass


def update(request):
    pass


def delete(request):
    pass


route_dict = {
    '/': index,
    '/add': add,
    '/update': update,
    '/edit': edit,
    '/delete': delete,
}