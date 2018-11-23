

def get_error_fn(error_type):
    if error_type == 0:
        return mse_error
    elif error_type == 1:
        return ma_error

def mse_error(a,b):
    return a+b

def ma_error(a,b):
    return max(a,b)

