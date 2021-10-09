from matplotlib import pyplot as plt


def plot_df(dfs):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for df in dfs:
        ax.plot(df)
    plt.show()
    plt.close()
