from flask import *
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
import random


app = Flask(__name__)


app.config['MONGO_URI'] = "mongodb://localhost:27017/jumbled-words"


Bootstrap(app)
mongo = PyMongo(app)


@app.route('/')
def jumbled_words():
    return render_template('home.html')


@app.route('/jumble', methods=['GET', 'POST'])
def jumble():
    if request.method == 'GET':
        return render_template('jumble.html')
    elif request.method == 'POST':
        doc = {'word': request.form.get('word').strip().upper()}
        mongo.db.words.insert_one(doc)
        return redirect('/')

index = 0
score = 0

@app.route('/figureout', methods=['GET', 'POST'])
def figure_out():
    global index, score
    docs = [dct['word'] for dct in list(mongo.db.words.find({}, {'_id': False}))]
    jumbled = []
    for word in docs:
        temp = list(word)
        random.shuffle(temp)
        word = ''.join(temp)
        jumbled.append(word)
    length = len(docs)
    if request.method == 'GET':
        if length == index:
            return render_template('figure_out.html', jumbled=[jumbled[index]], docs=docs, length=length, isfinished='Finish', index=index)
        return render_template('figure_out.html', jumbled=jumbled[index], docs=docs, length=length, isfinished='Submit', index=index)
    elif request.method == 'POST':
        index += 1
        correct = False
        for correct_word, jumbled_word in request.form.items():
            if correct_word.upper() == jumbled_word.upper():
                score += 1
                correct = True
        if index == length:
            index = 0
            return render_template('results.html', score=str(score), total=str(length))
        return render_template('after_each_word.html', correct=correct)


if __name__ == '__main__':
    app.run(debug=True)