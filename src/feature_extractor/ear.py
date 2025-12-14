import math


def euclidean_distance(p1, p2):
    return math.sqrt((p1["x"] - p2["x"]) ** 2 + (p1["y"] - p2["y"]) ** 2)


def compute_ear(eye_landmarks):
    """
    Computes Eye Aspect Ratio (EAR) for one eye.

    Args:
        eye_landmarks (list): list of 6 landmarks (dict with x, y)

    Returns:
        float: EAR value
    """
    if len(eye_landmarks) != 6:
        raise ValueError("EAR requires exactly 6 eye landmarks")

    p1, p2, p3, p4, p5, p6 = eye_landmarks

    vertical_1 = euclidean_distance(p2, p6)
    vertical_2 = euclidean_distance(p3, p5)
    horizontal = euclidean_distance(p1, p4)

    if horizontal == 0:
        return 0.0

    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
    return ear
