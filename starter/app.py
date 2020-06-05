import os
from flask import Flask, request, abort, jsonify, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Movies, Actors, setup_db, db
import json 
from auth import AuthError, requires_auth, get_token_auth_header

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app)

  cors = CORS(app, resources={r"/api/":{"origins": "*"}})

  '''CORS request set up
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Acccess-Control-Allow-Headers', 'GET, POST, DELETE, PATCH, OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*')

  @app.route('/homepage', methods=["GET"])
  def homepage():
    return render_template("index.html")

  @app.route('/actors')
  @requires_auth('get:actors')
  def actors():
    actors = Actors.query.all()
    formatted_actor = [actor.format() for actor in actors]
    return jsonify({
      'success':True,
      'actors': formatted_actor,
      'total_actors': len(formatted_actor)
    })

  @app.route('/movies')
  @requires_auth('get:movies')
  def movies():
    movies = Movies.query.all()
    formatted_movie = [movies.format() for movie in movies]
    return jsonify({
      'success':True,
      'movies': formatted_movie,
      'total_movie': len(formatted_movie)
    })

  @app.route('/actor/<int:actor_id>', mehtods =['DELETE'])
  @requires_auth('delete:actors')
  def del_actor(actor_id):
    del_actor = Actors.query.get(actor_id)
    if not del_actor:
      abort(404)
    try:
      del_actor.delete()
    except:
      del_actor.rollback()
      abort(422)

    return jsonify({
      'success': True,
      'deleted':actor_id
    }), 200


    @app.route('/movies/<int:movie_id>', methods = ["DELETE"])
    @requires_auth('delete:movies')
    def del_movies(movie_id):
      del_movie = Movies.query.get(movie_id)
      if not del_movie:
        abort(404)
      try:
        del_actor.delete()
      except:
        del_actor.rollback()
        abort(422)

      return jsonify({
        'success':True,
        'deleted': movie_id
      })

    @app.route('/actors', methods =["POST"])
    @requires_auth('post:actors')
    def add_actors():
      body = request.get_json()
      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)

      actors = Actors(
        name = name, 
        age = age, 
        gender = gender
      )

      actors.insert()
      formatted_actor = [actor.format() for actor in actors]
      return jsonify({
        'success': True,
        'actors': formatted_actor,
        'total_actors': len(formatted_actor)
      })

    @app.route('/movies', methods = ['POST'])
    @requires_auth('post:movies')
    def add_movies():
      body = request.get_json()
      title = request.get_json()
      runtime = request.get_json()
      release = request.get_json()

      movies = Movies(
        title = title,
        runtime = runtime,
        relase = release
      )

      movies.insert()
      formatted_movie = [movie.format() for movie in movies]

      return jsonify({
        'success': True,
        'movies': formatted_movie,
        'total_movies': len(formatted_movie)
      })


    @app.route('/actors<int:actors_id>', methods =["PATCH"])
    @requires_auth('patch:actors')
    def update_actors(actors_id):
      selected_actor = Actors.query.filter(Actors.id == actors_id).one_or_none()
      if selected_actor is None:
        abort(404)
      body = request.get_json()
      selected_actor.name = body.get('name', selected_actor.name)
      selected_actor.age = body.get('age', selected_actor.age)
      selected_actor.gender = body.get('gender', selected_actor.gender)
      selected_actor.update()

      actors = Actors.query.all()
      formatted_actor = [selected_actor.format() for actor in actors]

      return jsonify({
        'success': True,
        'actors': formatted_actor,
        'updated_actor': actors_id
      })

    @app.route('/movies<int:movies_id>', methods =["PATCH"])
    @requires_auth('patch:movies')
    def update_movie(movies_id):
      selected_movie = Movies.query.filter(Movies.id == movies_id).one_or_none()
      if selected_movie is None:
        abort(404)
      body = request.get_json()
      selected_movie.name = body.get('name', selected_movie.name)
      selected_movie.age = body.get('age', selected_movie.age)
      selected_movie.gender = body.get('gender', selected_movie.gender)
      selected_movie.update()

      movies = Movies.query.all()
      formatted_movie = [selected_movie.format() for movie in movie]

      return jsonify({
        'success': True,
        'movies': formatted_movie,
        'updated_movie': movies_id
      })

    #====================================================
    # Error handlers 
    #====================================================

    @app.errorhandler(422)
    def unproccessable(error):
      return jsonify({
              "success": False,
              "error": 422,
              "message": "Unprocessable"
          }), 422


    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Resources not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad request"
        }), 400




  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)