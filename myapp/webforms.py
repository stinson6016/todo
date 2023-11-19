from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class TodoForm(FlaskForm):
    title = StringField("Todo Title", render_kw={"placeholder": "Enter Todo..."}, validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Add")
    submit2 = SubmitField("Save")
    submit3 = SubmitField('Delete')
