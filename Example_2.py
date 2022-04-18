import PySimpleGUI as sg
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.

# VARS CONSTS:
_VARS = {'window': False}

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

#layout for experiment 1
layout1 = [[sg.Text('Please enter inputs for experiment 1')],
           [sg.Text('First parameter for experiment 1 (float):'),sg.Input(key='first_param1')],
           [sg.Text('Second parameter for experiment 1 (float): '),sg.Input(key='second_param1')],
           [sg.Text('Third parameter for experiment 1 (int):'),sg.Input(key='third_param1')],
           [sg.Text('Fourth parameter for experiment 1 (string):'),sg.Input(key='fourth_param1')]]

#layout for experiment 2
layout2 = [[sg.Text('Please enter inputs for experiment 2')],
           [sg.Text('First parameter for experiment 2 (float):'),sg.Input(key='first_param2')],
           [sg.Text('Second parameter for experiment 2 (float): '),sg.Input(key='second_param2')],
           [sg.Text('Third parameter for experiment 2 (string):'),sg.Input(key='third_param2')]]

#layout for experiment 3
layout3 = [[sg.Text('Please enter inputs for experiment 3')],
           [sg.Text('First parameter for experiment 3 (int):'),sg.Input(key='first_param3')],
           [sg.Text('Second parameter for experiment 3 (int): '),sg.Input(key='second_param3')],
           [sg.Text('Third parameter for experiment 3 (int):'),sg.Input(key='third_param3')],
           [sg.Text('Fourth parameter for experiment 3 (int): '),sg.Input(key='fourth_param3')],
           [sg.Text('Fifth parameter for experiment 3 (string): '),sg.Input(key='fifth_param3')]]

layout_all_exps = [
    [sg.T('X Label:'), sg.Input(default_text = 'x',key = 'x_label')],
    [sg.T('X Label:'), sg.Input(default_text = 'y',key = 'y_label')],
    [sg.T('What color would you like your plot?')],
    [sg.Combo(['red','blue','black','yellow','green','magenta','cyan'] ,default_value='black',key='color')],
    [sg.T('What style would you like your plot?')],
    [sg.Combo(['solid','dotted','dashed'], default_value='solid', key = 'linestyle')],
    [sg.Checkbox('Set x-range of plot (with floats)', default = False, key = 'x_range'),sg.T('From')
     ,sg.Input(key='x_min'),sg.T(' to '), sg.Input(key = 'x_max')],
    [sg.Checkbox('Set y-range of plot (with floats)', default = False, key = 'y_range'),sg.T('From')
     ,sg.Input(key='y_min'),sg.T(' to '), sg.Input(key = 'y_max')],
    [sg.Text("Choose a file to save inputs in: "), sg.Input(),sg.FileBrowse(key='file')],
    [sg.Button('Start'), sg.Button('Exit')]]

layout_plot = [
    [sg.B('Update Plot'), sg.B('Clear Canvas'),sg.B('Exit')],
    [sg.T('Controls:')],
    [sg.Canvas(key='controls_cv')],
               [sg.T('Figure:')],
               [sg.Column(
                   layout=[
                       [sg.Canvas(key='fig_cv',
                                  # it's important that you set this size
                                  size=(400 * 2, 800))]],
                   background_color='#DAE0E6',
                   pad=(0, 0))]]

# ----------- Create actual layout using Columns 
# This initially shows a drop down for type of experiment
# once one is chosen, it shows the layout corresponding to the experiment
# and asks for the proper inputs. It also allows user to choose where
# inputs are saved
layout = [[sg.Text('Experiments')],
            [sg.Text('What type of experiment would you like to run?')],
            [sg.Combo(['Experiment 1','Experiment 2','Experiment 3'],default_value='Experiment 1',key='type')],[sg.Button('Enter')],
            [sg.Column(layout1, visible = False, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-'), 
             sg.Column(layout3, visible=False, key='-COL3-'),sg.Column(layout_all_exps, visible=False, key='-All-')]]

# Create the Window
def make_win1():
    return sg.Window('Window Title', layout, location = (50,100), finalize=True)

def make_win2():
    return sg.Window('Second Window', layout_plot, finalize=True,
                             resizable=True,
                             location=(100, 100),
                             element_justification="center",
                             background_color='#FDF6E3')

_VARS = {'window': False}
window1, window2 = make_win1(), None        # start off with 1 window open

madeWindow = 0
layout = 1
fig = None

# Event Loop to process "events" and get the "values" of the inputs
while True:
    window,event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks exit
        if (window != None):
            window.close()
        if window == window2:       # if closing win 2, mark as closed
            window2 = None
        elif window == window1:     # if closing win 1, exit program
            window1=None
    
    if event == 'Enter':
        window[f'-COL{layout}-'].update(visible=False)
        window['-All-'].update(visible=False)
        if(values['type'] == 'Experiment 1'):
            layout = 1
        elif(values['type']=='Experiment 2'):
            layout = 2
        elif(values['type']=='Experiment 3'):
            layout = 3
        window[f'-COL{layout}-'].update(visible=True)
        window['-All-'].update(visible=True)
        
    if event == 'Start':
        if(layout == 1):
            
            # Code for Experiment 1
            exp1_params = {
            'first_param':   float(values['first_param1']), 
            'second_param':     float(values['second_param1']),
            'third_param':           int(values['third_param1']),
            'fourth_param':   values['fourth_param1']
                }

            plt.figure(1)
            fig = plt.gcf()
            DPI = fig.get_dpi()
            # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
            fig.set_size_inches(404 * 2 / float(DPI), 344 / float(DPI))
            # ------------------------------
            
            if (values['x_range']==True):
                x=np.linspace(float(values['x_min']),float(values['x_max']))
            else:
                # this can be changed to set the automatic x-range of the plot
                x = np.linspace(0, 2 * np.pi)
          
            # this should be changed to create your plot, and is just an example function
            # You should change code from here
            y = np.sin(x) * exp1_params['first_param'] + exp1_params['second_param']*exp1_params['third_param']
           
            plt.title(exp1_params['fourth_param'])
              
            plt.plot(x, y, color = values['color'],linestyle = values['linestyle'])
            
            # to here
          
            if (values['x_range']==True):
                plt.xlim(int(values['x_min']), int(values['x_max']))
          
            if (values['y_range']==True):
                plt.ylim(int(values['y_min']), int(values['y_max']))
      
            plt.xlabel(values['x_label'])
            plt.ylabel(values['y_label'])
            plt.grid(b=True)


            if (madeWindow == 0) :
                window2= make_win2()
                madeWindow = 1;
            
            
            if (values['file']!=''):
                with open(values['file'],'w') as datafile:
                    writer = csv.writer(datafile)
                    for key in exp1_params.keys():
                        datafile.write("%s,%s\n"%(key,exp1_params[key]))
          
            
        elif(layout == 2):
            # Code for Experiment 2
            exp2_params = {
            'first_param':   float(values['first_param2']), 
            'second_param':     float(values['second_param2']),
            'third_param':          values['third_param2']
                }
            
            plt.figure(1)
            fig = plt.gcf()
            DPI = fig.get_dpi()
            # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
            fig.set_size_inches(404 * 2 / float(DPI), 344 / float(DPI))
            # ------------------------------
            if (values['x_range']==True):
                x=np.linspace(float(values['x_min']),float(values['x_max']))
            else:
                # this can be changed to set the automatic x-range of the plot
                x = np.linspace(0, 2 * np.pi)
          
            # this should be changed to create your plot, and is just an example function
            # Change code from here
            y = np.cos(x) * exp2_params['first_param'] + exp2_params['second_param']
            plt.title(exp2_params['third_param'])
              
            plt.plot(x, y, color = values['color'],linestyle = values['linestyle'])
          
            # to here
          
            if (values['x_range']==True):
                plt.xlim(float(values['x_min']), float(values['x_max']))
          
            if (values['y_range']==True):
                plt.ylim(float(values['y_min']), float(values['y_max']))
      
            plt.xlabel(values['x_label'])
            plt.ylabel(values['y_label'])
            plt.grid(b=True)


            if (madeWindow == 0) :
                window2= make_win2()
                madeWindow = 1;
            
            if (values['file']!=''):
                with open(values['file'],'w') as datafile:
                    writer = csv.writer(datafile)
                    for key in exp2_params.keys():
                        datafile.write("%s,%s\n"%(key,exp2_params[key]))
          

        elif (layout ==3):
            # Code for Experiment 1
            exp3_params = {
            'first_param':   int(values['first_param3']), 
            'second_param':     int(values['second_param3']),
            'third_param':           int(values['third_param3']),
            'fourth_param':   int(values['fourth_param3']),
            'fifth_param':    values['fifth_param3']
                }
            
            plt.figure(1)
            fig = plt.gcf()
            DPI = fig.get_dpi()
            # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
            fig.set_size_inches(404 * 2 / float(DPI), 344 / float(DPI))
            # ------------------------------
            if (values['x_range']==True):
                x=np.linspace(float(values['x_min']),float(values['x_max']))
            else:
                # this can be changed to set the automatic x-range of the plot
                x = np.linspace(0, 2 * int(exp3_params['second_param']))
          
            # this should be changed to create your plot, and is just an example function
            # You should change code from here
            xpoints = np.array([exp3_params['first_param'],exp3_params['second_param']])
            ypoints = np.array([exp3_params['third_param'],exp3_params['fourth_param']])
            plt.title(exp3_params['fifth_param'])
            
            plt.plot(xpoints, ypoints, color = values['color'],linestyle = values['linestyle'])
            
            # to here
          
            if (values['x_range']==True):
                plt.xlim(float(values['x_min']), float(values['x_max']))
          
            if (values['y_range']==True):
                plt.ylim(float(values['y_min']), float(values['y_max']))
      
            plt.xlabel(values['x_label'])
            plt.ylabel(values['y_label'])
            plt.grid(b=True)


            if (madeWindow == 0) :
                window2= make_win2()
                madeWindow = 1;
            
            if (values['file']!=''):
                with open(values['file'],'w') as datafile:
                    writer = csv.writer(datafile)
                    for key in exp3_params.keys():
                        datafile.write("%s,%s\n"%(key,exp3_params[key]))
            
    elif event == 'Update Plot':
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)
            

    elif event == 'Clear Canvas':
        plt.close('all')
        plt.show()

        
window.close()



