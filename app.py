from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../pharmacy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','dev-secret')

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    category = db.Column(db.String(120))
    image_url = db.Column(db.String(500))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total = db.Column(db.Float)
    status = db.Column(db.String(50), default='pending')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

@app.route('/')
def index():
    products = Product.query.limit(20).all()
    return render_template('index.html', products=products)

@app.route('/product/<int:pid>')
def product_detail(pid):
    p = Product.query.get_or_404(pid)
    return render_template('product.html', product=p)

@app.route('/api/cart/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    user_id = data.get('user_id')
    items = data.get('items')
    total = 0
    order = Order(user_id=user_id, total=0)
    db.session.add(order)
    db.session.flush()
    for it in items:
        product = Product.query.get(it['product_id'])
        qty = int(it['qty'])
        price = product.price * qty
        total += price
        oi = OrderItem(order_id=order.id, product_id=product.id, quantity=qty, price=product.price)
        db.session.add(oi)
        product.stock = max(0, product.stock - qty)
    order.total = total
    db.session.commit()
    return jsonify({'order_id': order.id, 'total': total})

@app.route('/register', methods=['POST'])
def register():
    data = request.form
    username = data.get('username')
    email = data.get('email')
    pwd = data.get('password')
    pw_hash = generate_password_hash(pwd)
    u = User(username=username, email=email, password_hash=pw_hash)
    db.session.add(u)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', 'pharmacy.db')
    if not os.path.exists(db_path):
        db.create_all()
    app.run(debug=True)
