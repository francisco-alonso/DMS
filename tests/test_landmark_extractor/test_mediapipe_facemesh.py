import pytest
import numpy as np
import cv2
from unittest.mock import Mock, patch, MagicMock
from src.landmark_extractor.mediapipe_facemesh import MediaPipeFaceMeshExtractor


class TestMediaPipeFaceMeshExtractor:
    """Tests for MediaPipeFaceMeshExtractor class."""

    @patch("src.landmark_extractor.mediapipe_facemesh.mp.solutions.face_mesh")
    def test_init_default_params(self, mock_face_mesh_module):
        """Test initialization with default parameters."""
        mock_face_mesh = MagicMock()
        mock_face_mesh_module.FaceMesh = MagicMock(return_value=mock_face_mesh)

        extractor = MediaPipeFaceMeshExtractor()

        mock_face_mesh_module.FaceMesh.assert_called_once_with(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        assert extractor.face_mesh == mock_face_mesh

    @patch("src.landmark_extractor.mediapipe_facemesh.mp.solutions.face_mesh")
    def test_init_custom_params(self, mock_face_mesh_module):
        """Test initialization with custom parameters."""
        mock_face_mesh = MagicMock()
        mock_face_mesh_module.FaceMesh = MagicMock(return_value=mock_face_mesh)

        extractor = MediaPipeFaceMeshExtractor(
            max_num_faces=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.8,
        )

        mock_face_mesh_module.FaceMesh.assert_called_once_with(
            static_image_mode=False,
            max_num_faces=2,
            refine_landmarks=False,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.8,
        )

    @patch("src.landmark_extractor.mediapipe_facemesh.cv2.cvtColor")
    @patch("src.landmark_extractor.mediapipe_facemesh.mp.solutions.face_mesh")
    def test_extract_no_face_detected(self, mock_face_mesh_module, mock_cvt_color):
        """Test extract when no face is detected."""
        mock_face_mesh = MagicMock()
        mock_face_mesh_module.FaceMesh = MagicMock(return_value=mock_face_mesh)

        # Mock process to return no faces
        mock_process_result = MagicMock()
        mock_process_result.multi_face_landmarks = None
        mock_face_mesh.process.return_value = mock_process_result

        # Mock image conversion
        mock_image_bgr = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_image_rgb = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_cvt_color.return_value = mock_image_rgb

        extractor = MediaPipeFaceMeshExtractor()
        result = extractor.extract(mock_image_bgr)

        assert result["face_detected"] is False
        assert result["landmarks"] is None
        # Verify cv2.cvtColor was called with correct arguments
        mock_cvt_color.assert_called_once_with(mock_image_bgr, cv2.COLOR_BGR2RGB)

    @patch("src.landmark_extractor.mediapipe_facemesh.cv2.cvtColor")
    @patch("src.landmark_extractor.mediapipe_facemesh.mp.solutions.face_mesh")
    def test_extract_face_detected(self, mock_face_mesh_module, mock_cvt_color):
        """Test extract when face is detected."""
        mock_face_mesh = MagicMock()
        mock_face_mesh_module.FaceMesh = MagicMock(return_value=mock_face_mesh)

        # Create mock landmarks
        mock_landmark1 = MagicMock()
        mock_landmark1.x = 0.5
        mock_landmark1.y = 0.5
        mock_landmark1.z = 0.0

        mock_landmark2 = MagicMock()
        mock_landmark2.x = 0.6
        mock_landmark2.y = 0.6
        mock_landmark2.z = 0.1

        mock_face_landmarks = MagicMock()
        mock_face_landmarks.landmark = [mock_landmark1, mock_landmark2]

        # Mock process to return face
        mock_process_result = MagicMock()
        mock_process_result.multi_face_landmarks = [mock_face_landmarks]
        mock_face_mesh.process.return_value = mock_process_result

        # Mock image conversion
        mock_image_bgr = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_image_rgb = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_cvt_color.return_value = mock_image_rgb

        extractor = MediaPipeFaceMeshExtractor()
        result = extractor.extract(mock_image_bgr)

        assert result["face_detected"] is True
        assert result["landmarks"] is not None
        assert len(result["landmarks"]) == 2
        assert result["landmarks"][0] == {"x": 0.5, "y": 0.5, "z": 0.0}
        assert result["landmarks"][1] == {"x": 0.6, "y": 0.6, "z": 0.1}

    @patch("src.landmark_extractor.mediapipe_facemesh.mp.solutions.face_mesh")
    def test_close(self, mock_face_mesh_module):
        """Test close method calls face_mesh.close()."""
        mock_face_mesh = MagicMock()
        mock_face_mesh_module.FaceMesh = MagicMock(return_value=mock_face_mesh)

        extractor = MediaPipeFaceMeshExtractor()
        extractor.close()

        mock_face_mesh.close.assert_called_once()

    @patch("src.landmark_extractor.mediapipe_facemesh.cv2.cvtColor")
    @patch("src.landmark_extractor.mediapipe_facemesh.mp.solutions.face_mesh")
    def test_extract_multiple_faces_uses_first(
        self, mock_face_mesh_module, mock_cvt_color
    ):
        """Test that extract uses first face when multiple faces detected."""
        mock_face_mesh = MagicMock()
        mock_face_mesh_module.FaceMesh = MagicMock(return_value=mock_face_mesh)

        # Create mock landmarks for two faces
        mock_landmark1 = MagicMock()
        mock_landmark1.x = 0.5
        mock_landmark1.y = 0.5
        mock_landmark1.z = 0.0

        mock_landmark2 = MagicMock()
        mock_landmark2.x = 0.6
        mock_landmark2.y = 0.6
        mock_landmark2.z = 0.1

        mock_face_landmarks1 = MagicMock()
        mock_face_landmarks1.landmark = [mock_landmark1]

        mock_face_landmarks2 = MagicMock()
        mock_face_landmarks2.landmark = [mock_landmark2]

        # Mock process to return multiple faces
        mock_process_result = MagicMock()
        mock_process_result.multi_face_landmarks = [
            mock_face_landmarks1,
            mock_face_landmarks2,
        ]
        mock_face_mesh.process.return_value = mock_process_result

        # Mock image conversion
        mock_image_bgr = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_image_rgb = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_cvt_color.return_value = mock_image_rgb

        extractor = MediaPipeFaceMeshExtractor()
        result = extractor.extract(mock_image_bgr)

        # Should use first face only
        assert result["face_detected"] is True
        assert len(result["landmarks"]) == 1
        assert result["landmarks"][0] == {"x": 0.5, "y": 0.5, "z": 0.0}
