import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Camera could not be opened.")
    exit()

print("✅ Camera started.")
print("Press Q to close the camera.")

while True:
    success, frame = camera.read()

    if not success:
        print("❌ Failed to read camera frame.")
        break

    cv2.imshow("Vyom Assist - Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()