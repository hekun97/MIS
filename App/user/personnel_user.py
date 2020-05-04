# 员工信息管理 蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from App.auth import login_required
from App.db import get_db
from App.page_utils import Pagination
from App.page_utils import page_same
bp = Blueprint('personnel_user', __name__)

# 展示当前员工 路由
@bp.route('/show_user', methods=('GET', 'POST'))
def show_user():
    db = get_db()
    posts = db.execute(
        '''
            SELECT u.id,u.username,u.password,u.sex,u.email,u.tel,u.level,u.money,u.birthday,u.work_begin_day,
            (strftime('%Y', 'now') - strftime('%Y', birthday)) - (strftime('%m-%d', 'now') < strftime('%m-%d', birthday)) AS age,
            (strftime('%Y', 'now') - strftime('%Y', work_begin_day)) - (strftime('%m-%d', 'now') < strftime('%m-%d', work_begin_day)) AS work_age,
            (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
            (SELECT d.dp_name FROM department d WHERE u.dp_id = d.id) AS d_name,
            (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name          
            FROM user u WHERE u.username =?
        ''', (g.user['username'],)
    )
    return render_template('user/personnel/show.html', posts=posts)

# 修改当前员工 路由
@bp.route('/<int:id>/update_user', methods=('GET', 'POST'))
@login_required
def update(id):
    # 拿到数据库中的id，username,level
    db = get_db()
    post = get_post(id)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sex = request.form['sex']
        birthday = request.form['birthday']
        email = request.form['email']
        tel = request.form['tel']
        # 校验
        error = None
        if not username:
            error = '请填写用户名.'
        elif not password:
            error = '请填写密码.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ? AND id != ?', (
                username, id)
        ).fetchone() is not None:
            error = '用户名 {} 已经被注册.'.format(username)
        if error is not None:
            flash(error)
        else:
            db.execute(
                'UPDATE user SET username = ?, password = ?,sex=?,birthday=?,email=?,tel=?'
                ' WHERE id = ?',
                (username, password, sex, birthday, email, tel, id)
            )
            db.commit()
            return redirect(url_for('personnel_user.show_user'))

    return render_template('user/personnel/update.html', post=post)

# 展示所有员工
@bp.route('/show_all', methods=('GET', 'POST'))
def show_all():
    if request.method == 'POST':
        search_name = request.form['search_name']
        name = '%'+request.form['name']+'%'
        db = get_db()
        if search_name == '按姓名搜索':
            posts = db.execute(
                '''
                SELECT u.id,u.username,u.sex,u.email,u.tel,
                (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
                (SELECT d.dp_name FROM department d WHERE u.dp_id = d.id) AS d_name,
                (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name          
                FROM user u WHERE u.username LIKE ?
                ''', (name,)
            )
            li = page_same(posts)
            pager_obj = Pagination(request.args.get("page", 1), len(
                li), request.path, request.args, per_page_count=10)
            list = li[pager_obj.start:pager_obj.end]
            html = pager_obj.page_html()
            return render_template('user/personnel/show_all.html', list=list, html=html)
        elif search_name == '按性别搜索':
            posts = db.execute(
                '''
                SELECT u.id,u.username,u.sex,u.email,u.tel,
                (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
                (SELECT d.dp_name FROM department d WHERE u.dp_id = d.id) AS d_name,
                (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name          
                FROM user u WHERE u.sex LIKE ?
                ''', (name,)
            )
            li = page_same(posts)
            pager_obj = Pagination(request.args.get("page", 1), len(
                li), request.path, request.args, per_page_count=10)
            list = li[pager_obj.start:pager_obj.end]
            html = pager_obj.page_html()
            return render_template('user/personnel/show_all.html', list=list, html=html)
        elif search_name == '按职位搜索':
            posts = db.execute(
                '''
                SELECT u.id,u.username,u.sex,u.email,u.tel,
                (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
                (SELECT d.dp_name FROM department d WHERE u.dp_id = d.id) AS d_name,
                (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name          
                FROM user u WHERE p_name LIKE ?
                ''', (name,)
            )
            li = page_same(posts)
            pager_obj = Pagination(request.args.get("page", 1), len(
                li), request.path, request.args, per_page_count=10)
            list = li[pager_obj.start:pager_obj.end]
            html = pager_obj.page_html()
            return render_template('user/personnel/show_all.html', list=list, html=html)
        elif search_name == '按所属团队搜索':
            posts = db.execute(
                '''
                SELECT u.id,u.username,u.sex,u.email,u.tel,
                (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
                (SELECT d.dp_name FROM department d WHERE u.dp_id = d.id) AS d_name,
                (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name          
                FROM user u WHERE t_name LIKE ?
                ''', (name,)
            )
            li = page_same(posts)
            pager_obj = Pagination(request.args.get("page", 1), len(
                li), request.path, request.args, per_page_count=10)
            list = li[pager_obj.start:pager_obj.end]
            html = pager_obj.page_html()
            return render_template('user/personnel/show_all.html', list=list, html=html)
        elif search_name == '按所属部门搜索':
            posts = db.execute(
                '''
                SELECT u.id,u.username,u.sex,u.email,u.tel,
                (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
                (SELECT d.dp_name FROM department d WHERE u.dp_id = d.id) AS d_name,
                (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name          
                FROM user u WHERE d_name LIKE ?
                ''', (name,)
            )
            li = page_same(posts)
            pager_obj = Pagination(request.args.get("page", 1), len(
                li), request.path, request.args, per_page_count=10)
            list = li[pager_obj.start:pager_obj.end]
            html = pager_obj.page_html()
            return render_template('user/personnel/show_all.html', list=list, html=html)
    else:
        db = get_db()
        posts = db.execute(
            '''
            SELECT u.id,u.username,u.sex,u.email,u.tel,
            (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
            (SELECT d.dp_name FROM department d WHERE u.dp_id = d.id) AS d_name,
            (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name          
            FROM user u
            '''
        )
        li = page_same(posts)
        pager_obj = Pagination(request.args.get("page", 1), len(
            li), request.path, request.args, per_page_count=10)
        list = li[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()
        return render_template('user/personnel/show_all.html', list=list, html=html)

# 根据id值拿到相应的数据
def get_post(id):
    post = get_db().execute(
        'SELECT *'
        ' FROM user'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    return post
