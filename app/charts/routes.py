from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.charts.forms import ChartForm
from app.charts.models import Chart
from app.data_models.models import DataModel
import json

charts = Blueprint('charts', __name__)

@charts.route('/add/<int:dashboard_id>', methods=['GET', 'POST'])
@login_required
def add(dashboard_id):
    print(f"\n[DEBUG charts/add] ====== 路由被调用 ======")
    print(f"[DEBUG charts/add] 请求方法: {request.method}")
    print(f"[DEBUG charts/add] URL: {request.url}")
    print(f"[DEBUG charts/add] dashboard_id: {dashboard_id}")
    form = ChartForm()
    # 加载数据模型选项
    models = DataModel.query.filter_by(user_id=current_user.id).all()
    form.data_model_id.choices = [(m.id, m.name) for m in models]
    
    # 优先处理AJAX请求获取字段
    if request.is_json:
        data = request.get_json()
        print(f"[DEBUG charts/add] AJAX请求数据: {data}")
        if 'data_model_id' in data:
            model = DataModel.query.get(data['data_model_id'])
            print(f"[DEBUG charts/add] 找到模型: {model}")
            if model:
                print(f"[DEBUG charts/add] 模型字段原始数据: {model.fields}")
                try:
                    fields = json.loads(model.fields) if model.fields else []
                    print(f"[DEBUG charts/add] 解析后的字段: {fields}")
                    return jsonify({'fields': fields})
                except (json.JSONDecodeError, TypeError) as e:
                    print(f"[ERROR charts/add] 解析字段失败: {e}")
                    return jsonify({'fields': []})
        # AJAX 请求但不是获取字段，返回错误
        return jsonify({'error': 'Invalid AJAX request'}), 400
    
    # 设置维度和指标的 choices（即使是空的，避免验证错误）
    form.dimensions.choices = []
    form.metrics.choices = []
    if request.method == 'POST':
        submitted_dimensions = request.form.getlist('dimensions')
        submitted_metrics = request.form.getlist('metrics')
        if submitted_dimensions:
            form.dimensions.choices = [(d, d) for d in submitted_dimensions]
        if submitted_metrics:
            form.metrics.choices = [(m, m) for m in submitted_metrics]
    
    print(f"[DEBUG] 请求方法: {request.method}")
    print(f"[DEBUG] 是否提交: {form.is_submitted()}")
    print(f"[DEBUG] 是否验证: {form.validate()}")
    print(f"[DEBUG] 表单错误: {form.errors}")
    
    if form.validate_on_submit():
        # 处理维度和指标选择
        dimensions = request.form.getlist('dimensions')
        metrics = request.form.getlist('metrics')
        print(f"[DEBUG] 保存图表 - dashboard_id: {dashboard_id}")
        print(f"[DEBUG] 表单数据 - name: {form.name.data}, type: {form.type.data}")
        print(f"[DEBUG] 表单数据 - data_model_id: {form.data_model_id.data}")
        print(f"[DEBUG] 维度: {dimensions}")
        print(f"[DEBUG] 指标: {metrics}")
        # 计算新图表的位置（避免重叠）
        existing_charts = Chart.query.filter_by(dashboard_id=dashboard_id).count()
        offset = existing_charts * 30  # 每个新图表偏移30px
        
        chart = Chart(
            name=form.name.data,
            type=form.type.data,
            dashboard_id=dashboard_id,
            data_model_id=form.data_model_id.data,
            dimensions=json.dumps(dimensions),
            metrics=json.dumps(metrics),
            position_x=10 + offset,
            position_y=10 + offset,
            width=400,
            height=300
        )
        db.session.add(chart)
        db.session.commit()
        print(f"[DEBUG] 图表已保存 - ID: {chart.id}, dashboard_id: {chart.dashboard_id}")
        flash('图表添加成功', 'success')
        return redirect(url_for('dashboards.edit', id=dashboard_id))
    
    return render_template('charts/add.html', title='添加图表', form=form, dashboard_id=dashboard_id)

@charts.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    chart = Chart.query.filter_by(id=id).first_or_404()
    # 验证权限
    if chart.dashboard.user_id != current_user.id:
        flash('无权编辑此图表', 'danger')
        return redirect(url_for('dashboards.index'))
    
    form = ChartForm(obj=chart)
    # 加载数据模型选项
    models = DataModel.query.filter_by(user_id=current_user.id).all()
    form.data_model_id.choices = [(m.id, m.name) for m in models]
    
    # 优先处理AJAX请求获取字段
    if request.is_json:
        data = request.get_json()
        print(f"[DEBUG charts/edit] AJAX请求数据: {data}")
        if 'data_model_id' in data:
            model = DataModel.query.get(data['data_model_id'])
            print(f"[DEBUG charts/edit] 找到模型: {model}")
            if model:
                print(f"[DEBUG charts/edit] 模型字段原始数据: {model.fields}")
                try:
                    fields = json.loads(model.fields) if model.fields else []
                    print(f"[DEBUG charts/edit] 解析后的字段: {fields}")
                    return jsonify({'fields': fields})
                except (json.JSONDecodeError, TypeError) as e:
                    print(f"[ERROR charts/edit] 解析字段失败: {e}")
                    return jsonify({'fields': []})
        # AJAX 请求但不是获取字段，返回错误
        return jsonify({'error': 'Invalid AJAX request'}), 400
    
    # 设置维度和指标的 choices（即使是空的，避免验证错误）
    form.dimensions.choices = []
    form.metrics.choices = []
    if request.method == 'POST':
        submitted_dimensions = request.form.getlist('dimensions')
        submitted_metrics = request.form.getlist('metrics')
        if submitted_dimensions:
            form.dimensions.choices = [(d, d) for d in submitted_dimensions]
        if submitted_metrics:
            form.metrics.choices = [(m, m) for m in submitted_metrics]
    
    if form.validate_on_submit():
        # 处理维度和指标选择
        dimensions = request.form.getlist('dimensions')
        metrics = request.form.getlist('metrics')
        form.populate_obj(chart)
        chart.dimensions = json.dumps(dimensions)
        chart.metrics = json.dumps(metrics)
        db.session.commit()
        flash('图表更新成功', 'success')
        return redirect(url_for('dashboards.edit', id=chart.dashboard_id))
    
    # 初始化表单数据
    if chart.dimensions:
        form.dimensions.data = json.loads(chart.dimensions)
    if chart.metrics:
        form.metrics.data = json.loads(chart.metrics)
    
    return render_template('charts/edit.html', title='编辑图表', form=form, chart=chart)

@charts.route('/delete/<int:id>')
@login_required
def delete(id):
    chart = Chart.query.filter_by(id=id).first_or_404()
    # 验证权限
    if chart.dashboard.user_id != current_user.id:
        flash('无权删除此图表', 'danger')
        return redirect(url_for('dashboards.index'))
    
    dashboard_id = chart.dashboard_id
    db.session.delete(chart)
    db.session.commit()
    flash('图表删除成功', 'success')
    return redirect(url_for('dashboards.edit', id=dashboard_id))

@charts.route('/data/<int:id>')
@login_required
def get_chart_data(id):
    chart = Chart.query.filter_by(id=id).first_or_404()
    if chart.dashboard.user_id != current_user.id:
        return jsonify({'error': '无权访问此图表'}), 403
    
    model = chart.data_model
    source = model.data_source
    
    try:
        dimensions = json.loads(chart.dimensions) if chart.dimensions else []
        metrics = json.loads(chart.metrics) if chart.metrics else []
    except:
        dimensions = []
        metrics = []
    
    try:
        import pymysql
        import psycopg2
        import pandas as pd
        import os
        
        df = None
        
        if source.type in ['mysql', 'postgresql']:
            if source.type == 'mysql':
                conn = pymysql.connect(
                    host=source.host,
                    port=source.port,
                    user=source.username,
                    password=source.password,
                    database=source.database
                )
            else:
                conn = psycopg2.connect(
                    host=source.host,
                    port=source.port,
                    user=source.username,
                    password=source.password,
                    dbname=source.database
                )
            
            select_fields = []
            group_by_fields = []
            
            for dim in dimensions:
                select_fields.append(dim)
                group_by_fields.append(dim)
            
            for metric in metrics:
                select_fields.append(f'SUM({metric}) as {metric}')
            
            if not select_fields:
                select_fields = ['*']
            
            query = f"SELECT {', '.join(select_fields)} FROM {model.table_name}"
            
            if group_by_fields:
                query += f" GROUP BY {', '.join(group_by_fields)}"
            
            query += " LIMIT 50"
            
            df = pd.read_sql(query, conn)
            conn.close()
            
        elif source.type == 'excel':
            file_path = os.path.join(current_app.root_path, 'static', source.file_path)
            df = pd.read_excel(file_path, sheet_name=model.table_name)
            
            if dimensions and metrics:
                agg_dict = {metric: 'sum' for metric in metrics}
                df = df.groupby(dimensions).agg(agg_dict).reset_index()
                df = df.head(50)
        
        if df is None or df.empty:
            return jsonify({'error': '没有数据'})
        
        chart_config = generate_chart_config(chart.type, df, dimensions, metrics)
        
        return jsonify({'chart_config': chart_config})
        
    except Exception as e:
        import traceback
        print(f"[ERROR get_chart_data] 获取图表数据失败: {e}")
        print(traceback.format_exc())
        return jsonify({'error': f'获取数据失败: {str(e)}'})


@charts.route('/preview', methods=['POST'])
@login_required
def preview():
    if request.is_json:
        data = request.get_json()
        chart_type = data.get('type', 'bar')
        data_model_id = data.get('data_model_id')
        dimensions = data.get('dimensions', [])
        metrics = data.get('metrics', [])
        
        if not data_model_id:
            return jsonify({'error': '未选择数据模型'})
        
        # 获取数据模型
        model = DataModel.query.get(data_model_id)
        if not model:
            return jsonify({'error': '数据模型不存在'})
        
        # 获取数据源
        source = model.data_source
        if not source:
            return jsonify({'error': '数据源不存在'})
        
        try:
            import pymysql
            import psycopg2
            import pandas as pd
            import os
            from app import db
            
            df = None
            
            if source.type in ['mysql', 'postgresql']:
                if source.type == 'mysql':
                    conn = pymysql.connect(
                        host=source.host,
                        port=source.port,
                        user=source.username,
                        password=source.password,
                        database=source.database
                    )
                else:  # postgresql
                    conn = psycopg2.connect(
                        host=source.host,
                        port=source.port,
                        user=source.username,
                        password=source.password,
                        dbname=source.database
                    )
                
                # 构建查询
                select_fields = []
                group_by_fields = []
                
                # 添加维度字段
                for dim in dimensions:
                    select_fields.append(dim)
                    group_by_fields.append(dim)
                
                # 添加指标字段（使用 SUM 聚合）
                for metric in metrics:
                    select_fields.append(f'SUM({metric}) as {metric}')
                
                if not select_fields:
                    select_fields = ['*']
                
                query = f"SELECT {', '.join(select_fields)} FROM {model.table_name}"
                
                if group_by_fields:
                    query += f" GROUP BY {', '.join(group_by_fields)}"
                
                query += " LIMIT 20"  # 限制数据量
                
                print(f"[DEBUG preview] 查询SQL: {query}")
                
                df = pd.read_sql(query, conn)
                conn.close()
                
            elif source.type == 'excel':
                file_path = os.path.join(current_app.root_path, 'static', source.file_path)
                df = pd.read_excel(file_path, sheet_name=model.table_name)
                
                # 对Excel数据进行分组聚合
                if dimensions and metrics:
                    agg_dict = {metric: 'sum' for metric in metrics}
                    df = df.groupby(dimensions).agg(agg_dict).reset_index()
                    df = df.head(20)
            
            if df is None or df.empty:
                return jsonify({'error': '没有数据'})
            
            print(f"[DEBUG preview] 查询结果: {len(df)} 行")
            
            # 生成图表配置
            chart_config = generate_chart_config(chart_type, df, dimensions, metrics)
            
            return jsonify({'chart_config': chart_config})
            
        except Exception as e:
            import traceback
            print(f"[ERROR preview] 生成图表失败: {e}")
            print(traceback.format_exc())
            return jsonify({'error': f'生成图表失败: {str(e)}'})
    
    return jsonify({'error': 'Invalid request'})


def generate_chart_config(chart_type, df, dimensions, metrics):
    """根据数据生成 Chart.js 配置"""
    
    # 获取标签（维度值）
    if dimensions:
        if len(dimensions) == 1:
            labels = df[dimensions[0]].astype(str).tolist()
        else:
            # 多维度时，组合成字符串
            labels = df[dimensions].apply(lambda x: ' - '.join(x.astype(str)), axis=1).tolist()
    else:
        labels = [f'数据 {i+1}' for i in range(len(df))]
    
    # 生成数据集
    datasets = []
    colors = [
        'rgba(78, 115, 223, 0.8)',
        'rgba(28, 200, 138, 0.8)',
        'rgba(54, 185, 204, 0.8)',
        'rgba(246, 194, 62, 0.8)',
        'rgba(231, 74, 59, 0.8)',
        'rgba(133, 135, 150, 0.8)'
    ]
    
    if metrics:
        for i, metric in enumerate(metrics):
            if metric in df.columns:
                dataset = {
                    'label': metric,
                    'data': df[metric].tolist(),
                    'backgroundColor': colors[i % len(colors)],
                    'borderColor': colors[i % len(colors)].replace('0.8', '1'),
                    'borderWidth': 1
                }
                
                # 根据图表类型调整
                if chart_type == 'line':
                    dataset['fill'] = False
                    dataset['tension'] = 0.1
                elif chart_type == 'pie' or chart_type == 'doughnut':
                    # 饼图需要多个颜色
                    dataset['backgroundColor'] = [colors[j % len(colors)] for j in range(len(df))]
                    dataset['borderColor'] = '#ffffff'
                
                datasets.append(dataset)
    else:
        # 没有指标时，使用第一列数值数据
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            datasets.append({
                'label': col,
                'data': df[col].tolist(),
                'backgroundColor': colors[0],
                'borderColor': colors[0].replace('0.8', '1'),
                'borderWidth': 1
            })
    
    chart_config = {
        'type': chart_type,
        'data': {
            'labels': labels,
            'datasets': datasets
        },
        'options': {
            'responsive': True,
            'maintainAspectRatio': False,
            'plugins': {
                'legend': {
                    'display': True,
                    'position': 'top'
                }
            }
        }
    }
    
    # 饼图和环形图的特殊配置
    if chart_type in ['pie', 'doughnut']:
        chart_config['options']['plugins']['legend']['position'] = 'right'
    
    return chart_config
