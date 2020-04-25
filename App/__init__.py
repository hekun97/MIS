import os
from flask.app import Flask
# from App.views import init_route
from App.user import init_user
from App.admin import init_admin

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # 数据库的路径和名称
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # 从 views.py 中调用 init_route() 函数，称为懒加载
    # init_route(app)
    # 导入auth.py 的bp的 蓝图 函数
    from . import auth
    app.register_blueprint(auth.bp)

    # 导入系统 system.py 的 bp蓝图
    from . import system
    app.register_blueprint(system.bp)
    app.add_url_rule('/', endpoint='index')
    
    # 用户端蓝图
    init_user(app=app)

    # 管理员端蓝图
    init_admin(app=app)

    # 导入数据库文件 db.py
    from . import db
    db.init_app(app)

    return app
