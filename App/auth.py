import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from App.db import get_db

# 蓝图
bp = Blueprint('auth', __name__)
# 登录路由
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        # 拿到登录表单中的值
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        # 登录校验
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        if user is None:
            error = '用户名有误。'
        elif not check_password_hash(user['password'], password):
            error = '密码有误。'
        if error is None:
            session.clear()
            session['user_id'] = user['id']            
            if db.execute(
                    'SELECT id FROM user WHERE username = ? AND level = "管理员"', (username,)).fetchone() is not None:
                return redirect(url_for('system.index'))
            else:
                return redirect(url_for('system.user'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# 登出
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('system.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
