# coding: utf-8
import time

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
)

# 先要初始化一个 Flask 的实例
app = Flask(__name__)

# message_list 用来存储所有的 message
message_list = []


def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(time.time())
    dt = time.strftime(format, value)

    # 保存日志到log.txt
    with open('log.txt', 'w', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


@app.route('/', methods=['GET'])
def hello_world():
    return 'hello, world'


@app.route('/message')
def message_view():
    log('请求方法', request.method)
    log('request, query 参数', request.args)
    return render_template('message_index.html', messages=message_list)


@app.route('/message/add', methods=['POST'])
def message_add():
    log('message_add 请求方法：', request.method)
    log('request, POST 的 form 的表单数据：', request.form)
    msg = {
        'content': request.form.get('msg_post', '')
    }
    message_list.append(msg)
    # return redirect('/message')
    return redirect(url_for('message_view'))


# 运行服务器
if __name__ == '__main__':
    config = dict(
        host='0.0.0.0',
        port='2000',
        debug=True,
    )
    app.run(**config)
