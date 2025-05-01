
import mediapipe as mp
import cv2

class HeadTracker:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
        self.mp_drawing = mp.solutions.drawing_utils

    def detect_direction(self, frame):
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                nose_tip = face_landmarks.landmark[1]  # titik hidung
                x = nose_tip.x * w
                if x < w * 0.4:
                    return "left"
                elif x > w * 0.6:
                    return "right"
                else:
                    return "center"
        return "unknown"
