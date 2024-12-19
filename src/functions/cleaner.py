import numpy as np
import pandas as pd
import os

data_folder = '../src/data/raw'
# Ensure the directory exists
#os.makedirs(data_folder, exist_ok=True)

def cleaner(shoppingdata, 
            apply_clean_names=True, 
            remove_negative_NA=True, 
            remove_missing=True, 
            impute_missing=False,
            remove_extreme=True, 
            ):

    
#Create a copy of the original data so as not to modify it inplace
    shopping = shoppingdata.copy()

    #1. Change the name of the column revenue to Purchase
    shopping["Purchase"] = shopping["Revenue"]
    shopping = shopping.drop(columns="Revenue")
        
    #2. Replace negative numbers with missing numbers
    if remove_negative_NA:
        shopping[["Administrative_Duration","Informational_Duration","ProductRelated_Duration"]] = shopping[["Administrative_Duration","Informational_Duration","ProductRelated_Duration"]].apply(lambda x: x.where(x>=0))
    
    #3. Remove 14 rows with missing records
    if remove_missing:
        shopping = shopping.dropna()
    elif impute_missing:
        shopping = shopping.fillna(0)
        
    #4. Remove extreme values in ProductRelated Duration
    if remove_extreme:
        shopping = shopping[(shopping["ProductRelated_Duration"] < 60) & (shopping["ProductRelated_Duration"] >= 720*60)]
    
    #5. clean_column names    
    if apply_clean_names:
        cleaned_shopping = clean_names(shopping)
    else:
        raise ValueError("Cleaning was not applied. Please check the condition.")
    
    #6. drop duplicates
    cleaned_shopping = cleaned_shopping.drop_duplicates()
    
    return cleaned_shopping
    
    
import re                                                                        
def clean_names(df):
    # Function to convert camel case to snake case
    def to_snake_case(name):
        # Insert underscores before uppercase letters and convert to lowercase
        name_with_underscores = re.sub(r'(?<!^)(?=[A-Z])', '_', name)
        name_with_underscores = name_with_underscores.lower()
        return re.sub(r'_+','_',name_with_underscores)

    # Clean the column names
    df.columns = [to_snake_case(re.sub(r'[^a-zA-Z0-9]+', '_', str(col))) for col in df.columns]
    return df 