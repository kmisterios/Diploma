from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LinkForm(FlaskForm):
    link = StringField('', validators=[DataRequired()])
    submit = SubmitField('GO')

