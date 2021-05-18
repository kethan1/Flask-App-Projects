from flask import *
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/note-manager-db"


Bootstrap(app)
mongo = PyMongo(app)


@app.route('/', methods=['GET', 'POST'])
def note_saver():
    if request.method == 'GET':
        notes = list(mongo.db.NoteCollection.find({}, {'_id': False}))
        return render_template('page.html', notes=notes)
    elif request.method == 'POST':
        document = {}
        for key, item in request.form.items():
            if key != 'Save':
                document[key] = item
        mongo.db.NoteCollection.insert_one(document)
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
