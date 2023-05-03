import uuid
from flask import Flask, render_template, request, jsonify, abort
import json
from models.list import List, NewListDto
from models.entry import Entry, NewEntryDto

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

def write_json(objectToJson):
    return json.dumps(objectToJson, indent=4, cls=CustomEncoder)

# initialisiere Flask-Server
app = Flask(__name__)

user_id = str(uuid.uuid4())

todo_list_1 = List('f5ab07ac-e375-4d50-be64-87ec2bb5eb6a', 'Liste Eins')
todo_list_2 = List('cdd8b065-b318-40d3-8628-cc2a96d10b0e', 'Liste Zwei')
todo_1 = Entry('f5ab07ac-e375-4d50-be64-cc2a96d10b0e',
               'Eintrag Eins', 'Example Text One', user_id, todo_list_1.id)
todo_2 = Entry('cdd8b065-b318-40d3-8628-87ec2bb5eb6a',
               'Eintrag Zwei', 'Example Text Two', user_id, todo_list_2.id)

list_store = [todo_list_1, todo_list_2]
entry_store = [todo_1, todo_2]

# f = open("data.json", "r")
# data_store = json.load(f)
# f.close()

@app.route('/todo-list', methods=['GET', 'POST'])
def get_all_lists():
    match request.method:
        case 'GET':
            return write_json(list_store)
        case 'POST':
            data = request.get_json()
            new_list = List(str(uuid.uuid4()), data['name'])
            list_store.append(new_list)
            return write_json(new_list)


@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE', 'PATCH'])
def get_list(list_id):
    selected_list = None

    for list in list_store:
        if list.id == list_id:
            selected_list = list

    if selected_list == None:
        abort(404)

    match request.method:
        case 'GET':
            entries = []
            for entry in entry_store:
                if entry.list_id == list_id:
                    entries.append(entry)
            return write_json(entries)
        case 'DELETE':
            list_store.remove(selected_list)
        case 'PATCH':
            data = request.get_json()
            selected_list.name = data['name']
            return write_json(selected_list)
        case _:
            return '', 500
    
    return '', 200


@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def post_new_entry(list_id):
    data = request.get_json()
    
    new_entry = Entry(str(uuid.uuid4()), data['name'], data['description'], '', list_id)
    entry_store.append(new_entry)
    
    return write_json(new_entry)


@app.route('/entry/<entry_id>', methods=['PATCH', 'DELETE'])
def update_entry(entry_id):
    
    entry = None
    for l in entry_store:
        if l.id == entry_id:
            entry = l

    if entry == None:
        return '', 404
    
    match request.method:
        case 'PATCH':
            data = request.get_json()
            entry.name = data['name']
            entry.description = data['description']
        case 'DELETE':
            entry_store.remove(entry)
            return write_json({'deleted': True}), 200
        case _:
            return '', 500
            
    return write_json(entry), 200


if __name__ == '__main__':
    # starte Flask-Server
    app.run(host='0.0.0.0', port=4200)
