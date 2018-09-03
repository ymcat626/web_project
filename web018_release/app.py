from flask import Flask
from web018_release.config import secret_key


app = Flask(__name__)
app.secret_key = secret_key


from web018_release.routes.index import  main as index_routes

app.register_blueprint(index_routes)

if __name__ == '__main__':
    config = dict(
        debug=True,
        port=2000,
        host='0.0.0.0',
    )
    app.run(**config)
