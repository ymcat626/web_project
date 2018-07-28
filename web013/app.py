# coding; utf-8
from flask import (
    Flask,
)
from web013.routes.todo import main as todo_routes

app = Flask(__name__)
# 设置 secret_key 来使用 flask 自带的 session
app.secret_key = 'akfjakgfadjf'
# 注册蓝图
app.register_blueprint(todo_routes, url_prefix='/todo')

if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )
    app.run(**config)


