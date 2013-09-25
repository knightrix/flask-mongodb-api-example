from flask import Flask, jsonify, abort, make_response, request, Response
from flask.ext.pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId


app = Flask(__name__)
mongo = PyMongo(app)


def mongo_to_jsonResponse(mongobj):
    # dumps function convert mongo object into json
    js = dumps(mongobj)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/api/menus', methods=['GET'])
def get_tasks():
    # tasks_ids = mongo.db.tasks.insert(tasks)
    all_menus = mongo.db.menus.find()
    return mongo_to_jsonResponse(all_menus)


@app.route('/api/menus/<menu_id>', methods=['GET'])
def get_task(menu_id):
    #check if menu_id coming in from URL is a valid ObjectId format
    if (ObjectId.is_valid(menu_id)):
        menu = mongo.db.menus.find_one_or_404({'_id': ObjectId(menu_id)})
    else:
        abort(404)

    return mongo_to_jsonResponse(menu)


@app.route('/api/menus', methods=['POST'])
def create_task():
    if not request.json or not 'menu_name' in request.json:
        abort(400)
    menu = {
        'menu_name': request.json['menu_name'],
        'URL': request.json.get('URL', ""),
        'show_on_nav': request.json.get('show_on_nav', 0),
        'sort_order': request.json.get('sort_order', 99999999)

    }
    mongo.db.menus.insert(menu)
    return jsonify({'insert': 'success'}), 201


@app.route('/api/menus/<menu_id>', methods=['PUT'])
def update_task(menu_id):
    #check if menu_id coming in from URL is a valid ObjectId format
    if (ObjectId.is_valid(menu_id)):
        menu = mongo.db.menus.find_one_or_404({'_id': ObjectId(menu_id)})
    else:
        abort(404)

    if not request.json:
        abort(400)
    if 'menu_name' in request.json and type(request.json['menu_name']) != unicode:
        abort(400)

    mongo.db.menus.update({'_id': ObjectId(menu_id)},
        {"$set":{'menu_name': request.json.get('menu_name',menu['menu_name']),
               'URL': request.json.get('URL', menu['URL']),
               'show_on_nav': request.json.get('show_on_nav', menu['show_on_nav']),
               'sort_order': request.json.get('sort_order', menu['sort_order'])
    }})

    return jsonify({'update': 'success'})


@app.route('/api/menus/<menu_id>', methods=['DELETE'])
def delete_task(menu_id):
    #check if menu_id coming in from URL is a valid ObjectId format
    if (ObjectId.is_valid(menu_id)):
        mongo.db.menus.find_one_or_404({'_id': ObjectId(menu_id)})
    else:
        abort(404)
    mongo.db.menus.remove({'_id':ObjectId(menu_id)})
    return jsonify({'delete': 'success'})


@app.errorhandler(404)
def notfound(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)