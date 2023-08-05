def parseDunder(dunderMethodValue):
    split = str(dunderMethodValue)[1:-1].split(', ')
    values = {}

    for value in split:
        values[split.index(value)] = value

    return values