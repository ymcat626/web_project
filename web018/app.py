from flask import Flask
from web018.config import secret_key


# __main__
app = Flask(__name__)
# 设置 secret_key
app.secret_key = secret_key


from web018.routes.index import main as index_routes
from web018.routes.topic import main as topic_routes
from web018.routes.reply import main as reply_routes
app.register_blueprint(index_routes)
app.register_blueprint(topic_routes, url_prefix='/topic')
app.register_blueprint(reply_routes, url_prefix='/reply')


if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port='2000',
    )
    app.run(**config)