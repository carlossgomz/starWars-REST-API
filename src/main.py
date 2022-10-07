"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
# from crypt import methods
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorites
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
db_url = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
    "postgres://", 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)



## GET para todos los personajes, para traerlos por id ##
@app.route('/people', methods=['GET'])
@app.route('/people/<int:people_id>', methods=['GET'])
def handle_people(people_id=None):
    if request.method == 'GET':
        if people_id == None:
            people = People()
            people = people.query.all()
            return jsonify(list(map(lambda item: item.serialize(), people)), 200)
        else:
            people = People()
            people = people.query.get(people_id)
            if people:
                return jsonify(people.serialize())

        return jsonify({"Not found"}), 404



### GET para todos los planetas y para traer planetas por id###
@app.route('/planets', methods=['GET'])
@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_planet(planet_id=None):
    if request.method == 'GET':
        if planet_id == None:
            planet = Planet()
            planet = planet.query.all()
            return jsonify(list(map(lambda item: item.serialize(), planet)), 200)
        else:
            planet = Planet()
            planet = planet.query.get(planet_id)
            if planet:
                return jsonify(planet.serialize())

        return jsonify({"Not found"}), 404



## GET para traer los usuarios##
@app.route('/users', methods=['GET'])
def handle_user(user_id=None, nature=None, favorite_id=None):
    if request.method == 'GET':
        if user_id == None:
            user = User.query.all()
            return jsonify(list(map(lambda item: item.serialize(), user)), 200)
    return jsonify({"Not found"}),404



## GET para traer el usuario por su id correspondiente###
@app.route('/users/<int:user_id>', methods=['GET'])
def handle_user_id(user_id=None, nature=None, favorite_id=None):
    if request.method == 'GET':
        if user_id is not None:
            user=User()
            user=User.query.get(user_id)
            if user:
                return jsonify(user.serialize(), 200)
    return jsonify({"Not found"}),404



## para traer toda la lista de favoritos de los usuarios ##
@app.route('/users/favorite', methods=['GET'])
def handle_users_favorites():
    if request.method == 'GET':
        favorites = Favorites()
        favorites=Favorites.query.all()
        return jsonify(list(map(lambda items: items.serialize(), favorites))), 200
    else: 
        return jsonify({"Method not allowed"}),405



## para traer los favoritos de un usuario##
@app.route('/users/<int:user_id>/favorite', methods=['GET'])
def handle_user_favorite(user_id=None):
    if request.method == 'GET':
        if user_id is not None:
            favorites=Favorites.query.filter_by(user_id=user_id).all()
        return jsonify(list(map(lambda items: items.serialize(), favorites))), 200
    return jsonify({"Not found"}),404



### para hacer post de un favorito por su naturaleza###
@app.route('/users/<int:user_id>/favorite/<string:nature>/<int:nature_id>', methods=['POST'])
def handle_favorite_post(user_id = None, nature = None, nature_id=None):
    if request.method == 'POST':
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"message":"Error, couldn't find user"}), 404
        elif user:
            body = request.json
            if nature is not None and body['name'] is not None:
                another_fav = Favorites(name=body['name'], nature=nature, nature_id=body.get("nature_id"), user_id=user_id)
                db.session.add(another_fav)
            try:
                db.session.commit()
                return jsonify(another_fav.serialize()), 201
            except Exception as error:
                    print(error.args)
                    db.session.rollback()
                    return jsonify({"message": f"Error {error.args}"}), 500
    else: 
        return jsonify({"Method not allowed"}),405



### DELETE de un favorito segun su naturaleza ##
@app.route("/<int:user_id>/favorite/<string:nature>/<int:nature_id>/", methods=['DELETE'])
def handle_favorite_delete(nature_id = None, nature=None, user_id=None):
    if request.method == 'DELETE':
        body = request.json
        if body.get("nature") == "people" or body["nature"] == "planets":
            if nature_id:
                delete_favorito = Favorites.query.filter_by(nature_id=nature_id, user_id= user_id).first()
                print(delete_favorito.serialize())
                if delete_favorito is None:
                    return jsonify({"message":"Not found"}), 404
                else:
                    db.session.delete(delete_favorito)
                    try:
                        db.session.commit()
                        return jsonify([]), 204
                    except Exception as error:
                        print(error.args)
                        db.session.rollback()
                        return jsonify({"message":f"Error {error.args}"}),500
    else: 
        return jsonify({"Method not allowed"}),405





# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)