from werkzeug.exceptions import abort

def judge(user):
    # 判断用户权限
    if user == '员工':
        abort(404,"抱歉！你访问的页面不存在......")