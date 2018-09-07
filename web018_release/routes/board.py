from flask import (
    Blueprint,
    url_for,
    redirect,
    request,
    render_template,
)

from ..models.board import Board
from . import current_user

main = Blueprint('board', __name__)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    u = current_user()
    m = Board.new(form)
    return redirect(url_for('topic.detail'))


@main.route('/admin')
def index():
    return render_template('board/admin_index.html')
