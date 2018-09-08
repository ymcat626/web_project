from flask import (
    Blueprint,
    url_for,
    redirect,
    request,
    render_template,
    abort,
)
from ..models.topic import Topic
from . import current_user

main = Blueprint('topic', __name__)


@main.route('/')
def index():
    ms = Topic.all()
    return render_template('topic/index.html', ms=ms)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route('/new')
def new():
    u = current_user()
    if u is None:
        return redirect(url_for('index.login'))
    else:
        return render_template('topic/new.html')


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    return render_template('topic/detail.html', topic=m)


@main.route('/delete')
def delete():
    id = int(request.args.get('id'))
    # token = request.args.get('token')
    u = current_user()
    if u is None:
        abort(403)
    else:
        Topic.delete(id)
        return redirect(url_for('.index'))
