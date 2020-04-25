# 请假信息管理 蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from App.auth import login_required
from App.db import get_db

bp = Blueprint('leave_user', __name__)

# 申请请假 路由
@bp.route('/create_leave', methods=('GET', 'POST'))
def create_leave():
    if request.method == 'POST':
        begin_time = request.form['begin_time']
        end_time = request.form['end_time']
        leave_time = request.form['leave_time']
        leave_name = request.form['leave_name']
        leave_describe = request.form['leave_describe']
        db = get_db()
        error = None
        if not leave_describe:
            error = '请填写请假理由！'
        if error is None:
            # 将注册值插入到数据库
            db.execute(
                'INSERT INTO leave (username, leave_name,begin_time,end_time,leave_time,leave_describe) VALUES (?,?,?,?,?,?)',
                (g.user['username'], leave_name, begin_time,
                 end_time, leave_time, leave_describe)
            )
            db.commit()
            return redirect(url_for('leave_user.level_leave'))

        flash(error)
    return render_template('user/leave/create.html')

# 请假状态 路由
@bp.route('/level_leave', methods=('GET', 'POST'))
def level_leave():
    if request.method == 'POST':
        search_name = request.form['search_name']
        name = '%'+request.form['name']+'%'
        db = get_db()
        if search_name == '按请假类型搜索':
            posts = db.execute(
                'SELECT * FROM leave WHERE leave_name LIKE ? AND username=? ORDER BY id DESC', (
                    name, g.user['username'],)
            )
            return render_template('user/leave/level.html', posts=posts)
        elif search_name == '按批复人搜索':
            posts = db.execute(
                'SELECT * FROM leave WHERE allow_name LIKE ? AND username=? ORDER BY id DESC', (
                    name, g.user['username'],)
            )
            return render_template('user/leave/level.html', posts=posts)
        elif search_name == '按批复状态搜索':
            posts = db.execute(
                'SELECT * FROM leave WHERE allow_level LIKE ? AND username=? ORDER BY id DESC', (
                    name, g.user['username'],)
            )
            return render_template('user/leave/level.html', posts=posts)
    else:
        db = get_db()
        posts = db.execute(
            'SELECT * FROM leave WHERE username=? ORDER BY id DESC', (
                g.user['username'],)
        )
        return render_template('user/leave/level.html', posts=posts)

# 根据id值拿到相应的数据


def get_post(id):
    post = get_db().execute(
        'SELECT *'
        ' FROM leave'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post 的 id值 {0} 不存在！".format(id))
    return post
