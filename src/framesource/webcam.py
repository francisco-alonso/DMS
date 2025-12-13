import cv2
import time


class WebcamFrameSource:
    def __init__(self, device_index=0):
        self.cap = cv2.VideoCapture(device_index)
        if not self.cap.isOpened():
            raise RuntimeError(
                "Could not open webcam. Try device_index=1 if you have multiple cameras."
            )

        self.frame_id = 0

    def read(self):
        ok, frame_bgr = self.cap.read()
        if not ok:
            return None

        frame = {
            "frame_id": self.frame_id,
            "timestamp_ms": int(time.time() * 1000),
            "image": frame_bgr,
        }

        self.frame_id += 1
        return frame

    def release(self):
        self.cap.release()
