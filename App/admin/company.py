# 部门信息管理 蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from App.auth import login_required
from App.db import get_db

bp = Blueprint('company', __name__)

# 展示主页信息 路由
@bp.route('/home', methods=('GET','POST'))
def home():
    db = get_db()
    posts = db.execute(
        # 使用count()函数计算人数
        '''
        SELECT * FROM company WHERE cp_level='首页信息'
        '''
    )
    return render_template('admin/home/show.html', posts=posts)

# 修改主页信息 路由
@bp.route('/<int:id>/update_home', methods=('GET', 'POST'))
@login_required
def update_home(id):
    # 拿到数据库中的值
    post = get_post(id)
    if request.method == 'POST':
        cp_title = request.form['cp_title']
        cp_body = request.form['cp_body']
        db = get_db()
        # 校验
        error = None
        if not cp_title:
            error = '请填写主页信息名称。'
        elif db.execute(
            'SELECT id FROM company WHERE cp_title = ? AND id != ?', (cp_title,id)
        ).fetchone() is not None:
            error = '主页信息名称 {} 已经被使用.'.format(cp_title)
        if error is not None:
            flash(error)
        else:
            db.execute(
                'UPDATE company SET cp_title = ?, cp_body = ?'
                ' WHERE id = ?',
                (cp_title, cp_body,id)
            )
            db.commit()
            return redirect(url_for('company.home'))
    return render_template('admin/home/update.html', post=post)

# 展示更多信息 路由
@bp.route('/show_more', methods=('GET','POST'))
def show_more():
    db = get_db()
    posts = db.execute(
        # 使用count()函数计算人数
        '''
        SELECT * FROM company WHERE cp_level='更多信息'
        '''
    )
    return render_template('admin/home/show_more.html', posts=posts)

# 修改更多信息 路由
@bp.route('/<int:id>/update_more', methods=('GET', 'POST'))
@login_required
def update_more(id):
    # 拿到数据库中的值
    post = get_post(id)
    if request.method == 'POST':
        cp_title = request.form['cp_title']
        cp_body = request.form['cp_body']
        db = get_db()
        # 校验
        error = None
        if not cp_title:
            error = '请填写更多信息名称。'
        elif db.execute(
            'SELECT id FROM company WHERE cp_title = ? AND id != ?', (cp_title,id)
        ).fetchone() is not None:
            error = '更多信息名称 {} 已经被使用.'.format(cp_title)
        if error is not None:
            flash(error)
        else:
            db.execute(
                'UPDATE company SET cp_title = ?, cp_body = ?'
                ' WHERE id = ?',
                (cp_title, cp_body,id)
            )
            db.commit()
            return redirect(url_for('company.show_more'))
    return render_template('admin/home/update_more.html', post=post)


# 根据id值拿到相应的数据
def get_post(id):
    post = get_db().execute(
        'SELECT *'
        ' FROM company'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post 的 id值 {0} 不存在！".format(id))
    return post