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
bp = Blueprint('personnel', __name__)

# 展示员工 路由
@bp.route('/show', methods=('GET', 'POST'))
def show():
    db = get_db()
    if request.method == 'POST':
        search_name = request.form['search_name']
        # 变成模糊搜索格式
        name = '%'+request.form['name']+'%'
        # 按姓名搜索
        if search_name == '按姓名搜索':
            posts = db.execute(
                '''
                SELECT u.id,u.username,u.password,u.sex,u.email,u.tel,u.level,u.money,u.birthday,u.work_begin_day,
                (strftime('%Y', 'now') - strftime('%Y', birthday)) - (strftime('%m-%d', 'now') < strftime('%m-%d', birthday)) AS age,
                (strftime('%Y', 'now') - strftime('%Y', work_begin_day)) - (strftime('%m-%d', 'now') < strftime('%m-%d', work_begin_day)) AS work_age,
                (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
                (SELECT d.dp_name FROM department d WHERE u.dp_id = d.id) AS d_name,
                (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name          
                FROM user u WHERE u.username LIKE ?
                ''', (name,)
            )
            li = page_same(posts)
            pager_obj = Pagination(request.args.get("page", 1), len(
                li), request.path, request.args, per_page_count=10)
            list = li[pager_obj.start:pager_obj.end]
            html = pager_obj.page_html()
            return render_template('admin/personnel/show.html', list=list, html=html)
        # 按性别搜索
        elif search_name == '按性别搜索':
            posts = db.execute(
                '''
                SELECT u.id,u.username,u.password,u.sex,u.email,u.tel,u.level,u.money,u.birthday,u.work_begin_day,
                (strftime('%Y', 'now') - strftime('%Y', birthday)) - (strftime('%m-%d', 'now') < strftime('%m-%d', birthday)) AS age,
                (strftime('%Y', 'now') - strftime('%Y', work_begin_day)) - (strftime('%m-%d', 'now') < strftime('%m-%d', work_begin_day)) AS work_age,
                (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
                (SELECT d.dp_name FROM department d WHERE u.dp_id = d.id) AS d_name,
                (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name          
                FROM user u WHERE u.sex LIKE ?
                ''', (name,)
            )
            li = page_same(posts)
            pager_obj = Pagination(request.args.get("page", 1), len(
                li), request.path, request.args, per_page_count=10)
            list = li[pager_obj.start:pager_obj.end]
            html = pager_obj.page_html()
            return render_template('admin/personnel/show.html', list=list, html=html)
        # 按权限搜索
        elif search_name == '按权限搜索':
            posts = db.execute(
                '''
                SELECT u.id,u.username,u.password,u.sex,u.email,u.tel,u.level,u.money,u.birthday,u.work_begin_day,
                (strftime('%Y', 'now') - strftime('%Y', birthday)) - (strftime('%m-%d', 'now') < strftime('%m-%d', birthday)) AS age,
                (strftime('%Y', 'now') - strftime('%Y', work_begin_day)) - (strftime('%m-%d', 'now') < strftime('%m-%d', work_begin_day)) AS work_age,
                (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
                (SELECT d.dp_name FROM department d WHERE u.dp_id = d.id) AS d_name,
                (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name          
                FROM user u WHERE u.level LIKE ?
                ''', (name,)
            )
            li = page_same(posts)
            pager_obj = Pagination(request.args.get("page", 1), len(
                li), request.path, request.args, per_page_count=10)
            list = li[pager_obj.start:pager_obj.end]
            html = pager_obj.page_html()
            return render_template('admin/personnel/show.html', list=list, html=html)
        # 按职位搜索
        elif search_name == '按职位搜索':
            posts = db.execute(
                '''
                SELECT u.id,u.username,u.password,u.sex,u.email,u.tel,u.level,u.money,u.birthday,u.work_begin_day,
                (strftime('%Y', 'now') - strftime('%Y', birthday)) - (strftime('%m-%d', 'now') < strftime('%m-%d', birthday)) AS age,
                (strftime('%Y', 'now') - strftime('%Y', work_begin_day)) - (strftime('%m-%d', 'now') < strftime('%m-%d', work_begin_day)) AS work_age,
                (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
                (SELECT d.dp_name FROM department d WHERE u.dp_id = d.id) AS d_name,
                (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name          
                FROM user u WHERE p_name LIKE ?
                ''', (name,)
            )
            li = page_same(posts)
            pager_obj = Pagination(request.args.get("page", 1), len(
                li), request.path, request.args, per_page_count=10)
            list = li[pager_obj.start:pager_obj.end]
            html = pager_obj.page_html()
            return render_template('admin/personnel/show.html', list=list, html=html)
        # 按所属团队搜索
        elif search_name == '按所属团队搜索':
            posts = db.execute(
                '''
                SELECT u.id,u.username,u.password,u.sex,u.email,u.tel,u.level,u.money,u.birthday,u.work_begin_day,
                (strftime('%Y', 'now') - strftime('%Y', birthday)) - (strftime('%m-%d', 'now') < strftime('%m-%d', birthday)) AS age,
                (strftime('%Y', 'now') - strftime('%Y', work_begin_day)) - (strftime('%m-%d', 'now') < strftime('%m-%d', work_begin_day)) AS work_age,
                (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
                (SELECT d.dp_name FROM department d WHERE u.dp_id = d.id) AS d_name,
                (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name          
                FROM user u WHERE t_name LIKE ?
                ''', (name,)
            )
            li = page_same(posts)
            pager_obj = Pagination(request.args.get("page", 1), len(
                li), request.path, request.args, per_page_count=10)
            list = li[pager_obj.start:pager_obj.end]
            html = pager_obj.page_html()
            return render_template('admin/personnel/show.html', list=list, html=html)
        # 按所属部门搜索
        elif search_name == '按所属部门搜索':
            posts = db.execute(
                '''
                SELECT u.id,u.username,u.password,u.sex,u.email,u.tel,u.level,u.money,u.birthday,u.work_begin_day,
                (strftime('%Y', 'now') - strftime('%Y', birthday)) - (strftime('%m-%d', 'now') < strftime('%m-%d', birthday)) AS age,
                (strftime('%Y', 'now') - strftime('%Y', work_begin_day)) - (strftime('%m-%d', 'now') < strftime('%m-%d', work_begin_day)) AS work_age,
                (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
                (SELECT d.dp_name FROM department d WHERE u.dp_id = d.id) AS d_name,
                (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name          
                FROM user u WHERE d_name LIKE ?
                ''', (name,)
            )
            li = page_same(posts)
            pager_obj = Pagination(request.args.get("page", 1), len(
                li), request.path, request.args, per_page_count=10)
            list = li[pager_obj.start:pager_obj.end]
            html = pager_obj.page_html()
            return render_template('admin/personnel/show.html', list=list, html=html)
    # 默认条件下
    posts = db.execute(
        '''
        SELECT u.id,u.username,u.password,u.sex,u.email,u.tel,u.level,u.money,u.birthday,u.work_begin_day,
        (strftime('%Y', 'now') - strftime('%Y', birthday)) - (strftime('%m-%d', 'now') < strftime('%m-%d', birthday)) AS age,
        (strftime('%Y', 'now') - strftime('%Y', work_begin_day)) - (strftime('%m-%d', 'now') < strftime('%m-%d', work_begin_day)) AS work_age,
        (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
        (SELECT d.dp_name FROM department d WHERE u.dp_id = d.id) AS d_name,
        (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name          
        FROM user u
        '''
    )
    li = page_same(posts)
    pager_obj = Pagination(request.args.get("page", 1), len(
        li), request.path, request.args, per_page_count=10)
    list = li[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template('admin/personnel/show.html', list=list, html=html)
# 展示员工详细信息
@bp.route('/<int:id>/show_one_more')
@login_required
def show_one_more(id):
    get_post(id)
    db = get_db()
    posts = db.execute(
        '''
            SELECT u.id,u.username,u.password,u.sex,u.email,u.tel,u.level,u.money,u.birthday,u.work_begin_day,
            (strftime('%Y', 'now') - strftime('%Y', birthday)) - (strftime('%m-%d', 'now') < strftime('%m-%d', birthday)) AS age,
            (strftime('%Y', 'now') - strftime('%Y', work_begin_day)) - (strftime('%m-%d', 'now') < strftime('%m-%d', work_begin_day)) AS work_age,
            (SELECT t.team_name FROM team t WHERE u.team_id = t.id) AS t_name,
            (SELECT d.dp_name FROM department d WHERE u.dp_id = d.id) AS d_name,
            (SELECT p.pt_name FROM position p WHERE u.pt_id = p.id) AS p_name          
            FROM user u WHERE u.id =?
        ''', (id,)
    )
    return render_template('admin/personnel/show_more.html', posts=posts)


# 添加员工 路由
@bp.route('/create', methods=('GET', 'POST'))
def create():
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
        team_posts = db.execute(
            '''
            SELECT id FROM team WHERE team_name=?
            ''', (team_name,)
        )
        # 将team表的id赋值给user表的team_id
        for post in team_posts:
            team_id = post['id']
        # 拿到部门的id
        dp_posts = db.execute(
            '''
            SELECT id FROM department WHERE dp_name=?
            ''', (dp_name,)
        )
        # 将department表的id赋值给user表的dp_id
        for post in dp_posts:
            dp_id = post['id']
        # 拿到职位的id
        pt_posts = db.execute(
            '''
            SELECT id FROM position WHERE pt_name=?
            ''', (pt_name,)
        )
        # 将position表的id赋值给user表的pt_id
        for post in pt_posts:
            pt_id = post['id']

        # 添加员工校验
        error = None
        if not username:
            error = '请填写用户名！'
        elif not password:
            error = '请填写密码！'
        elif not money or isinstance(money, int) == False:
            error = '请输入正确的薪酬数字！'
        elif not tel or isinstance(tel, int) == False:
            error = '请填写密码！'  
       
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = '用户名 {} 已经被注册.'.format(username)
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
        if len(posts)==0:
            po=('请先添加部门',)
            posts.append(po)
        # 拿到团队的数据
        team_posts = db.execute(
            'SELECT team_name FROM team'
        ).fetchall()
        # 判断是否有团队
        if len(team_posts)==0:
            po=('请先添加团队',)
            team_posts.append(po)
        # 拿到职位的信息
        pt_posts = db.execute(
            'SELECT pt_name FROM position'
        ).fetchall()
        # 判断是否有职位
        if len(pt_posts)==0:
            po=('请先添加职位',)
            pt_posts.append(po)
        return render_template('admin/personnel/create.html', posts=posts, team_posts=team_posts, pt_posts=pt_posts)

# 修改员工 路由
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
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
        team_posts = db.execute(
            '''
            SELECT id FROM team WHERE team_name=?
            ''', (team_name,)
        )
        # 将team表的id赋值给user表的team_id
        for post in team_posts:
            team_id = post['id']
        # 拿到部门的id
        dp_posts = db.execute(
            '''
            SELECT id FROM department WHERE dp_name=?
            ''', (dp_name,)
        )
        # 将department表的id赋值给user表的dp_id
        for post in dp_posts:
            dp_id = post['id']
        # 拿到职位的id
        pt_posts = db.execute(
            '''
            SELECT id FROM position WHERE pt_name=?
            ''', (pt_name,)
        )
        # 将position表的id赋值给user表的pt_id
        for post in pt_posts:
            pt_id = post['id']

        db = get_db()
        # 校验
        error = None
        if not username:
            error = '请填写用户名.'
        elif not password:
            error = '请填写密码.'
        elif db.execute(
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
                ''', (username, password, sex, level, money, birthday,
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
