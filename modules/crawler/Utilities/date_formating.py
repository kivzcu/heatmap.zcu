def date_formatter(string_date: str) -> str:
    """

    Args:
        string_date: string containing date in format 22.08.2018 12:27:00

    Returns:
        string of date in format YYYY-mm-dd-hh
    """
    if string_date[11].isspace():
        pos = 0
        srr = ""
        for i in string_date:

            if pos == 10:
                srr = srr + '0'
            else:
                srr = srr + i

            pos = pos + 1

        string_date = srr

    return_date = string_date[6:10] + '-' + string_date[
        3:5] + '-' + string_date[:2]

    return return_date


def date_time_formatter(string_date: str) -> str:
    """
    Converts one type of date format "dd.mm.yyyy hh.mm.ss" to date format YYYY-mm-dd-hh
    Args:
        string_date: string containing date in format 22.08.2018 12:27:00

    Returns:
        string of date in format YYYY-mm-dd-hh
    """
    if string_date[11].isspace():
        pos = 0
        srr = ""
        for i in string_date:

            if pos == 10:
                srr = srr + '0'
            else:
                srr = srr + i

            pos = pos + 1

        string_date = srr

    return_date = string_date[6:10] + '-' + string_date[
        3:5] + '-' + string_date[:2] + '-' + string_date[11:13]

    return return_date
