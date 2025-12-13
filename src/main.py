import cv2
import time
from framesource.webcam import WebcamFrameSource


def main():
    source = WebcamFrameSource(device_index=0)

    prev_time = time.time()

    while True:
        frame = source.read()
        if frame is None:
            continue

        image = frame["image"]

        # ---- FPS calculation ----
        current_time = time.time()
        delta = current_time - prev_time
        prev_time = current_time

        fps = 1.0 / delta if delta > 0 else 0.0

        # ---- Draw FPS on screen ----
        cv2.putText(
            image,
            f"FPS: {fps:.2f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        cv2.imshow("Webcam test with FPS - press q to quit", image)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    source.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
