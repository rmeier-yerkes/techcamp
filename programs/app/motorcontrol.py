from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms_components import NumberRangeField
from wtforms.validators import DataRequired

class submitForm(FlaskForm):
	submit = SubmitField(label= 'Submit')

class mpForm(FlaskForm):
	power = NumberRangeField('power', default =0,)

class mtForm(FlaskForm):
	time = SelectField(
		'Time',
		choices=[('-1','Back 1 sec'),('1','Forward 1 sec')]
	)
class servoForm(FlaskForm):
	time = SelectField(
		'Time',
		choices=[('0','Servo 0'),('1','Servo 1')]
	)
