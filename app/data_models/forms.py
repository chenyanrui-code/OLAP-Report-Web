from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class DataModelForm(FlaskForm):
    name = StringField('模型名称', validators=[DataRequired(), Length(max=100)])
    data_source_id = SelectField('数据源', choices=[], validators=[DataRequired()])
    table_name = SelectField('表名', choices=[], validators=[DataRequired()])
    fields = MultiCheckboxField('字段')
    submit = SubmitField('保存')
