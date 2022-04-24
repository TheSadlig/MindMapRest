from flask import Flask, request, jsonify

import unittest

from models.db import db
from models.mindmap import MindMap
from models.node import Node
from controller import MindMapController

class testMindMapController(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///unittest.sqlite"
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def test_mindmap_creation(self):
        with self.app.app_context():
            map_name = 'test'
            MindMapController.create_mind_map(map_name)
            
            map = MindMapController.get_map_by_name(map_name)
            self.assertEqual(map.map_name, map_name)
            self.assertEqual(map.root_node_id, 1)
            self.assertEqual(map.root_node.node_name, 'root')
            self.assertEqual(map.root_node.parent_node, None)


