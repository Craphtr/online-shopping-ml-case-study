# src/functions/save_data.py

import pandas as pd
import os
from utils.config_loader import load_config

# Load config
config = load_config()

# Use config to save data
def save_data(data, data_name, file_name):
    # save train,test or validation data into the interim directory
    interim_data_path = config['data']['interim_data_path']
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
    interim_data_path = os.path.abspath(os.path.join(base_path,interim_data_path))
   
    # make directory if it doesnt exist
    os.makedirs(interim_data_path, exist_ok=True)
    
    #save the dataset to the interim folder with the provided name
    file_path = os.path.join(interim_data_path, file_name)
    data.to_pickle(file_path)
    print(f"Saved {data_name} successfully to {file_path}")
