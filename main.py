import cv2 as cv
import numpy as np
import streamlink
from dotenv import load_dotenv
import os

load_dotenv()

slits = []

slit_height = 3

line: list[()] = []


# Bresenham's line algorithm to get the points on the line
def bresenham_line(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return points


def mouse_callback(event, x, y, flags, param):
    global frame_global
    if event == cv.EVENT_LBUTTONDOWN:
        if len(line) >= 2:
            line.clear()
        line.append((x, y))


cv.namedWindow("Frame")
cv.setMouseCallback("Frame", mouse_callback)


def main():
    cap = cv.VideoCapture("media/resized.mp4")
    pixel_values = []
    expanded_slit = []
    pixel_np_array = []
    c = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_h, frame_w = frame.shape[:2]

        if len(line) == 2:
            pixel_values = [frame[y, x] for x, y in bresenham_line(*line[0], *line[1])]
            pixel_np_array = np.array(pixel_values, dtype=np.uint8).reshape(-1, 1, 3)
            expanded_slit.append(pixel_np_array)
            cv.line(frame, line[0], line[1], (0, 255, 0), 2)

        if len(pixel_values) > 0:
            # display expanded_slit as an image
            if len(expanded_slit) > 400:
                cv.imshow("Current Slit Source", np.hstack(expanded_slit[-400:]))
            else:
                cv.imshow("Current Slit Source", np.hstack(expanded_slit))

        cv.imshow("Frame", frame)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break
        c += 1


if __name__ == "__main__":
    main()
