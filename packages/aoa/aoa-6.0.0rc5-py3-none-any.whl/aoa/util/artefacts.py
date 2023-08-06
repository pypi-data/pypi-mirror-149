

def save_plot(title, dpi=500):
    """
    This assumes the plot has already been rendered and we only need to save it.
    :param title: the title of the plot and the file name to save as (spaces replaced with _ and all lower)
    :param dpi: the dpi setting
    :return: None
    """
    import matplotlib.pyplot as plt

    plt.title(title)
    fig = plt.gcf()
    filename = title.replace(" ", "_").lower()
    fig.savefig('artifacts/output/{}'.format(filename), dpi=dpi)
    plt.clf()
