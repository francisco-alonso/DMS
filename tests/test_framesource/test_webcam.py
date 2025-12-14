import pytest
import cv2
import time
from unittest.mock import Mock, patch, MagicMock
from src.framesource.webcam import WebcamFrameSource


class TestWebcamFrameSource:
    """Tests for WebcamFrameSource class."""

    @patch("src.framesource.webcam.cv2.VideoCapture")
    def test_init_success(self, mock_video_capture):
        """Test successful initialization of WebcamFrameSource."""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_video_capture.return_value = mock_cap

        source = WebcamFrameSource(device_index=0)

        mock_video_capture.assert_called_once_with(0)
        assert source.cap == mock_cap
        assert source.frame_id == 0

    @patch("src.framesource.webcam.cv2.VideoCapture")
    def test_init_failure_camera_not_opened(self, mock_video_capture):
        """Test initialization fails when camera cannot be opened."""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = False
        mock_video_capture.return_value = mock_cap

        with pytest.raises(RuntimeError, match="Could not open webcam"):
            WebcamFrameSource(device_index=0)

    @patch("src.framesource.webcam.cv2.VideoCapture")
    @patch("src.framesource.webcam.time.time")
    def test_read_success(self, mock_time, mock_video_capture):
        """Test successful frame read."""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_video_capture.return_value = mock_cap

        # Mock frame data
        mock_frame = MagicMock()
        mock_cap.read.return_value = (True, mock_frame)
        mock_time.return_value = 1234.567

        source = WebcamFrameSource(device_index=0)
        result = source.read()

        assert result is not None
        assert result["frame_id"] == 0
        assert result["timestamp_ms"] == 1234567
        assert result["image"] == mock_frame
        assert source.frame_id == 1

    @patch("src.framesource.webcam.cv2.VideoCapture")
    @patch("src.framesource.webcam.time.time")
    def test_read_multiple_frames(self, mock_time, mock_video_capture):
        """Test reading multiple frames increments frame_id correctly."""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_video_capture.return_value = mock_cap

        mock_frame = MagicMock()
        mock_cap.read.return_value = (True, mock_frame)
        mock_time.return_value = 1234.567

        source = WebcamFrameSource(device_index=0)

        # Read first frame
        result1 = source.read()
        assert result1["frame_id"] == 0
        assert source.frame_id == 1

        # Read second frame
        result2 = source.read()
        assert result2["frame_id"] == 1
        assert source.frame_id == 2

    @patch("src.framesource.webcam.cv2.VideoCapture")
    def test_read_failure_returns_none(self, mock_video_capture):
        """Test read returns None when capture fails."""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_video_capture.return_value = mock_cap

        mock_cap.read.return_value = (False, None)

        source = WebcamFrameSource(device_index=0)
        result = source.read()

        assert result is None
        # frame_id should NOT increment when read fails
        assert source.frame_id == 0

    @patch("src.framesource.webcam.cv2.VideoCapture")
    def test_release(self, mock_video_capture):
        """Test release method calls cap.release()."""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_video_capture.return_value = mock_cap

        source = WebcamFrameSource(device_index=0)
        source.release()

        mock_cap.release.assert_called_once()

    @patch("src.framesource.webcam.cv2.VideoCapture")
    def test_different_device_index(self, mock_video_capture):
        """Test initialization with different device index."""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_video_capture.return_value = mock_cap

        source = WebcamFrameSource(device_index=1)

        mock_video_capture.assert_called_once_with(1)
