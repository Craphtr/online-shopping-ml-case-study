# Load session
import dill
import os

from utils.config_loader import load_config

# Load config
config = load_config()

def load_session(filename):

    '''load session data from file

    Parameters:
    filename (str): Name of the file to load the session data from

    Returns:
    dict: Dictionary containing all variables in the session'''

    session_data_path = config['data']['session_data_path']
    file_path = os.path.join(session_data_path,filename)
    print(f" Loading session data from {file_path}")

    with open(filename,'rb') as f: #open the binary file for reading
        session_data = dill.load(f) #deserialize the data and load into a dictionary
    globals().update(session_data) #add all variables back to the current global namespace
    print(f"Session loaded from {file_path}")
    #