from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.dashboards.models import Dashboard
from app.charts.models import Chart
import json

dashboards = Blueprint('dashboards', __name__)

@dashboards.route('/')
@login_required
def index():
    dashboards = Dashboard.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboards/index.html', title='仪表盘管理', dashboards=dashboards)

@dashboards.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            # 创建默认布局
            default_layout = json.dumps({"rows": 10, "cols": 12})
            dashboard = Dashboard(
                name=name,
                layout=default_layout,
                user_id=current_user.id
            )
            db.session.add(dashboard)
            db.session.commit()
            flash('仪表盘创建成功', 'success')
            return redirect(url_for('dashboards.index'))
    return render_template('dashboards/add.html', title='创建仪表盘')

@dashboards.route('/edit/<int:id>')
@login_required
def edit(id):
    dashboard = Dashboard.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return render_template('dashboards/edit.html', title='编辑仪表盘', dashboard=dashboard)

@dashboards.route('/delete/<int:id>')
@login_required
def delete(id):
    dashboard = Dashboard.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(dashboard)
    db.session.commit()
    flash('仪表盘删除成功', 'success')
    return redirect(url_for('dashboards.index'))

@dashboards.route('/save_layout/<int:id>', methods=['POST'])
@login_required
def save_layout(id):
    dashboard = Dashboard.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    if request.is_json:
        data = request.get_json()
        if 'layout' in data:
            # 保存仪表盘布局
            dashboard.layout = json.dumps(data['layout'])
            
            # 更新每个图表的位置和大小
            for item in data['layout']:
                chart = Chart.query.get(item.get('id'))
                if chart and chart.dashboard_id == dashboard.id:
                    chart.position_x = item.get('x', 10)
                    chart.position_y = item.get('y', 10)
                    chart.width = item.get('width', 400)
                    chart.height = item.get('height', 300)
            
            db.session.commit()
            return jsonify({'success': True})
    return jsonify({'success': False})

@dashboards.route('/get_charts/<int:id>')
@login_required
def get_charts(id):
    dashboard = Dashboard.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    # 获取仪表盘的所有图表
    charts = []
    print(f"[DEBUG get_charts] 仪表盘ID: {id}, 图表数量: {len(dashboard.charts)}")
    for chart in dashboard.charts:
        print(f"[DEBUG get_charts] 图表: {chart.id} - {chart.name}, 位置: ({chart.position_x}, {chart.position_y}), 大小: {chart.width}x{chart.height}")
        charts.append({
            'id': chart.id,
            'name': chart.name,
            'type': chart.type,
            'x': chart.position_x,
            'y': chart.position_y,
            'width': chart.width,
            'height': chart.height
        })
    return jsonify({'charts': charts})
