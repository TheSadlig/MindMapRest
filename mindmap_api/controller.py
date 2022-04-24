from models.db import db
from models.mindmap import MindMap
from models.node import Node

class MindMapController:
    def get_map_by_name(map_name):
        map = MindMap.query.filter(MindMap.map_name == map_name).first()
        if map == None:
            raise MindMapApiError("MindMap does not exist", map_name)
        return map


    def create_mind_map(map_name):
        map = MindMap(map_name=map_name)
        root = map.create_root_node()
        db.session.add(map)
        db.session.add(root)
        db.session.commit()

    def add_node(map_name, node_path, node_name):
        map = MindMapController.get_map_by_name(map_name)
        map.add_node_to_path(node_path, node_name)
    
    def get_node_by_path(map_name, node_path):
        map = MindMapController.get_map_by_name(map_name)
        node = map.find_node(node_path)
        return node
