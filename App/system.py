# 系统主页蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, url_for
)
from App.auth import login_required
from App.admin.level_judge import judge


bp = Blueprint('system', __name__)

# 默认 为管理员端 路由
@bp.route('/')
@login_required
def index():
    # 判断用户权限
    judge(g.user['level'])
    return render_template('admin/index.html')



# 用户端 蓝图
@bp.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    return render_template('user/user.html')