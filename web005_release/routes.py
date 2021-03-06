import random

from web005_release.models.user import User
from web005_release.utils import template, log


# 存储session
session = {}
message_list = []


def random_str():
    seed = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    result = ''
    for i in range(16):
        index = random.randint(1, len(range(16)) - 1)
        result += seed[index]
    return result


def current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '【游客】')
    return username


def response_with_headers(headers, code=200):
    '''
    :param headers: dict,用于构建请求头的信息
    :return: string
    '''
    header_dict = {
        200: 'HTTP/1.1 200 OK\r\n',
        302: 'HTTP/1.1 302 Temporarily Moved\r\n'
    }
    header = header_dict[code]
    # 出现bug，当headersv只有一项时，'\r\n'并不加到字符串里
    # header += '\r\n'.join(['{}: {}'.format(k, v) for k, v in headers.items()])
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    return header


def route_index(request):
    headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('example.html')
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
    header_dict = {
        'Content-Type': 'text/html'
    }
    body = template('login.html')
    username = ''
    result = ''
    if request.method == 'POST':
        form = request.form()
        user = User.new(form)
        if user.validate_login():
            result = '登录成功！'

            # 添加session
            session_id = random_str()
            session[session_id] = user.username
            header_dict['Set-Cookie'] = 'user={}'.format(session_id)

        else:
            result = '帐号或者密码错误！'
    headers = response_with_headers(header_dict)
    username = current_user(request)
    body = body.replace('{{username}}', username)
    body = body.replace('{{result}}', result)

    r = headers + '\r\n' + body
    # log('login_response:', r)
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