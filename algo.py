def get_moving_average(close, window_size):
    window = close.rolling(window_size)
    ma = window.mean().to_frame()
    return ma
