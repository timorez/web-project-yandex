from flask import Flask
from flask import render_template
from flask import redirect
from loginform import *
from data import db_session
from data.users import User
from forms.user import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
@app.route('/sign_up', methods=['GET', 'POST'])
def login():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('web_sign_up.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            password=form.password.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/signin')
    return render_template('web_sign_up.html', title='Sign up', form=form)


@app.route('/signin')
def signin():
    form = RegisterForm()
    return render_template('web_sign_in.html', title='Sign in', form=form)


if __name__ == '__main__':
    db_session.global_init('db/Users.sqlite')
    app.run(port=8080, host='127.0.0.1')
