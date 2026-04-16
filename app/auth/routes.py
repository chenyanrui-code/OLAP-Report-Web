from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.auth.forms import RegistrationForm, LoginForm
from app.auth.models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboards.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='注册', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('登录失败，请检查邮箱和密码', 'danger')
    
    return render_template('auth/login.html', title='登录', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """用户设置页面"""
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_profile':
            # 更新基本信息
            username = request.form.get('username')
            email = request.form.get('email')
            
            # 检查用户名是否被其他用户使用
            existing_user = User.query.filter_by(username=username).first()
            if existing_user and existing_user.id != current_user.id:
                flash('用户名已被使用', 'danger')
                return redirect(url_for('auth.settings'))
            
            # 检查邮箱是否被其他用户使用
            existing_email = User.query.filter_by(email=email).first()
            if existing_email and existing_email.id != current_user.id:
                flash('邮箱已被使用', 'danger')
                return redirect(url_for('auth.settings'))
            
            current_user.username = username
            current_user.email = email
            db.session.commit()
            flash('个人信息更新成功', 'success')
            
        elif action == 'change_password':
            # 修改密码
            old_password = request.form.get('old_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if not current_user.verify_password(old_password):
                flash('原密码错误', 'danger')
                return redirect(url_for('auth.settings'))
            
            if new_password != confirm_password:
                flash('两次输入的新密码不一致', 'danger')
                return redirect(url_for('auth.settings'))
            
            if len(new_password) < 6:
                flash('密码长度不能少于6位', 'danger')
                return redirect(url_for('auth.settings'))
            
            current_user.password = new_password
            db.session.commit()
            flash('密码修改成功', 'success')
    
    return render_template('auth/settings.html', title='个人设置')
