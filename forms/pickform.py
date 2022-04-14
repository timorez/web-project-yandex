from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PickForm(FlaskForm):
    carry = StringField('carry', validators=[DataRequired()])
    mid = StringField('mid', validators=[DataRequired()])
    off = StringField('off', validators=[DataRequired()])
    four = StringField('four', validators=[DataRequired()])
    five = StringField('five', validators=[DataRequired()])
    submit = SubmitField('Analysis')
