#import grpc
#import myitems_pb2
#import myitems_pb2_grpc
import os
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

GRPC_HOST = os.getenv("GRPC_HOST", "localhost")
GRPC_PORT = os.getenv("GRPC_PORT", "50051")



# In-memory data store

items = []
next_id = 1

# Helper: Find item by id
def find_item(item_id):
    return next((item for item in items if item['id'] == item_id), None)

# GET /items - List all items
@app.route('/items', methods = ['GET'])
def get_items():
    return jsonify(items), 200

# GET /items/<id> - Retrieve specific item
@app.route('/items/<int:item_id>', methods = ['GET'])
def get_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item), 200

# POST /items - Create a new item (auto-increment the ID)
@app.route('/items', methods = ['POST'])
def create_item():
    global next_id
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    item = {'id': next_id, 'name': data['name']}
    items.append(item)
    next_id += 1
    return jsonify(item), 201

# PUT /items/<id> - Update an existing item
@app.route('/items/<int:item_id>', methods = ['PUT'])
def update_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    data =  request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    item['name'] = data['name']
    return jsonify(item), 200

# DELETE /items/<id> - Delete item
@app.route('/items/<int:item_id>', methods = ['DELETE'])
def delete_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}, 404)
    items.remove(item)
    return jsonify({'message': 'Item deleted'}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug = True)
