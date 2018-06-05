# coding: utf-8
import random

from web005.models import User, Message
from web005.util import log


def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        r = f.read()
        return r


def random_str():
    # 生成随机的字符
    seed = 'asdfjqeruoprtkjgfddzxcvnnmlpoidjiruqdfjjka'
    s = ''
    for i in range(16):
        index = random.randint(1, len(seed) - 1)
        s += seed[index]
    return s


def current_user(request):
    # cookies = request.cookies
    # session_id = cookies['user']
    # username = session[session_id]
    # return username
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '【游客】')
    return username


def response_with_header(headers, code=200):
    header_dict = {
        200: 'HTTP/1.1 200 OK\r\n',
        301: 'HTTP/1.1 301 Permanently Moved\r\n',
        302: 'HTTP/1.1 302 Temporarily Moved\r\n',
    }
    header = header_dict[code]
    # 这样写的原因是''.join()要比字符串的拼接效率高
    # for k, v in headers:
    #     header += '{}: {}\r\n'.format(k, v)
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    return header


def route_static(request):
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    # with open(path, 'rb', encoding='utf-8') as f:
    # ValueError: binary mode doesn't take an encoding argument
    # 二进制数据不应该指定编码格式
    with open(path, 'rb') as f:
        body = f.read()
        log('图片：', body)
    header = b'HTTP/1.1 200 OK\r\nContent: image/gif\r\n'
    r = header + b'\r\n' + body
    return r


def route_index(request):
    header_dict = {
        'Content-Type': 'text/html'
    }
    headers = response_with_header(header_dict)
    body = template('index.html')
    username = current_user(request)
    body = body.replace('{{username}}', username)
    r = headers + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_register(request):
    header_dict = {
        'Content-Type': 'text/html'
    }
    headers = response_with_header(header_dict)
    if request.method == 'POST':
        form = request.form()
        user = User.new(form)
        if user.validate_register():
            result = '注册成功！'
            user.save()
        else:
            result = '用户名或者密码小于等于2位'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = headers + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_login(request):
    header_dict = {
        'Content-Type': 'text/html'
    }
    if request.method == 'POST':
        form = request.form()
        user = User.new(form)
        if user.validate_login():
            result = '登陆成功！'
            # 设置session和cookie
            session_id = random_str()
            session[session_id] = user.username
            header_dict['Set-Cookie'] = 'user={}'.format(session_id)

        else:
            result = '用户名错误或密码错误！'
    else:
        result = ''
    username = current_user(request)
    body = template('login.html')
    body = body.replace('{{username}}', username)
    body = body.replace('{{result}}', result)
    headers = response_with_header(header_dict)
    r = headers + '\r\n' + body
    return r.encode(encoding='utf-8')


message_list = []
session = {}


def route_messages(request):
    header_dict = {
        'Content-Type': 'text/html'
    }
    headers = response_with_header(header_dict)
    if request.method == 'POST':
        form = request.form()
        message = Message.new(form)
        message.save()
        message_list.append(message)
    msg = '\n'.join([str(m) for m in message_list])
    body = template('html_basic.html')
    log('message', msg)
    body = body.replace('{{messages}}', msg)
    log('替代后：', body)
    r = headers + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_profile(request):
    header_dict = {
        'Content-Type': 'text/html'
    }
    headers = response_with_header(header_dict)
    body = template('profile.html')
    username = current_user(request)
    if username == '【游客】':
        header_dict['Location'] = 'http://localhost:3000/login'
        headers = response_with_header(header_dict, 302)
    else:
        user = User.find_by(username=username)
        body = body.replace('{{username}}', user.username)
        body = body.replace('{{id}}', str(user.id))
        body = body.replace('{{note}}', user.note)

    r = headers + '\r\n' + body
    return r.encode(encoding='utf-8')


route_dict = {
    '/': route_index,
    '/register': route_register,
    '/login': route_login,
    '/messages': route_messages,
    '/profile': route_profile,
}
