import hashlib

# 用 ascii 编码转换成 bytes 对象
pwd = 'hashdemo'.encode('ascii')
# 创建 md5 对象
m = hashlib.md5(pwd)
# 返回摘要字符串
print(m.hexdigest())

# 创建 sha1 对象
sha1 = hashlib.sha1(pwd)
print(sha1.hexdigest())
