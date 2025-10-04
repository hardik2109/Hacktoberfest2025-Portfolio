# app.py
from flask import Flask, jsonify, request, abort
app = Flask(__name__)
todos = {}
next_id = 1

@app.route('/todos', methods=['GET'])
def list_todos():
    return jsonify(list(todos.values()))

@app.route('/todos', methods=['POST'])
def create_todo():
    global next_id
    data = request.json or {}
    if 'title' not in data:
        abort(400, 'title required')
    todo = {"id": next_id, "title": data['title'], "done": False}
    todos[next_id] = todo
    next_id += 1
    return jsonify(todo), 201

@app.route('/todos/<int:tid>', methods=['PUT'])
def update_todo(tid):
    if tid not in todos:
        abort(404)
    data = request.json or {}
    todos[tid].update({k: data[k] for k in ('title','done') if k in data})
    return jsonify(todos[tid])

@app.route('/todos/<int:tid>', methods=['DELETE'])
def delete_todo(tid):
    todos.pop(tid, None)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)
