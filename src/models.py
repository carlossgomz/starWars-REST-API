from flask_sqlalchemy import SQLAlchemy
from enum import Enum, unique

db = SQLAlchemy()

class Nature(Enum):
    people="people",
    planets="planets"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(100), nullable=False)

    favorites = db.relationship("Favorites", backref="user", uselist=True)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "email": self.email
        }

class People(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False, unique=True)
    age=db.Column(db.String(100), nullable=False)
    gender=db.Column(db.String(100), nullable=False)
    height=db.Column(db.String(100), nullable=False)
    birth_year=db.Column(db.String(100), nullable=False)
    eye_color=db.Column(db.String(100), nullable=False)
    hair_color=db.Column(db.String(100), nullable=False)
    skin_color=db.Column(db.String(100), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "gender":self.gender,
            "age":self.age,
            "birth_year": self.birth_year,
            "hair_color":self.hair_color,
            "height":self.height,
            "eye_color":self.eye_color,            
            "skin_color":self.skin_color
        }



class Planet(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False, unique=True)
    climate=db.Column(db.String(100), nullable=False)
    orbital_period=db.Column(db.String(100), nullable=False)
    rotation_period=db.Column(db.String(100), nullable=False)
    population=db.Column(db.String(100), nullable=False)
    diameter=db.Column(db.String(100), nullable=False)


    def serialize(self):
        return{
            "id":self.id,
            "name":self.name,
            "climate":self.climate,
            "rotation_period":self.rotation_period,
            "population":self.population,
           "orbital_period":self.orbital_period,
           "diameter":self.diameter
        }

class Favorites(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(250), nullable=False)
    nature=db.Column(db.Enum(Nature), nullable=False)
    nature_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "nature": self.nature.name,
            "nature_id": self.nature_id
        }