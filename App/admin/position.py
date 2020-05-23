# 职位信息管理 蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from App.auth import login_required
from App.db import get_db
from App.page_utils import Pagination
from App.admin.level_judge import judge

bp = Blueprint('position', __name__)

# 展示员工 路由
@bp.route('/show_pt', methods=('GET','POST'))
@login_required
def show_pt():
    # 判断用户权限
    judge(g.user['level'])
    db = get_db()
    if request.method == 'POST':
        pt_name=request.form['pt_name']
        posts = db.execute(
        '''
            SELECT p.id,p.pt_name,p.pt_describe,
            (SELECT COUNT(*) FROM user u WHERE u.pt_id=p.id) AS pt_count
            FROM position p WHERE p.pt_name=?
        ''',(pt_name,)
        ).fetchall()
    else:
        posts = db.execute(
            '''
            SELECT p.id,p.pt_name,p.pt_describe,
            (SELECT COUNT(*) FROM user u WHERE u.pt_id=p.id) AS pt_count
            FROM position p
            '''
        ).fetchall()
    pager_obj = Pagination(request.args.get("page", 1), len(
        posts), request.path, request.args, per_page_count=10)
    list = posts[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template('admin/position/show.html', list=list, html=html)

# 添加职位 路由
@bp.route('/create_pt', methods=('GET', 'POST'))
@login_required
def create_pt():
    # 判断用户权限
    judge(g.user['level'])
    db = get_db()
    if request.method == 'POST':
        pt_name = request.form['pt_name']
        pt_describe = request.form['pt_describe']
        # 添加职位校验
        error = None
        if db.execute(
            'SELECT id FROM position WHERE pt_name = ?', (pt_name,)
        ).fetchone() is not None:
            error = '职位{}已经被使用！'.format(pt_name)
        if error is None:
            # 将值插入到数据库
            db.execute(
                'INSERT INTO position (pt_name, pt_describe) VALUES (?, ?)',
                (pt_name,  pt_describe)
            )
            db.commit()
            return redirect(url_for('position.show_pt'))
        else:
            flash(error)
    return render_template('admin/position/create.html')

# 修改员工 路由
@bp.route('/<int:id>/update_pt', methods=('GET', 'POST'))
@login_required
def update_pt(id):
    # 判断用户权限
    judge(g.user['level'])
    # 拿到数据库中的id，pt_name,pt_describe
    post = get_post(id)
    if request.method == 'POST':
        pt_name = request.form['pt_name']
        pt_describe = request.form['pt_describe']
        db = get_db()
        # 校验
        error = None
        if db.execute(
            'SELECT id FROM position WHERE pt_name = ? AND id != ?', (pt_name,id)
        ).fetchone() is not None:
            error = '职位{}已经被使用！'.format(pt_name)
        if error is not None:
            flash(error)
        else:
            db.execute(
                'UPDATE position SET pt_name = ?, pt_describe = ?'
                ' WHERE id = ?',
                (pt_name, pt_describe,id)
            )
            db.commit()
            return redirect(url_for('position.show_pt'))
    return render_template('admin/position/update.html', post=post)

# 删除职位 蓝图
@bp.route('/<int:id>/delete_pt', methods=('POST',))
@login_required
def delete_pt(id):
    # 判断用户权限
    judge(g.user['level'])
    post=get_post(id)
    db = get_db()
    error=None
    if db.execute(
        '''
        SELECT id FROM user WHERE pt_id=?
        ''',(id,)
    ).fetchone() is not None:
        error='删除失败，仍有员工担任职位{}！'.format(post[1])
    if error is None:
        db.execute('DELETE FROM position WHERE id = ?', (id,))
        db.commit()
    else:
        flash(error)
    return redirect(url_for('position.show_pt'))


# 根据id值拿到相应的数据
def get_post(id):
    post = get_db().execute(
        'SELECT *'
        ' FROM position'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post 的 id值 {0} 不存在！".format(id))
    return post