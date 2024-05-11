"""Utils
Helpfull mini functions.
"""

def round_int_uni(value, base=100, step=10):
    """Integer rounding
    Arguments:
    value -- The valuse to round.
    base  -- The base value for rounding (default 100).
    step  -- The steps it will be round. If step is zero, it will be round to
             the zero base. If step is equvell base, it will be round to the
             base (default 10).
    Return:  It returns the rounded value.
    """
    factor = 1

    if not base:
        return value

    if step <= 0:
        correction = 0
        step = base
    elif step >= base:
        correction = base - 1
    else:
        correction = (step - 1) // 2
        factor = base // step

    result = ((value + correction) * factor // base) * step
    return result

def round_int_uni_difference(value, base=100, step=10):
    """Integer rounding difference
    Uses `rount_int_uni()` to determine the rounding difference.

    Arguments:
    value -- The valuse to round.
    base  -- The base value for rounding (default 100).
    step  -- The steps it will be round. If step is zero, it will be round to
             the zero base. If step is equvell base, it will be round to the
             base (default 10).
    Return:  It returns the rounded value.
    """
    result = round_int_uni(value, base, step)
    result = result - value
    return result

