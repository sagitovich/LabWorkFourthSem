from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[InputRequired(message="Заполните поле")])
    password = PasswordField('Пароль', validators=[InputRequired(message="Заполните поле")])
    confirm_password = PasswordField('Подтверждение пароля', validators=[
        InputRequired(message="Подтвердите пароль"),
        EqualTo('password', message="Пароли не совпадают")
    ])

    def validate_on_submit(self):
        return self.is_submitted() and self.validate()


class EditUserForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired(), Length(min=1, max=100)])
    last_name = StringField('Фамилия', validators=[DataRequired(), Length(min=1, max=100)])
    password = PasswordField('Пароль', validators=[Length(min=6, max=128)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[EqualTo('password')])
    submit = SubmitField('Сохранить изменения')

