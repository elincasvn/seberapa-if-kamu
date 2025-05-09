import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Gagal membuka kamera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal membaca frame")
        break

    cv2.imshow("Test Kamera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()