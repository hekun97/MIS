# 团队信息管理 蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from App.auth import login_required
from App.db import get_db
from App.page_utils import Pagination
from App.admin.level_judge import judge
bp = Blueprint('team', __name__)

# 展示员工 路由
@bp.route('/show_team', methods=('GET','POST'))
@login_required
def show_team():
    # 判断用户权限
    judge(g.user['level'])
    if request.method == 'POST':
        team_name=request.form['team_name']
        db = get_db()
        posts = db.execute(
            '''
            SELECT t.id,t.team_name,t.team_describe,
            (SELECT COUNT(*) FROM user u WHERE u.team_id=t.id) AS team_count
            FROM team t WHERE team_name=?
            ''',(team_name,)
        )
        li = []
        for post in posts:
            li.append(post)
        pager_obj = Pagination(request.args.get("page", 1), len(
            li), request.path, request.args, per_page_count=10)
        list = li[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()
        return render_template('admin/team/show.html', list=list, html=html)
    else:
        db = get_db()
        posts = db.execute(
            '''
            SELECT t.id,t.team_name,t.team_describe,
            (SELECT COUNT(*) FROM user u WHERE u.team_id=t.id) AS team_count
            FROM team t
            '''
        )
        li = []
        for post in posts:
            li.append(post)
        pager_obj = Pagination(request.args.get("page", 1), len(
            li), request.path, request.args, per_page_count=10)
        list = li[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()
        return render_template('admin/team/show.html', list=list, html=html)

# 添加团队 路由
@bp.route('/create_team', methods=('GET', 'POST'))
@login_required
def create_team():
    # 判断用户权限
    judge(g.user['level'])
    if request.method == 'POST':
        team_name = request.form['team_name']
        team_describe = request.form['team_describe']
        db = get_db()
        # 添加团队校验
        error = None
        if not team_name:
            error = '请填写团队名称.'
        elif db.execute(
            'SELECT id FROM team WHERE team_name = ?', (team_name,)
        ).fetchone() is not None:
            error = '团队名称： {} 已经被注册。'.format(team_name)

        if error is None:
            # 将值插入到数据库
            db.execute(
                'INSERT INTO team (team_name, team_describe) VALUES (?, ?)',
                (team_name,  team_describe)
            )
            db.commit()
            return redirect(url_for('team.show_team'))
        flash(error)
    return render_template('admin/team/create.html')

# 修改员工 路由
@bp.route('/<int:id>/update_team', methods=('GET', 'POST'))
@login_required
def update_team(id):
    # 判断用户权限
    judge(g.user['level'])
    # 拿到数据库中的id，team_name,team_describe
    post = get_post(id)
    if request.method == 'POST':
        team_name = request.form['team_name']
        team_describe = request.form['team_describe']
        db = get_db()
        # 校验
        error = None
        if not team_name:
            error = '请填写团队名称。'
        elif db.execute(
            'SELECT id FROM team WHERE team_name = ? AND id != ?', (team_name,id)
        ).fetchone() is not None:
            error = '用户名 {} 已经被注册.'.format(team_name)
        if error is not None:
            flash(error)
        else:
            db.execute(
                'UPDATE team SET team_name = ?, team_describe = ?'
                ' WHERE id = ?',
                (team_name, team_describe,id)
            )
            db.commit()
            return redirect(url_for('team.show_team'))

    return render_template('admin/team/update.html', post=post)

# 删除团队 蓝图
@bp.route('/<int:id>/delete_team', methods=('POST',))
@login_required
def delete_team(id):
    # 判断用户权限
    judge(g.user['level'])
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM team WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('team.show_team'))


# 根据id值拿到相应的数据
def get_post(id):
    post = get_db().execute(
        'SELECT *'
        ' FROM team'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post 的 id值 {0} 不存在！".format(id))
    return post