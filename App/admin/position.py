# 职位信息管理 蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from App.auth import login_required
from App.db import get_db
from App.page_utils import Pagination

bp = Blueprint('position', __name__)

# 展示员工 路由
@bp.route('/show_pt', methods=('GET','POST'))
def show_pt():
    if request.method == 'POST':
        pt_name=request.form['pt_name']
        db = get_db()
        posts = db.execute(
        '''
            SELECT p.id,p.pt_name,p.pt_describe,
            (SELECT COUNT(*) FROM user u WHERE u.pt_id=p.id) AS pt_count
            FROM position p WHERE p.pt_name=?
        ''',(pt_name,)
        )
        li = []
        for post in posts:
            li.append(post)
        pager_obj = Pagination(request.args.get("page", 1), len(
            li), request.path, request.args, per_page_count=10)
        list = li[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()
        return render_template('admin/position/show.html', list=list, html=html)
    else:
        db = get_db()
        posts = db.execute(
            '''
            SELECT p.id,p.pt_name,p.pt_describe,
            (SELECT COUNT(*) FROM user u WHERE u.pt_id=p.id) AS pt_count
            FROM position p
            '''
        )
        li = []
        for post in posts:
            li.append(post)
        pager_obj = Pagination(request.args.get("page", 1), len(
            li), request.path, request.args, per_page_count=10)
        list = li[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()
        return render_template('admin/position/show.html', list=list, html=html)

# 添加职位 路由
@bp.route('/create_pt', methods=('GET', 'POST'))
def create_pt():
    if request.method == 'POST':
        pt_name = request.form['pt_name']
        pt_describe = request.form['pt_describe']
        db = get_db()
        # 添加职位校验
        error = None
        if not pt_name:
            error = '请填写职位名称.'
        elif db.execute(
            'SELECT id FROM position WHERE pt_name = ?', (pt_name,)
        ).fetchone() is not None:
            error = '职位名称： {} 已经被注册。'.format(pt_name)

        if error is None:
            # 将值插入到数据库
            db.execute(
                'INSERT INTO position (pt_name, pt_describe) VALUES (?, ?)',
                (pt_name,  pt_describe)
            )
            db.commit()
            return redirect(url_for('position.show_pt'))
        flash(error)
    return render_template('admin/position/create.html')

# 修改员工 路由
@bp.route('/<int:id>/update_pt', methods=('GET', 'POST'))
@login_required
def update_pt(id):
    # 拿到数据库中的id，pt_name,pt_describe
    post = get_post(id)
    if request.method == 'POST':
        pt_name = request.form['pt_name']
        pt_describe = request.form['pt_describe']
        db = get_db()
        # 校验
        error = None
        if not pt_name:
            error = '请填写职位名称。'
        elif db.execute(
            'SELECT id FROM position WHERE pt_name = ? AND id != ?', (pt_name,id)
        ).fetchone() is not None:
            error = '职位 {} 已经被注册.'.format(pt_name)
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
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM position WHERE id = ?', (id,))
    db.commit()
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