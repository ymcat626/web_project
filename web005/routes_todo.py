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
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    body = template('todo_index.html')

    todo_list = Todo.all()
    # 列表推导用来生成html语句

    # todo_html = ''.join(['<h3>{}: {}</h3>'.format(todo.id, todo.title) for todo in todo_list])
    todos = []
    for todo in todo_list:
        t = '<h3>{}: {}</h3>'.format(todo.id, todo.title)
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
    if request.method == 'POST':
        form = request.form()
        todo = Todo.new(form)
        todo.save()
        log('debug add todo:', todo.id, todo.title)

    return redirect('/todo')


# 路由字典
# key 是路由（路由就是 path）
# value 是路由处理函数（就是响应）
route_dict = {
    '/todo': index,
    '/todo/add': add,
}