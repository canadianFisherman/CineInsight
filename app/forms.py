from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, StringField, FileField, PasswordField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed, FileRequired


class ReviewForm(FlaskForm):
    text = TextAreaField('Текст отзыва',
                         validators=[DataRequired(message="Поле не должно быть пустым")])
    score = SelectField('Оценка',
                        choices=[(i, i) for i in range(1, 11)])
    submit = SubmitField('Добавить отзыв')


class MovieForm(FlaskForm):
    title = StringField('Название',
                        validators=[DataRequired(message="Поле не должно быть пустым")])
    genre = SelectField('Жанр', choices=[('fant', 'Фантастика'), ('adv', 'Приключения'), ('dr', 'Драма'), ('tr', 'Триллер'), ('hor', 'Фильм ужасов'), ('anime', 'Аниме'), ('cart', 'Мультфильм'), ('hist', 'Исторический'), ('act', 'Боевик')], validators=[DataRequired(message="Поле не должно быть пустым")])

    description = TextAreaField('Описание',
                                validators=[DataRequired(message="Поле не должно быть пустым")])
    image = FileField('Изображение',
                      validators=[FileRequired(message="Поле не должно быть пустым"),
                                  FileAllowed(['jpg', 'jpeg', 'png'], message="Неверный формат файла")])
    submit = SubmitField('Добавить фильм')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(message="Поле не должно быть пустым")])
    password = PasswordField('Пароль', validators=[DataRequired(message="Поле не должно быть пустым")])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(message="Поле не должно быть пустым"), Length(min=4, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired(message="Поле не должно быть пустым")])
    submit = SubmitField('Зарегистрироваться')
