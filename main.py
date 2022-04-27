from flask import Flask, request, jsonify

from mindmap_api.models.db import db
from mindmap_api.models.mindmap import MindMap
from mindmap_api.models.node import Node
from mindmap_api.controller import MindMapController, MindMapControllerError

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from flask_sqlalchemy import SQLAlchemy

import json
import os

HTTP_CODE_OK = 200
HTTP_CODE_SUCCESS = 201
HTTP_CODE_NOT_FOUND = 404
HTTP_CODE_CONFLICT = 409
HTTP_CODE_WRONG_CONTENT = 415
HTTP_CODE_TEAPOT = 418


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.get("/isalive")
def isalive():
    return "The teapot is running", HTTP_CODE_TEAPOT

@app.post("/map/<map_name>/node")
def add_node(map_name):
    raw_json = request.get_json()
    node_path = raw_json['path']
    node_name = raw_json['text']

    try:
        node = MindMapController.add_node(map_name, node_path, node_name)
    except MindMapControllerError as e:
        return generate_exception('Could find Mind Map', e), HTTP_CODE_NOT_FOUND
    except NodeError as e:
        return generate_exception('Node path cannot be found', e), HTTP_CODE_NOT_FOUND
    
    return node.get_json(), HTTP_CODE_SUCCESS 

@app.get("/map/<map_name>/node/<path:node_path>")
def get_node(map_name, node_path): 
    try:
        node = MindMapController.get_node_by_path(map_name, str(node_path)) 
    except MindMapControllerError as e:
        return generate_exception('Could find Mind Map', e), HTTP_CODE_NOT_FOUND
    except NodeError as e:
        return generate_exception('Node path cannot be found', e), HTTP_CODE_NOT_FOUND

    return node.get_json(), HTTP_CODE_OK 

@app.get("/map/<map_name>/print")
def pretty_print(map_name):
    try:
        map = MindMapController.get_map_by_name(map_name)    
    except MindMapControllerError as e:
        return generate_exception('Could find Mind Map', e), HTTP_CODE_NOT_FOUND

    return map.pretty_print(), HTTP_CODE_OK 

@app.post("/map")
def create_mind_map():
    if request.is_json:
        raw_json = request.get_json()
        # Using map_name to avoid confusion with database IDs
        map_name = raw_json['id']

        try:
            map = MindMapController.create_mind_map(map_name)
            return map.get_json(), HTTP_CODE_OK
        except MindMapControllerError as e:
            return generate_exception('Could not create Mind Map', e), HTTP_CODE_CONFLICT

    return generate_exception('Request must be JSON'), HTTP_CODE_WRONG_CONTENT

def generate_exception(message, ex: None) -> str:
    if ex == None:
        return {'error': message}
    return {'error': message, 'exception': ex.message}

with app.app_context():
    # TODO: add ability to NOT create tables
    print(os.getenv('DATABASE_URI'))
    db.create_all()