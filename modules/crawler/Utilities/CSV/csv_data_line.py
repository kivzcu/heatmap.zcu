class CSVDataLine:
    """
    Class that specifies the look of data line in processed csv file
    prepared for database
    """
    def __init__(self, name: str, date: str, occurrence: int) -> None:
        try:
            test_val = int(occurrence)
        except ValueError:
            print("Occurence should be and integer value!")

        if len(date) != 13:
            raise ValueError("Invalid date format YYYY-dd-mm-hh expected!")

        self.name = name
        self.date = date
        self.occurrence = test_val

    def to_csv(self) -> str:
        return self.name + ";" + str(self.occurrence) + ";" + self.date
