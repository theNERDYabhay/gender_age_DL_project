
from flask import Blueprint, request, jsonify
from ai import predict

api = Blueprint("api", __name__)

@api.route("/predict", methods=["POST"])
def predict_route():
    # TODO:
    # Decode uploaded image into OpenCV frame.
    # Call predict(frame).
    result = predict(None)
    return jsonify(result)
