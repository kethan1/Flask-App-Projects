from flask import *
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/one-stop-shop"
app.secret_key = b"h\xa2\\xe\xdc\x82*\xffc<<vx\xa0\x84\xfe\xcd\xdd/?,\x8d\x89\xfd.T;\xb0\fdasdfa/sdfa/assdfjwijiwjiejijeijfijifjidjofdijpoijdipjiojdiodijijzx2838 amr33j8j82j8j jj8jxae\x1a\x9f\\x`."
mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    elif request.method == 'POST':
        doc = {}
        for item in request.form:
            if item != 'add':
                doc[item] = request.form[item]
        mongo.db.products.insert_one(doc)
        return redirect('/')


@app.route('/buy', methods=['GET', 'POST'])
def buy():
    if request.method == 'GET':
        # if 'cart-items' in session:
        #     session['cart-items'] = {}
        items = list(mongo.db.products.find({}))
        return render_template('buy.html', products=items)
    elif request.method == 'POST':
        try:
            items2 = session['cart-items']
        except KeyError:
            items2 = {}
        items = {}
        for name, value in request.form.items():
            items[name] = int(value)
        if items2 != {}:
            for key, value in items.items():
                if (int(items[key]) + int(items2[key])) > int(mongo.db.products.find_one({'_id': ObjectId(key)})['QuantityLimit']):
                    items[key] = mongo.db.products.find_one({'_id': ObjectId(key)})['QuantityLimit']
                else:
                    items[key] += int(items2[key])
        session['cart-items'] = items
        session.modified = True
        return redirect(url_for('buy'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        try:
            cart_items = session['cart-items']
        except:
            session['cart-items'] = {}
            cart_items = {}
        items = []
        for ID in cart_items:
            found_item = mongo.db.products.find_one({'_id': ObjectId(ID)})
            items.append([found_item, int(cart_items[ID])])
        total = 0
        for each in items:
            total += (int(each[1])*float(each[0]['price']))
        return render_template('checkout.html', items=items, total=total)
    elif request.method == 'POST':
        pass


@app.route('/clear_cart')
def clear_cart():
    session['cart-items'] = {}
    return redirect('/checkout')


if __name__ == '__main__':
    app.run(debug=True)