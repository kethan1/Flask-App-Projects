from flask import *
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/login-system"
app.secret_key = b"h\xa2\\xe\xdc\x82*\xffc<<vx\xa0\x84\xfe\xcd\xdd/?,\x8d\x89\xfd.T;\xb0\fdasdfa/sdfa/assdfjwijiwjiejijeijfijifjidjofdijpoijdipjiojdiodijijzx2838 amr33j8j82j8j jj8jxae\x1a\x9f\\x`."
mongo = PyMongo(app)


@app.route('/', methods=['GET', 'POST'])
def sign_up():
    try:
        if session['logged_in'] != {}:
            flash('You are Already Logged In')
            return redirect('/home')
    except:
        pass
    if request.method == 'GET':
        return render_template('sign_up.html')
    elif request.method == 'POST':
        dict1 = {}
        for each in request.form:
            dict1[each] = request.form[each]
        found = mongo.db.users.find_one({'email': dict1['email']})
        if found is None:
            mongo.db.users.insert(dict1)
            session['logged_in'] = {'first_name': request.form['firstname'], 'last_name': request.form['lastname'], 'email': request.form['email']}
            flash('Sign up Successful')
            return redirect('/home')
        else:
            flash('An Account is Already Registered With This Email Address')
            return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if session['logged_in'] != {}:
            flash('You are Already Logged In')
            return redirect('/home')
    except:
        pass
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        info = {'email': request.form['email'], 'password': request.form['password']}
        found = mongo.db.users.find_one(info)
        if found is None:
            flash('The Email and Password Do Not Belong to a User in Our Records')
            return redirect('/login')
        else:
            print(found)
            session['logged_in'] = {'first_name': found['firstname'], 'last_name': found['lastname'], 'email': request.form['email']}
            flash('Login Successful')
            return redirect('/home')


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        try:
            if session['logged_in'] == {}:
                flash('Please Sign Up or Log In to Continue')
                return redirect('/')
        except:
            flash('Please Sign Up or Log In to Continue')
            return redirect('/')

        return render_template('home.html', first_name=session['logged_in']['first_name'], last_name=session['logged_in']['last_name'], email=session['logged_in']['email'])


@app.route('/logout')
def logout():
    session['logged_in'] = {}
    return redirect('/')


@app.route('/change_data', methods=['GET', 'POST'])
def change_data():
    if request.method == 'GET':
        return render_template('change_data.html')
    elif request.method == 'POST':
        info = {}
        for item in request.form:
            if request.form[item] != '':
                info[item] = request.form[item]
        emailbefore = session['logged_in']['email']
        if 'email' in info:
            email = info['email']
            query = mongo.db.users.find_one({'email': email})
            if query is None:
                change = {'$set': {'email': email} }
                filter = {'email': session['logged_in']['email']}
                mongo.db.users.update_one(filter, change)
                if 'firstname' in info:
                    change = {'$set': {'firstname': info['firstname']}}
                    filter = {'email': email}
                    mongo.db.users.update_one(filter, change)
                if 'lastname' in info:
                    change = {'$set': {'lastname': info['lastname']}}
                    filter = {'email': email}
                    mongo.db.users.update_one(filter, change)
                if 'password' in info:
                    change = {'$set': {'password': info['password']}}
                    filter = {'email': email}
                    mongo.db.users.update_one(filter, change)
                d = mongo.db.users.find_one({'email': request.form['email']})
                print(d)
                session['logged_in'] = {'first_name': info['firstname'], 'last_name': info['lastname'], 'email': request.form['email']}
                print(session)
                flash('Info Successfully Changed')
                return redirect('/home')
            else:
                flash('An Account is Already Registered With That Email Address')
                return redirect('/home')
        else:
            if 'firstname' in info:
                change = {'$set': {'firstname': info['firstname']}}
                filter = {'email': session['logged_in']['email']}
                mongo.db.users.update_one(filter, change)
            if 'lastname' in info:
                change = {'$set': {'lastname': info['lastname']}}
                filter = {'email': session['logged_in']['email']}
                mongo.db.users.update_one(filter, change)
            if 'password' in info:
                change = {'$set': {'password': info['password']}}
                filter = {'email': session['logged_in']['email']}
                mongo.db.users.update_one(filter, change)
            info = mongo.db.users.find_one({'email': session['logged_in']['email']})
            session['logged_in'] = {'first_name': info['firstname'], 'last_name': info['lastname'], 'email': session['logged_in']['email']}
            flash('Info Successfully Changed')
            return redirect('/home')



if __name__ == '__main__':
    app.run(debug=True)
