import os 
from flask_migrate import Migrate 
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import sqlalchemy
#=======================
#App Config
#======================

database_path = 'postgresql://postgres:7Pillars@localhost:5432/capstone'
db = SQLAlchemy()

def setup_db(app, db_path = database_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app 
    migrate = Migrate(app,db)
    db.create_all()



    #====================================
    #Models
    #===================================
    class Movies(db.model):

        __tablename__ = 'movies'
        id = Column(Integer, primary_key=True)
        title = Column(db.String(120), index = True)
        runtime = Column(db.Ineger())
        genre = Column(db.String(120))
        release_date = Column(db.Integer())
        actors = db.relationship("Actors", backref="movies")

        def __init__(self, title, runtime, genre, release_date):

            self.title = title
            self.runtime = runtime
            self.genre = genre 
            self.release_date = release_date

        def insert(self):
            db.session.add(self)
            db.session.commit()
        
        def update(self):
            db.session.commit()

        def delete(self):
            db.session.delete(self)
            db.session.commit()

        def format(self):
            return{
                'id': self.id,
                'runtime': self.runtime,
                'genre': self.genre,
                'release_date': self.release_date,
                'actors': [actor.id for actor in self.actors]
            }


    class Actors(db.model):
        
        __tablename__  = 'actprs'
        id = Column(Integer, primary_key=True)
        name = Column(db.String(120))
        age = Column(db.Integer())
        gender = Column(db.String(1))
        movies = db.relationship("Movies", backref="actors")

        def __init__(self, name, age, gender):

            self.name = name
            self.age = age
            self.gender = gender

        def insert(self):
            db.session.add(self)
            db.session.commit()
        
        def update(self):
            db.session.commit()

        def delete(self):
            db.session.delete(self)
            db.session.commit()

        def format(self):

            return {
                'id': self.id,
                'name': self.name,
                'age': self.age,
                'gender': self.gender,
                'movies': [movie.id for movie in self.movies]
            }

            

        class Casting(db.model):

            __tablename__ = 'casting'
            Actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), primary_key=True)
            Movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
