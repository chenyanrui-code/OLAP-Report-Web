from app import create_app, db
from app.charts.models import Chart

app = create_app()
with app.app_context():
    charts = Chart.query.filter_by(dashboard_id=1).all()
    print(f'仪表盘1的图表数量: {len(charts)}')
    for c in charts:
        print(f'ID: {c.id}, 名称: {c.name}, 位置: ({c.position_x}, {c.position_y}), 大小: {c.width}x{c.height}')
