# 请假信息管理 蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from App.auth import login_required
from App.db import get_db
from App.page_utils import Pagination
bp = Blueprint('leave', __name__)

# 已批准请假 路由
@bp.route('/allow', methods=('GET', 'POST'))
def allow():
    db = get_db()
    if request.method == 'POST':
        search_name=request.form['search_name']
        name = '%'+request.form['name']+'%'
        # 按员工姓名搜索
        if search_name=='按员工姓名搜索':
            posts = db.execute(
                '''
                SELECT * FROM leave WHERE username LIKE ? AND allow_level!="未批复"
                ''', (name,)
            ).fetchall()
        # 按请假类型搜索
        elif search_name=='按请假类型搜索':
            posts = db.execute(
                '''
                SELECT * FROM leave WHERE leave_name LIKE ? AND allow_level!="未批复"
                ''', (name,)
            ).fetchall()
        # 按批复人搜索
        elif search_name=='按批复人搜索':
            posts = db.execute(
                '''
                SELECT * FROM leave WHERE allow_name LIKE ? AND allow_level!="未批复"
                ''', (name,)
            ).fetchall()
        # 按批复状态搜索
        elif search_name=='按批复状态搜索':
            posts = db.execute(
                '''
                SELECT * FROM leave WHERE allow_level LIKE ? AND allow_level!="未批复"
                ''', (name,)
            ).fetchall()
    # 默认状态
    else:
        posts = db.execute(
            'SELECT * FROM leave WHERE allow_level!="未批复"'
        ).fetchall()
    # 分页
    pager_obj = Pagination(request.args.get("page", 1), len(
        posts), request.path, request.args, per_page_count=10)
    posts = posts[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template('admin/leave/allow.html', posts=posts, html=html)

# 未批准请假 路由
@bp.route('/not_allow', methods=('GET', 'POST'))
def not_allow():
    if request.method == 'POST':
        search_name=request.form['search_name']
        name = '%'+request.form['name']+'%'
        db = get_db()
        # 按员工姓名搜索
        if search_name=='按员工姓名搜索':
            posts = db.execute(
                'SELECT * FROM leave WHERE username LIKE ? AND allow_level="未批复"', (
                    name,)
            ).fetchall()
        # 按请假类型搜索
        elif search_name=='按请假类型搜索':
            posts = db.execute(
                'SELECT * FROM leave WHERE leave_name LIKE ? AND allow_level="未批复"', (
                    name,)
            ).fetchall()
    else:
        db = get_db()
        posts = db.execute(
            'SELECT * FROM leave WHERE allow_level="未批复"'
        ).fetchall()
    # 分页
    pager_obj = Pagination(request.args.get("page", 1), len(
        posts), request.path, request.args, per_page_count=10)
    posts = posts[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template('admin/leave/not_allow.html',  posts=posts, html=html)


# 请假操作 路由
@bp.route('/<int:id>/not_allow_describe', methods=('GET', 'POST'))
@login_required
def not_allow_describe(id):
    post = get_post(id)
    if request.method == 'POST':
        allow_name = g.user['username']
        allow_level = request.form['allow_level']
        not_allow_describe = request.form['not_allow_describe']
        db = get_db()
        # 将值插入到数据库
        db.execute(
            'UPDATE leave SET allow_name = ?, allow_level = ?,not_allow_describe=?'
            ' WHERE id = ?',
            (allow_name, allow_level, not_allow_describe, id)
        )
        db.commit()
        return redirect(url_for('leave.not_allow'))
    return render_template('admin/leave/level.html')


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
