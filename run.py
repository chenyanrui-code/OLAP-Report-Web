from app import create_app, db
# 导入所有模型，确保数据库表被创建
from app.auth.models import User
from app.data_sources.models import DataSource
from app.data_models.models import DataModel
from app.dashboards.models import Dashboard
from app.charts.models import Chart

app = create_app()

# 初始化数据库
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
