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

bp = Blueprint('company', __name__)
sql = '''SELECT * FROM company'''

'''
主页部分路由
'''
# 展示主页信息 路由
@bp.route('/home', methods=('GET', 'POST'))
@login_required
def home():
    # 判断用户权限
    judge(g.user['level'])
    db = get_db()
    posts = db.execute(
        sql +
        '''
        WHERE cp_level='首页信息'
        '''
    )
    return render_template('admin/home/show.html', posts=posts)

# 修改主页信息 路由
@bp.route('/<int:id>/update_home', methods=('GET', 'POST'))
@login_required
def update_home(id):
    # 判断用户权限
    judge(g.user['level'])
    # 拿到数据库中的值
    post = get_post(id)
    if request.method == 'POST':
        cp_title = request.form['cp_title']
        cp_body = request.form['cp_body']
        db = get_db()
        # 校验
        error = None
        if not cp_title:
            error = '请填写主页信息名称。'
        elif db.execute(
            sql +
            '''
            WHERE cp_title = ? AND id != ?
            ''', (
                cp_title, id)
        ).fetchone() is not None:
            error = '主页信息名称 {} 已经被使用.'.format(cp_title)
        if error is not None:
            flash(error)
        else:
            db.execute(
                'UPDATE company SET cp_title = ?, cp_body = ?'
                ' WHERE id = ?',
                (cp_title, cp_body, id)
            )
            db.commit()
            return redirect(url_for('company.home'))
    return render_template('admin/home/update.html', post=post)

# 展示更多信息 路由
@bp.route('/show_more', methods=('GET', 'POST'))
@login_required
def show_more():
    # 判断用户权限
    judge(g.user['level'])
    db = get_db()
    posts = db.execute(
        # 使用count()函数计算人数
        sql +
        '''
        WHERE cp_level='更多信息'
        '''
    )
    return render_template('admin/home/show_more.html', posts=posts)

# 修改更多信息 路由
@bp.route('/<int:id>/update_more', methods=('GET', 'POST'))
@login_required
def update_more(id):
    # 判断用户权限
    judge(g.user['level'])
    # 拿到数据库中的值
    post = get_post(id)
    if request.method == 'POST':
        cp_title = request.form['cp_title']
        cp_body = request.form['cp_body']
        db = get_db()
        # 校验
        error = None
        if not cp_title:
            error = '请填写更多信息名称。'
        elif db.execute(
            sql +
            '''
            WHERE cp_title = ? AND id != ?
            ''', (
                cp_title, id)
        ).fetchone() is not None:
            error = '更多信息名称 {} 已经被使用.'.format(cp_title)
        if error is not None:
            flash(error)
        else:
            db.execute(
                'UPDATE company SET cp_title = ?, cp_body = ?'
                ' WHERE id = ?',
                (cp_title, cp_body, id)
            )
            db.commit()
            return redirect(url_for('company.show_more'))
    return render_template('admin/home/update_more.html', post=post)


'''
通知信息管理路由
'''
nt_sql = '''
        SELECT c.id, cp_title, cp_body, cp_created, username
        FROM company c JOIN user u ON (c.author_id = u.id AND cp_level='普通内容')
        '''
# 展示通知信息 路由
@bp.route('/notice', methods=('GET', 'POST'))
@login_required
def notice():
    # 判断用户权限
    judge(g.user['level'])
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
        if search_name=='按发布人搜索':
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
    # 分页
    pager_obj = Pagination(request.args.get("page", 1), len(
        posts), request.path, request.args, per_page_count=10)
    posts = posts[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template('admin/notice/show.html', posts=posts, html=html)

# 展示详细的通知详情
@bp.route('/<int:id>/show_more_notice', methods=('GET', 'POST'))
@login_required
def show_more_notice(id):
    # 判断用户权限
    judge(g.user['level'])
    get_post(id)
    db = get_db()
    posts = db.execute(
        nt_sql +
        '''
        AND  c.id=?
        ''',(id,)
    ).fetchall()
    return render_template('admin/notice/show_more.html', posts=posts)

# 添加通知信息 路由
@bp.route('/create_notice', methods=('GET', 'POST'))
@login_required
def create_notice():
    # 判断用户权限
    judge(g.user['level'])
    db = get_db()
    if request.method == 'POST':
        cp_title = request.form['cp_title']
        cp_body = request.form['cp_body']
        author_id = g.user['id']
        # 校验                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        error = None
        if db.execute(
            sql +
            '''
            WHERE cp_title = ? 
            ''', (cp_title,)
        ).fetchone() is not None:   
            error = '通知信息名称 {} 已经被使用！'.format(cp_title)
        if error is not None:
            flash(error)
            return redirect(url_for('company.create_notice'))
        else:
            db.execute(
                '''
                INSERT INTO company (cp_title,cp_body,author_id) VALUES (?,?,?)
                ''', (cp_title, cp_body, author_id)
            )
            db.commit()
        return redirect(url_for('company.notice'))
    # 默认进入添加页面
    else:
        return render_template('admin/notice/create.html')

# 修改通知 路由
@bp.route('/<int:id>/update_notice', methods=('GET', 'POST'))
@login_required
def update_notice(id):
    # 判断用户权限
    judge(g.user['level'])
    # 拿到数据库中的值
    db = get_db()
    post = get_post(id)
    if request.method == 'POST':
        cp_title = request.form['cp_title']
        cp_body = request.form['cp_body']
        author_id = g.user['id']
        # 校验
        error = None
        if db.execute(
            sql +
            '''
            WHERE cp_title = ? AND id != ?
            ''', (cp_title, id)
        ).fetchone() is not None:
            error = '通知信息名称 {} 已经被使用！'.format(cp_title)
        if error is not None:
            flash(error)
        else:
            db.execute(
                'UPDATE company SET cp_title = ?, cp_body = ?,author_id = ?'
                ' WHERE id = ?',
                (cp_title, cp_body, author_id, id)
            )
            db.commit()
            return redirect(url_for('company.notice'))
    return render_template('admin/notice/update.html', post=post)

# 删除通知 蓝图
@bp.route('/<int:id>/delete_notice', methods=('POST',))
@login_required
def delete_notice(id):
    # 判断用户权限
    judge(g.user['level'])
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM company WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('company.notice'))

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
