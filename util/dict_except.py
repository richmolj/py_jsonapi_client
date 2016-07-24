def dict_except(dct, *exclusions):
    new_dct = {}
    for k in dct:
        if not k in exclusions:
            new_dct[k] = dct[k]
    return new_dct
