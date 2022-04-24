from models.db import db
from models.mindmap import MindMap
from models.node import Node
from sqlalchemy.exc import IntegrityError

class MindMapController:
    def get_map_by_name(map_name) -> MindMap:
        map = MindMap.query.filter(MindMap.map_name == map_name).first()
        if map == None:
            raise MindMapControllerError("MindMap does not exist", map_name)
        return map


    def create_mind_map(map_name) -> MindMap:
        try:
            map = MindMap(map_name=map_name)
            root = map.create_root_node()
            db.session.add(map)
            db.session.add(root)
            db.session.commit()
            return map
        except IntegrityError as e:
            raise MindMapControllerError("Could not create Mind Map", map_name) from e

    def add_node(map_name, node_path, node_name):
        map = MindMapController.get_map_by_name(map_name)
        map.add_node_to_path(MindMapController.normalize_path(node_path), node_name)
    
    def get_node_by_path(map_name, node_path) -> Node:
        map = MindMapController.get_map_by_name(map_name)
        node = map.find_node(MindMapController.normalize_path(node_path))
        return node

    # This method normalize paths by remove starting and trailing /
    def normalize_path(path) -> str:
        new_path = path
        if path[0] == '/':
            new_path = path[1:]
        if path[-1] == '/':
            new_path = new_path[:-1]
        return new_path


class MindMapControllerError(Exception):
    def __init__(self, message, map_name):
        self.message = message
        self._map_name = map_name
        super().__init__(self.message)
        
    def __str__(self):
        if self._map_name == None:
            return "Error occurred with mindmap: None"
        return "Error occurred with mindmap: " + self._map_name