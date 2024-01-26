from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder.compact = False  # Corrected attribute name

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()  # Corrected method name 'query()' to 'query.all()'
    
    bakery_list = [bakery.to_dict() for bakery in bakeries]  # Convert each Bakery object to a dictionary
    
    response = make_response(
        jsonify(bakery_list),
        200
    )
    response.headers["Content-Type"] = "application/json"
    
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)  # Corrected method name 'query()' to 'query.get()'
    
    if bakery:
        bakery_dict = bakery.to_dict()
        
        response = make_response(
            jsonify(bakery_dict),
            200
        )
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        return 'Bakery not found', 404

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()

    baked_goods_list = [baked_good.to_dict() for baked_good in baked_goods]

    response = make_response(
        jsonify(baked_goods_list),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
     
    prices = [baked_good.price for baked_good in most_expensive_good]

    highest_price = max(prices)
    
    
    response = make_response(
        jsonify(highest_price.to_dict()),
        200
    )

    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
