import cv2 as cv
import numpy as np
import streamlink
from dotenv import load_dotenv
import os

load_dotenv()

# load url from environment variable

stream_url = (
    os.environ.get("STREAM_URL") or "https://www.youtube.com/watch?v=5qap5aO4i9A"
)
url = stream_url
# Create a Streamlink session

# Get the streams for the given URL
streams = streamlink.streams(stream_url)

print(streams)
# print(streams["small"])
# Get the best stream
best_stream = streams["worst"]
best_stream_url = best_stream.to_url()


slits = []

slit_height = 3


def main():
    cap = cv.VideoCapture(best_stream_url)
    c = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_h, frame_w = frame.shape[:2]
        print(frame_h, frame_w)
        row = 620
        slits.append(frame[row : row + slit_height, :])

        cv.line(frame, (0, row - 2), (frame_w, row - 2), (0, 255, 255), 2)
        cv.imshow("Frame", frame)
        # show the last 340 slits
        slits_to_show = frame_h // slit_height
        if c > slits_to_show:
            cv.imshow("Slits", np.vstack(slits[-slits_to_show:]))
        else:
            cv.imshow("Slits", np.vstack(slits))
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
