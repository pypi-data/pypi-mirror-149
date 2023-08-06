import tkinter
import matplotlib.pyplot as plt
import numpy as np
from tkinter import (TOP, BOTH)
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from textwrap import wrap


def make_barh_graph(y_content_list: list, x_content_list: list, x_label: str = "", title: str = "", **kwargs):
    figure, axes = plt.subplots(**kwargs)
    y_pos = np.arange(len(y_content_list))
    axes.barh(y_pos, x_content_list, align='center')
    y_content_list = ['\n'.join(wrap(content, 20)) for content in y_content_list]
    axes.set_yticks(y_pos)
    axes.set_ylabel(y_content_list)
    axes.invert_yaxis()  # labels read top-to-bottom
    axes.set_xlabel(x_label)
    axes.set_title(title)
    return figure


def set_tkinter_embed_matplotlib_barh(y_content_list: list, x_content_list: list,
                                      show_figure_window: tkinter.Tk = None,
                                      x_label: str = "", title: str = "", **kwargs):
    if show_figure_window is None:
        show_figure_window = tkinter.Tk()
        show_figure_window.title = ""
        window_width, window_height = show_figure_window.winfo_screenwidth(), show_figure_window.winfo_screenheight()
        show_figure_window.geometry("%dx%d+0+0" % (window_width, window_height))
    else:
        show_figure_window.title = ""
        window_width, window_height = show_figure_window.winfo_screenwidth(), show_figure_window.winfo_screenheight()
        show_figure_window.geometry("%dx%d+0+0" % (window_width, window_height))
    figure = make_barh_graph(y_content_list, x_content_list, x_label, title)
    canvas = FigureCanvasTkAgg(figure, master=show_figure_window)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    show_figure_window.mainloop()
