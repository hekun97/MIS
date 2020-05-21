# 员工信息管理 蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from App.auth import login_required
from App.db import get_db
from App.page_utils import Pagination
from App.page_utils import page_same
import re
bp = Blueprint('personnel', __name__)

# 拿到员工的相应信息
sql = '''
SELECT u.id,u.username,u.password,u.sex,u.email,u.tel,u.level,u.money,u.birthday,u.work_begin_day,
(strftime('%Y', 'now') - strftime('%Y', birthday)) - (strftime('%m-%d', 'now') < strftime('%m-%d', birthday)) AS age,
(strftime('%Y', 'now') - strftime('%Y', work_begin_day)) - (strftime('%m-%d', 'now') < strftime('%m-%d', work_begin_day)) AS work_age,
(SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
(SELECT d.dp_name FROM department d WHERE u.dp_id = d.id) AS d_name,
(SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name FROM user u
'''

# 展示员工 路由
@bp.route('/show', methods=('GET', 'POST'))
@login_required
def show():
    db = get_db()
    if request.method == 'POST':
        search_name = request.form['search_name']
        # 变成模糊搜索格式
        name = '%'+request.form['name']+'%'
        # 按姓名搜索
        if search_name == '按姓名搜索':
            posts = db.execute(
                sql + '''WHERE u.username LIKE ?''', (name,)
            ).fetchall()
        # 按性别搜索
        elif search_name == '按性别搜索':
            posts = db.execute(
                sql + '''WHERE u.sex LIKE ?''', (name,)
            ).fetchall()
        # 按权限搜索
        elif search_name == '按权限搜索':
            posts = db.execute(
                sql + '''WHERE u.level LIKE ?''', (name,)
            )
        # 按职位搜索
        elif search_name == '按职位搜索':
            posts = db.execute(
                sql + '''WHERE p_name LIKE ?''', (name,)
            ).fetchall()
        # 按所属团队搜索
        elif search_name == '按所属团队搜索':
            posts = db.execute(
                sql + '''WHERE t_name LIKE ?''', (name,)
            ).fetchall()
        # 按所属部门搜索
        elif search_name == '按所属部门搜索':
            posts = db.execute(
                sql+'''WHERE d_name LIKE ?''', (name,)
            ).fetchall()
    # 默认条件下展示所有员工
    else:
        # 判断用户权限
        if g.user['level'] == '员工':
            return '你的权限不够！'
        posts = db.execute(sql).fetchall()
    '''
    current_page——表示当前页。
    total_count——表示数据总条数。
    base_url——表示分页URL前缀，请求的前缀获取可以通过Flask的request.path方法，无需自己指定。
    例如：我们的路由方法为@app.route('/test')，request.path方法即可获取/test。
    params——表示请求传入的数据，params可以通过request.args动态获取。
    例如：我们链接点击为：http://localhost:5000/test?page=10，此时request.args获取数据为ImmutableMultiDict([('page', u'10')])
    per_page_count——指定每页显示数。
    max_pager_count——指定页面最大显示页码
    '''
    # 分页
    pager_obj = Pagination(request.args.get("page", 1), len(
        posts), request.path, request.args, per_page_count=10)
    list = posts[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template('admin/personnel/show.html', list=list, html=html)

# 展示员工详细信息
@bp.route('/<int:id>/show_one_more')
@login_required
def show_one_more(id):
    # 判断用户权限
    if g.user['level'] == '员工':
        return '你的权限不够！'
    get_post(id)
    db = get_db()
    posts = db.execute(
        sql+''' WHERE u.id =?''', (id,)
    )
    return render_template('admin/personnel/show_more.html', posts=posts)


# 添加员工 路由
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    db = get_db()
    # 判断用户权限
    if g.user['level'] == '员工':
        return '你的权限不够！'
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sex = request.form['sex']
        level = request.form['level']
        money = request.form['money']
        birthday = request.form['birthday']
        work_begin_day = request.form['work_begin_day']
        team_name = request.form['team_name']
        dp_name = request.form['dp_name']
        pt_name = request.form['pt_name']
        tel = request.form['tel']
        email = request.form['email']
        # 拿到team的id
        team_post = db.execute(
            '''
            SELECT id FROM team WHERE team_name=?
            ''', (team_name,)
        ).fetchone()
        # 将team表的id赋值给user表的team_id
        team_id = team_post[0]
        # 拿到部门的id
        dp_post = db.execute(
            '''
            SELECT id FROM department WHERE dp_name=?
            ''', (dp_name,)
        ).fetchone()
        # 将department表的id赋值给user表的dp_id
        dp_id = dp_post[0]
        # 拿到职位的id
        pt_post = db.execute(
            '''
            SELECT id FROM position WHERE pt_name=?
            ''', (pt_name,)
        ).fetchone()
        # 将position表的id赋值给user表的pt_id
        pt_id = pt_post[0]

        # 添加员工校验
        error = None
        # 验证员工姓名
        if db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = '用户名 {} 已经被注册！'.format(username)
        # 验证部门
        elif dp_name == '请先添加部门':
            error = '请先添加部门'
        # 验证团队
        elif team_name == '请先添加团队':
            error = '请先添加团队'
        # 验证职位
        elif pt_name == '请先添加职位':
            error = '请先添加职位'
        if error is None:
            # 将注册值插入到数据库
            db.execute(
                'INSERT INTO user (username, password,sex,level,money,birthday,work_begin_day,team_id,pt_id,dp_id,tel,email) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                (username, generate_password_hash(password), sex, level, money,
                 birthday, work_begin_day, team_id, pt_id, dp_id, tel, email)
            )
            db.commit()
            return redirect(url_for('personnel.show'))
        flash(error)
        return redirect(url_for('personnel.create'))
    else:
        # 拿到部门的数据
        posts = db.execute(
            'SELECT dp_name FROM department'
        ).fetchall()
        # 判断是否有部门
        if len(posts) == 0:
            po = ('请先添加部门',)
            posts.append(po)
        # 拿到团队的数据
        team_posts = db.execute(
            'SELECT team_name FROM team'
        ).fetchall()
        # 判断是否有团队
        if len(team_posts) == 0:
            po = ('请先添加团队',)
            team_posts.append(po)
        # 拿到职位的信息
        pt_posts = db.execute(
            'SELECT pt_name FROM position'
        ).fetchall()
        # 判断是否有职位
        if len(pt_posts) == 0:
            po = ('请先添加职位',)
            pt_posts.append(po)
        return render_template('admin/personnel/create.html', posts=posts, team_posts=team_posts, pt_posts=pt_posts)

# 修改员工 路由
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    # 判断用户权限
    if g.user['level'] == '员工':
        return '你的权限不够！'
    # 拿到数据库中的id，username,level
    post = get_post(id)
    db = get_db()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sex = request.form['sex']
        level = request.form['level']
        money = request.form['money']
        birthday = request.form['birthday']
        work_begin_day = request.form['work_begin_day']
        team_name = request.form['team_name']
        dp_name = request.form['dp_name']
        pt_name = request.form['pt_name']
        tel = request.form['tel']
        email = request.form['email']
        # 拿到team的id
        team_post = db.execute(
            '''
            SELECT id FROM team WHERE team_name=?
            ''', (team_name,)
        ).fetchone()
        # 将team表的id赋值给user表的team_id
        team_id = team_post[0]
        # 拿到部门的id
        dp_post = db.execute(
            '''
            SELECT id FROM department WHERE dp_name=?
            ''', (dp_name,)
        ).fetchone()
        # 将department表的id赋值给user表的dp_id
        dp_id = dp_post[0]
        # 拿到职位的id
        pt_post = db.execute(
            '''
            SELECT id FROM position WHERE pt_name=?
            ''', (pt_name,)
        ).fetchone()
        # 将position表的id赋值给user表的pt_id
        pt_id = pt_post[0]

        db = get_db()
        # 校验
        error = None
        if db.execute(
            'SELECT id FROM user WHERE username = ? AND id != ?', (
                username, id)
        ).fetchone() is not None:
            error = '用户名 {} 已经被注册.'.format(username)
        if error is not None:
            flash(error)
        else:
            posts = db.execute(
                'SELECT dp_name FROM department'
            )
            team_posts = db.execute(
                'SELECT team_name FROM team'
            )
            pt_posts = db.execute(
                'SELECT pt_name FROM position'
            )
            db.execute(
                '''
                UPDATE
                    user
                SET
                    username = ?, password = ?,sex=?,level=?,money=?,birthday=?,work_begin_day=?,team_id=?,pt_id=?,dp_id=?,tel=?,email=?
                WHERE
                    id = ?
                ''', (username, generate_password_hash(password), sex, level, money, birthday,
                      work_begin_day, team_id, pt_id, dp_id, tel, email, id)
            )
            db.commit()
            return redirect(url_for('personnel.show'))
    else:
        # 当前用户部门的部门名称
        dp_fact = db.execute(
            'SELECT dp_name FROM department WHERE id=?', (post['dp_id'],)
        )
        # 其他部门的名称
        dp_others = db.execute(
            'SELECT dp_name FROM department WHERE id!=?', (post['dp_id'],)
        )
        # 当前用户团队的团队名称
        team_fact = db.execute(
            'SELECT team_name FROM team WHERE id=?', (post['team_id'],)
        )
        # 其他团队的名称
        team_others = db.execute(
            'SELECT team_name FROM team WHERE id!=?', (post['team_id'],)
        )
        # 当前用户职位的职位名称
        pt_fact = db.execute(
            'SELECT pt_name FROM position WHERE id=?', (post['pt_id'],)
        )
        # 其他职位的名称
        pt_others = db.execute(
            'SELECT pt_name FROM position WHERE id!=?', (post['pt_id'],)
        )
        return render_template('admin/personnel/update.html', post=post, dp_fact=dp_fact, dp_others=dp_others, team_fact=team_fact, team_others=team_others, pt_fact=pt_fact, pt_others=pt_others)

# 删除用户 蓝图
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    # 判断用户权限
    if g.user['level'] == '员工':
        return '你的权限不够！'
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM user WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('personnel.show'))


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
