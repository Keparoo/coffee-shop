import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

#----------------------------------------------------------------------------#
# App Config
#----------------------------------------------------------------------------#

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"*": {"origins": "*"}})

#----------------------------------------------------------------------------#
# Uncomment for first run.
# Comment out after DB is setup or the DB will be reset on each run.
#----------------------------------------------------------------------------#

db_drop_and_create_all()

#----------------------------------------------------------------------------#
# Routes
#----------------------------------------------------------------------------#

@app.route('/drinks', methods=['GET'])
def get_drinks():
  '''
  This endpoint handles GET requests to /drinks
  It is a public endpoint. 
  It returns a simple list of all drinks.
  '''
  drinks = Drink.query.all()
  
  if len(drinks) == 0:
    abort(404)

  return jsonify({
    'success': True,
    'drinks': [drink.short() for drink in drinks]
  })

@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_detail(jwt):
  '''
  This endpoint handles GET requests to /drinks-detail
  It requires the get:drinks-detail permission.
  It returns a list of all drinks and ingredients.
  '''
  drinks = Drink.query.all()
  
  if len(drinks) == 0:
    abort(404)

  return jsonify({
    'success': True,
    'drinks': [drink.long() for drink in drinks]
  })

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(jwt):
  '''
  This endpoint handles POST requests to /drinks
  It requires the post:drinks permission.
  It adds a new drink to the database.
  '''
  body = request.get_json()

  if 'title' and 'recipe' not in body:
    abort(422)

  title = body['title']
  recipe = json.dumps(body['recipe'])

  drink = Drink(title=title, recipe=recipe)
  drink.insert()

  return jsonify({
    'success': True,
    'drinks': [drink.long()]
  })

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, id):
  '''
  This endpoint handles PATCH requests to /drinks/<id>
  It requires the patch:drinks permission.
  It modifies a drink and updates the database.
  '''
  drink = Drink.query.get(id)

  if (drink == None):
    abort(404)
  
  body = request.get_json()

  if 'title' in body:
    drink.title = body['title']

  if 'recipe' in body:
    drink.recipe = json.dumps(body['recipe'])

  drink.update()

  return jsonify({
  'success': True,
  'drinks': [drink.long()]
})

@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
  '''
  This endpoint handles DELETE requests to /drinks/<id>
  It requires the delete:drinks permission.
  It deletes a drink from the database.
  '''
  drink = Drink.query.get(id)

  if (drink == None):
    abort(404)

  drink.delete()

  return jsonify({
  'success': True,
  'delete': id
})

#----------------------------------------------------------------------------#
# Error Handling
#----------------------------------------------------------------------------#

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401

@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'Bad Request'
    }), 400

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": 'Method Not Allowed'
    }), 405

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error'
    }), 500