# 培训信息管理 蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from App.auth import login_required
from App.db import get_db
from App.admin.level_judge import judge

bp = Blueprint('train', __name__)

# 查看培训信息 路由
@bp.route('/show_train', methods=('GET', 'POST'))
@login_required
def show_train():
    # 判断用户权限
    judge(g.user['level'])
    db = get_db()
    if request.method == 'POST':
        train_title = request.form['train_title']
        posts = db.execute(
            '''
            SELECT t.id,train_title,train_time,username
            FROM train t user u WHERE author_id=u.id AND t.train_title=?
        ''', (train_title,)
        )
        return render_template('admin/train/show.html', posts=posts)
    else:
        posts = db.execute(
            '''
            SELECT t.id,train_title,train_time,create_time,
            (SELECT COUNT(*) FROM user u WHERE join_id=u.id) AS count_join,
            (SELECT username FROM user u WHERE author_id=u.id) AS author           
            FROM train t
            '''
        )
        return render_template('admin/train/show.html', posts=posts)

# 添加培训 路由
@bp.route('/create_train', methods=('GET', 'POST'))
@login_required
def create_train():
    # 判断用户权限
    judge(g.user['level'])
    if request.method == 'POST':
        train_title = request.form['train_title']
        train_body = request.form['train_body']
        train_begin_time = request.form['train_begin_time']
        train_end_time = request.form['train_end_time']
        train_time = request.form['train_time']
        author_id = g.user['id']

        db = get_db()
        # 添加职位校验
        error = None
        if not train_title:
            error = '请填写培训名称.'
        elif db.execute(
            'SELECT id FROM train WHERE train_title = ?', (train_title,)
        ).fetchone() is not None:
            error = '培训名称： {} 已经被使用。'.format(train_title)

        if error is None:
            # 将值插入到数据库
            db.execute(
                '''
                INSERT INTO train (train_title, train_body,train_begin_time,train_end_time,train_time,author_id) VALUES (?,?,?,?,?,?)
                ''', (train_title,  train_body, train_begin_time, train_end_time, train_time, author_id)
            )
            db.commit()
            return redirect(url_for('train.show_train'))
        flash(error)
    return render_template('admin/train/create.html')


