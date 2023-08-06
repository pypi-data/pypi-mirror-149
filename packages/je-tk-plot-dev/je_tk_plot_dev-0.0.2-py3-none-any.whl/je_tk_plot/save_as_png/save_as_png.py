from matplotlib import pyplot


def save_as_png(filename: str, what_plot_you_want_to_save: pyplot, **kwargs):
    what_plot_you_want_to_save.savefig(filename, bbox_inches='tight', **kwargs)
