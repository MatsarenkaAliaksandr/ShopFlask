from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    quantity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.title


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/detail/<int:id>')
def detail(id):
    item = Item.query.get(id)
    return render_template('detail.html', item=item)


@app.route('/detail/<int:id>/delete')
def about_delete(id):
    item = Item.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        return redirect('/')
    except:
        return "An error occurred when deleting the article!"


@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": str(item.price) + '00'
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/detail/<int:id>/update', methods=['POST', 'GET'])
def posts_update(id):
    item = Item.query.get(id)
    if request.method == 'POST':
        item.title = request.form['title']
        item.price = request.form['price']
        item.description = request.form['description']
        item.quantity = request.form['quantity']
        item.image = request.form['image']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "An error occurred while adding an article!!!"
    else:
        return render_template("product_update.html",item=item)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']
        quantity = request.form['quantity']
        image = request.form['image']
        item = Item(title=title, price=price, description=description, quantity=quantity, image=image)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "An error occurred while adding the product!"
    else:
        return render_template('create.html')


@app.route('/aboutstore')
def about_store():
    return render_template('aboutstore.html')


if __name__ == '__main__':
    app.run(debug=True)
