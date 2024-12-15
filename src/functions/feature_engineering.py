# feature_engineering.py
import numpy as np
import pandas as pd

def feature_engineering(cleaned_prepd_shopping):
                        
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

    #1.2. Engagement_Intensity computed tp predict user's intention as interaction between page_values, product_related_duration and informational_duration
    #prepd_and_engineered_shopping['engagement_intensity'] = prepd_and_engineered_shopping['product_related_duration']*prepd_and_engineered_shopping['page_values']*prepd_and_engineered_shopping['informational_duration']
    #print("Number of Null values in Engagement Intensity", prepd_and_engineered_shopping['engagement_intensity'].isnull().sum())

#2. Behavioural Indicators
    #2.1. Info_Explorer captures time spent exploring info related pages during the session duration
    prepd_and_engineered_shopping['info_explorer'] = prepd_and_engineered_shopping['informational_duration'] / prepd_and_engineered_shopping['session_duration'].replace([np.inf,-np.inf],prepd_and_engineered_shopping['informational_duration']).fillna(0)
    print("Number of Null values in info_explorer", prepd_and_engineered_shopping['info_explorer'].isnull().sum())

    #2.2. Product Explorer captures value to indicate purchase intent
    prepd_and_engineered_shopping['product_explorer'] = prepd_and_engineered_shopping['product_related_duration'] / prepd_and_engineered_shopping['session_duration'].replace([np.inf,-np.inf], prepd_and_engineered_shopping['product_related_duration']).fillna(0)
    print("Number of Null values in product_explorer", prepd_and_engineered_shopping['product_explorer'].isnull().sum())

    #2.3. Interaction Strength captures fraction of time spent between exploring and product interest
    prepd_and_engineered_shopping['interaction_strength'] = prepd_and_engineered_shopping['informational_duration'] + prepd_and_engineered_shopping['product_related_duration']
    print("Number of Null values in interaction_strength", prepd_and_engineered_shopping['interaction_strength'].isnull().sum())

    #2.4. Interaction Depth Are users going to more of product pages or spending more time learning 
    prepd_and_engineered_shopping['interaction_depth'] = prepd_and_engineered_shopping['product_related'] / prepd_and_engineered_shopping['informational'].replace([np.inf,-np.inf], prepd_and_engineered_shopping['product_related'])

    #2.5. Adjusted Bounce Rate weights bounce rate with session duration for a more realistic interpretation
    prepd_and_engineered_shopping['adjusted_bounce_rate'] = prepd_and_engineered_shopping['bounce_rates'] * prepd_and_engineered_shopping['session_duration']

    #2.6. Combined Dropoff Rate provides a more holistic view of how likely a session is to end without meaningful engagement
    prepd_and_engineered_shopping['combined_dropoff'] = prepd_and_engineered_shopping['bounce_rates'] * prepd_and_engineered_shopping['exit_rates']

#3. Traffic Source Impact
    #3.1 Source Value evaluates how traffic source impacts session value
    prepd_and_engineered_shopping['source_value'] = prepd_and_engineered_shopping['traffic_type'] * prepd_and_engineered_shopping['page_values']

    #3.2. Source Duration computes engagement differences by traffic type
    prepd_and_engineered_shopping['source_duration'] = prepd_and_engineered_shopping['traffic_type'] * prepd_and_engineered_shopping['session_duration']




