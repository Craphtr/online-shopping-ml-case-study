#save session data
import dill
import os
from utils.config_loader import load_config

#load config
config = load_config()
def save_session(filename):
    
    '''Save all variables in the curent session to a file

    Parameters: 
    filename (str): Name of the file to save the session data'''

   #Use the config to define where to save the session data
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
    session_data_path = os.path.join(base_path,config['data']['session_data_path'])
    os.makedirs(session_data_path,exist_ok=True)

    #Full file path
    file_path = os.path.join(session_data_path,filename)

    print('Saving session data...')
    with open(file_path,'wb') as f: #open the file for binary writing
        dill.dump(globals(),f) #serialize all global variables and save 'em in a file
    print(f"Session saved successfully to {file_path}")
