from flask import Blueprint, request, jsonify
from config import subjects_collection, trainers_collection

subject_bp = Blueprint('subject', __name__)

@subject_bp.route('/api/subject', methods=['POST'])
def add_subject():
    data = request.json
    subjects_collection.insert_one(data)
    return jsonify({"msg": "Subject added successfully"})

@subject_bp.route('/api/subject', methods=['GET'])
def get_subjects():
    subjects = list(subjects_collection.find({}, {'_id': 0}))
    return jsonify(subjects)

@subject_bp.route('/api/subject/<string:subject_id>', methods=['GET'])
def get_subject_with_trainers(subject_id):
    trainers = list(trainers_collection.find({"subject": subject_id}, {'_id': 0}))
    return jsonify({"subject": subject_id, "trainers": trainers})
