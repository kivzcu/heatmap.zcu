from typing import Dict

SKIP = "SKIP"
UNKNOWN = "UNKNOWN!"


def should_skip(device: Dict[str, str]) -> bool:
    return device['x'] == SKIP or device['y'] == SKIP or device[
        'x'] == UNKNOWN or device['y'] == UNKNOWN


def detect_change(first: Dict[str, str], second: Dict[str, str],
                  compareKeys: [str]) -> bool:
    """Detects change between two dictonaries

    Args:
        first (Dict[str, str]): First dictionary
        second (Dict[str, str]): Second dictionary
        compareKeys ([type]): Keys to handle comparison

    Returns:
        bool: Is there a change ?
    """
    for key in compareKeys:
        if key not in second or key not in first:
            return True
        if first[key] != second[key]:
            return True
    return False
