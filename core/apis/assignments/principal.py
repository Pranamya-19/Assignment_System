from flask import Blueprint, request, jsonify
from models import Assignment, db
import json

principal_assignments_bp = Blueprint('principal_assignments', __name__)

@principal_assignments_bp.route('/principal/assignments', methods=['GET'])
def get_principal_assignments():
    principal_header = request.headers.get('X-Principal')
    if not principal_header:
        return jsonify({'error': 'Unauthorized'}), 401

    principal = json.loads(principal_header)
    if not principal.get('principal_id'):
        return jsonify({'error': 'Unauthorized'}), 401

    assignments = Assignment.query.filter(
        Assignment.state.in_(['SUBMITTED', 'GRADED'])
    ).all()

    return jsonify({'data': [assignment.to_dict() for assignment in assignments]}), 200

@principal_assignments_bp.route('/principal/assignments/grade', methods=['POST'])
def grade_principal_assignment():
    principal_header = request.headers.get('X-Principal')
    if not principal_header:
        return jsonify({'error': 'Unauthorized'}), 401

    principal = json.loads(principal_header)
    if not principal.get('principal_id'):
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    assignment_id = data.get('id')
    grade = data.get('grade')

    assignment = Assignment.query.filter_by(id=assignment_id).first()
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404

    assignment.grade = grade
    assignment.state = 'GRADED'
    db.session.commit()

    return jsonify({'data': assignment.to_dict()}), 200
