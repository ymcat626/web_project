import os

from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    request,
    session,
    send_from_directory,
)
from . import current_user
from ..models.user import User
from ..config import user_file_director
from werkzeug.utils import secure_filename


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


@main.route('/profile/')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


def allow_file(filename):
    suffix = filename.split('.')[-1]
    from ..config import accept_user_file_type
    return suffix in accept_user_file_type


@main.route('/addimg', methods=['POST'])
def add_img():
    u = current_user()
    print('debug:', request.url)
    if u is None:
        return redirect(url_for('.profile'))

    if 'file' not in request.files:
        return redirect(url_for(request.url))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for(request.url))

    if allow_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(user_file_director, filename))
        u.user_image = filename
        u.save()

    return redirect(url_for('.profile'))


@main.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(user_file_director, filename)
