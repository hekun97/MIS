# 培训信息管理 蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from App.auth import login_required
from App.db import get_db

bp = Blueprint('train', __name__)

# 查看培训信息 路由
@bp.route('/show_train', methods=('GET', 'POST'))
def show_train():
    if request.method == 'POST':
        train_title = request.form['train_title']
        db = get_db()
        posts = db.execute(
            '''
            SELECT t.id,t.train_title,t.create_time,
            (SELECT username FROM user u2 WHERE t.author_id=u2.id) AS train_author,
            (SELECT COUNT(*) FROM user u WHERE t.join_id=u.id) AS train_count
            FROM train t WHERE t.train_title=?
        ''', (train_title,)
        )
        return render_template('admin/train/show.html', posts=posts)
    else:
        db = get_db()
        posts = db.execute(
            '''
            SELECT t.id,t.train_title,t.create_time,
            (SELECT username FROM user u2 WHERE t.author_id=u2.id) AS train_author,
            (SELECT COUNT(*) FROM user u WHERE t.join_id=u.id) AS train_count
            FROM train t
            '''
        )
        return render_template('admin/train/show.html', posts=posts)

# 添加职位 路由
@bp.route('/create_train', methods=('GET', 'POST'))
def create_train():
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
                INSERT INTO train (train_title, train_body,train_begin_time,train_end_time,train_time,author_id,create_time) VALUES (?,?,?,?,?,?,date("now"))
                ''', (train_title,  train_body, train_begin_time, train_end_time, train_time, author_id)
            )
            db.commit()
            return redirect(url_for('train.show_train'))
        flash(error)
    return render_template('admin/train/create.html')


