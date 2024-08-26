from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField,TextAreaField,StringField, SelectField, SelectMultipleField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class GoalForm(FlaskForm):
    height = StringField('Height (cm)', validators=[DataRequired()])
    weight = StringField('Weight (kg)', validators=[DataRequired()])
    
    fitness_level = SelectField(
        'Fitness Level',
        choices=[('sedentary', 'Sedentary'), ('normal', 'Normal'), ('highly_active', 'Highly Active')]
    )
    
    health_issues = SelectMultipleField(
        'Health Issues',
        choices=[
            ('heart_disease', 'Heart Disease'), 
            ('diabetes', 'Diabetes'), 
            ('hypertension', 'Hypertension')
        ],
        option_widget=BooleanField.widget
    )

    veg_preference = SelectField(
        'Veg Preference',
        choices=[('veg'), ('non-veg')]
    )

    weight_goal = SelectField(
        'Weight Goal',
        choices=[('gain', 'Gain'), ('lose', 'Lose')]
    )

    dietary_restrictions = StringField('Dietary Restrictions')

    submit = SubmitField('Submit')