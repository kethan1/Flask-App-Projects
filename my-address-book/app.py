from flask import *
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/address-book"


Bootstrap(app)
mongo = PyMongo(app)


@app.route('/', methods=['GET', 'POST'])
def address_book():
    if request.method == 'GET':
        contacts = list(mongo.db.AddressBook.find({}))
        return render_template('address_book.html', contacts=contacts)
    elif request.method == 'POST':
        document = {}
        for key, item in request.form.items():
            if key != 'Save':
                document[key] = item
        mongo.db.AddressBook.insert_one(document)
        return redirect('/')

@app.route('/delete/<identity>')
def delete_contact(identity):
    found = mongo.db.AddressBook.find_one({'_id': ObjectId(identity)})
    mongo.db.AddressBook.delete_one(found)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
