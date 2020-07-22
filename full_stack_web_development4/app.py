from flask import *
from flask_pymongo import PyMongo
import datetime


app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/full-stack-web-development4"
app.secret_key = \
    b"h\xa2\\xe\xdc\x82*\xffc<<vx\xa0\x84\xfe\xcd\xdd/?,\x8d\x89\xfd.T;\xb0\fdasdfa/sdfa/assdfjwijiwjieji" \
    b"jeijfijifjidjofdijpoijdipjiojdiodijijzx2838 amr33j8j82j8j jj8jxae\x1a\x9f\\x`."
mongo = PyMongo(app)


@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', year=datetime.date.today().year)
    elif request.method == 'POST':
        if request.form['confirm_password'] == request.form['password']:
            if mongo.db.find_one({'email': request.form['email']}) is None:
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                email = request.form['email']
                password = request.form['password']
                mongo.db.users.insert_one({
                    'first_name': first_name, 'last_name': last_name, 'email': email, 'password': password
                })
                session['logged_in'] = {
                    'first_name': first_name, 'last_name': last_name, 'email': email, 'password': password
                }
                return session['logged_in']
            else:
                flash('Account with That Email Already Exists')
        else:
            flash('Confirm Password Does Not Match Password')
            return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)