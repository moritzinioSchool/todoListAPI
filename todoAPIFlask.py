import uuid

from flask import Flask, jsonify, request, abort

# initialize Flask server
app = Flask(__name__)

#create unique id for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = uuid.uuid4()
todo_2_id = uuid.uuid4()
todo_3_id = uuid.uuid4()
todo_4_id = uuid.uuid4()

# define internal data structures with example data
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
    {'id': todo_3_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id},
]

# GET single ToDo-list by UUID
@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE'])
def get_list(list_id):
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    if not list_item:
        abort(404)
    if request.method == 'GET':
        print('Returning todo list...')
        return jsonify([i for i in todos if i['list'] == list_id])
    elif request.method == 'DELETE':
        # delete list with given id
        print('Deleting todo list...')
        todo_lists.remove(list_item)
        return '', 200

# POST single ToDo-List
@app.route('/todo-list', methods=['POST'])
def add_new_todoList():
    new_list = request.get_json(force=True)
    print('Got new list to be added: {}'.format(new_list))
    new_list['id'] = uuid.uuid4()
    todo_lists.append(new_list)
    return jsonify(new_list), 200

# POST a single entry onto ToDo-List
@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def add_entry(list_id):
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    if not list_item:
        abort(404)
    new_entry = request.get_json(force=True)
    list_item.append(new_entry)
    return jsonify(list_item), 200

# UPDATE list entry
@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT'])
def update_entry(list_id, entry_id):
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    if not list_item:
        abort(404)
    entry_item = None
    for e in list_item:
        if e['id'] == entry_id:
            entry_item = e
            e = request.get_json(force=True)
            break
    if not entry_item:
        abort(404)
    return jsonify(list_item)

# DELETE single entry
@app.route('/todo-list/<list_id>/entry/<entry_id>/delete', methods=['DELETE'])
def delete_entry(list_id, entry_id):
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    if not list_item:
        abort(404)
    entry_item = None
    for e in list_item:
        if e['id'] == entry_id:
            entry_item = e
            list_item.remove(entry_item)
            break
    if not entry_item:
        abort(404)
    return '', 200

if __name__ == '__main__':
    app.run(debug=True)
