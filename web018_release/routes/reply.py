from flask import (
Blueprint,
url_for,
redirect,
request,
render_template,
)

from ..models.reply import Reply
from . import current_user

main = Blueprint('reply', __name__)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    u = current_user()
    m = Reply.new(form, user_id=u.id)
    print('Debug:', m)
    return redirect(url_for('topic.detail', id=m.topic_id))
