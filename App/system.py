# 系统主页蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, url_for
)
from App.auth import login_required


bp = Blueprint('system', __name__)

# 默认 为管理员端 路由
@bp.route('/')
def index():
    # 检测用户是否登录
    if g.user is None:
        return redirect(url_for('auth.login'))
    # 检测用户的权限
    elif g.user['level']=='用户':
        return redirect(url_for('system.user'))
    else:
        return render_template('admin/index.html')



# 用户端 蓝图
@bp.route('/user', methods=['GET', 'POST'])
def user():
    # 检测用户是否登录
    if g.user is None:
        return redirect(url_for('auth.login'))
    # 检测用户的权限
    else:
        return render_template('user/user.html')