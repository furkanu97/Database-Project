from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField
from wtforms.validators import DataRequired, Optional

from datetime import datetime

class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class ProductEditForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    imported = StringField("Imported", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    info = StringField("Info", validators=[Optional()])

class UserEditForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    phone_number = IntegerField("Phone Number", validators=[DataRequired()])