import numpy as np
import pandas as pd
import os
import re
import sys
sys.path.append("../src/") 

from sklearn.pipeline import Pipeline
from src.functions.load_raw_data import load_raw_data
from src.functions.cleaner_shopping import cleaner_shopping
from src.functions.preprocessor_shopping import preprocessor_shopping

data_folder = "../data/raw"

#load in the original data
shoppingdata = load_raw_data()

#Clean and preprocesses the data
cleaned_shopping = cleaner_shopping(shoppingdata, 
                    apply_clean_names=True, 
                    remove_negative_NA=True, 
                    remove_missing=True, 
                    impute_missing=False,
                    remove_extreme=False,)
print('Number of null values after cleaning is',cleaned_shopping.isnull().sum())    


#Save cleaned data to file
cleaned_shopping.to_pickle(os.path.join(data_folder,'cleaned_shopping_data.pkl'))

clean_prepd_shopping = preprocessor_shopping(cleaned_shopping,
                          numeric_to_cat=True,
                          duration_to_mins = True,
                          visitor_to_binary=True,
                          OS_level=None, 
                          Browser_level=None, 
                          Region_level=None, 
                          TrafficType_level=None,
                          month_to_numeric=True,
                          log_xform=True, 
                          encoder=False,
                          column_selection=None,
                          apply_clean_names=True)

print('Number of null values after preprocessing is',clean_prepd_shopping.isnull().sum())    
print("No encoding was applied and all columns selected")
print("Cleaning & Preprocessing complete and data saved with no encoding.")


#Save the cleaned & preprocessed raw data with no encoding
clean_prepd_shopping.to_pickle(os.path.join(data_folder,'../data/cleaned_and_preprocessed_shopping_data.pkl'))



#----
#Split the cleaned and preprocessed data into train, validation and test sets in a 60:20:20 ratio
#Define the Shopping train set which is 60% of the cleaned and prepd data
shopping_train_noencoding = clean_prepd_shopping.sample(frac=0.6, random_state=3789)
print('Number of null values after preprocessing with noencoding is',shopping_train_noencoding.isnull().sum())    

#Define the validation set which is 20% of sets remaining 
shopping_val_noencoding = clean_prepd_shopping.loc[~clean_prepd_shopping.index.isin(shopping_train_noencoding.index)].sample(frac=0.5, random_state=23789)
                 
#Define the test set which is the remaining 20%
shopping_test_noencoding = clean_prepd_shopping.loc[~clean_prepd_shopping.index.isin(shopping_train_noencoding.index) & ~clean_prepd_shopping.index.isin(shopping_val_noencoding.index)]

#save to raw splits file
shopping_train_noencoding.to_pickle(os.path.join(data_folder,'shopping_train_noencoding.pkl'))
shopping_val_noencoding.to_pickle(os.path.join(data_folder,'shopping_val_noencoding.pkl'))
shopping_test_noencoding.to_pickle(os.path.join(data_folder,'shopping_test_noencoding.pkl'))
#----

 
    
#----
#Preprocess the cleaned and preprocessed data without encoding
shopping_train_preprocessed_noencoder = preprocessor_shopping(shopping_train_noencoding, duration_to_mins=False, log_xform=False, encoder=False)
#----



#----
#Apply encoding to the Training Set
shopping_train_preprocessed_encoded = preprocessor_shopping(shopping_train_noencoding, 
                                                            duration_to_mins=False, 
                                                            log_xform=False, 
                                                            encoder=True)
print("Encoding applied to training set and saved")
print('Number of null values after preprocessing with encoding is',shopping_train_preprocessed_encoded.isnull().sum())    


#Apply the same encoding to the validation set (using the training set's encoding scheme)
shopping_val_preprocessed_encoded = preprocessor_shopping(shopping_val_noencoding,
                                                          column_selection=list(shopping_train_preprocessed_encoded.columns),
                                                          OS_level = shopping_train_preprocessed_noencoder["operating_systems"].unique(),
                                                          Browser_level = shopping_train_preprocessed_noencoder["browser"].unique(),
                                                          Region_level = shopping_train_preprocessed_noencoder['region'].unique(),
                                                          TrafficType_level = shopping_train_preprocessed_noencoder["traffic_type"].unique(),
                                                          duration_to_mins=False, log_xform=False, encoder=True)
print("Encoding applied to validation set and saved")
                                           
#Apply the same encoding to the test set
shopping_test_preprocessed_encoded = preprocessor_shopping(shopping_test_noencoding,
                                                           column_selection=list(shopping_train_preprocessed_encoded.columns),
                                                           OS_level = shopping_train_preprocessed_noencoder["operating_systems"].unique(),
                                                           Browser_level = shopping_train_preprocessed_noencoder["browser"].unique(),
                                                           Region_level = shopping_train_preprocessed_noencoder["region"].unique(),
                                                           TrafficType_level = shopping_train_preprocessed_noencoder["traffic_type"].unique(),
                                                           duration_to_mins=False, log_xform=False,encoder=True)
print("Encoding applied to test set and saved")

#save the encoded slpits
shopping_train_preprocessed_encoded.to_pickle(os.path.join(data_folder, 'shopping_train_preprocessed_encoded.pkl'))
shopping_val_preprocessed_encoded.to_pickle(os.path.join(data_folder, 'shopping_val_preprocessed_encoded.pkl'))
shopping_test_preprocessed_encoded.to_pickle(os.path.join(data_folder, 'shopping_test_preprocessed_encoded.pkl'))
#----






