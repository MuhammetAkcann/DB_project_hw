from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import queries


class RegistrationForm(FlaskForm):
    address = StringField('address',
                           validators=[DataRequired(), Length(min=2, max=20)])
    user_type = StringField('user_type',
                           validators=[DataRequired()])
    mail = StringField('mail',
                        validators=[DataRequired()])
    name = StringField('name',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_mail(self, mail):
        maill = queries.select("mail", "patient", where="mail = '{}'".format(mail.data))
        if(len(maill)!=0):
            raise ValidationError("this mail has been taken already")
        mail = queries.select("mail", "psychologist", where="mail = '{}'".format(mail.data))
        if(len(mail)!=0):
            raise ValidationError("this mail has been taken already")


class LoginForm(FlaskForm):
    mail = StringField('mail',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')