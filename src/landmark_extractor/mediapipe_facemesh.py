import mediapipe as mp
import cv2


class MediaPipeFaceMeshExtractor:
    def __init__(
        self,
        max_num_faces=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ):
        self.mp_face_mesh = mp.solutions.face_mesh

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=max_num_faces,
            refine_landmarks=False,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def extract(self, image_bgr):
        """
        Args:
            image_bgr (np.ndarray): BGR image from OpenCV

        Returns:
            dict:
                {
                  "face_detected": bool,
                  "landmarks": list[{"x","y","z"}] | None
                }
        """
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image_rgb)

        if not results.multi_face_landmarks:
            return {
                "face_detected": False,
                "landmarks": None,
            }

        face_landmarks = results.multi_face_landmarks[0]

        landmarks = [
            {
                "x": lm.x,
                "y": lm.y,
                "z": lm.z,
            }
            for lm in face_landmarks.landmark
        ]

        return {
            "face_detected": True,
            "landmarks": landmarks,
        }

    def close(self):
        self.face_mesh.close()
