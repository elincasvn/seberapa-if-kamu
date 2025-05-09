import cv2

class HeadTracker:
    def __init__(self):
        # Gunakan file Haar Cascade dari folder lokal assets
        self.face_cascade = cv2.CascadeClassifier("assets/haarcascade_frontalface_default.xml")
        self.last_x = None

    def detect_direction(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        direction = None
        for (x, y, w, h) in faces:
            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            center_x = x + w // 2

            if self.last_x is not None:
                if center_x < self.last_x - 20:
                    direction = "left"
                elif center_x > self.last_x + 20:
                    direction = "right"

            self.last_x = center_x
            break  # only track the first face detected

        return direction
