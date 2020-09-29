import os
import shelve
# Import the framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# Create an instance of Flask
app = Flask(__name__)
#app.config["DEBUG"] = True
# Create the API
api = Api(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("AllFillings.db")
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
  return "test"

class GetFilling(Resource):
    def get(self, identifier):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (identifier in shelf):
            return {'message': 'Record not found', 'data': {}}, 404

        return {'message': 'Record found', 'data': shelf[identifier]}, 200

class Create(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('unique_id', required=True)
        parser.add_argument('link')
        parser.add_argument('user')
        parser.add_argument('stockCodes')
        parser.add_argument('row_id')
        parser.add_argument('order_id')
        parser.add_argument('created_date')
        # Parse the arguments into an object
        args = parser.parse_args()
        shelf = get_db()
        shelf[args['identifier']] = args

        return {'message': 'Record Created', 'data': args}, 201
    
api.add_resource(Create, '/createfilling')    
api.add_resource(GetFilling, '/filing/<string:identifier>')
