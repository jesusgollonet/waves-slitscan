import cv2 as cv
import numpy as np

# video optical flow

# read video
cap = cv.VideoCapture("../media/resized.mp4")
# capture first frame
ret, frame1 = cap.read()
# convert to grayscale
prvs = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
# create hsv image
hsv = np.zeros_like(frame1)

# set saturation to maximum
hsv[..., 1] = 255


cv.imshow("video", frame1)

# advance frame when pressing spacebar
while True:
    # if cv.waitKey(1) & 0xFF == ord(" "):
    # print("spacebar pressed")
    ret, frame = cap.read()
    if not ret:
        break
    next = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    flow = cv.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
    bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    cv.imshow("optical flow", bgr)
    cv.imshow("video", frame)
    prvs = next

    if cv.waitKey(1) & 0xFF == ord("q"):
        break

# while True:
# ret, frame = cap.read()
# if not ret:
# break

# cv.imshow("frame", frame)
# if cv.waitKey(1) & 0xFF == ord("q"):
# break

cap.release()
cv.destroyAllWindows()
