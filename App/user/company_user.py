# 主页信息管理 蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from App.auth import login_required
from App.db import get_db
from App.page_utils import Pagination

bp = Blueprint('company_user', __name__)
'''
主页信息
'''
# 展示主页信息 路由
@bp.route('/home_user', methods=('GET', 'POST'))
def home_user():
    db = get_db()
    posts = db.execute(
        # 使用count()函数计算人数
        '''
        SELECT * FROM company WHERE cp_level='首页信息'
        '''
    )
    return render_template('user/home/show.html', posts=posts)


# 展示更多信息 路由
@bp.route('/show_more_user', methods=('GET', 'POST'))
def show_more_user():
    db = get_db()
    posts = db.execute(
        # 使用count()函数计算人数
        '''
        SELECT * FROM company WHERE cp_level='更多信息'
        '''
    )
    return render_template('user/home/show_more.html', posts=posts)


'''
通知路由
'''
nt_sql = '''
        SELECT c.id, cp_title, cp_body, cp_created, username
        FROM company c JOIN user u ON (c.author_id = u.id AND cp_level='普通内容')
        '''
# 展示通知信息 路由
@bp.route('/notice_user', methods=('GET', 'POST'))
def notice_user():
    db = get_db()
    if request.method == 'POST':
        search_name = request.form['search_name']
        name = '%'+request.form['name']+'%'
        if search_name == '按标题搜索':
            posts = db.execute(
                nt_sql +
                '''
                AND cp_title LIKE ?
                ORDER BY cp_created DESC
                ''', (name,)
            ).fetchall()
        else:
            posts = db.execute(
                nt_sql +
                '''
                AND username LIKE ?
                ORDER BY cp_created DESC
                ''', (name,)
            ).fetchall()
    else:
        posts = db.execute(
            nt_sql +
            '''
            ORDER BY cp_created DESC
            '''
        ).fetchall()
    pager_obj = Pagination(request.args.get("page", 1), len(
        posts), request.path, request.args, per_page_count=10)
    posts = posts[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template('user/notice/show.html', posts=posts, html=html)
    
# 展示详细的通知详情
@bp.route('/<int:id>/show_more_notice_user', methods=('GET', 'POST'))
def show_more_notice_user(id):
    get_post(id)
    db = get_db()
    posts = db.execute(
          nt_sql +
        '''
        AND  c.id=?
        ''',(id,)
    ).fetchall()
    return render_template('user/notice/show_more.html', posts=posts)

# 根据id值拿到相应的数据
def get_post(id):
    post = get_db().execute(
        'SELECT *'
        ' FROM company'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post 的 id值 {0} 不存在！".format(id))
    return post
