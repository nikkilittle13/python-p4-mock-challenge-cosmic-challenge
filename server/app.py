#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/scientists', methods=['GET', 'POST'])
def scientists():
    if request.method == 'GET':
        scientists = []
        for scientist in Scientist.query.all():
            scientist_dict = {
                "id": scientist.id,
                "name": scientist.name,
                "field_of_study": scientist.field_of_study
            }
            scientists.append(scientist_dict)

        return make_response(jsonify(scientists), 200)
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            new_scientist = Scientist(
                name=data.get('name'),
                field_of_study=data.get('field_of_study')
            )
            db.session.add(new_scientist)
            db.session.commit()
            return make_response(new_scientist.to_dict(), 201)
        except:
            return make_response(jsonify({"errors": ["validation errors"]}), 400)

@app.route('/scientists/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def scientist_by_id(id):
    scientist = Scientist.query.filter(Scientist.id==id).first()

    if not scientist:
        return make_response(jsonify({"error": "Scientist not found"}), 404)
    
    elif request.method == 'GET':
        return make_response(scientist.to_dict(), 200)
    
    elif request.method == 'DELETE':
        db.session.delete(scientist)
        db.session.commit()
        return make_response({}, 204)
    
    elif request.method == 'PATCH':
        try:
            data = request.get_json()
            for attr, value in data.items():
                setattr(scientist, attr, value)

            db.session.add(scientist)
            db.session.commit()

            return make_response(scientist.to_dict(), 202)

        except:
            return make_response(jsonify({"errors": ["validation errors"]}), 400)
        
@app.route('/planets')
def planets():
        planets = []
        for planet in Planet.query.all():
            planet_dict = {
                "id": planet.id,
                "name": planet.name,
                "distance_from_earth": planet.distance_from_earth,
                "nearest_star": planet.nearest_star
            }
            planets.append(planet_dict)
        
        return make_response(jsonify(planets), 200)

@app.route('/missions', methods=['GET', 'POST'])
def missions():
    if request.method == 'POST':
        try:
            data = request.get_json()
            new_mission = Mission(
                name=data.get('name'),
                scientist_id=data.get('scientist_id'),
                planet_id=data.get('planet_id')
            )
            db.session.add(new_mission)
            db.session.commit()

            return make_response(new_mission.to_dict(), 201)
        
        except:
            return make_response(jsonify({"errors": ["validation errors"]}), 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
