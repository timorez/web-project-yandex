from flask import Flask
from flask import render_template
from flask import redirect
from data import db_session
from data.users import User
from forms.registerform import RegisterForm
from forms.loginform import LoginForm
from flask_login import login_user, login_required, logout_user, LoginManager, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/main')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', text='main')
    return render_template('index.html', text='не авторизован')


@app.route('/', methods=['GET', 'POST'])
@app.route('/sign_up', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('web_sign_up.html', title='Sign up',
                                   form=form,
                                   message="This user is already registered")
        user = User(
            email=form.email.data,
            password=form.password.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/signin')
    return render_template('web_sign_up.html', title='Sign up', form=form,
                           message='')


@app.route('/signin', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/main')
        return render_template('web_sign_in.html.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('web_sign_in.html', title='Авторизация', form=form,
                           message='')


@login_manager.user_loader
def load_user(email):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(email)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init('db/Users.sqlite')
    app.run(port=8080, host='127.0.0.1')
