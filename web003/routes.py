# coding: utf-8
from web003.models import User, Message


def template(name):
    path = 'templates/{}'.format(name)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_static(request):
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        headers = b'HTTP/1.1 200 ok\r\nContent-Type: image/gif\r\n'
        body = f.read()
        image = headers + b'\r\n' + body
        return image


def route_index(request):
    headers = 'HTTP/1.1 200 OL\r\nConnection: close\r\nContent: text/html\r\n'
    body = template('index.html')
    r = headers + '\r\n' + body
    return r.encode('utf-8')


def route_register(request):
    headers = 'HTTP/1.1 200 ok\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        user = User.new(form)
        if user.validate_register():
            user.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = headers + '\r\n' + body
    return r.encode('utf-8')


def route_login(request):
    headers = 'HTTP/1.1 200 ok\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        user = User.new(form)
        if user.validate_login():
            result = '登录成功'
        else:
            result = '用户名或者密码错误'

    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)
    r = headers + '\r\n' + body
    return r.encode('utf-8')


# message_list 存储了所有的 message
message_list = []


def route_message(request):
    if request.method == 'POST':
        form = request.form()
        message = Message(form)
        message_list.append(message)
    headers = 'HTTP/1.1 200 ok\r\nContent-Type: text/html\r\n'
    msgs = '\n'.join([str(m) for m in message_list])
    body = template('html_basic.html')
    body = body.replace('{{messages}}', msgs)
    r = headers + '\r\n' + body
    return r.encode('utf-8')


route_dict = {
    '/': route_index,
    '/register': route_register,
    '/login': route_login,
    '/messages': route_message,
}
