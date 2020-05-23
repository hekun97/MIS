# 部门信息管理 蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from App.auth import login_required
from App.db import get_db
from App.page_utils import Pagination
from App.admin.level_judge import judge

bp = Blueprint('department', __name__)

# 展示部门 路由
@bp.route('/show_dp', methods=('GET','POST'))
@login_required
def show_dp():
    # 判断用户权限
    judge(g.user['level'])
    if request.method == 'POST':
        dp_name="%"+request.form['dp_name']+"%"
        db = get_db()
        posts = db.execute(
            # 使用count()函数计算人数
            '''
            SELECT d.id,d.dp_name,d.dp_describe,
            (SELECT COUNT(*) FROM user u WHERE u.dp_id=d.id) AS dp_count
            FROM department d WHERE dp_name LIKE ?
            ''',(dp_name,)
        ).fetchall()
    else:
        db = get_db()
        posts = db.execute(
            # 使用count()函数计算人数
            '''
            SELECT d.id,d.dp_name,d.dp_describe,
            (SELECT COUNT(*) FROM user u WHERE u.dp_id=d.id) AS dp_count
            FROM department d
            '''
        ).fetchall()
    pager_obj = Pagination(request.args.get("page", 1), len(
        posts), request.path, request.args, per_page_count=10)
    list = posts[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template('admin/department/show.html', list=list, html=html)

# 添加部门 路由
@bp.route('/create_dp', methods=('GET', 'POST'))
@login_required
def create_dp():
    # 判断用户权限
    judge(g.user['level'])
    if request.method == 'POST':
        dp_name = request.form['dp_name']
        dp_describe = request.form['dp_describe']
        db = get_db()
        # 添加部门校验
        error = None
        if db.execute(
            'SELECT id FROM department WHERE dp_name = ?', (dp_name,)
        ).fetchone() is not None:
            error = '部门名称{}已经被使用！'.format(dp_name)
        if error is None:
            # 将值插入到数据库
            db.execute(
                'INSERT INTO department (dp_name, dp_describe) VALUES (?, ?)',
                (dp_name,  dp_describe)
            )
            db.commit()
            return redirect(url_for('department.show_dp'))
        else:
            flash(error)
    return render_template('admin/department/create.html')

# 修改部门 路由
@bp.route('/<int:id>/update_dp', methods=('GET', 'POST'))
@login_required
def update_dp(id):
    # 判断用户权限
    judge(g.user['level'])
    # 拿到数据库中的值
    post = get_post(id)
    if request.method == 'POST':
        dp_name = request.form['dp_name']
        dp_describe = request.form['dp_describe']
        db = get_db()
        # 校验
        error = None
        if db.execute(
            'SELECT id FROM department WHERE dp_name = ? AND id != ?', (dp_name,id)
        ).fetchone() is not None:
            error = '部门名称{}已经被使用！'.format(dp_name)
        if error is not None:
            flash(error)
        else:
            db.execute(
                'UPDATE department SET dp_name = ?, dp_describe = ?'
                ' WHERE id = ?',
                (dp_name, dp_describe,id)
            )
            db.commit()
            return redirect(url_for('department.show_dp'))

    return render_template('admin/department/update.html', post=post)

# 删除部门 蓝图
@bp.route('/<int:id>/delete_dp', methods=('POST',))
@login_required
def delete_dp(id):
    # 判断用户权限
    judge(g.user['level'])
    post=get_post(id)
    db = get_db()
    error=None
    if db.execute(
        '''
        SELECT id FROM user WHERE dp_id=?
        ''',(id,)
    ).fetchone() is not None:
        error='删除失败，仍有员工在{}中！'.format(post[1])
    if error is None:
        db.execute('DELETE FROM department WHERE id = ?', (id,))
        db.commit()
    else:
        flash(error)
    return redirect(url_for('department.show_dp'))


# 根据id值拿到相应的数据
def get_post(id):
    post = get_db().execute(
        'SELECT *'
        ' FROM department'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post 的 id值{0}不存在！".format(id))
    return post