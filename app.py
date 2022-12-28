from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
# import os
#C:\Users\damec\OneDrive\Desktop\react\DD-Delights\API

app = Flask(__name__)
CORS(app)

# comment just for git pus
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://jkljqovvxgepqa:ed24599588952b78c91d9eaee976162907a119e57d08bf6966144af73e33604d@ec2-52-203-118-49.compute-1.amazonaws.com:5432/deflp1naa9sq06"


db = SQLAlchemy(app)
ma = Marshmallow(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    item_name = db.Column(db.String, unique=True, nullable=False)
    item_price = db.Column(db.String, nullable=True)
    item_category = db.Column(db.String, nullable=True)
    item_img = db.Column(db.String, unique=True)

    def __init__(self, item_name, item_price, item_category, item_img):
        self.item_name = item_name
        self.item_price = item_price
        self.item_category = item_category
        self.item_img = item_img

class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'item_name', 'item_price', 'item_category', 'item_img')

item_schema = ItemSchema()
many_item_schema = ItemSchema(many=True)


#endpoints start
@app.route('/item/add', methods=["POST"])
def add_item():
    if request.content_type != 'application/json':
        return jsonify("Error: must be json")

    post_data = request.get_json()
    item_name = post_data.get('item_name')
    item_price = post_data.get('item_price')
    item_category = post_data.get('item_category')
    item_img = post_data.get('item_img')

    #for nullable variables
    if item_name == None:
        return jsonify('Error: Must define item_name')

    if item_price == None:
        return jsonify('Error: Must define item_price')

    new_item = Item(item_name, item_price, item_category, item_img)
    db.session.add(new_item)
    db.session.commit()

    return jsonify(item_schema.dump(new_item))


@app.route('/item/get')
def get_items():
    all_items = db.session.query(Item).all()
    return jsonify(many_item_schema.dump(all_items))

@app.route('/item/get/<id>')
def get_one_item(id):
    one_item = db.session.query(Item).filter(Item.id == id).first()
    return jsonify(item_schema.dump(one_item))

@app.route('/item/edit/<id>', methods=["PUT"])
def edit_item(id):
    if request.content_type != 'application/json':
        return jsonify('Error: must be json')

    put_data = request.get_json()
    item_name = put_data.get('item_name')
    item_price = put_data.get('item_price')
    item_category = put_data.get('item_category')
    item_img = put_data.get('item_img')

    edit_item = db.session.query(Item).filter(Item.id == id).first()

    if item_name != None:
        edit_item.item_name = item_name
    if item_price != None:
        edit_item.item_price = item_price
    if item_price != None:
        edit_item.item_category = item_category
    if item_img != None:
        edit_item.item_img = item_img

    db.session.commit()

    return jsonify(item_schema.dump(edit_item))

@app.route('/item/delete/<id>', methods=["DELETE"])
def delete_item(id):
    delete_item = db.session.query(Item).filter(Item.id == id).first()
    db.session.delete(delete_item)
    db.session.commit()

    return jsonify('Item deleted successfully.')

@app.route('/item/add/many', methods=["POST"])
def add_many_items():
    if request.content_type != "application/json":
        return jsonify("Error: send data as json to proceed")
    
    post_data = request.get_json()
    items = post_data.get('items')

    new_items = []
    
    for item in items:
        item_name = item.get('item_name')
        item_price = item.get('item_price')
        item_category = item.get('item_category')
        item_img = item.get('item_img')

        existing_item_check = db.session.query(Item).filter(Item.item_name == item_name).first()
        if existing_item_check is None:
            new_item = Item(item_name, item_price, item_category, item_img)
            db.session.add(new_item)
            db.session.commit()
            new_items.append(new_item)

    return jsonify(many_item_schema.dump(new_items))





if __name__ == '__main__':
    app.run(debug=True)