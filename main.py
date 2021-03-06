from flask import Flask
from flask import render_template
from flask import redirect
from data import db_session
from data.users import User
from data.heroes import Hero
from forms.registerform import RegisterForm
from forms.loginform import LoginForm
from forms.aboutform import AboutForm
from forms.pickform import PickForm
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

url = 'https://api.opendota.com/api/players/{}/wl'


@app.route('/main', methods=['GET', 'POST'])
def index():
    form = PickForm()
    percent = 0
    if current_user.is_authenticated:
        if form.validate_on_submit():
            carry = form.carry.data.strip()
            mid = form.mid.data.strip()
            off = form.off.data.strip()
            four = form.four.data.strip()
            five = form.five.data.strip()
            try:
                percent = main_analysis([carry, mid, off, four, five])
            except:
                percent = 'wrong names'
        return render_template('index.html', form=form,
                               result='we expect victory with probability - {}persent'.format(percent))
    return render_template('not_authorised.html', text='не авторизован')


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
        return render_template('web_sign_in.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('web_sign_in.html', title='Авторизация', form=form,
                           message='')


@app.route('/about', methods=['GET', 'POST'])
def about():
    form = AboutForm()
    wr = 0
    if current_user.is_authenticated:
        if form.validate_on_submit():
            resp = requests.get(url.format(form.id.data)).json()
            if len(resp) > 1:
                if resp['win'] != 0 and resp['lose'] != 0:
                    wr = str(resp['win'] / (resp['win'] + resp['lose']))
                else:
                    wr = 'no data(new user)'
            else:
                wr = 'incorrect id'
        return render_template('about.html', form=form, response='wr - {}'.format(wr))
    return render_template('not_authorised.html')


@login_manager.user_loader
def load_user(email):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(email)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/heroes')
def heroes():
    return render_template('heroes.html', title='heroes')


def main_analysis(hero_names):
    db_sess = db_session.create_session()
    res = ''
    carry = db_sess.query(Hero).filter(Hero.name == hero_names[0]).first()
    mid = db_sess.query(Hero).filter(Hero.name == hero_names[1]).first()
    off = db_sess.query(Hero).filter(Hero.name == hero_names[2]).first()
    four = db_sess.query(Hero).filter(Hero.name == hero_names[3]).first()
    five = db_sess.query(Hero).filter(Hero.name == hero_names[4]).first()
    lst = [carry, mid, off, four, five]
    if lst.count(carry) == 1 and lst.count(mid) == 1 and \
            lst.count(off) == 1 and lst.count(four) == 1 and lst.count(five) == 1:
        res = 0
        farm = 0
        meta = 0
        front = 0
        lane = 0
        active_sup = 0
        for i in lst:
            farm += i.farm
            meta += i.meta
            front += i.front
            lane += i.lane
            active_sup += i.active_sup
        res += 0.2 * ((farm / 9) * 100)
        res += 0.2 * ((meta / 5) * 100)
        res += 0.2 * ((front / 1) * 100)
        res += 0.2 * ((lane / 5) * 100)
        res += 0.2 * ((active_sup / 2) * 100)
    else:
        res = 'same heroes'
    return res


if __name__ == '__main__':
    db_session.global_init('db/Users.sqlite')
    app.run(port=8080, host='127.0.0.1')
