from flask import *
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo


app = Flask(__name__)


app.config['MONGO_URI'] = "mongodb://localhost:27017/note-manager-db"


Bootstrap(app)
mongo = PyMongo(app)


@app.route('/')
def jumbled_words():
    return render_template('home.html')


@app.route('/jumble', methods=[])
def jumble():
    if request.method == 'GET':
        return render_template('jumble.html')
    elif request.method == 'POST':
        doc = {'word': request.form.get('word').strip().upper()}
        mongo.db.words.insert_one(doc)
        return redirect('/')

@app.route('/')
def figure_out():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)