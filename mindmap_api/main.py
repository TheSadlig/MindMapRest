from flask import Flask, request, jsonify

from mindmap.mindmap import MindMap
from mindmap.node import Node

app = Flask(__name__)

maps = {}

@app.post("/map/<map_id>/leaf")
def add_leaf(map_id):
    if not map_id in maps:
        raise MindMapApiError("Mind map does not exist, please create it first", map_id)
    
    raw_json = request.get_json()
    leaf_name = raw_json['text']

    n = Node(leaf_name)
    return map_id, 201 

@app.post("/map")
def add_mind_map():
    if request.is_json:
        raw_json = request.get_json()
        request_id = raw_json['id']
        maps[request_id] = MindMap(request_id)

        return request_id, 201
    return {"error": "Request must be JSON"}, 415


class MindMapApiError(Exception):
    def __init__(self, mind_map_id):
        self._mind_map_id = mind_map_id
    
    def __str__(self):
        return "Error occurred with mindmap:" + self._mind_map_id