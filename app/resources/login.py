from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username = data["username"]).first()
    if user and user.check_password(data["password"]):
        return jsonify({"message": "Login sucessful"}), 200
    return jsonify({"message": "Failed login"}), 401
