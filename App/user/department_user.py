# 查看部门信息 蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from App.auth import login_required
from App.db import get_db
from App.page_utils import Pagination
from App.page_utils import page_same
bp = Blueprint('department_user', __name__)

# 展示所有部门
@bp.route('/show_user_dp', methods=('GET', 'POST'))
def show_user_dp():
    db = get_db()
    if request.method == 'POST':
        dp_name = request.form['dp_name']
        posts = db.execute(
            '''
            SELECT d.id,d.dp_name,d.dp_describe,
            (SELECT COUNT(*) FROM user u WHERE u.dp_id=d.id) AS dp_count
            FROM department d WHERE d.dp_name=?
            ''', (dp_name,)
        )
        li = page_same(posts)
        pager_obj = Pagination(request.args.get("page", 1), len(
            li), request.path, request.args, per_page_count=10)
        list = li[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()
        return render_template('user/department.html', list=list, html=html)
    else:
        posts = db.execute(
            '''
            SELECT d.id,d.dp_name,d.dp_describe,
            (SELECT COUNT(*) FROM user u WHERE u.dp_id=d.id) AS dp_count
            FROM department d
            '''
        )
        li = page_same(posts)
        pager_obj = Pagination(request.args.get("page", 1), len(
            li), request.path, request.args, per_page_count=10)
        list = li[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()
        return render_template('user/department.html', list=list, html=html)
# 展示所有同部门员工
@bp.route('/show_user_dp_same', methods=('GET', 'POST'))
def show_user_dp_same():
    db = get_db()
    # 拿到部门的名称
    d_posts=db.execute(
        '''
        SELECT dp_name FROM department WHERE id=?
        ''', (g.user['dp_id'],)
    )
    # 按条件搜索时
    if request.method == 'POST':
        search_name = request.form['search_name']
        name = '%'+request.form['name']+'%'
        # 按姓名搜索
        if search_name == '按姓名搜索':
            posts = db.execute(
                '''
                SELECT u.id,u.username,u.sex,u.email,u.tel,
                (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
                (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name
                FROM user u WHERE u.dp_id=? AND u.username LIKE ?
                ''', (g.user['dp_id'], name,)
            )
            li = page_same(posts)
            pager_obj = Pagination(request.args.get("page", 1), len(
                li), request.path, request.args, per_page_count=10)
            list = li[pager_obj.start:pager_obj.end]
            html = pager_obj.page_html()
            return render_template('user/department/show_same.html', list=list, html=html, d_posts=d_posts)
        # 按性别搜索
        elif search_name == '按姓名搜索':
            posts = db.execute(
                '''
                SELECT u.id,u.username,u.sex,u.email,u.tel,
                (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
                (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name
                FROM user u WHERE u.dp_id=? AND u.sex LIKE ?
                ''', (g.user['dp_id'], name,)
            )
            li = page_same(posts)
            pager_obj = Pagination(request.args.get("page", 1), len(
                li), request.path, request.args, per_page_count=10)
            list = li[pager_obj.start:pager_obj.end]
            html = pager_obj.page_html()
            return render_template('user/department/show_same.html', list=list, html=html, d_posts=d_posts)
        # 按职位搜索
        elif search_name == '按职位搜索':
            posts = db.execute(
                '''
                SELECT u.id,u.username,u.sex,u.email,u.tel,
                (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
                (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name
                FROM user u WHERE u.dp_id=? AND p_name LIKE ?
                ''', (g.user['dp_id'], name,)
            )
            li = page_same(posts)
            pager_obj = Pagination(request.args.get("page", 1), len(
                li), request.path, request.args, per_page_count=10)
            list = li[pager_obj.start:pager_obj.end]
            html = pager_obj.page_html()
            return render_template('user/department/show_same.html', list=list, html=html, d_posts=d_posts)
        # 按所属团队搜索
        elif search_name == '按所属团队搜索':
            posts = db.execute(
                '''
                SELECT u.id,u.username,u.sex,u.email,u.tel,
                (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
                (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name
                FROM user u WHERE u.dp_id=? AND t_name LIKE ?
                ''', (g.user['dp_id'], name,)
            )
            li = page_same(posts)
            pager_obj = Pagination(request.args.get("page", 1), len(
                li), request.path, request.args, per_page_count=10)
            list = li[pager_obj.start:pager_obj.end]
            html = pager_obj.page_html()
            return render_template('user/department/show_same.html', list=list, html=html, d_posts=d_posts)

    else:
        # 拿到同部门同事的参数
        posts=db.execute(
            '''
            SELECT u.id,u.username,u.sex,u.email,u.tel,
            (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
            (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name
            FROM user u WHERE u.dp_id=?
            ''', (g.user['dp_id'],)
        )
        li = page_same(posts)
        pager_obj = Pagination(request.args.get("page", 1), len(
            li), request.path, request.args, per_page_count=10)
        list = li[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()
        return render_template('user/department/show_same.html', list=list, html=html, d_posts=d_posts)
