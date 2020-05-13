import os.path
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)
import numpy as np


def upload_model_results(file, params, train_scores, val_scores):
    """
    args: 
    file = a json file name in the current directory
    params: a list of hyperparams of a model
    train_scores: a list of performance values over the train dataset
    val_scores: a list of performance values over the train dataset
    """
    item = [params, train_scores, val_scores]
    
    if os.path.isfile(file):
        
        # load data from file
        with open(file) as f:
            data = json.load(f)
        data.append(item)
        
        # overwrite the file
        with open(file, mode='w') as f:
            json.dump(data, f)
            
    else:
        with open(file, mode='w') as f:
            json.dump([item], f)

def plot_model_results(file, score_label='loss', index=-1):
    """
    args
    file = output of upload_model_results function. file must be in the current directory
    index = list index of the output of upload_mode_results.
    score_label (string): name of the score e.g. 'accuracy', 'loss'
    """
    with open(file) as f:
        data = json.load(f)
    
    train_scores = data[index][1]
    val_scores = data[index][2]
    epochs = len(data[index][1])
    title = data[index][0]
    
    fig, ax = plt.subplots()
    ax.plot(range(epochs), train_scores, marker='.', label='train')
    ax.plot(range(epochs), val_scores, marker='.', label='val')
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    if score_label == 'accuracy':
        ax.set_yticks(np.arange(0, 1.2, 0.2))
    ax.set_xlabel('epochs')
    ax.set_ylabel(score_label)
    ax.grid()
    ax.set_title(title)
    ax.legend(loc='upper right')
