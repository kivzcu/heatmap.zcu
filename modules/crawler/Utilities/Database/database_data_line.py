from typing import Dict


class DatabaseDataLine:
    """
    Class that specifies the look of data line in database
    """
    def __init__(self, name: str, longitude: float, latitude: float, date: str,
                 occurrence: int):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.date = date
        self.occurrence = occurrence

    def to_dictionary(self) -> Dict[str, any]:
        return {
            "place": self.name,
            "x": self.longitude,
            "y": self.latitude,
            "number": self.occurrence,
            "date": self.date
        }
