# encoding utf-8

import socket

# 构建socket实例
host = 'g.cn'
port = 80

# 也可以写成s = socket.socket()
# https 的 socket 连接需要 import ssl
# 并且使用 s = ssl.wrap_socket(socket.socket()) 来初始化
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 构建连接
s.connect((host, port))

# 返回的是本机的ip和端口号
ip, port = s.getsockname()

# 构建request请求
http_request = 'GET / HTTP/1.1\r\nhost:{}\r\n\r\n'.format(host)
request = http_request.encode('utf-8')
print(request)

# 发送请求
s.send(request)

# 得到响应，并解码
response = s.recv(1024)
print(response.decode('utf-8'))
