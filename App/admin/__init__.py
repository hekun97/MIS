def init_admin(app):
    # 导入员工 personnel.py 的bp蓝图
    from App.admin import personnel
    app.register_blueprint(personnel.bp)

    # 导入部门 department.py的bp蓝图
    from App.admin import department
    app.register_blueprint(department.bp)

    # 导入团队 team.py 的bp蓝图
    from App.admin import team
    app.register_blueprint(team.bp)

    # 导入职位 position.py 的bp蓝图
    from App.admin import position
    app.register_blueprint(position.bp)

    # 导入请假信息 leave.py 的bp蓝图
    from App.admin import leave
    app.register_blueprint(leave.bp)
    # 导入公司信息 company.py 的bp蓝图
    from App.admin import company
    app.register_blueprint(company.bp)
    # 导入培训信息 train.py 的bp蓝图
    from App.admin import train
    app.register_blueprint(train.bp)