# src/functions/save_data.py

import pandas as pd
import os
from src.utils.config_loader import load_config

# Load config
config = load_config()

# Use config to save data
def save_data(data, file_name, data_type='train'):
    # save train,test or validation data into the interim directory
    interim_data_path = config['data']['interim_data_path']
    # make directory if it doesnt exist
    os.makedirs(interim_data_path, exist_ok=True)
    file_path = os.path