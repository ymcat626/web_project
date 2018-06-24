from web005.routes import (
    current_user,
    User,
)
from web005.todo import Todo
from web005.util import log


def template(name):
    """
    根据名字读取 templates 文件夹里的一个文件并返回
    """
    path = 'templates/{}'.format(name)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def response_with_headers(headers, code=200):
    header = 'HTTP/1.1 {} OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    return header


def redirect(url):
    '''
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    '''
    headers = {
        'Content-Type': 'text/html',
        'Location': url,
    }
    r = response_with_headers(headers, 302) + '\r\n'
    log('redirect:', r)
    return r.encode('utf-8')


def index(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')

    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    body = template('todo_index.html')

    todo_list = Todo.find_all(user_id=u.id)
    # 列表推导用来生成html语句
    # todo_html = ''.join(['<h3>{}: {}</h3>'.format(todo.id, todo.title) for todo in todo_list])
    todos = []
    for todo in todo_list:
        edit_link = '<a href="/todo/edit?id={}">编辑</a>'.format(todo.id)
        delete_link = '<a href="/todo/delete?id={}">删除</a>'.format(todo.id)
        t = '<h3>{}: {} {} {}</h3>'.format(todo.id, todo.title, edit_link, delete_link)
        todos.append(t)
    todo_html = ''.join(todos)
    # 开始body.replace()替换这里出现bug，原因是自己对str.replace()的不熟悉
    # body.replace('{{todos}}', todos)
    body = body.replace('{{todos}}', todo_html)
    # log('debug body', body)
    r = header + '\r\n' + body
    # log('debug todo_index', r)
    return r.encode('utf-8')


def add(request):
    '''
    用于增加新的 TODO 的路由函数
    :param request:
    :return:
    '''
    uname = current_user(request)
    u = User.find_by(username=uname)
    if request.method == 'POST':
        form = request.form()
        todo = Todo.new(form)
        todo.user_id = u.id
        todo.save()
        log('debug add todo:', todo.id, todo.title)

    return redirect('/todo')


def edit(request):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')

    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u.id:
        return redirect('/login')

    body = template('todo_edit.html')
    body = body.replace('{{id}}', str(todo_id))
    r = header + '\r\n' + body
    return r.encode('utf-8')


def update(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    if request.method == 'POST':
        form = request.form()
        todo_id = int(form.get('id', -1))
        todo = Todo.find_by(id=todo_id)
        if todo is not None:
            todo.title = form.get('title', todo.title)
            todo.save()
        return redirect('/todo')


def delete(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    # 找到todo的id,判断todo是否存在
    todo_id = int(request.query.get('id', -1))
    todo = Todo.find_by(id=todo_id)
    if todo.user_id != u.id:
        return redirect('/login')
    if todo is not None:
        todo.remove()
    return redirect('/todo')


# 路由字典
# key 是路由（路由就是 path）
# value 是路由处理函数（就是响应）
route_dict = {
    # 用于显示页面
    '/todo': index,
    '/todo/edit': edit,
    # 用于对数据进行处理
    '/todo/add': add,
    '/todo/update': update,
    '/todo/delete': delete,
}
