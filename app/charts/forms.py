from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class ChartForm(FlaskForm):
    name = StringField('图表名称', validators=[DataRequired(), Length(max=100)])
    type = SelectField('图表类型', choices=[
        ('bar', '柱状图'),
        ('line', '折线图'),
        ('area', '面积图'),
        ('pie', '饼图'),
        ('doughnut', '环形图'),
        ('scatter', '散点图'),
        ('bubble', '气泡图'),
        ('histogram', '直方图'),
        ('boxplot', '箱线图'),
        ('sunburst', '旭日图'),
        ('scatter3d', '3D散点图'),
        ('scattergeo', '地理散点图')
    ], validators=[DataRequired()])
    data_model_id = SelectField('数据模型', choices=[], validators=[DataRequired()], coerce=int)
    dimensions = MultiCheckboxField('维度', choices=[])
    metrics = MultiCheckboxField('指标', choices=[])
    submit = SubmitField('保存')
