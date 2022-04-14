from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route('/heroes')
def button():
    return render_template('heroes.html', title='heroes')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')