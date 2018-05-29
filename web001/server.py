import socket

host = ''
port = 2000
s = socket.socket()

# 绑定主机和端口
s.bind((host, port))

while True:
    # 监听
    s.listen(5)

    # 接受请求
    connection, address = s.accept()
    request = connection.recv(1024)
    print(request.decode())

    # 发送响应
    response = b'haha123'
    connection.sendall(response)
    connection.close()
