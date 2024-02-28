from pathlib import Path

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename

from . import app, db
from .forms import ReviewForm, MovieForm, LoginForm, RegistrationForm
from .models import Movie, Review, login_manager, User

BASEDIR = Path(__file__).parent
UPLOAD_FOLDER = BASEDIR / 'static' / 'images'


@app.route('/')
def index():
    movies = Movie.query.order_by(Movie.id.desc()).all()

    return render_template('index.html',
                           movies=movies)


from flask_login import current_user, login_required


@app.route('/movie/<int:id>', methods=['GET', 'POST'])
def movie(id):
    movie = Movie.query.get(id)
    if movie.reviews:
        avg_score = round(sum(review.score for review in movie.reviews) / len(movie.reviews), 2)
    else:
        avg_score = 0

    form = ReviewForm(score=10)

    if form.validate_on_submit():
        if current_user.is_authenticated:
            review = Review()
            review.name = current_user.username  # Use the current user's username
            review.text = form.text.data
            review.score = form.score.data
            review.movie_id = movie.id
            db.session.add(review)
            db.session.commit()
            return redirect(url_for('movie', id=movie.id))
        else:
            return redirect(url_for('login'))

    return render_template('movie.html',
                           movie=movie,
                           avg_score=avg_score,
                           form=form)


@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        movie = Movie()
        movie.title = form.title.data
        movie.description = form.description.data
        image = form.image.data
        image_name = secure_filename(image.filename)
        UPLOAD_FOLDER.mkdir(exist_ok=True)
        image.save(UPLOAD_FOLDER / image_name)
        movie.image = image_name
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('movie', id=movie.id))

    if request.remote_addr == '127.0.0.1':
        return render_template('add_movie.html',
                               form=form)
    else:
        return render_template('access_denied.html')


@app.route('/reviews')
def reviews():
    reviews = Review.query.order_by(Review.created_date.desc()).all()
    return render_template('reviews.html',
                           reviews=reviews)


@app.route('/delete_review/<int:id>')
def delete_review(id):
    review = Review.query.get(id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('reviews'))


def get_top_movies(genre):
    movies = Movie.query.all()
    data = {}
    for movie in movies:
        s = 0
        k = 0
        if genre != "Все жанры" and movie.genre != genre:
            # print(movie.title, movie.genre)
            continue
        else:
            reviews_ = movie.reviews
            for review_score in reviews_:
                s += int(review_score.score)
                k += 1

            if k != 0:
                data[movie] = [movie.id, round(s / k, 2)]
    return data


@app.route('/top_movies')
def top_movies():
    genre_filter = request.args.get('genre_filter', None)
    if genre_filter is None:
        genre_filter = 'Все жанры'
    genres = {
        "Фантастика": "Фантастика",
        "Приключения": "Приключения",
        "Драма": "Драма",
        "Триллер": "Триллер",
        "Фильм ужасов": "Фильм ужасов",
        "Аниме": "Аниме",
        "Мультфильм": "Мультфильм",
        "Исторический": "Исторический",
        "Боевик": "Боевик",
        "Все жанры": "Все жанры"
    }
    del genres[genre_filter]
    genres[genre_filter] = genre_filter
    data = get_top_movies(genre_filter)
    data = dict(sorted(data.items(), key=lambda item: item[1]))
    return render_template('top_movies.html', movie_list=data,
                           selected_genre=genre_filter, genres=genres)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data)
        existing_user = User.query.filter_by(username=new_user.username).first()
        if existing_user:
            flash('Пользователь с таким именем уже существует!', 'danger')
        else:
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Регистрация прошла успешно! Пожалуйста войдите в аккаунт.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Неправильное имя пользователя или пароль!', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
