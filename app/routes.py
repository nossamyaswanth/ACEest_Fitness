from flask import Blueprint, jsonify

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    return jsonify({"message": "Welcome to ACEest Fitness & Gym!"}), 200

@bp.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200
