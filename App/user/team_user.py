# 查看团队信息 蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from App.auth import login_required
from App.db import get_db
from App.page_utils import Pagination
from App.page_utils import page_same
bp = Blueprint('team_user', __name__)


# 展示所有团队
@bp.route('/show_user_team', methods=('GET', 'POST'))
def show_user_team():
    db = get_db()
    if request.method == 'POST':
        team_name = request.form['team_name']
        posts = db.execute(
            '''
            SELECT t.id,t.team_name,t.team_describe,
            (SELECT COUNT(*) FROM user u WHERE u.team_id=t.id) AS team_count
            FROM team t WHERE t.team_name=?
            ''', (team_name,)
        ).fetchall()
    else:
        posts = db.execute(
            '''
            SELECT t.id,t.team_name,t.team_describe,
            (SELECT COUNT(*) FROM user u WHERE u.team_id=t.id) AS team_count
            FROM team t
            '''
        ).fetchall()
    pager_obj = Pagination(request.args.get("page", 1), len(
        posts), request.path, request.args, per_page_count=10)
    list = posts[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template('user/team.html', list=list, html=html)
# 展示所有同团队员工
@bp.route('/show_user_team_same', methods=('GET', 'POST'))
def show_user_team_same():
    db = get_db()
    # 拿到部门的名称
    d_posts = db.execute(
        '''
        SELECT dp_name FROM department WHERE id=?
        ''', (g.user['dp_id'],)
    )
    # 拿到团队的名称
    t_posts = db.execute(
        '''
        SELECT team_name FROM team WHERE id=?
        ''', (g.user['team_id'],)
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
                (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name
                FROM user u WHERE u.dp_id=? AND u.username LIKE ?
                ''', (g.user['dp_id'], name,)
            ).fetchall()
        # 按性别搜索
        elif search_name == '按性别搜索':
            posts = db.execute(
                '''
                SELECT u.id,u.username,u.sex,u.email,u.tel,
                (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name
                FROM user u WHERE u.dp_id=? AND u.sex LIKE ?
                ''', (g.user['dp_id'], name,)
            ).fetchall()
        # 按职位搜索
        elif search_name == '按职位搜索':
            posts = db.execute(
                '''
                SELECT u.id,u.username,u.sex,u.email,u.tel,
                (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name
                FROM user u WHERE u.dp_id=? AND p_name LIKE ?
                ''', (g.user['dp_id'], name,)
            ).fetchall()
    else:
        # 拿到同团队同事的参数
        posts = db.execute(
            '''
            SELECT u.id,u.username,u.sex,u.email,u.tel,
            (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name
            FROM user u WHERE u.dp_id=?
            ''', (g.user['dp_id'],)
        ).fetchall()
    pager_obj = Pagination(request.args.get("page", 1), len(
        posts), request.path, request.args, per_page_count=10)
    list = posts[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template('user/team/show_same.html', list=list, html=html, d_posts=d_posts, t_posts=t_posts)
