import cv2
from cvzone.HandTrackingModule import HandDetector

def close_window(camera):
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        camera.release()
        cv2.destroyAllWindows()
        exit()

camera = cv2.VideoCapture(0)
camera.set(3, 640)
camera.set(4, 480)

detector = HandDetector(detectionCon=0.3, maxHands=1)

zoom_level = 1.0

def main():
    global zoom_level
    while camera.isOpened():
        ret, frame = camera.read()
        if not ret:
            print("Failed to open the camera")
            break

        frame = cv2.flip(frame, 1)
        hands, gambar = detector.findHands(frame)

        if hands:
            hand = hands[0]
            lmList = hand["lmList"]
            text_x = int(lmList[0][0]) - 110
            text_y = int(lmList[0][1]) + 50

            if len(lmList) != 0:
                fingers = detector.fingersUp(hand)

                if fingers == [0, 0, 0, 0, 0]:
                    zoom_level = 1.5
                    cv2.putText(frame, "Zoom In", (text_x + 20, text_y), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 4)
                elif fingers == [0, 1, 1, 0, 0]:
                    zoom_level = 1.0
                    cv2.putText(frame, "No Zoom", (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 4)
                else:
                    zoom_level = 0.5
                    cv2.putText(frame, "Zoom Out", (text_x - 20, text_y), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 4)

                height, width, _ = frame.shape
                gambar = cv2.resize(frame, (int(width * zoom_level), int(height * zoom_level)))

        cv2.imshow("Your hand", gambar)
        close_window(camera)

if __name__ == "__main__":
    main()