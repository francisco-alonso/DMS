
import cv2

from feature_extractor.ear import compute_ear
from framesource.webcam import WebcamFrameSource
from landmark_extractor.mediapipe_facemesh import MediaPipeFaceMeshExtractor

LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]


def main():
    source = WebcamFrameSource(device_index=0)
    landmark_extractor = MediaPipeFaceMeshExtractor()

    while True:
        frame = source.read()
        if frame is None:
            continue

        image = frame["image"]
        result = landmark_extractor.extract(image)

        ear_avg = 0.0  # Default value when no face is detected

        if result["face_detected"]:
            landmarks = result["landmarks"]
            h, w, _ = image.shape
            left_eye = [landmarks[idx] for idx in LEFT_EYE_IDX]
            right_eye = [landmarks[idx] for idx in RIGHT_EYE_IDX]

            ear_left = compute_ear(left_eye)
            ear_right = compute_ear(right_eye)
            ear_avg = (ear_left + ear_right) / 2.0

            # Draw LEFT eye landmarks (green)
            for idx in LEFT_EYE_IDX:
                lm = landmarks[idx]
                x = int(lm["x"] * w)
                y = int(lm["y"] * h)
                cv2.circle(image, (x, y), 3, (0, 255, 0), -1)

            # Draw RIGHT eye landmarks (red)
            for idx in RIGHT_EYE_IDX:
                lm = landmarks[idx]
                x = int(lm["x"] * w)
                y = int(lm["y"] * h)
                cv2.circle(image, (x, y), 3, (0, 0, 255), -1)

        cv2.putText(
            image,
            f"EAR (avg): {ear_avg:.3f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        cv2.imshow("Webcam test with smoothed FPS - press q to quit", image)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    landmark_extractor.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
