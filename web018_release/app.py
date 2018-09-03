from flask import Flask
from web018_release.config import secret_key


app = Flask(__name__)
app.secret_key = secret_key


from web018_release.routes.index import  main as index_routes
from web018_release.routes.topic import  main as topic_routes
from web018_release.routes.reply import  main as reply_routes

app.register_blueprint(index_routes)
app.register_blueprint(topic_routes, url_prefix='/topic')
app.register_blueprint(reply_routes, url_prefix='/reply')

if __name__ == '__main__':
    config = dict(
        debug=True,
        port=2000,
        host='0.0.0.0',
    )
    app.run(**config)
