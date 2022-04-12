import PySimpleGUI as sg
import numpy as np

"""
    Example GUI
"""

# ------------------------------- This is to include a matplotlib figure in a Tkinter canvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)


class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)


# ------------------------------- PySimpleGUI CODE

layout1 = [
    [sg.T('Manually enter your function (use the form np.func(x) for numpy functions)'), 
     sg.Input(default_text='np.sin(x)',key='function')],
    [sg.T('X Label:'), sg.Input(default_text = 'x',key = 'x_label')],
    [sg.T('X Label:'), sg.Input(default_text = 'y',key = 'y_label')],
    [sg.T('What color would you like your plot?')],
    [sg.Combo(['red','blue','black','yellow','green','magenta','cyan'] ,default_value='black',key='color')],
    [sg.T('What style would you like your plot?')],
    [sg.Combo(['solid','dotted','dashed'], default_value='solid', key = 'linestyle')],
    [sg.Checkbox('Set x-range of plot', default = False, key = 'x_range'),sg.T('From')
     ,sg.Input(key='x_min'),sg.T(' to '), sg.Input(key = 'x_max')],
    [sg.Checkbox('Set y-range of plot', default = False, key = 'y_range'),sg.T('From')
     ,sg.Input(key='y_min'),sg.T(' to '), sg.Input(key = 'y_max')],
    [sg.B('Plot'), sg.B('Clear Canvas'),sg.B('Exit')],
    [sg.T('Controls:')],
    [sg.Canvas(key='controls_cv')],
    [sg.T('Figure:')],
    [sg.Column(
        layout=[
            [sg.Canvas(key='fig_cv',
                       # it's important that you set this size
                       size=(400 * 2, 800))]],
        background_color='#DAE0E6',
        pad=(0, 0)
    )]
    ]

layout = [
                         #this can be changed to set the size of the window
    [sg.Column(layout1, scrollable = True, size = (900,600))]]

window = sg.Window('Graph with controls', layout)

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):  # always,  always give a way out!
        break
    elif event == 'Plot':
        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()
        # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
        fig.set_size_inches(404 * 2 / float(DPI), 344 / float(DPI))
        # ------------------------------
        # this can be changed to set the automatic x-range of the plot
        x = np.linspace(0, 2 * np.pi)
        
        y = eval(values['function'])
        plt.title(values['function'])
            
        plt.plot(x, y, color = values['color'],linestyle = values['linestyle'])
        
        if (values['x_range']==True):
            plt.xlim(int(values['x_min']), int(values['x_max']))
        
        if (values['y_range']==True):
            plt.ylim(int(values['y_min']), int(values['y_max']))
    
        plt.xlabel(values['x_label'])
        plt.ylabel(values['y_label'])
        plt.grid(b=True)

        # ------------------------------- Instead of plt.show()
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)
    
    elif event == 'Clear Canvas':
        plt.close('all')
        plt.show()
window.close()
