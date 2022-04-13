from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AboutForm(FlaskForm):
    id = StringField('id', validators=[DataRequired()])
    submit = SubmitField('Show info')
