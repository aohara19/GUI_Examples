# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 08:49:38 2022

@author: allis
"""
import PySimpleGUI as sg
import numpy as np
import time
#from matplotlib.animation import FuncAnimation
import psutil
import collections
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
        
def plot_live_data(i,data,canvas,controls_canvas):
   for ax in plt.gcf().axes:
       
       # delete plots older than the most recent 4
       # make the newest plot red and the older ones blue
       # the older the plot, the more transparent
       if i >= 5:
           ax.get_lines()[i%5].remove()
           ax.get_lines()[3].set_color("blue")
           for j in range(4):
               ax.get_lines()[j].set_alpha(0.2*(j+1))
           
       elif i!=0:
           ax.get_lines()[i-1].set_color("blue")
           for j in range(i):
               ax.get_lines()[j].set_alpha(0.2*j)
           
       
   plt.figure(1)
   fig = plt.gcf()
   DPI = fig.get_dpi()
   # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
   fig.set_size_inches(404 * 2 / float(DPI), 344 / float(DPI))
   
       
   # plot cpu
   plt.plot(data,color='red')
   plt.ylim(0,100)    # plot memory

   draw_figure_w_toolbar(
       canvas, fig,controls_canvas)

# ------------------------------- PySimpleGUI CODE

layout1 = [
    [sg.B('Plot live data'),sg.B('Stop plotting live data'),sg.B('Exit')],
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

window = sg.Window('Graph with controls', layout,finalize=True)

# start collections with zeros
cpu = collections.deque(np.zeros(10))


canvas_elem = window['fig_cv']
canvas_plotting = canvas_elem.TKCanvas
canvas_toolbar = window['controls_cv'].TKCanvas

 # draw the intitial plot
fig, ax = plt.subplots()
ax.grid(True)

live_counter = 0
plot_live = False


while True:
    # set timeout equal to the the number of milliseconds between iterations of the graph
    # values smaller than 50 may not show the graph effectively
    event, values = window.read(timeout=200)
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):  # always,  always give a way out!
        break
    
    if event == 'Plot live data':
        plot_live = True
        
    elif event == 'Stop plotting live data':
        plot_live = False
        
    if plot_live is True:
        cpu.popleft()
        cpu.append(psutil.cpu_percent())
        plot_live_data(live_counter,cpu,canvas_plotting,canvas_toolbar)
        live_counter = live_counter + 1

     
window.close()
