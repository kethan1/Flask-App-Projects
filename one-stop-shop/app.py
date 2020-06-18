from flask import *
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/note-manager-db"

Bootstrap(app)
mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    elif request.method == 'POST':
        pass


@app.route('/buy', methods=['GET', 'POST'])
def buy():
    if request.method == 'GET':
        return render_template('buy.html')
    elif request.method == 'POST':
        pass


if __name__ == '__main__':
    app.run(debug=True)