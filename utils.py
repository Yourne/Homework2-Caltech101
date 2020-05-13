import os.path
import json

def upload(file, params, values):
    """
    args: 
    file = a json file name in the current directory
    params: a list of hyperparams of a model
    values: a list of performance values for the given hyperparams
    """
    item = [params, values]
    
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
