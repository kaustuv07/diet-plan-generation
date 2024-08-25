from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField,TextAreaField
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
    calories = StringField('Calories', validators=[DataRequired()])
    protein = StringField('Protein', validators=[DataRequired()])
    carbs = StringField('Carbs', validators=[DataRequired()])
    fat = StringField('Fat', validators=[DataRequired()])
    bmi = StringField('BMI')
    fitness_level = StringField('Fitness Level')
    health_issues = TextAreaField('Health Issues')
    veg_preference = StringField('Veg Preference')
    weight_goal = StringField('Weight Goal')
    dietary_restrictions = TextAreaField('Dietary Restrictions')
    submit = SubmitField('Submit')
