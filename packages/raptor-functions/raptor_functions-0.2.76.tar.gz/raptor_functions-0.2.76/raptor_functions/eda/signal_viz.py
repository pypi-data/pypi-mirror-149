import matplotlib
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_sensors(df, all = True, exps_numbers = [1,2,3], sensors_numbers = [1,2,3,4,5,6,7,8,9,10,11,12], overlap = False, figure_name = 'sensor_response', path = os.getcwd()):
    """
    Returns a figure with the visualisation of the sensor response, and saves it as a .pdf figure
    
    Plot: the time dependent profiles of the sensor response [mV] against the elapsed time [s] for a wide range of combination of experiments.

    Parameters
    ----------
    df: pandas dataframe
        Dataframe containing all the experiments and sensor mesaurements. See raptor_functions 'preprocessing' functions to generate this dataframe from the raw .txt files
        df = [exp_unique_id, exp_name, timesteps, sensor_1 ... sensor_n, Humidity (r.h.), measurement_stage, date_exp,time_elapsed, datetime_exp_start,datetime_exp, filename,result]
    exps_numbers: list of integers
        Selection list of the experiments to be plotted. The 'exp_numbers' are given by the 'exp_unique_id' of the pandas dataframe 'df'.
    sensor_numbers: list of integers
        Selection list of the sensors to be plotted. The 'sensors_numbers' are given by the columns of the pandas dataframe 'df' - usually containing 24 sensor columns.
    overlap: boolean
        If overlap = True -> the different experiments (for one single sensor) are plotted in the same axis. Better for comparison of the response between different experiments.
        If overlap = False -> different experiments are plotted in different columns. Better to look at individual responses.
        Default: False
    figure_name: str
        Name to give the figure to be saved as .pdf
    path: str
        Absolute path where the figure will be saved. If nothing provided, saved in the working directory.
    
    Returns
    -------
    figure
        Outputs a matplolib object figure.
    file
        Saves a .pdf in the path with the figure

    """
    # -----------------------------------------------------------
    # 
    n_total_sensors = len(list(filter(lambda k: 'sensor' in k, df.columns.tolist())))
    n_total_exps = df['exp_unique_id'].nunique()
    # 
    if all == True:
        sensors_numbers = list(np.linspace(1, n_total_sensors, n_total_sensors, dtype= int))
        exps_numbers = list(np.linspace(0, n_total_exps-1, n_total_exps, dtype=int))  
    # 
    # Pre-processing
    experiments = []
    n_exp = len(exps_numbers)
    for i in range(len(exps_numbers)):
        df_exp = df.loc[df['exp_unique_id'] == exps_numbers[i]]
        experiments.append(df_exp)
    # 
    sensors = []
    n_subplots_y = len(sensors_numbers)
    for i in range(len(sensors_numbers)):
        sensor_number = sensors_numbers[i]
        sensor = 'sensor_' + str(sensor_number)
        sensors.append(sensor)
    # 
    legend = True
    # 
    if overlap == False and len(exps_numbers) == 1:
        overlap = True
    # 
    if len(exps_numbers) == 1 and len(sensors_numbers)==1:
        # 
        fig, ax = plt.subplots(figsize=(6, 2), tight_layout=True)
        ax.plot(df_exp['time_elapsed'], df_exp[sensor])
        ax.set_xlabel(r'{Time [s]}')
        ax.set_ylabel(r'{Response [mV]}')
        ax.set_title('Experiment ' + str(exps_numbers[0]) + ': ' + str(sensors[0]))
        # 

    elif overlap == True:
        alpha_val = 1
        linewidth_val = 1
        if n_exp >3:
            print("Warning: adding line tansparency (alpha = 0.7) and thinner lines (0.5) for enhaced visualisation.")
            alpha_val = 0.7
            linewidth_val = 0.5
        # 
        fig, axs = plt.subplots(n_subplots_y,1,figsize=(6, 1.5*n_subplots_y),sharex=True,tight_layout=True)
        for i in range(n_subplots_y):
            try:
                if i == 0:
                    axs[i].set_title('Experiments ' + str(exps_numbers) + '\n' + str(sensors[i]))
                else:
                    axs[i].set_title(str(sensors[i]))
                # 
                for j in range(n_exp):
                    axs[i].plot(experiments[j]['time_elapsed'], experiments[j][sensors[i]],label = str(exps_numbers[j]), alpha=alpha_val, linewidth = linewidth_val)
                    handles, labels = axs[i].get_legend_handles_labels()
                axs[i].set_ylabel(r'{Response [mV]}')
                if i == n_subplots_y -1:
                    axs[i].set_xlabel(r'{Time [s]}')
                    fig.legend(handles, labels, bbox_to_anchor=(1,0.5), loc="center left", borderaxespad=0)
            except: # Handling error when axis is 1D: axs[i]. -> axs.
                if i == 0:
                    axs.set_title('Experiments ' + str(exps_numbers) + '\n' + str(sensors[i]))
                else:
                    axs.set_title(str(sensors[i]))
                # 
                for j in range(n_exp):
                    axs.plot(experiments[j]['time_elapsed'], experiments[j][sensors[i]],label = str(exps_numbers[j]), alpha=alpha_val, linewidth = linewidth_val)
                    handles, labels = axs.get_legend_handles_labels()
                axs.set_ylabel(r'{Response [mV]}')
                if i == n_subplots_y -1:
                    axs.set_xlabel(r'{Time [s]}')
                    fig.legend(handles, labels, bbox_to_anchor=(1,0.5), loc="center left", borderaxespad=0)
                
        # 
    else:
        n_subplots_x = n_exp
        fig, axs = plt.subplots(n_subplots_y, n_subplots_x,figsize=(6*n_subplots_x, 1.5*n_subplots_y),sharex=True,tight_layout=True)
        for j in range(n_subplots_x):
            for i in range(n_subplots_y):
                try:
                    if i == 0:
                        axs[i,j].set_title('Experiment ' + str(exps_numbers[j]) + '\n' + str(sensors[i]))
                    else:
                        axs[i,j].set_title(str(sensors[i]))
                    # 
                    axs[i,j].plot(experiments[j]['time_elapsed'], experiments[j][sensors[i]])
                    axs[i,j].set_ylabel(r'{Response [mV]}')
                    if i == n_subplots_y -1:
                        axs[i,j].set_xlabel(r'{Time [s]}')
                except: # Above fails when n_sensors = 1 -> as the axs[i,j] become a 2d Array
                    if i == 0:
                        axs[j].set_title('Experiment ' + str(exps_numbers[j]) + '\n' + str(sensors[i]))
                    else:
                        axs[j].set_title(str(sensors[i]))
                    # 
                    axs[j].plot(experiments[j]['time_elapsed'], experiments[j][sensors[i]])
                    axs[j].set_ylabel(r'{Response [mV]}')
                    if i == n_subplots_y -1:
                        axs[j].set_xlabel(r'{Time [s]}')
        # 
    # -----------------------------------------------------------
    figure_name_full = figure_name + '.pdf'
    if path != os.getcwd():
        plt.savefig(path + "/" + figure_name_full, bbox_inches='tight')
        print('Plot saved sucesfully!')
    else: 
        plt.savefig(figure_name_full, bbox_inches='tight')
        print('Plot saved sucesfully!')