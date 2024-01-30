# Import necessary modules from Flask
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

# Import the function 'check_user_credentials' from the 'models' module
from models import check_user_credentials

# Create a Blueprint named 'auth'
auth_bp = Blueprint('auth', __name__)

# Define a route for handling user login, accessible via HTTP POST requests
@auth_bp.route('/login', methods=['POST'])
def login():
    # Retrieve 'username' and 'password' from the JSON data in the request
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    # Check the user credentials using the 'check_user_credentials' function
    if check_user_credentials(username, password):
        # If the credentials are valid, create an access token for the user
        access_token = create_access_token(identity=username)
        
        # Return the access token as JSON response with HTTP status code 200 (OK)
        return jsonify(access_token=access_token), 200
    else:
        # If the credentials are invalid, return a JSON response with an error message
        # and HTTP status code 401 (Unauthorized)
        return jsonify({"msg": "Bad username or password"}), 401

