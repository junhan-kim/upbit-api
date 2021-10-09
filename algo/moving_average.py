import pyupbit
from matplotlib import pyplot as plt


def get_moving_averages():
    # open / high / low / close / volume
    ohlcv = pyupbit.get_ohlcv(
        "KRW-BTC", interval="minute15", count=300)  # 15 분봉
    close = ohlcv['close']

    # moving averages
    window = close.rolling(5)
    ma5 = window.mean().to_frame()

    window = close.rolling(10)
    ma10 = window.mean().to_frame()

    window = close.rolling(20)
    ma20 = window.mean().to_frame()

    window = close.rolling(60)
    ma60 = window.mean().to_frame()

    window = close.rolling(120)
    ma120 = window.mean().to_frame()

    return ma5, ma10, ma20, ma60, ma120


def plot_moving_averages():
    ma5, ma10, ma20, ma60, ma120 = get_moving_averages()

    # plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(ma5)
    ax.plot(ma10)
    ax.plot(ma20)
    ax.plot(ma60)
    ax.plot(ma120)
    plt.show()
    plt.close()
