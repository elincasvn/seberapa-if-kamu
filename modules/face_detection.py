import mediapipe as mp
import cv2

mp_face_mesh = mp.solutions.face_mesh

class FaceDirectionDetector:
    def __init__(self):
        self.face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

    def get_head_direction(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            nose = landmarks[1]
            if nose.x < 0.4:
                return 'left'
            elif nose.x > 0.6:
                return 'right'
            else:
                return 'center'
        return None