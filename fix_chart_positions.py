from app import create_app, db
from app.charts.models import Chart

app = create_app()
with app.app_context():
    # 获取仪表盘1的所有图表
    charts = Chart.query.filter_by(dashboard_id=1).order_by(Chart.id).all()
    print(f'更新前图表位置:')
    for c in charts:
        print(f'ID: {c.id}, 名称: {c.name}, 位置: ({c.position_x}, {c.position_y})')
    
    # 更新位置，避免重叠
    for i, chart in enumerate(charts):
        offset = i * 50  # 每个图表偏移50px
        chart.position_x = 10 + offset
        chart.position_y = 10 + offset
        print(f'更新图表 {chart.id} 位置到 ({chart.position_x}, {chart.position_y})')
    
    db.session.commit()
    print('数据库已更新')
    
    # 验证
    print(f'\n更新后图表位置:')
    for c in charts:
        print(f'ID: {c.id}, 名称: {c.name}, 位置: ({c.position_x}, {c.position_y})')
