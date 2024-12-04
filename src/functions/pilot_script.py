import numpy as np
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','src')))

from functions.load_raw_data import load_raw_data
from functions.save_data import save_data
from functions.cleaner import cleaner
from functions.preprocessor import preprocessor


#load in the original data
shoppingdata = load_raw_data()

#Clean and preprocesses the data
print('Data Cleaning started')
cleaned_shopping = cleaner(shoppingdata, 
                    apply_clean_names=True, 
                    remove_negative_NA=True, 
                    remove_missing=True, 
                    impute_missing=False,
                    remove_extreme=False,)
print('Number of null values after cleaning raw data is',cleaned_shopping.isnull().sum())    


#Save cleaned data to file
save_data(cleaned_shopping,'cleaned_data','cleaned_shopping_data.pkl')

print('First preprocessing of cleaned data started')
clean_prepd_shopping = preprocessor(cleaned_shopping,
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

print('Number of null values after first preprocessing of cleaned data is',clean_prepd_shopping.isnull().sum())    
print("No encoding was applied to first instance of cleaning and preprocessing and all columns selected")
print("First instance of Cleaning & Preprocessing complete and data saved with no encoding.")


#Save the cleaned & preprocessed raw data with no encoding
save_data(clean_prepd_shopping, 'cleaned_preprocessed_data', 'cleaned_and_preprocessed_shopping_data.pkl')



#----
#Split the cleaned and preprocessed data into train, validation and test sets in a 60:20:20 ratio
print("Splitting cleaned and preprocessed data to Train, Test and Validation sets")

#Define the Shopping train set which is 60% of the cleaned and prepd data
shopping_train_noencoding = clean_prepd_shopping.sample(frac=0.6, random_state=3789)
print('Number of null values in training data with noencoding is',shopping_train_noencoding.isnull().sum())    

#Define the validation set which is 20% of sets remaining 
shopping_val_noencoding = clean_prepd_shopping.loc[~clean_prepd_shopping.index.isin(shopping_train_noencoding.index)].sample(frac=0.5, random_state=23789)
print('Number of null values in validation data with noencoding is',shopping_train_noencoding.isnull().sum())    
                
#Define the test set which is the remaining 20%
shopping_test_noencoding = clean_prepd_shopping.loc[~clean_prepd_shopping.index.isin(shopping_train_noencoding.index) & ~clean_prepd_shopping.index.isin(shopping_val_noencoding.index)]
print('Number of null values in test data with noencoding is',shopping_train_noencoding.isnull().sum())    

#save to raw splits file
save_data(shopping_train_noencoding, 'training_data', 'shopping_train_noencoding.pkl')
save_data(shopping_val_noencoding, 'validation_data', 'shopping_val_noencoding.pkl')
save_data(shopping_test_noencoding, 'test_data', 'shopping_test_noencoding.pkl')

#----

 
    
#----
#Preprocess the cleaned and preprocessed data without encoding
shopping_train_preprocessed_noencoder = preprocessor(shopping_train_noencoding, duration_to_mins=False, log_xform=False, encoder=False)
#----



#----
#Apply encoding to the Training Set
print("Applying Encoding to training set")
shopping_train_preprocessed_encoded = preprocessor(shopping_train_noencoding, 
                                                            duration_to_mins=False, 
                                                            log_xform=False, 
                                                            encoder=True)
print('Number of null values after preprocessing training data with encoding is',shopping_train_preprocessed_encoded.isnull().sum())    
save_data(shopping_train_preprocessed_encoded, 'encoded_training_data', 'shopping_train_preprocessed_encoded.pkl')


#Apply the same encoding to the validation set (using the training set's encoding scheme)
print("Applying Encoding to validation set")
shopping_val_preprocessed_encoded = preprocessor(shopping_val_noencoding,
                                                          column_selection=list(shopping_train_preprocessed_encoded.columns),
                                                          OS_level = shopping_train_preprocessed_noencoder["operating_systems"].unique(),
                                                          Browser_level = shopping_train_preprocessed_noencoder["browser"].unique(),
                                                          Region_level = shopping_train_preprocessed_noencoder['region'].unique(),
                                                          TrafficType_level = shopping_train_preprocessed_noencoder["traffic_type"].unique(),
                                                          duration_to_mins=False, log_xform=False, encoder=True)
print('Number of null values after preprocessing validation data with encoding is',shopping_val_preprocessed_encoded.isnull().sum())    
save_data(shopping_val_preprocessed_encoded, 'encoded_validation_data', 'shopping_val_preprocessed_encoded.pkl')


#Apply the same encoding to the test set
print("Applying Encoding to Test set")
shopping_test_preprocessed_encoded = preprocessor(shopping_test_noencoding,
                                                           column_selection=list(shopping_train_preprocessed_encoded.columns),
                                                           OS_level = shopping_train_preprocessed_noencoder["operating_systems"].unique(),
                                                           Browser_level = shopping_train_preprocessed_noencoder["browser"].unique(),
                                                           Region_level = shopping_train_preprocessed_noencoder["region"].unique(),
                                                           TrafficType_level = shopping_train_preprocessed_noencoder["traffic_type"].unique(),
                                                           duration_to_mins=False, log_xform=False,encoder=True)
print('Number of null values after preprocessing test data with encoding is',shopping_test_preprocessed_encoded.isnull().sum())    
save_data(shopping_test_preprocessed_encoded, 'encoded_test_data', 'shopping_test_preprocessed_encoded.pkl')

#----






