import sys
import numpy as np
import face_recognition
from db import insert_person


def load_encodings_from_images(image_paths):
    encodings = []
    for path in image_paths:
        img = face_recognition.load_image_file(path)
        face_encs = face_recognition.face_encodings(img)
        if not face_encs:
            print(f"No face found in {path}")
            continue
        encodings.append(face_encs[0])
    return encodings


def enroll(name, image_paths):
    encs = load_encodings_from_images(image_paths)
    if not encs:
        print("No encodings found. Aborting.")
        return
    # average multiple images to get a stable embedding
    embedding = np.mean(encs, axis=0).tolist()
    person_id = insert_person(name, embedding, metadata={"source": "enroll_script", "images": image_paths})
    print(f"Enrolled {name} as id={person_id}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python enroll.py <name> <image1> [image2 ...]")
        sys.exit(1)
    name = sys.argv[1]
    images = sys.argv[2:]
    enroll(name, images)
