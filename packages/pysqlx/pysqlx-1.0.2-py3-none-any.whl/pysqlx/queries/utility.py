

def check_cols(cols, cols_all):
    for col in cols:
        if col not in cols_all:
            return False
    return True


def check_order_by_cols(cols0, cols1):
    if not all((cols0, cols1)):
        return True

    for col in cols0:
        if col in cols1:
            return False

    for col in cols1:
        if col in cols0:
            return False

    return True
