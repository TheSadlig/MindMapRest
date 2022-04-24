from flask import Flask, request, jsonify

import unittest

from models.db import db
from models.mindmap import MindMap
from models.node import Node, NodeError
from controller import MindMapController, MindMapControllerError

class testMindMapController(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///unittest.sqlite"
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def test_normalize_path(self):
        # No change
        res = MindMapController.normalize_path('i/like')
        self.assertEqual(res, 'i/like')

        # remove trailing /
        res = MindMapController.normalize_path('i/like/')
        self.assertEqual(res, 'i/like')
        
        # remove starting /
        res = MindMapController.normalize_path('/i/like')
        self.assertEqual(res, 'i/like')

        # remove starting and trailing /
        res = MindMapController.normalize_path('/i/like/')
        self.assertEqual(res, 'i/like')


    def test_mindmap_creation_success(self):
        with self.app.app_context():
            map_name = 'test'
            MindMapController.create_mind_map(map_name)
            
            map = MindMapController.get_map_by_name(map_name)
            self.assertEqual(map.map_name, map_name)
            self.assertEqual(map.root_node_id, 1)
            self.assertEqual(map.root_node.node_name, 'root')
            self.assertEqual(map.root_node.parent_node, None)

    def test_mindmap_creation_existing(self):
        with self.app.app_context():
            map_name = 'test'
            MindMapController.create_mind_map(map_name)
            self.assertRaises(MindMapControllerError, MindMapController.create_mind_map, map_name)
    
    def test_mindmap_creation_null_name(self):
        with self.app.app_context():
            map_name = None
            self.assertRaises(MindMapControllerError, MindMapController.create_mind_map, map_name)
    
    def test_node_insertion_simple_success(self):
        with self.app.app_context():
            map_name = 'test'
    
            map = MindMapController.create_mind_map(map_name)            
            MindMapController.add_node(map_name, '/', 'i')
            n = MindMapController.get_node_by_path(map_name, 'i')
            self.assertEqual(n.node_name, 'i')
            n = MindMapController.get_node_by_path(map_name, 'i/')
            self.assertEqual(n.node_name, 'i')


    def test_node_insertion_multiple_success(self):
        with self.app.app_context():
            map_name = 'test'
            map = MindMapController.create_mind_map(map_name)            
            MindMapController.add_node(map_name, '/', 'i')
            MindMapController.add_node(map_name, 'i', 'like')

            # Branch 1 
            MindMapController.add_node(map_name, 'i/like', 'sushis')
            MindMapController.add_node(map_name, 'i/like/sushis', 'very')
            MindMapController.add_node(map_name, 'i/like/sushis/very', 'much')

            # Branch 2  
            MindMapController.add_node(map_name, 'i/like', 'chicken')
            MindMapController.add_node(map_name, 'i/like/chicken', 'a')
            MindMapController.add_node(map_name, 'i/like/chicken/a', 'bit')


            n = MindMapController.get_node_by_path(map_name, 'i')
            self.assertEqual(n.node_name, 'i')
            n = MindMapController.get_node_by_path(map_name, '/i/like')
            self.assertEqual(n.node_name, 'like')
            
            # Branch 1
            n = MindMapController.get_node_by_path(map_name, '/i/like/sushis')
            self.assertEqual(n.node_name, 'sushis')
            n = MindMapController.get_node_by_path(map_name, '/i/like/sushis/very')
            self.assertEqual(n.node_name, 'very')
            n = MindMapController.get_node_by_path(map_name, '/i/like/sushis/very/much')
            self.assertEqual(n.node_name, 'much')

            # Branch 2
            n = MindMapController.get_node_by_path(map_name, '/i/like/chicken')
            self.assertEqual(n.node_name, 'chicken')
            n = MindMapController.get_node_by_path(map_name, '/i/like/chicken/a')
            self.assertEqual(n.node_name, 'a')
            n = MindMapController.get_node_by_path(map_name, '/i/like/chicken/a/bit')
            self.assertEqual(n.node_name, 'bit')


    def test_map_pretty_print(self):
        with self.app.app_context():
            map_name = 'test'
            map = MindMapController.create_mind_map(map_name)            
            MindMapController.add_node(map_name, '/', 'start')
            MindMapController.add_node(map_name, 'start', 'a')
            MindMapController.add_node(map_name, 'start', 'b')
            MindMapController.add_node(map_name, 'start/a', '1')
            MindMapController.add_node(map_name, 'start/b', '2')
            map_print = map.pretty_print()
            self.assertEqual(map_print, 
            '''root/
    start/
        a/
            1
        b/
            2
''')


    def test_node_simple_absent(self):
        with self.app.app_context():
            map_name = 'test'
            node_name = 'i'
            map = MindMapController.create_mind_map(map_name)    
            self.assertRaises(NodeError, MindMapController.get_node_by_path, map_name, node_name)

