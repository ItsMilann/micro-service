from dataclasses import dataclass
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
from sqlalchemy import UniqueConstraint

from producer import publish


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/admin'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)

db = SQLAlchemy(app)

@dataclass
class  Product(db.Model):
    id:int
    title:str
    image:str
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))



@dataclass
class ProductUser(db.Model):
    id:int
    user_id:int
    product_id:int
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/')
def index():
    return jsonify(Product.query.all())


@app.route('/<int:id>/like/', methods=["GET"])
def like(id):
    res = requests.get("http://host.docker.internal:8000/api/users")
    if res.status_code not in range(200, 300):
        return {"message": "Something went wrong."}
    try:
        data = res.json()
        product_user = ProductUser(user_id=data["user"], product_id=id, id=data["user"]+id)
        db.session.add(product_user)
        db.session.commit()
        publish("product_liked", id)
        return {"message": "Product liked!"}
    except Exception as e:
        raise e
        # return {"message": "Already liked!"}
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
