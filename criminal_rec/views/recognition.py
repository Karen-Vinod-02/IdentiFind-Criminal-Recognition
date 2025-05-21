import os
from retinaface import RetinaFace  # RetinaFace for face detection
from deepface import DeepFace       # DeepFace for ArcFace recognition
from django.conf import settings

# Load the database paths 
def load_face_image_paths():
    face_db_dir = r"media\front"
    database = {}

    if not os.path.exists(face_db_dir):
        print(f"Error: Face directory not found at {face_db_dir}")
        return {}

    for filename in os.listdir(face_db_dir):
        if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
            criminal_id = os.path.splitext(filename)[0]
            database[criminal_id] = os.path.join(face_db_dir, filename)

    return database

face_database = load_face_image_paths()

def match_face_with_db(image_path, model_name='ArcFace', threshold=None):
    print(image_path)
    default_threshold = 0.4

    try:
        best_match = None

        # Step 1: Use RetinaFace for face detection
        faces = RetinaFace.detect_faces(image_path)
        if not faces:
            return {"match": False, "message": "No face detected in the image."}

        # Step 2: Use ArcFace (via DeepFace) for face recognition
        for criminal_id, db_image_path in face_database.items():
            try:
                result = DeepFace.verify(
                    img1_path=image_path,
                    img2_path=db_image_path,
                    model_name=model_name,
                    enforce_detection=False
                )

                is_verified = result.get("verified", False)
                distance = result.get("distance")
                max_threshold = result.get("max_threshold_to_verify")

                effective_threshold = threshold or max_threshold or default_threshold

                if is_verified and distance is not None and distance <= effective_threshold:
                    confidence = max(0.0, 1.0 - (distance / effective_threshold))
                    confidence = round(confidence, 2)

                    best_match = {
                        "criminal_id": criminal_id,
                        "distance": distance,
                        "threshold": effective_threshold,
                        "confidence": confidence
                    }
                    break  

            except Exception as e:
                print(f"Error verifying with {criminal_id}: {e}")
                continue

        if best_match:
            return {
                "match": True,
                "criminal_id": best_match["criminal_id"],
                "distance": best_match["distance"],
                "threshold": best_match["threshold"],
                "confidence": best_match["confidence"]
            }
        else:
            return {"match": False, "message": "No match found above the threshold."}

    except Exception as e:
        return {"match": False, "error": str(e)}
