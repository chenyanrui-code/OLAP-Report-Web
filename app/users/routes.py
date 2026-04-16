from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, abort
from flask_login import login_required, current_user
from app import db
from app.auth.models import User
from werkzeug.security import generate_password_hash
from datetime import datetime
from functools import wraps

users = Blueprint('users', __name__)

# 管理员权限装饰器
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('您没有权限访问此页面', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@users.route('/')
@login_required
@admin_required
def index():
    users_list = User.query.order_by(User.id.desc()).all()
    return render_template('users/index.html', title='用户管理', users=users_list)

@users.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        is_admin = request.form.get('is_admin') == 'on'
        
        # 验证输入
        if not username or not email or not password:
            flash('请填写所有必填字段', 'danger')
            return redirect(url_for('users.add'))
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'danger')
            return redirect(url_for('users.add'))
        
        # 检查邮箱是否已存在
        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册', 'danger')
            return redirect(url_for('users.add'))
        
        # 创建新用户
        user = User(
            username=username,
            email=email,
            is_admin=is_admin
        )
        user.password = password
        
        db.session.add(user)
        db.session.commit()
        flash('用户添加成功', 'success')
        return redirect(url_for('users.index'))
    
    return render_template('users/add.html', title='添加用户')

@users.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        is_admin = request.form.get('is_admin') == 'on'
        
        # 检查用户名是否被其他用户使用
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != id:
            flash('用户名已被使用', 'danger')
            return redirect(url_for('users.edit', id=id))
        
        # 检查邮箱是否被其他用户使用
        existing_email = User.query.filter_by(email=email).first()
        if existing_email and existing_email.id != id:
            flash('邮箱已被使用', 'danger')
            return redirect(url_for('users.edit', id=id))
        
        user.username = username
        user.email = email
        user.is_admin = is_admin
        
        # 如果提供了新密码，则更新密码
        if password:
            user.password = password
        
        db.session.commit()
        flash('用户信息更新成功', 'success')
        return redirect(url_for('users.index'))
    
    return render_template('users/edit.html', title='编辑用户', user=user)

@users.route('/delete/<int:id>')
@login_required
@admin_required
def delete(id):
    # 防止删除自己
    if id == current_user.id:
        flash('不能删除当前登录的用户', 'danger')
        return redirect(url_for('users.index'))
    
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('用户删除成功', 'success')
    return redirect(url_for('users.index'))

@users.route('/check_username')
@login_required
def check_username():
    username = request.args.get('username', '')
    user_id = request.args.get('user_id', type=int)
    
    query = User.query.filter_by(username=username)
    if user_id:
        query = query.filter(User.id != user_id)
    
    exists = query.first() is not None
    return jsonify({'exists': exists})

@users.route('/check_email')
@login_required
def check_email():
    email = request.args.get('email', '')
    user_id = request.args.get('user_id', type=int)
    
    query = User.query.filter_by(email=email)
    if user_id:
        query = query.filter(User.id != user_id)
    
    exists = query.first() is not None
    return jsonify({'exists': exists})
