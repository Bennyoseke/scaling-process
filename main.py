import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):  # This is a dictionary comprehension function created inside the Cafe class definition. It will be used to turn rows into a dictionary before sending it to jsonify.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}



with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random")
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe={
        "id": random_cafe.id,
        "name": random_cafe.name,
        "map_url": random_cafe.map_url,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,
        "seats": random_cafe.seats,
        "has_toilet": random_cafe.has_toilet,
        "has_wifi": random_cafe.has_wifi,
        "has_sockets": random_cafe.has_sockets,
        "can_take_calls": random_cafe.can_take_calls,
        "coffee_price": random_cafe.coffee_price,
    })

@app.route("/all")
def all():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    cf = [
        {"id": cafe.id, "name": cafe.name, "map_url": cafe.map_url, "img_url": cafe.img_url, "location": cafe.location,
         "seats": cafe.seats, "has_toilet": cafe.has_toilet, "has_wifi": cafe.has_wifi, "has_sockets": cafe.has_sockets,
         "can_take_calls": cafe.can_take_calls, "coffee_price": cafe.coffee_price, } for cafe in all_cafes]
    # This uses a List Comprehension but you could also split it into 3 lines.
    return jsonify(cafes = cf)

@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


@app.route("/search/")
def search():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(cafes = [each.to_dict() for each in all_cafes])
    else:
        return jsonify(error = {"Not Found": "Sorry, we don't have a cafe at that location."}), 404


@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.get_or_404(Cafe, cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response = {"success": "Successfully updated the price."}), 200
    else:
        # 404 = Resource not found
        return jsonify(error = {"Not Found": "Sorry a cafe with that id was not found in the database."}), 404

API_KEY = "TopSecretAPIKey"

@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def report_closed(cafe_id):
    api_key = request.args.get("api-key")
    cafe = db.get_or_404(Cafe, cafe_id)
    if cafe:
        if api_key == API_KEY:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response = {"success": "Successfully deleted the cafe."}), 200
        else:
            return jsonify(error = {"Sorry that's not allowed. Make sure you hav the right api key."}), 403
    else:
        return jsonify(error = {"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


URL = https://documenter.getpostman.com/view/29543460/2s9YBz1a9v


## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record



if __name__ == '__main__':
    app.run(debug=True)
