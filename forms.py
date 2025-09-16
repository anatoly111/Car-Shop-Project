from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField,RadioField,TextAreaField
from wtforms.validators import InputRequired,EqualTo,Email

class registrationForm(FlaskForm):
    user_id = StringField("Username",validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    password2 = PasswordField("Repeat password",validators=[EqualTo("password"), InputRequired()])
    submit = SubmitField("Submit")


class loginForm(FlaskForm):
    user_id = StringField("User id", validators=[InputRequired()])
    password = PasswordField("Password",validators=[InputRequired()])
    submit = SubmitField("Submit")

class profileForm(FlaskForm):
    name = StringField("enter new name", validators=[InputRequired()])
    submit = SubmitField("submit")
    oldname = StringField("enter your oldname", validators=[InputRequired()])

class passForm(FlaskForm):
    name = StringField("name",validators=[InputRequired()])
    new_pass = PasswordField("new password",validators= [InputRequired()])
    submit = SubmitField("Submit")

class checkoutForm(FlaskForm):
    num = IntegerField("card number",validators=[InputRequired()])
    submit = SubmitField("Submit")
    box = StringField()

class filterForm(FlaskForm):
    price = RadioField(choices=["highest-lowest","lowest-highest"])
    make = RadioField(choices=['Audi',"BMW","Ford","Volkswagen","Mercedes","Trolley"])
    submit = SubmitField("submit")

class infoForm(FlaskForm):
    name = StringField("Enter your name")
    age = IntegerField("Enter your age")
    email = StringField("enter your email")
    submit = SubmitField("submit")

class contactForm(FlaskForm):
    name = StringField("Name",validators=[InputRequired("Name input required")])
    email = StringField("Email",validators=[Email("Invalid email address"),InputRequired("Please enter an email address")])
    message = TextAreaField("Message",validators=[InputRequired("Message box cannot be left empty")])
    submit = SubmitField("Submit")