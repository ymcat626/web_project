from flask import (
    Blueprint,
    url_for,
    redirect,
    request,
render_template

)
from ..models.topic import Topic
from . import current_user

main = Blueprint('topic', __name__)


@main.route('/')
def index():
    ms = Topic.all()
    return render_template('topic/login.html', ms=ms)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail'), id=m.id)