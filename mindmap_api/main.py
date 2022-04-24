from flask import Flask, request, jsonify

from models.db import db
from models.mindmap import MindMap
from models.node import Node
from controller import MindMapController

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
    raw_json = request.get_json()
    node_path = raw_json['path']
    node_name = raw_json['text']

    MindMapController.add_node(map_name, node_path, node_name)

    return "OK.", 201 

@app.get("/map/<map_name>/node/<path:node_path>")
def get_node(map_name, node_path):    
    node = MindMapController.get_node_by_path(map_name, str(node_path)) 

    return node.get_json(), 201 

@app.get("/map/<map_name>/print")
def pretty_print(map_name):
    map = MindMapController.get_map_by_name(map_name)    
    
    str = map.pretty_print()
    print(str)

    return str, 201 

@app.post("/map")
def add_mind_map():
    if request.is_json:
        raw_json = request.get_json()
        # Using map_name to avoid confusion with database IDs
        map_name = raw_json['id']

        MindMapController.create_mind_map(map_name)
        return map_name, 201
    return {"error": "Request must be JSON"}, 415

with app.app_context():
    # TODO: add ability to NOT create tables
    db.create_all()