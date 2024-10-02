# mathscript/stdlib/utils.py

def len_(obj):
    return len(obj)

def range_(start, end=None, step=1):
    if end is None:
        return range(start)
    else:
        return range(start, end, step)

def type_(obj):
    return type(obj).__name__
