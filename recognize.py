import sys
import cv2
import numpy as np
import face_recognition
from db import find_nearest

# threshold for face distance - 0.6 is typical; tune for your data
DISTANCE_THRESHOLD = 0.6


def recognize_from_image(image_path):
    img = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(img)
    encodings = face_recognition.face_encodings(img, face_locations)
    results = []
    for loc, enc in zip(face_locations, encodings):
        neighbors = find_nearest(enc.tolist(), top_k=3)
        if neighbors:
            best_id, best_name, best_embedding, best_distance = neighbors[0]
            if best_distance <= DISTANCE_THRESHOLD:
                results.append({"name": best_name, "distance": float(best_distance), "location": loc})
            else:
                results.append({"name": None, "distance": float(best_distance), "location": loc})
        else:
            results.append({"name": None, "distance": None, "location": loc})
    return results


def recognize_from_webcam():
    video_capture = cv2.VideoCapture(0)
    print("Press 'q' to quit")
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        for (top, right, bottom, left), enc in zip(face_locations, encodings):
            neighbors = find_nearest(enc.tolist(), top_k=1)
            name = "Unknown"
            if neighbors:
                _id, n, _emb, dist = neighbors[0]
                if dist <= DISTANCE_THRESHOLD:
                    name = n
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--webcam":
        recognize_from_webcam()
    elif len(sys.argv) == 2:
        image = sys.argv[1]
        res = recognize_from_image(image)
        print(res)
    else:
        print("Usage: python recognize.py <image_path>  OR  python recognize.py --webcam")
