from web005_release.models.user import User
from web005_release.utils import template


def route_index(request):
    headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    username = ''
    body = body.replace('{{username}}', username)
    r = headers + '\r\n' + body
    return r.encode('utf-8')


def route_register(request):
    headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('register.html')
    result = ''
    if request.method == 'POST':
        form = request.form()
        user = User.new(form)
        if user.validate_register():
            result = user.username
            user.save()
    body = body.replace('{{result}}', result)
    r = headers + '\r\n' + body
    return r.encode('utf-8')


def route_login(request):
    headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('login.html')

    username = ''
    result = ''
    if request.method == 'POST':
        form = request.form()
        user = User.new(form)
        if user.validate_login():
            username = user.username
            result = '登录成功！'
        else:
            result = '帐号或者密码错误！'
    body = body.replace('{{username}}', username)
    body = body.replace('{{result}}', result)

    r = headers + '\r\n' + body
    return r.encode('utf-8')


def route_message(request):
    headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('message.html')
    r = headers + '\r\n' + body
    return r.encode('utf-8')


def route_static(request):
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        body = f.read()
    headers = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
    r = headers + b'\r\n' + body
    return r


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/message': route_message,
}