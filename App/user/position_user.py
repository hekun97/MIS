# 查看部门信息 蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from App.auth import login_required
from App.db import get_db
from App.page_utils import Pagination

bp = Blueprint('position_user', __name__)


# 展示所有职位 路由
@bp.route('/show_user_pt', methods=('GET','POST'))
def show_user_pt():
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
        li=[]
        for post in posts:
            li.append(post)
        pager_obj = Pagination(request.args.get("page", 1), len(
            li), request.path, request.args, per_page_count=10)
        list = li[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()
        return render_template('user/position.html', list=list, html=html)
    else:
        db = get_db()
        posts = db.execute(
            '''
            SELECT p.id,p.pt_name,p.pt_describe,
            (SELECT COUNT(*) FROM user u WHERE u.pt_id=p.id) AS pt_count
            FROM position p
            '''
        )
        li=[]
        for post in posts:
            li.append(post)
        pager_obj = Pagination(request.args.get("page", 1), len(
            li), request.path, request.args, per_page_count=10)
        list = li[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()
        return render_template('user/position.html', list=list, html=html)
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
