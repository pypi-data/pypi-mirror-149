import math

def is_number(value):
    try:
        float(value)
        return True
    except:
        return False