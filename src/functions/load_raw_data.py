# src/functions/load_data.py

import pandas as pd
from utils.config_loader import load_config

# Load config
config = load_config()

# Use config to load raw data

def load_raw_data():
    raw_data_path = config['data']['raw_data_path']
    print(f"Attempting to load data from: {raw_data_path}")
    data = pd.read_csv(raw_data_path)
    return data