from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    request,
    session)
from . import current_user
from ..models.user import User

main = Blueprint('index', __name__)


@main.route('/')
def index():
    u = current_user()
    return render_template('index.html', user=u)


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.index'))
    else:
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)
