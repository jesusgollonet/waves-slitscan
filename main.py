import cv2 as cv
import numpy as np


slits = []

slit_height = 3


def main():
    cap = cv.VideoCapture("media/video.mp4")
    c = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_h, frame_w = frame.shape[:2]
        print(frame_h, frame_w)
        row = 220
        slits.append(frame[row : row + slit_height, :])

        cv.line(frame, (0, row - 2), (frame_w, row - 2), (0, 255, 255), 2)
        cv.imshow("Frame", frame)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break
        c += 1

    print(len(slits))
    # create an image to contain all slits
    mosaic = np.zeros((len(slits) * slit_height, frame_w, 3), dtype=np.uint8)
    for i, slit in enumerate(slits):
        print(i)
        current_h = i * slit_height
        mosaic[current_h : current_h + slit_height, :] = slit

    cv.imwrite("media/mosaic.png", mosaic)


if __name__ == "__main__":
    main()
