from flask import (
Blueprint,
url_for,
redirect,
request,
render_template,
)

main = Blueprint('reply', __name__)


@main.route('/add', methods=['POST'])
def add():
    pass
