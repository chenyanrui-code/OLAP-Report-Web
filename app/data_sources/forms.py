from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Optional

class DataSourceForm(FlaskForm):
    name = StringField('数据源名称', validators=[DataRequired(), Length(max=100)])
    type = SelectField('数据源类型', choices=[('mysql', 'MySQL'), ('postgresql', 'PostgreSQL'), ('excel', 'Excel文件')], validators=[DataRequired()])
    host = StringField('主机地址', validators=[Optional()])
    port = IntegerField('端口', validators=[Optional()])
    username = StringField('用户名', validators=[Optional()])
    password = PasswordField('密码', validators=[Optional()])
    database = StringField('数据库名称', validators=[Optional()])
    submit = SubmitField('保存')
