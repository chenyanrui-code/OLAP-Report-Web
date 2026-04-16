from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.data_sources.models import DataSource
from app.data_models.models import DataModel
from app.dashboards.models import Dashboard
from app.charts.models import Chart

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    # 获取统计数据
    data_sources_count = DataSource.query.filter_by(user_id=current_user.id).count()
    data_models_count = DataModel.query.filter_by(user_id=current_user.id).count()
    dashboards_count = Dashboard.query.filter_by(user_id=current_user.id).count()
    charts_count = Chart.query.join(Dashboard).filter(Dashboard.user_id == current_user.id).count()
    
    return render_template('main/index.html', 
                          title='首页',
                          data_sources_count=data_sources_count,
                          data_models_count=data_models_count,
                          dashboards_count=dashboards_count,
                          charts_count=charts_count)
