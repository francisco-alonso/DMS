from src.decision_engine.time_consecutive import TimeConsecutiveDecisionEngine


class TestTimeConsecutiveDecisionEngine:
    """Tests for TimeConsecutiveDecisionEngine class."""

    def test_initialization(self):
        """Test that engine initializes with correct default state."""
        engine = TimeConsecutiveDecisionEngine(
            ear_threshold=0.35, min_closed_time_sec=1.5
        )
        assert engine.ear_threshold == 0.35
        assert engine.min_closed_time_sec == 1.5
        assert engine.closed_start_ts is None
        assert engine.state == "AWAKE"

    def test_initial_state_awake(self):
        """Test that initial state is AWAKE."""
        engine = TimeConsecutiveDecisionEngine(
            ear_threshold=0.35, min_closed_time_sec=1.5
        )
        result = engine.update(ear=0.4, timestamp_ms=0)
        assert result["state"] == "AWAKE"
        assert result["closed_time_sec"] == 0.0

    def test_stays_awake_when_ear_above_threshold(self):
        """Test that state remains AWAKE when EAR is above threshold."""
        engine = TimeConsecutiveDecisionEngine(
            ear_threshold=0.35, min_closed_time_sec=1.5
        )

        result1 = engine.update(ear=0.4, timestamp_ms=0)
        assert result1["state"] == "AWAKE"
        assert result1["closed_time_sec"] == 0.0

        result2 = engine.update(ear=0.5, timestamp_ms=100)
        assert result2["state"] == "AWAKE"
        assert result2["closed_time_sec"] == 0.0

        result3 = engine.update(ear=0.6, timestamp_ms=200)
        assert result3["state"] == "AWAKE"
        assert result3["closed_time_sec"] == 0.0

    def test_stays_awake_when_ear_below_threshold_short_time(self):
        """Test that state remains AWAKE when EAR is below threshold but not long enough."""
        engine = TimeConsecutiveDecisionEngine(
            ear_threshold=0.35, min_closed_time_sec=1.5
        )

        result1 = engine.update(ear=0.3, timestamp_ms=0)
        assert result1["state"] == "AWAKE"
        assert result1["closed_time_sec"] == 0.0

        result2 = engine.update(ear=0.3, timestamp_ms=1000)
        assert result2["state"] == "AWAKE"
        assert abs(result2["closed_time_sec"] - 1.0) < 1e-6

        result3 = engine.update(ear=0.3, timestamp_ms=1400)
        assert result3["state"] == "AWAKE"
        assert abs(result3["closed_time_sec"] - 1.4) < 1e-6

    def test_transitions_to_drowsy_when_threshold_exceeded(self):
        """Test that state transitions to DROWSY when closed time exceeds threshold."""
        engine = TimeConsecutiveDecisionEngine(
            ear_threshold=0.35, min_closed_time_sec=1.5
        )

        engine.update(ear=0.3, timestamp_ms=0)

        result1 = engine.update(ear=0.3, timestamp_ms=1000)
        assert result1["state"] == "AWAKE"

        result2 = engine.update(ear=0.3, timestamp_ms=1500)
        assert result2["state"] == "DROWSY"
        assert abs(result2["closed_time_sec"] - 1.5) < 1e-6

        result3 = engine.update(ear=0.3, timestamp_ms=2000)
        assert result3["state"] == "DROWSY"
        assert abs(result3["closed_time_sec"] - 2.0) < 1e-6

    def test_returns_to_awake_when_ear_goes_above_threshold(self):
        """Test that state returns to AWAKE when EAR goes above threshold."""
        engine = TimeConsecutiveDecisionEngine(
            ear_threshold=0.35, min_closed_time_sec=1.5
        )

        engine.update(ear=0.3, timestamp_ms=0)
        engine.update(ear=0.3, timestamp_ms=1500)
        result_drowsy = engine.update(ear=0.3, timestamp_ms=2000)
        assert result_drowsy["state"] == "DROWSY"

        result_awake = engine.update(ear=0.4, timestamp_ms=2500)
        assert result_awake["state"] == "AWAKE"
        assert result_awake["closed_time_sec"] == 0.0

        assert engine.closed_start_ts is None

    def test_resets_closed_time_when_eyes_open(self):
        """Test that closed time resets when eyes open."""
        engine = TimeConsecutiveDecisionEngine(
            ear_threshold=0.35, min_closed_time_sec=1.5
        )

        engine.update(ear=0.3, timestamp_ms=0)
        result1 = engine.update(ear=0.3, timestamp_ms=1000)
        assert result1["closed_time_sec"] == 1.0

        result2 = engine.update(ear=0.4, timestamp_ms=1500)
        assert result2["closed_time_sec"] == 0.0

        result3 = engine.update(ear=0.3, timestamp_ms=2000)
        assert result3["closed_time_sec"] == 0.0

        result4 = engine.update(ear=0.3, timestamp_ms=2500)
        assert abs(result4["closed_time_sec"] - 0.5) < 1e-6

    def test_exact_threshold_boundary(self):
        """Test behavior at exact EAR threshold boundary."""
        engine = TimeConsecutiveDecisionEngine(
            ear_threshold=0.35, min_closed_time_sec=1.5
        )

        result = engine.update(ear=0.35, timestamp_ms=0)
        assert result["state"] == "AWAKE"
        assert result["closed_time_sec"] == 0.0

        result = engine.update(ear=0.349, timestamp_ms=100)
        assert result["state"] == "AWAKE"
        assert result["closed_time_sec"] == 0.0

    def test_exact_time_threshold_boundary(self):
        """Test behavior at exact minimum closed time threshold."""
        engine = TimeConsecutiveDecisionEngine(
            ear_threshold=0.35, min_closed_time_sec=1.5
        )

        engine.update(ear=0.3, timestamp_ms=0)

        result1 = engine.update(ear=0.3, timestamp_ms=1499)
        assert result1["state"] == "AWAKE"
        assert abs(result1["closed_time_sec"] - 1.499) < 1e-6

        result2 = engine.update(ear=0.3, timestamp_ms=1500)
        assert result2["state"] == "DROWSY"
        assert abs(result2["closed_time_sec"] - 1.5) < 1e-6

    def test_multiple_open_close_cycles(self):
        """Test multiple cycles of opening and closing eyes."""
        engine = TimeConsecutiveDecisionEngine(
            ear_threshold=0.35, min_closed_time_sec=1.5
        )

        engine.update(ear=0.3, timestamp_ms=0)
        engine.update(ear=0.3, timestamp_ms=1000)
        result1 = engine.update(ear=0.4, timestamp_ms=1500)
        assert result1["state"] == "AWAKE"

        engine.update(ear=0.3, timestamp_ms=2000)
        engine.update(ear=0.3, timestamp_ms=3500)
        result2 = engine.update(ear=0.3, timestamp_ms=4000)
        assert result2["state"] == "DROWSY"

        result3 = engine.update(ear=0.4, timestamp_ms=4500)
        assert result3["state"] == "AWAKE"

    def test_very_low_ear_values(self):
        """Test behavior with very low EAR values."""
        engine = TimeConsecutiveDecisionEngine(
            ear_threshold=0.35, min_closed_time_sec=1.5
        )

        result1 = engine.update(ear=0.01, timestamp_ms=0)
        assert result1["state"] == "AWAKE"
        assert result1["closed_time_sec"] == 0.0

        result2 = engine.update(ear=0.01, timestamp_ms=1500)
        assert result2["state"] == "DROWSY"
        assert abs(result2["closed_time_sec"] - 1.5) < 1e-6

    def test_negative_ear_value(self):
        """Test behavior with negative EAR (edge case)."""
        engine = TimeConsecutiveDecisionEngine(
            ear_threshold=0.35, min_closed_time_sec=1.5
        )

        result = engine.update(ear=-0.1, timestamp_ms=0)
        assert result["state"] == "AWAKE"
        assert result["closed_time_sec"] == 0.0

    def test_timestamp_overflow_handling(self):
        """Test that timestamps can handle large values."""
        engine = TimeConsecutiveDecisionEngine(
            ear_threshold=0.35, min_closed_time_sec=1.5
        )

        result1 = engine.update(ear=0.3, timestamp_ms=1000000)
        assert result1["state"] == "AWAKE"

        result2 = engine.update(ear=0.3, timestamp_ms=1001500)
        assert result2["state"] == "DROWSY"
        assert abs(result2["closed_time_sec"] - 1.5) < 1e-6

    def test_non_consecutive_timestamps(self):
        """Test behavior with non-consecutive timestamps (time gaps)."""
        engine = TimeConsecutiveDecisionEngine(
            ear_threshold=0.35, min_closed_time_sec=1.5
        )

        engine.update(ear=0.3, timestamp_ms=0)

        result = engine.update(ear=0.3, timestamp_ms=5000)
        assert result["state"] == "DROWSY"
        assert abs(result["closed_time_sec"] - 5.0) < 1e-6

    def test_different_threshold_values(self):
        """Test with different EAR threshold values."""
        engine_low = TimeConsecutiveDecisionEngine(
            ear_threshold=0.2, min_closed_time_sec=1.5
        )
        result1 = engine_low.update(ear=0.25, timestamp_ms=0)
        assert result1["state"] == "AWAKE"

        engine_low.update(ear=0.15, timestamp_ms=0)
        result2 = engine_low.update(ear=0.15, timestamp_ms=1500)
        assert result2["state"] == "DROWSY"

        engine_high = TimeConsecutiveDecisionEngine(
            ear_threshold=0.5, min_closed_time_sec=1.5
        )
        result3 = engine_high.update(ear=0.55, timestamp_ms=0)
        assert result3["state"] == "AWAKE"

        engine_high.update(ear=0.45, timestamp_ms=0)
        result4 = engine_high.update(ear=0.45, timestamp_ms=1500)
        assert result4["state"] == "DROWSY"

    def test_different_min_closed_time_values(self):
        """Test with different minimum closed time values."""
        engine_short = TimeConsecutiveDecisionEngine(
            ear_threshold=0.35, min_closed_time_sec=0.5
        )
        engine_short.update(ear=0.3, timestamp_ms=0)
        result1 = engine_short.update(ear=0.3, timestamp_ms=500)
        assert result1["state"] == "DROWSY"

        engine_long = TimeConsecutiveDecisionEngine(
            ear_threshold=0.35, min_closed_time_sec=3.0
        )
        engine_long.update(ear=0.3, timestamp_ms=0)
        result2 = engine_long.update(ear=0.3, timestamp_ms=2000)
        assert result2["state"] == "AWAKE"

        result3 = engine_long.update(ear=0.3, timestamp_ms=3000)
        assert result3["state"] == "DROWSY"
