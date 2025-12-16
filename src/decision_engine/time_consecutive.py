class TimeConsecutiveDecisionEngine:
    def __init__(self, ear_threshold, min_closed_time_sec):
        self.ear_threshold = ear_threshold
        self.min_closed_time_sec = min_closed_time_sec

        self.closed_start_ts = None
        self.state = "AWAKE"

    def update(self, ear, timestamp_ms):
        """
        Update decision state based on EAR value and time.

        Args:
            ear (float): Eye Aspect Ratio
            timestamp_ms (int): timestamp in milliseconds

        Returns:
            dict: {
                "state": str,
                "closed_time_sec": float
            }
        """
        if ear < self.ear_threshold:
            if self.closed_start_ts is None:
                self.closed_start_ts = timestamp_ms

            closed_time_sec = (timestamp_ms - self.closed_start_ts) / 1000.0

            if closed_time_sec >= self.min_closed_time_sec:
                self.state = "DROWSY"
            else:
                self.state = "AWAKE"
        else:
            self.closed_start_ts = None
            closed_time_sec = 0.0
            self.state = "AWAKE"

        return {
            "state": self.state,
            "closed_time_sec": closed_time_sec,
        }
