from flask import Blueprint, request, jsonify, render_template
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

@subject_bp.route('/subject', methods=['GET'])
def show_subject_page():
    trainers = list(trainers_collection.find())
    subjects = list(subjects_collection.find({}, {'_id': 0}))
    return render_template('subjects.html', subjects=enumerate(subjects, start=1), trainers=trainers)

# @subject_bp.route('/api/subject/<string:subject_id>', methods=['GET'])
# def get_subject(subject_id):
#     try:
#         subject = subjects_collection.find_one({"_id": ObjectId(subject_id)})
#         if subject:
#             subject['_id'] = str(subject['_id'])  # Convert ObjectId to string
#             return jsonify(subject)
#         return jsonify({"error": "Subject not found"}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@subject_bp.route('/api/subject/name/<string:subject_name>', methods=['GET'])
def get_subject_by_name(subject_name):
    try:
        subject = subjects_collection.find_one({"name": subject_name})
        if subject:
            subject['_id'] = str(subject['_id'])  # Optional
            return jsonify(subject)
        return jsonify({"error": "Subject not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@subject_bp.route('/api/subject/name/<string:subject_name>', methods=['PUT'])
def edit_subject_by_name(subject_name):
    try:
        data = request.json
        result = subjects_collection.update_one(
            {"name": subject_name},
            {"$set": data}
        )

        if result.matched_count == 0:
            return jsonify({"error": "Subject not found"}), 404

        return jsonify({"msg": "Subject updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
