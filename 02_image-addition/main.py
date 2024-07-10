import cv2 as cv
import numpy as np

cap = cv.VideoCapture("../media/video2.mp4")

window_name = "frame"
cv.namedWindow(window_name, cv.WINDOW_NORMAL)
cv.moveWindow(window_name, 0, 0)

window_name2 = "blend"
cv.namedWindow(window_name2, cv.WINDOW_NORMAL)
cv.moveWindow(window_name2, 0, 520)
# why float? (to avoid overflow during accumulation)
ret, frame = cap.read()
accumulator = np.zeros_like(frame, dtype=np.float32)
while True:
    frame_float = frame.astype(np.float32)
    cv.accumulateWeighted(frame_float, accumulator, 0.01)
    cv.imshow("frame", frame)
    cv.imshow("blend", accumulator.astype(np.uint8))

    ret, frame = cap.read()
    if cv.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv.destroyAllWindows()
