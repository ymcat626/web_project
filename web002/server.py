# coding: utf-8
import socket


def log(*args, **kwargs):
    print('log', *args, **kwargs)


def route_index():
    # headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n '
    # 就因为headers里多余一个空格，页面会显示空白
    headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<h1>hello world</h1><img src="doge.gif"/>'
    r = headers + '\r\n' + body
    return r.encode('utf-8')


def route_image():
    with open('doge.gif', 'rb') as f:
        headers = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        r = headers + b'\r\n' + f.read()
        return r


def error(code=404):
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>'
    }
    return e.get(code, b'')


def response_for_path(path):
    response_dict = {
        '/': route_index,
        '/doge.gif': route_image,
    }
    response = response_dict.get(path, error)
    return response()


def run(host='', port=3000):
    # 用with可以在发生错误的时候，自动关闭socket连接，释放端口
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connect, addr = s.accept()
            request = connect.recv(1024).decode('utf-8')
            log('ip and request:{}\n{}'.format(addr, request))

            # 因为 chrome 会发送空请求导致 split 得到空 list
            # 所以这里用 try 防止程序崩溃
            try:
                # 对request分割后，第二个即是path
                path = request.split()[1]
                response = response_for_path(path)
                connect.sendall(response)
            except Exception as e:
                log('error', e)
            connect.close()


if __name__ == '__main__':
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
