from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# 创建数据库实例
db = SQLAlchemy()

# 创建登录管理器
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    
    # 配置文件
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
    
    # 确保上传目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    
    # 注册蓝图
    from app.auth.routes import auth
    from app.data_sources.routes import data_sources
    from app.data_models.routes import data_models
    from app.dashboards.routes import dashboards
    from app.charts.routes import charts
    from app.main.routes import main
    from app.users.routes import users
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(data_sources, url_prefix='/data_sources')
    app.register_blueprint(data_models, url_prefix='/data_models')
    app.register_blueprint(dashboards, url_prefix='/dashboards')
    app.register_blueprint(charts, url_prefix='/charts')
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(main, url_prefix='/')
    
    # 主路由
    @app.route('/')
    def index():
        return redirect(url_for('main.index'))
    
    return app
