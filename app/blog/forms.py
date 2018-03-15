from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField
from wtforms.validators import DataRequired


class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    stay_logged_in = BooleanField("Stay Logged In")
    submit = SubmitField('Log In')


class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Enter Your Post')
    # category = StringField('Tags')
    submit = SubmitField('Publish')

    def to_model(self, entry):
        self.title.data = entry.title
        self.content.data = entry.content
        # self.category.data = entry.category
        # self.timestamp.data = entry.timestamp

    def from_model(self, entry):
        entry.title = self.title.data
        entry.content = self.content.data
        # entry.category = self.category.data
        # self.timestamp = self.timestamp.data


class SearchBar(FlaskForm):
    search = StringField('Search.. ', validators=[DataRequired()])
