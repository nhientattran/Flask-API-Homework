from flask import Blueprint, request, jsonify
from TFT_inventory.helpers import token_required, champion_info_generator
from TFT_inventory.models import db, Champion, champion_schema, champions_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def get(data):
    return {'some':'value'}

# Create Champion Endpoint
@api.route('/champions', methods = ['POST'])
@token_required
def create_champion(our_user):
    name = request.json['name']
    description = request.json['description']
    skill = request.json['skill']
    skill_description = request.json['skill_description']
    cost = request.json['cost']
    traits = request.json['traits']
    series = request.json['series']
    random_info = champion_info_generator()
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    champion = Champion(name, description, skill, skill_description, cost, traits, series, random_info, user_token)
    
    db.session.add(champion)
    db.session.commit()

    response = champion_schema.dump(champion)

    return jsonify(response)    

# Read 1 single Champion Endpoint
@api.route('/champions/<id>', methods=['GET'])
@token_required
def get_champion(our_user, id):
    if id:
        champion = Champion.query.get(id)
        response = champion_schema.dump(champion)
        return jsonify(response)
    else:
        return jsonify({'message': 'ID is missing'}), 401

# Read all the Champions
@api.route('/champions', methods=['GET'])
@token_required
def get_champions(our_user):
    token = our_user.token
    champions = Champion.query.filter_by(user_token = token).all()
    response = champions_schema.dump(champions)
    return jsonify(response)

# Update 1 Champion by ID
@api.route('/champions/<id>', methods=['PUT'])
@token_required
def update_champion(our_user, id):
    champion = Champion.query.get(id)

    champion.name = request.json['name']
    champion.description = request.json['description']
    champion.skill = request.json['skill']
    champion.skill_description = request.json['skill_description']
    champion.cost = request.json['cost'] 
    champion.traits = request.json['traits']
    champion.series = request.json['series']
    champion.champion_info = champion_info_generator()
    champion.user_token = our_user.token

    db.session.commit()

    response = champion_schema.dump(champion)
    return jsonify(response)

# Delete 1 Champion by ID
@api.route('/champions/<id>', methods = ['DELETE'])
@token_required
def delete_champion(our_user, id):
    champion = Champion.query.get(id)
    db.session.delete(champion)
    db.session.commit()

    response = champion_schema.dump(champion)

    return jsonify(response)