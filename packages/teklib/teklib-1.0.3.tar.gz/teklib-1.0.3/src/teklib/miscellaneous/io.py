def loadtxt(filename, transpose=False, skip_header=0, usecols=None):
    """
    Load text with string and number datatypes. 
    Returns column data as row data for unpacking
    """
    import numpy
    raw_data = numpy.genfromtxt(filename, dtype=None, encoding=None, skip_header=skip_header, 
                                usecols=usecols)

    if transpose:
        curated_data = [numpy.array(arr) for arr in zip(*raw_data)]
        for ivar, row in enumerate(curated_data):
            if isinstance(row[0], numpy.bytes_):
                curated_data[ivar] = numpy.r_[[item.decode("utf-8") for item in row]]

    else:
        curated_data = []
        for row in raw_data:
            curated_data.append([item.decode("utf-8") if isinstance(item, numpy.bytes_) else item for item in row])
    return curated_data