from flask import Flask, request, jsonify

import unittest

from main import app
from mindmap_api.models.db import db

# Unit testing HTTP codes from endpoints
class testMain(unittest.TestCase):
    
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///unittest.sqlite"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)
        with app.app_context():
            db.drop_all()
            db.create_all()
        self.app = app.test_client()
        
    def testIsAlive(self):
        response = self.app.get('/isalive')
        self.assertEqual(response.status_code, 418)

    def testCreateMapSuccessAndDuplicate(self):
        response = self.app.post('/map', json={'id':'test'})
        self.assertEqual(response.status_code, 201)

        response = self.app.post('/map', json={'id':'test'})
        self.assertEqual(response.status_code, 409)

    def testAddNodeSuccessAndDuplicate(self):
        self.app.post('/map', json={'id':'test'})
        response = self.app.post('/map/test/node', json={'path': '/','text': 'i'})
        self.assertEqual(response.status_code, 201)
        response = self.app.post('/map/test/node', json={'path': '/i','text': 'test'})
        self.assertEqual(response.status_code, 201)

        response = self.app.post('/map/test/node', json={'path': '/i','text': 'test'})
        self.assertEqual(response.status_code, 404)

    def testGetNodeSuccessAndNotFound(self):
        self.app.post('/map', json={'id':'test'})
        
        response = self.app.get('/map/test/node/i')
        self.assertEqual(response.status_code, 404)

        self.app.post('/map/test/node', json={'path': '/','text': 'i'})
        response = self.app.get('/map/test/node/i')
        self.assertEqual(response.status_code, 200)
    