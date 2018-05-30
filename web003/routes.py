# coding: utf-8


def template(name):
    path = 'templates/{}'.format(name)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_static(request):
    pass


def route_index(request):
    headers = 'HTTP/1.1 200 OL\r\nConnection: close\r\nContent: text/html\r\n'
    body = template('index.html')
    r = headers + '\r\n' + body
    return r.encode('utf-8')


def route_register(request):
    pass


def route_login(request):
    pass


def route_message(request):
    pass


route_dict = {
    '/': route_index,
    '/register': route_register,
    '/login': route_login,
    '/message': route_message,
}
