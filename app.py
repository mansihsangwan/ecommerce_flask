# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    price = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }

@app.route('/product', methods=['POST'])
def add_product():
    # Bug: No data validation
    print(request.json)
    new_product = Product(name=request.json['name'], price=request.json['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict())

@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    # Bug: Incorrect SQL query
    product = Product.query.filter_by(name=id).first()
    return jsonify(product.to_dict())

@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    # Bug: Wrong route method
    product = Product.query.get(id)
    product.name = request.json['name']
    product.price = request.json['price']
    db.session.commit()
    return jsonify(product.to_dict())

@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    # Bug: No error handling for non-existing product
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)