from flask import Flask, request, jsonify

from models.db import db
from models.mindmap import MindMap
from models.node import Node

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.post("/map/<map_name>/node")
def add_node(map_name):
    map = MindMap.query.filter(MindMap.map_name == map_name).first()
    if map == None:
        raise MindMapApiError("MindMap does not exist", map_name)
    
    raw_json = request.get_json()
    node_path = raw_json['path']
    node_name = raw_json['text']
    map.add_node_to_path(node_path, node_name)

    return "OK.", 201 

@app.get("/map/<map_name>/node/<path:node_path>")
def get_node(map_name, node_path):
    print(str(node_path))
    map = MindMap.query.filter(MindMap.map_name == map_name).first()
    print(str(node_path))
    if map == None:
        raise MindMapApiError("MindMap does not exist", map_name)
    
    node = map.find_node(str(node_path))
    print(node.node_name)

    return node.get_json(), 201 

@app.get("/map/<map_name>/print")
def pretty_print(map_name):
    map = MindMap.query.filter(MindMap.map_name == map_name).first()
    if map == None:
        raise MindMapApiError("MindMap does not exist", map_name)
    
    map.pretty_print()

    return "OK.", 201 

@app.post("/map")
def add_mind_map():
    if request.is_json:
        raw_json = request.get_json()
        # Using map_name to avoid confusion with database IDs
        map_name = raw_json['id']
        map = MindMap(map_name=map_name)
        root = map.create_root_node()
        db.session.add(map)
        db.session.add(root)
        db.session.commit()
        return map_name, 201
    return {"error": "Request must be JSON"}, 415

class MindMapApiError(Exception):
    def __init__(self, message, mind_map_id):
        self.message = message
        self._mind_map_id = mind_map_id
        super().__init__(self.message)
        
    def __str__(self):
        return "Error occurred with mindmap: " + self._mind_map_id

with app.app_context():
    # TODO: add ability to NOT create tables
    db.create_all()