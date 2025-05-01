import cv2

def draw_question(frame, question, choices):
    h, w, _ = frame.shape
    cv2.putText(frame, question, (w//8, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
    cv2.putText(frame, f"⬅ {choices[0]}", (50, h-50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200,200,255), 2)
    cv2.putText(frame, f"{choices[1]} ➡", (w//2 + 50, h-50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200,200,255), 2)
    return frame