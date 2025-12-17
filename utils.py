def is_valid_time(t):
    if len(t) != 5 or t[2] != ":":
        return False
    hh, mm = t.split(":")
    if not (hh.isdigit() and mm.isdigit()):
        return False
    return 0 <= int(hh) < 24 and 0 <= int(mm) < 60
