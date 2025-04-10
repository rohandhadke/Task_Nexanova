from flask import Blueprint, request, jsonify, render_template, session, redirect
from config import trainers_collection, subjects_collection
from routes.auth_routes import login_required

trainer_bp = Blueprint('trainer', __name__)

@trainer_bp.route('/trainer', methods=['GET'])
@login_required
def trainer_page():
    subjects = list(subjects_collection.find({}, {'_id': 0}))
    trainers = list(trainers_collection.find())
    return render_template('trainer.html', trainers=trainers,subjects = subjects)

@trainer_bp.route('/api/trainer', methods=['POST'])
@login_required
def add_trainer():
    data = request.json
    print(data)
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    dob = data.get('dob')
    subject = data.get('subjects')

    last_trainer = trainers_collection.find_one(
        {"tid": {"$regex": "^T"}}, sort=[("tid", -1)]
    )

    if last_trainer and 'tid' in last_trainer:
        try:
            last_number = int(last_trainer['tid'].replace('T', ''))
        except ValueError:
            last_number = 0
        new_id = f"T{last_number + 1:03d}"
    else:
        new_id = "T001"
    
    new_trainer = {
        "tid": new_id,
        "name": name,
        "email": email,
        "phone": phone,
        "dob": dob,
        "subject": subject
    }

    trainers_collection.insert_one(new_trainer)
    return jsonify({"msg": "Trainer added successfully", "tid": new_id})

@trainer_bp.route('/api/trainer/<tid>', methods=['GET'])
@login_required
def get_trainer(tid):
    trainer = trainers_collection.find_one({"tid": tid})
    if not trainer:
        return jsonify({"error": "Trainer not found"}), 404

    trainer['_id'] = str(trainer['_id']) 
    return jsonify(trainer)

@trainer_bp.route('/trainer/<tid>', methods=['GET'])
@login_required
def show_trainer_profile(tid):
    trainer = trainers_collection.find_one({"tid": tid})
    subjects = list(subjects_collection.find({}, {'_id': 0}))
    if not trainer:
        return render_template('404.html', message="Trainer not found"), 404

    trainer['_id'] = str(trainer['_id'])  
    return render_template('trainer_profile.html', trainer=trainer)
    
@trainer_bp.route('/api/trainer/<string:subject>/topic', methods=['GET'])
@login_required
def get_trainers_by_subject(subject):
    trainers = list(trainers_collection.find({"subject": subject}, {'_id': 0}))
    return jsonify(trainers)

@trainer_bp.route('/api/trainer/<string:trainer_id>', methods=['DELETE'])
@login_required
def delete_trainer(trainer_id):
    trainers_collection.delete_one({"tid": trainer_id})
    return jsonify({"msg": "Trainer deleted"})

@trainer_bp.route('/api/trainer/update', methods=['PUT'])
@login_required
def update_trainer():
    print("Received JSON:", request.json)  

    data = request.json
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    tid = data.get('tid')
    if not tid:
        return jsonify({"error": "Trainer ID is required"}), 400

    update_fields = {
        "name": data.get('name'),
        "email": data.get('email'),
        "subjects": data.get('subjects'),
        "batches": data.get('batches')
    }

    trainers_collection.update_one({'tid': tid}, {'$set': update_fields})
    return jsonify({"msg": "Trainer updated successfully"})


@trainer_bp.route('/api/trainer', methods=['GET'])
@login_required
def get_all_trainers():
    try:
        trainers = list(trainers_collection.find({}, {'_id': 0}))
        return jsonify(trainers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
