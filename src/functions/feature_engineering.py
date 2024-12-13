# feature_engineering.py
import numpy as np
import pandas as pd

def feature_engineering(cleaned_prepd_shopping,
                        apply_compute_engagement=True,
                        ):
    """
    This function performs feature engineering on the cleaned and preprocessed shopping data
    
    Parameters:
    cleaned_prepd_shopping (DataFrame): cleaned and preprocessed shopping data
    
    Returns: 
    prepd_and_engineered_shopping (DataFrame): preprocessed and engineered data
     
    Usage:
    prepd_and_engineered_shopping = feature_engineering(cleaned_prepd_shopping):
    """
    prepd_and_engineered_shopping = cleaned_prepd_shopping.copy()


    # Add New Engineered Features   

#1. User Engagement Features
    #1.1. Session_duration captures the total time spent during a session
    prepd_and_engineered_shopping['session_duration'] = prepd_and_engineered_shopping[['administrative_duration','informational_duration','product_related_duration']].sum(axis=1)

    #1.2. Engagement_Intensity computes the ratio of page_values/session_duration to reflect how valuable the session was relative to the time spent
    if apply_compute_engagement:
        prepd_and_engineered_shopping['engagement_intentsity'] = prepd_and_engineered_shopping.apply(compute_engagement,axis=1)
        print("Number of Null values in Engagement Intensity", prepd_and_engineered_shopping['engagement_intensity'].isnull().sum())

#2. Behavioural Indicators
    #2.1. Info_Explorer captures time spent exploring info related pages during the session duration
    prepd_and_engineered_shopping['info_explorer'] = prepd_and_engineered_shopping['informational_duration']/prepd_and_engineered_shopping['session_duration'].replace([np.inf,-np.inf],1e4).fillna(0)

    #2.2. Product Explorer captures value to indicate purchase intent
    prepd_and_engineered_shopping['product_explorer'] = prepd_and_engineered_shopping['product_related_duration']/prepd_and_engineered_shopping['session_duration'].replace([np.inf,-np.inf], 1e6).fillna(0)

    #2.3. Interaction Strength captures fraction of time spent between exporing and product interest
    





#Compute Engagement
def compute_engagement(row):
    if row['session_duration'] == 0:
        if row['purchase'] == 1:
            return 1e6 #Assign a large value for decisive engagement
        else:
            return 0 #Assign 0 for a likely bounce
    else: return row['page_values']/row['session_duration']

#Compute Info Explorer
def compute_info_explorer(row):
    if row['informational_duration']/row['session_duration'] == np.inf()
