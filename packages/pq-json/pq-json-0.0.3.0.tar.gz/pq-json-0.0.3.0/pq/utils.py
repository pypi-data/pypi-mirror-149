def odig(dct, keys, value=None, condition=True):
    if type(dct) == dict and condition:
        for key in keys:
            try:
                dct = dct[key]
            except KeyError:
                return value
        return dct
    else:
        return value

def splitl(dct, key, new_key):
    lst = []
    if type(dct[key]) == list:
        for item in dct[key]:
            tmp_dct = dict(dct)
            del tmp_dct[key]
            tmp_dct[new_key] = item
            lst.append(tmp_dct)
    return lst


