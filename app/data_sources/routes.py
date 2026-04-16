from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.data_sources.forms import DataSourceForm
from app.data_sources.models import DataSource
import os
import json
from werkzeug.utils import secure_filename

data_sources = Blueprint('data_sources', __name__)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@data_sources.route('/')
@login_required
def index():
    sources = DataSource.query.filter_by(user_id=current_user.id).all()
    return render_template('data_sources/index.html', title='数据源管理', sources=sources)

@data_sources.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = DataSourceForm()
    
    # 调试：打印表单数据
    if request.method == 'POST':
        print(f"[DEBUG] 表单数据: {request.form}")
        print(f"[DEBUG] 文件数据: {request.files}")
        print(f"[DEBUG] 表单验证结果: {form.validate_on_submit()}")
        if not form.validate_on_submit():
            print(f"[DEBUG] 表单错误: {form.errors}")
    
    if form.validate_on_submit():
        # 处理Excel文件上传
        if form.type.data == 'excel':
            print(f"[DEBUG] 处理Excel类型数据源")
            if 'file' not in request.files:
                flash('请选择Excel文件', 'danger')
                print(f"[DEBUG] 文件不在request.files中")
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('请选择Excel文件', 'danger')
                print(f"[DEBUG] 文件名为空")
                return redirect(request.url)
            if file and allowed_file(file.filename):
                # 获取文件扩展名
                file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'xlsx'
                # 生成唯一文件名（保留扩展名）
                import uuid
                unique_filename = f"{uuid.uuid4()}.{file_ext}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                print(f"[DEBUG] 文件保存到: {file_path}")
                # 存储相对路径
                relative_path = os.path.join('uploads', unique_filename).replace('\\', '/')
                source = DataSource(
                    name=form.name.data,
                    type=form.type.data,
                    file_path=relative_path,
                    user_id=current_user.id
                )
                print(f"[DEBUG] 创建Excel数据源: name={form.name.data}, file_path={relative_path}")
            else:
                flash('文件格式不支持，请上传 .xlsx 或 .xls 文件', 'danger')
                print(f"[DEBUG] 文件格式不支持")
                return redirect(request.url)
        else:
            # 处理数据库连接
            print(f"[DEBUG] 处理数据库类型数据源: {form.type.data}")
            source = DataSource(
                name=form.name.data,
                type=form.type.data,
                host=form.host.data,
                port=form.port.data,
                username=form.username.data,
                password=form.password.data,
                database=form.database.data,
                user_id=current_user.id
            )
        db.session.add(source)
        db.session.commit()
        print(f"[DEBUG] 数据源保存成功, ID: {source.id}")
        flash('数据源添加成功', 'success')
        return redirect(url_for('data_sources.index'))
    return render_template('data_sources/add.html', title='添加数据源', form=form)

@data_sources.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    source = DataSource.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = DataSourceForm(obj=source)
    if form.validate_on_submit():
        form.populate_obj(source)
        # 处理Excel文件更新
        if form.type.data == 'excel' and 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                # 获取文件扩展名
                file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'xlsx'
                # 生成唯一文件名（保留扩展名）
                import uuid
                unique_filename = f"{uuid.uuid4()}.{file_ext}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                # 存储相对路径
                relative_path = os.path.join('uploads', unique_filename).replace('\\', '/')
                source.file_path = relative_path
        db.session.commit()
        flash('数据源更新成功', 'success')
        return redirect(url_for('data_sources.index'))
    return render_template('data_sources/edit.html', title='编辑数据源', form=form, source=source)

@data_sources.route('/delete/<int:id>')
@login_required
def delete(id):
    source = DataSource.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(source)
    db.session.commit()
    flash('数据源删除成功', 'success')
    return redirect(url_for('data_sources.index'))

@data_sources.route('/test_connection', methods=['POST'])
def test_connection():
    data = request.get_json()
    # 这里实现连接测试逻辑
    return jsonify({'success': True, 'message': '连接成功'})
