from flask import request, jsonify
from functools import wraps
import secrets
import decimal
import requests
import json

from TFT_inventory.models import User

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        """
        This function takes in any number of args & kwargs and verifies that the token
        passed into the headers is associated with a user in the database. 
        """
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split()[1]
            print(token)

        if not token:
            return jsonify({'message': 'Tokenn is missing'}), 401 # Client error no
        
        try:
            our_user = User.query.filter_by(token=token).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Token is invalid'}), 401
        except:
            our_user = User.query.filter_by(token=token).first()
            if token != our_user.token and secrets.compare_digest(token, our_user.token):
                return jsonify({'message': 'Token is invalid'}), 401
        return our_flask_function(our_user, *args, **kwargs)
    return decorated

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return json.JSONEncoder(JSONEncoder, self).default(obj)
    
def champion_info_generator(name):
    url = f"https://league-of-legends-champions.p.rapidapi.com/champions/en-us/{name}"

    headers = {
        "X-RapidAPI-Key": "4150364e67mshd14a8c1aa2795d4p10d4c4jsnb57e2361fc4d",
        "X-RapidAPI-Host": "league-of-legends-champions.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    return data['champion'][0]['lore']