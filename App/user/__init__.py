def init_user(app):
    # 导入员工 personnel.py 的bp蓝图
    from App.user import personnel_user
    app.register_blueprint(personnel_user.bp)
    # 导入员工 personnel.py 的bp蓝图
    from App.user import leave_user
    app.register_blueprint(leave_user.bp)
    # 导入部门 的蓝图
    from App.user import department_user
    app.register_blueprint(department_user.bp)
    # 导入团队 的蓝图
    from App.user import team_user
    app.register_blueprint(team_user.bp)
     # 导入职位 的蓝图
    from App.user import position_user
    app.register_blueprint(position_user.bp) 
    # 导入主页 的蓝图
    from App.user import company_user
    app.register_blueprint(company_user.bp) 