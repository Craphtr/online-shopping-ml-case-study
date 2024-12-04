# src/utils/confoig_loader.py

from dotenv import load_dotenv
import os
import yaml

def load_config(config_file='configs/config.yaml'):

    #define the path of the config file relative to the project root i.e two levels up
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
    
    #Load environment varioables from .env file
    load_dotenv(dotenv_path=os.path.join(base_path,'.env'))
    # Check if PYTHONPATH is loaded
    print("Environment Variables Loaded:")
    print("PYTHONPATH:", os.getenv('PYTHONPATH'))  # Check if PYTHONPATH is set

    #Full path to configuration file
    config_file_path = os.path.join(base_path,config_file)
    
    #Load and return the configuration
    try:
        with open(config_file_path, 'r') as file:
            config = yaml.safe_load(file)
        #Convert relative paths to absolute paths
        for key, relative_path in config['data'].items():
            if isinstance(relative_path, str) and relative_path:
                config['data'][key] = os.path.abspath(os.path.join(base_path,relative_path))
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")
