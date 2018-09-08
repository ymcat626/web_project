import uuid

from flask import (
    Blueprint,
    url_for,
    redirect,
    request,
    render_template,
    abort,
)
from ..models.topic import Topic
from ..models.board import Board
from . import current_user

main = Blueprint('topic', __name__)
csrf_token = dict()


@main.route('/')
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.find_all(board_id=board_id)
    bs = Board.all()
    # print('ms', ms)
    token = str(uuid.uuid4())
    u = current_user()
    csrf_token[token] = u.id
    return render_template('topic/index.html', ms=ms, bs=bs, token=token)


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
        bs = Board.all()
        return render_template('topic/new.html', bs=bs)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    return render_template('topic/detail.html', topic=m)


@main.route('/delete')
def delete():
    id = int(request.args.get('id'))
    token = request.args.get('token')
    u = current_user()
    if token in csrf_token and csrf_token[token] == u.id:
        csrf_token.pop(token)
        if u is not None:
            Topic.delete(id)
            return redirect(url_for('.index'))
        else:
            abort(404)
    else:
        abort(403)
