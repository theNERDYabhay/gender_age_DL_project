
"""AI helper module.

Replace the placeholder logic with your OpenCV DNN inference code.
"""

import random

COMPLIMENTS = [
    "You have a wonderful smile!",
    "Looking confident today!",
    "Keep shining!",
    "You have a great sense of style!",
    "Hope you have an amazing day!"
]

def predict(frame):
    # TODO:
    # Run face detection
    # Run age model
    # Run gender model
    return {
        "age": "(25-32)",
        "gender": "Male",
        "confidence": 0.97,
        "compliment": random.choice(COMPLIMENTS)
    }
