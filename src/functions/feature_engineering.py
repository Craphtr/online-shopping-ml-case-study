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
    #Session_duration captures the total time spent during a session
    prepd_and_engineered_shopping['session_duration'] = prepd_and_engineered_shopping[['administrative_duration','informational_duration','product_related_duration']].sum(axis=1)

    #Engagement_Intensity computes the ratio of page_values/session_duration to reflect how valuable the session was relative to the time spent
    if apply_compute_engagement:
        prepd_and_engineered_shopping['engagement_intentsity'] = prepd_and_engineered_shopping.apply(compute_engagement,axis=1)









def compute_engagement(row):
    if row['session_duration'] == 0:
        if row['purchase'] == 1:
            return 1e6 #Assign a large value for decisive engagement
        else:
            return 0 #Assign 0 for a likely bounce
    else: return row['page_values']/row['session_duration']