import string

def showUserDefinedProperty(obj, output=False, formated=False):
    """Return an list of user defined propertys. """
    properties = filter(lambda (x): string.find(x, "__") == -1, dir(obj))
    if output:
        if formated:
            for p in properties:
                print p
        else:
            print properties
    else:
        return properties
    return None
        