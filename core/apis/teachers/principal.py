from flask import Blueprint, request, jsonify
from models import Teacher
import json

principal_teachers_bp = Blueprint('principal_teachers', __name__)

@principal_teachers_bp.route('/principal/teachers', methods=['GET'])
def get_principal_teachers():
    principal_header = request.headers.get('X-Principal')
    if not principal_header:
        return jsonify({'error': 'Unauthorized'}), 401

    principal = json.loads(principal_header)
    if not principal.get('principal_id'):
        return jsonify({'error': 'Unauthorized'}), 401

    teachers = Teacher.query.all()

    return jsonify({'data': [teacher.to_dict() for teacher in teachers]}), 200
