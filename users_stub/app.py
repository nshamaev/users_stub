import json
from sys import maxsize
from flask import Flask, jsonify
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'users'
app.config['MONGO_HOST'] = 'db'

mongo = PyMongo(app)


@app.route('/users/<user_id>')
def get_user(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return json.dumps({"error": "User id should be integer type"}), 400
    if user_id > maxsize or user_id < -maxsize:
        return json.dumps({"error": "User id can not be greater than %d" % maxsize}), 400
    user = mongo.db.users.find_one_or_404({'id': user_id}, {'_id': False})
    return json.dumps(user, ensure_ascii=False)


if __name__ == '__main__':
    app.run()