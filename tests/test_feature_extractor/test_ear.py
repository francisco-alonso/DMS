import math

import pytest

from src.feature_extractor.ear import compute_ear, euclidean_distance


class TestEuclideanDistance:
    """Tests for euclidean_distance function."""

    def test_euclidean_distance_same_point(self):
        """Test distance between same point is zero."""
        p1 = {"x": 0.5, "y": 0.5}
        p2 = {"x": 0.5, "y": 0.5}
        assert euclidean_distance(p1, p2) == 0.0

    def test_euclidean_distance_horizontal(self):
        """Test distance between points on horizontal line."""
        p1 = {"x": 0.0, "y": 0.5}
        p2 = {"x": 1.0, "y": 0.5}
        assert euclidean_distance(p1, p2) == 1.0

    def test_euclidean_distance_vertical(self):
        """Test distance between points on vertical line."""
        p1 = {"x": 0.5, "y": 0.0}
        p2 = {"x": 0.5, "y": 1.0}
        assert euclidean_distance(p1, p2) == 1.0

    def test_euclidean_distance_diagonal(self):
        """Test distance between points on diagonal."""
        p1 = {"x": 0.0, "y": 0.0}
        p2 = {"x": 1.0, "y": 1.0}
        expected = math.sqrt(2.0)
        assert abs(euclidean_distance(p1, p2) - expected) < 1e-10

    def test_euclidean_distance_arbitrary_points(self):
        """Test distance between arbitrary points."""
        p1 = {"x": 0.3, "y": 0.7}
        p2 = {"x": 0.8, "y": 0.2}
        expected = math.sqrt((0.3 - 0.8) ** 2 + (0.7 - 0.2) ** 2)
        assert abs(euclidean_distance(p1, p2) - expected) < 1e-10


class TestComputeEAR:
    """Tests for compute_ear function."""

    def test_compute_ear_requires_six_landmarks(self):
        """Test that EAR requires exactly 6 landmarks."""
        with pytest.raises(ValueError, match="EAR requires exactly 6 eye landmarks"):
            compute_ear([])

        with pytest.raises(ValueError, match="EAR requires exactly 6 eye landmarks"):
            compute_ear([{"x": 0.0, "y": 0.0}] * 5)

        with pytest.raises(ValueError, match="EAR requires exactly 6 eye landmarks"):
            compute_ear([{"x": 0.0, "y": 0.0}] * 7)

    def test_compute_ear_zero_horizontal_distance(self):
        """Test EAR when horizontal distance is zero (edge case)."""
        # All points at same x coordinate
        eye_landmarks = [
            {"x": 0.5, "y": 0.0},  # p1
            {"x": 0.5, "y": 0.2},  # p2
            {"x": 0.5, "y": 0.3},  # p3
            {"x": 0.5, "y": 0.0},  # p4 (same x as p1)
            {"x": 0.5, "y": 0.3},  # p5
            {"x": 0.5, "y": 0.2},  # p6
        ]
        assert compute_ear(eye_landmarks) == 0.0

    def test_compute_ear_typical_open_eye(self):
        """Test EAR calculation for a typical open eye."""
        # Simulate an open eye: wider horizontally than vertically
        # p1 and p4 are outer corners (horizontal)
        # p2, p6 and p3, p5 are top/bottom points (vertical)
        eye_landmarks = [
            {"x": 0.3, "y": 0.5},  # p1: left outer corner
            {"x": 0.4, "y": 0.4},  # p2: top left
            {"x": 0.5, "y": 0.4},  # p3: top center
            {"x": 0.7, "y": 0.5},  # p4: right outer corner
            {"x": 0.5, "y": 0.6},  # p5: bottom center
            {"x": 0.4, "y": 0.6},  # p6: bottom left
        ]

        # Calculate expected values
        vertical_1 = euclidean_distance(eye_landmarks[1], eye_landmarks[5])  # p2-p6
        vertical_2 = euclidean_distance(eye_landmarks[2], eye_landmarks[4])  # p3-p5
        horizontal = euclidean_distance(eye_landmarks[0], eye_landmarks[3])  # p1-p4
        expected_ear = (vertical_1 + vertical_2) / (2.0 * horizontal)

        result = compute_ear(eye_landmarks)
        assert abs(result - expected_ear) < 1e-10
        assert result > 0.0

    def test_compute_ear_closed_eye(self):
        """Test EAR calculation for a closed eye (small vertical distance)."""
        # Simulate a closed eye: very small vertical distances
        eye_landmarks = [
            {"x": 0.3, "y": 0.5},  # p1: left outer corner
            {"x": 0.4, "y": 0.49},  # p2: top left (very close to center)
            {"x": 0.5, "y": 0.49},  # p3: top center
            {"x": 0.7, "y": 0.5},  # p4: right outer corner
            {"x": 0.5, "y": 0.51},  # p5: bottom center
            {"x": 0.4, "y": 0.51},  # p6: bottom left
        ]

        result = compute_ear(eye_landmarks)
        # Closed eye should have very low EAR
        assert result < 0.1
        assert result >= 0.0

    def test_compute_ear_wide_eye(self):
        """Test EAR calculation for a wide open eye."""
        # Simulate a wide open eye: larger vertical distances relative to horizontal
        # Using realistic values: wider horizontal distance, moderate vertical distances
        eye_landmarks = [
            {"x": 0.30, "y": 0.5},  # p1: left outer corner
            {"x": 0.38, "y": 0.45},  # p2: top left
            {"x": 0.50, "y": 0.44},  # p3: top center
            {"x": 0.70, "y": 0.5},  # p4: right outer corner (wider)
            {"x": 0.50, "y": 0.56},  # p5: bottom center
            {"x": 0.38, "y": 0.55},  # p6: bottom left
        ]

        result = compute_ear(eye_landmarks)
        # Wide open eye should have higher EAR than closed eye
        # Typical EAR range for eyes is 0.2-0.4 for open, <0.2 for closed
        assert result > 0.2
        assert result < 0.5  # Even wide open eyes rarely exceed 0.5
