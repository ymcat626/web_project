# coding: utf-8
from web005_release.todo import Todo
from web005_release.utils import template, log


def response_with_headers(headers, code=200):
    header = 'HTTP/1.1 {} OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    return header


def redirect(url):
    headers = {
        'Content-Type': 'text/html',
        'Location': url
    }
    r = response_with_headers(headers, code=302) + '\r\n'
    return r.encode('utf-8')


def route_index(request):
    headers_dict = {
        'Content': 'text/html'
    }
    header = response_with_headers(headers_dict)
    body = template('todo_index.html')

    # 获取TODO的实例对象
    todos = ''
    todo_list = Todo.all()
    todo_str_list = []

    # 拼接字符
    # todos += ''.join(['<h3>{}: {} {} {}</h3>'.format(todo.id, todo.title, url_edit, url_delete) for todo in todo_list])
    for todo in todo_list:
        url_edit = '<a href="/todo/edit?id={}">编辑</a>'.format(todo.id)
        url_delete = '<a href="/todo/delete?id={}">删除</a>'.format(todo.id)
        todo_str = '<h3>{}: {} {} {}</h3>'.format(todo.id, todo.title, url_edit, url_delete)
        todo_str_list.append(todo_str)
    todos += ''.join(todo_str_list)
    body = body.replace('{{todos}}', todos)

    r = header + '\r\n' + body
    return r.encode('utf-8')


def route_add(request):
    # 点击add按钮后，新建一个todo对象，然后save
    form = request.form()
    todo = Todo.new(form)
    todo.save()
    return redirect('/todo')


def route_edit(request):
    header_dict = {
        'Content-Type': 'text/html',
    }
    headers = response_with_headers(header_dict)

    body = template('todo_edit.html')
    todo_id = request.query.get('id', -1)
    id = str(todo_id)
    body = body.replace('{{id}}', id)
    r = headers + '\r\n' + body
    return r.encode('utf-8')


def route_update(request):
    form = request.form()
    todos = Todo.all()
    todo_id = int(form.get('id', -1))
    for todo in todos:
        if todo_id == todo.id:
            todo.title = form.get('title')
            todo.save()
            break
    return redirect('/todo')


def route_delete(request):
    todo_id = request.query.get('id', -1)
    todo_id = int(todo_id)
    todo = Todo.find_by(id=todo_id)
    # log('debug: route_delete', todo)
    # 'NoneType' object has no attribute 'remove'
    todo.remove()
    return redirect('/todo')


route_dict = {
    '/todo': route_index,
    '/todo/edit': route_edit,
    '/todo/update': route_update,
    '/todo/delete': route_delete,
    '/todo/add': route_add,
}