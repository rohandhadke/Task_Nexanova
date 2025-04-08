from flask import Blueprint, request, jsonify, render_template
from config import subjects_collection, trainers_collection
from bson import ObjectId
from datetime import datetime
from routes.auth_routes import login_required


subject_bp = Blueprint('subject', __name__)

@subject_bp.route('/api/subject', methods=['POST'])
@login_required
def add_subject():
    data = request.json

    # Generate new subject_id
    last_subject = subjects_collection.find_one(sort=[("subject_id", -1)])
    if last_subject and "subject_id" in last_subject:
        # Extract numeric part and increment
        last_id = int(last_subject["subject_id"].replace("SUB", ""))
        new_id = f"SUB{last_id + 1:03d}"
    else:
        new_id = "SUB001"

    # Add subject_id to the data
    data["subject_id"] = new_id
    now = datetime.now()
    data["registered_on"] = now.strftime("%Y-%m-%d (%A)")

    subjects_collection.insert_one(data)
    return jsonify({"msg": "Subject added successfully", "subject_id": new_id})


@subject_bp.route('/api/subject', methods=['GET'])
@login_required
def get_subjects():
    subjects = list(subjects_collection.find({}, {'_id': 0,"name": 1}))
    return jsonify(subjects)

@subject_bp.route('/api/subject/<string:subject_id>', methods=['GET'])
@login_required
def get_subject_with_trainers(subject_id):
    # Find subject by custom subject_id field instead of ObjectId
    subject = subjects_collection.find_one({"subject_id": subject_id}, {'_id': 0})
    if not subject:
        return jsonify({"error": "Subject not found"}), 404

    # Find trainers who have this subject in their 'subjects' list
    trainers = list(trainers_collection.find({"subjects": subject["name"]}, {'_id': 0}))
    subject['trainers'] = trainers  # Add trainers info to subject dictionary

    return jsonify(subject)


@subject_bp.route('/subject', methods=['GET'])
@login_required
def show_subject_page():
    trainers = list(trainers_collection.find())
    subjects = list(subjects_collection.find({}, {'_id': 0}))
    return render_template('subjects.html', subjects=enumerate(subjects, start=1), trainers=trainers)


@subject_bp.route('/api/subject/name/<string:subject_name>', methods=['GET'])
@login_required
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
@login_required
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
