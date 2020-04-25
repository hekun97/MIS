# 部门信息管理 蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from App.auth import login_required
from App.db import get_db

bp = Blueprint('company_user', __name__)

# 展示主页信息 路由
@bp.route('/home_user', methods=('GET','POST'))
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
@bp.route('/show_more_user', methods=('GET','POST'))
def show_more_user():
    db = get_db()
    posts = db.execute(
        # 使用count()函数计算人数
        '''
        SELECT * FROM company WHERE cp_level='更多信息'
        '''
    )
    return render_template('user/home/show_more.html', posts=posts)
