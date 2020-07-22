from flask import *
from flask_pymongo import PyMongo
from datetime import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
import os

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/my-digital-diary"
app.secret_key = b"h\xa2\\xe\xdc\x82*\xffc<<vx\xa0\x84\xfe\xcd\xdd/?,\x8d\x89\xfd.T;\xb0\fdasdfa/sdfa/assdfjwijiwjiejijeijfijifjidjofdijpoijdipjiojdiodijijzx2838 amr33j8j82j8j jj8jxae\x1a\x9f\\x`."
mongo = PyMongo(app)


def send_email(message, html_display, receiver_email, sender_email="cci.throwaway.summer@gmail.com", text="Error. Your email client does not support HTML (Fancier) emails."):

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html_display, "html"))

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, os.environ.get('Password')[::-1])
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


@app.route('/', methods=['GET', 'POST'])
def sign_up():
    try:
        if session['logged_in'] != {}:
            flash('You are Already Logged In')
            return redirect('/diary')
    except:
        pass
    if request.method == 'GET':
        return render_template('sign_up.html')
    elif request.method == 'POST':
        dict1 = {}
        for each in request.form:
            dict1[each] = request.form[each]
        if dict1['password'] == dict1['password2']:
            found = mongo.db.users.find_one({'email': dict1['email']})
            if found is None:
                mongo.db.users.insert(dict1)
                now = datetime.now()
                time = [now.strftime("%D"), now.strftime("%H"), now.strftime("%M"), now.strftime("%S")]
                if int(time[1]) > 12:
                    time[1] = str(int(time[1]) - 12)
                session['logged_in'] = {
                    'first_name': request.form['firstname'],
                    'last_name': request.form['lastname'],
                    'email': request.form['email'],
                    'logintime': time
                }
                flash('Sign up Successful')
                return redirect('/diary')
            else:
                flash('An Account is Already Registered With This Email Address')
                return redirect('/')
        else:
            flash('Confirm Password Does Not Match Password')
            return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if session['logged_in'] != {}:
            flash('You are Already Logged In')
            return redirect('/diary')
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
            now = datetime.now()
            time = [now.strftime("%D"), now.strftime("%H"), now.strftime("%M"), now.strftime("%S")]
            if int(time[1]) > 12:
                time[1] = str(int(time[1]) - 12)
            session['logged_in'] = {
                'first_name': found['firstname'],
                'last_name': found['lastname'],
                'email': request.form['email'],
                'logintime': time
            }
            flash('Login Successful')
            return redirect('/diary')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    try:
        if session['logged_in'] != {}:
            flash('You Are Already Logged In')
            return redirect('/diary')
    except:
        pass
    if request.method == 'GET':
        return render_template('forgot_password.html')
    elif request.method == 'POST':

        found = mongo.db.users.find_one({
            'email': request.form['email'], 'firstname': request.form['firstname'], 'lastname': request.form['lastname']
        })

        message = MIMEMultipart("alternative")
        message["Subject"] = "Password Reset for Kethan's CCI Fair Project 2020 Summer"
        message["From"] = "cci.throwaway.summer@gmail.com"
        message["To"] = request.form['email']

        # Create the plain-text and HTML version of your message
        html = """
            <!DOCTYPE html>
            <html>
              <body>
                <p>Hi, %s
                    <br>
                    <br>
                    Your Password is: %s
                    <br>
                    <br>
                    Thank you,<br>
                        Kethan's CCI Fair Project
                </p>
              </body>
            </html>
        """ % (mongo.db.users.find_one({'email': request.form['email']})['firstname'], mongo.db.users.find_one({'email': request.form['email']})['password'])

        send_email(message, html, request.form['email'])
        return redirect('/login')

@app.route('/diary', methods=['GET', 'POST'])
def diary():
    try:
        if session['logged_in'] == {}:
            flash('Please Sign Up or Log In to Continue')
            return redirect('/')
    except:
        flash('Please Sign Up or Log In to Continue')
        return redirect('/')
    if request.method == 'GET':
        return render_template('diary.html', first_name=session['logged_in']['first_name'], last_name=session['logged_in']['last_name'], email=session['logged_in']['email'], logintime = session['logged_in']['logintime'], entries = list(reversed(list(mongo.db.entries.find({'user': session['logged_in']['email']})))))
    elif request.method == 'POST':
        now = datetime.now()
        time = [now.strftime("%D"), now.strftime("%H"), now.strftime("%M"), now.strftime("%S")]
        if int(time[1]) > 12:
            time[1] = str(int(time[1]) - 12)
        to_insert = {'text': request.form['textarea'], 'time': time, 'user': session['logged_in']['email']}
        print(to_insert)
        mongo.db.entries.insert_one(to_insert)
        return redirect('/diary')


@app.route('/logout')
def logout():
    session['logged_in'] = {}
    return redirect('/')


@app.route('/change_data', methods=['GET', 'POST'])
def change_data():
    try:
        if session['logged_in'] == {}:
            flash('Please Sign Up or Log In to Continue')
            return redirect('/')
    except:
        flash('Please Sign Up or Log In to Continue')
        return redirect('/')
    if request.method == 'GET':
        return render_template('change_data.html')
    elif request.method == 'POST':
        info = {}
        for item in request.form:
            if request.form[item] != '':
                info[item] = request.form[item]
        if info['password'] == info['password2']:
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
                    session['logged_in'] = {'first_name': info['firstname'], 'last_name': info['lastname'], 'email': request.form['email'], 'logintime': session['logged_in']['logintime']}
                    print(session)
                    flash('Info Successfully Changed')
                    return redirect('/diary')
                else:
                    flash('An Account is Already Registered With That Email Address')
                    return redirect('/diary')
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
                session['logged_in'] = {'first_name': info['firstname'], 'last_name': info['lastname'], 'email': session['logged_in']['email'], 'logintime': session['logged_in']['logintime']}
                flash('Info Successfully Changed')
                return redirect('/diary')
        else:
            flash('Confirm Password Does Not Match Password')
            return redirect('/change_data')


@app.route('/delete_user_confirmation', methods=['GET', 'POST'])
def delete_user_confirmation():
    try:
        if session['logged_in'] == {}:
            flash('Please Sign Up or Log In to Continue')
            return redirect('/')
    except:
        flash('Please Sign Up or Log In to Continue')
        return redirect('/')
    if request.method == 'GET':
        return render_template('delete_confirmation.html')
    elif request.method == 'POST':
        if request.form['secret'] == 'asdfasdfasdfaj i2orj 8ijfiaojiow3pjifjpioajpfiosdjfiop':
            mongo.db.users.delete_one({'email': session['logged_in']['email']})
            session['logged_in'] = {}
            flash('Account Removed')
            return redirect('/')
        else:
            flash('Account Deletion Canceled')
            return redirect('/diary')


@app.errorhandler(404)
def page_not_found(e):
    flash('Page Not Found')
    return render_template('page_not_found.html', error=e)


if __name__ == '__main__':
    print('http://192.168.0.19:5000')
    app.run(host='0.0.0.0', debug=True)
