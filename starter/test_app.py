import os
import unittest
import json
from flask_sqlalchemy import flask_sqlalchemy

from app import create_app
from models import Movie, Actor, setup_db, db


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://postgres:7Pillars@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
        
    def tearDown(self):
        pass

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['total_actors']))

    def test_get_actors_fail(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertFalse(data['total__actors'])
        self.assertFalse(len(data['total_actors']))

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_movie'])
        self.assertTrue(len(data['total_movie']))

    def test_get_movies_fail(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertFalse(data['total__movie'])
        self.assertFalse(len(data['total_movie']))

    def test_delete_questions(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True )
        self.assertEqual(data['deleted'], 'Resource not Found')
    
    def test_delete_questions_fail(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['suuccess'])
        self.assertFalse(data['message'], 'Resources not found')

    def test_post_actors(self):
        res = self.client().post('/actors',
            json = {'name': 'Tom Cruise',
                    'age': '42',
                    'gender': 'M'
                    })
        data = json.loads(res.data)
        self.assertEqual (res.statsu_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))
    
    def test_post_actors_fail(self):
        res = self.client().post('/actors',
            json ={
                    'name': 'Brad Pitt',
                    'age':'47',
                    'gender':'M'
                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertFalse(data['total_actors'])
        self.assertFalse(len(data['actors']))

    def test_post_movie(self):
        res = self.client().post('/movies',
            json = {'title': 'Some movie',
                    'runtime': '2 hours',
                    'release_date': '2019'
                    })
        data = json.loads(res.data)
        self.assertEqual (res.statsu_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))
    
    def test_post_movie_fail(self):
        res = self.client().post('/movie',
            json ={
                    'title': 'Some movie 2',
                    'runtime': '1.5 hours',
                    'release':'2020'
                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertFalse(data['total_movies'])
        self.assertFalse(len(data['movies']))


    def test_patch_actors(self):
        res = self.client().patch('/actors/2',
            json = {'name': 'Peter Griffin',
                    'age': '40',
                    'gender': 'M'
                    })
        data = json.loads(res.data)
        self.assertEqual (res.statsu_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))
    
    def test_patch_actors_fail(self):
        res = self.client().patch('/actors/4',
            json ={
                    'name': 'Tyson Fury',
                    'age':'32',
                    'gender':'M'
                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertFalse(data['total_actors'])
        self.assertFalse(len(data['actors']))

    def test_patch_movie(self):
        res = self.client().patch('/movies/3',
            json = {'title': 'Raptors vs Tigers',
                    'runtime': '2 hours',
                    'release_date': '1988'
                    })
        data = json.loads(res.data)
        self.assertEqual (res.statsu_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))
    
    def test_patch_movie_fail(self):
        res = self.client().patch('/movie/6',
            json ={
                    'title': 'Ronald Mcdonald: The Movie',
                    'runtime': '1.5 hours',
                    'release':'2030'
                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertFalse(data['total_movies'])
        self.assertFalse(len(data['movies']))