import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler

data_folder = '../data/'

#Read the cleaned data and create a copy of it so as not to modify it inplace
#cleaned_shopping = pd.read_pickle('../data/cleaned_shopping_data.pkl')
def preprocessor(cleaned_shopping,
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
                scaler=False,
                column_selection=None,
                apply_clean_names=True
                ):
    
   
    preprocessed_shopping = cleaned_shopping.copy()
    
    #1. Convert Weekend to Numeric
    preprocessed_shopping["weekend"] = preprocessed_shopping["weekend"].astype("int64")

    # Convert Month to categorical and arranged in order
    #preprocessed_shopping["month"] = preprocessed_shopping["month"].str.strip().str.title()
    if not pd.api.types.is_categorical_dtype(preprocessed_shopping["month"]):
        month_order = ['Feb','Mar','May','June','Jul','Aug','Sep','Oct','Nov','Dec']
        preprocessed_shopping["month"] = pd.Categorical(preprocessed_shopping['month'],categories=month_order, ordered=True)

    #2. Convert operating systems, browser, traffic type and region numeric features to categorical 
    if numeric_to_cat:
        preprocessed_shopping[["operating_systems", "browser", "traffic_type","region"]] = preprocessed_shopping[["operating_systems", "browser", "traffic_type","region"]].astype(str)

    #3. Convert duration from seconds to minutes
    if duration_to_mins:
        preprocessed_shopping[["administrative_duration","informational_duration","product_related_duration"]] =  preprocessed_shopping[["administrative_duration","informational_duration","product_related_duration"]].apply(lambda x: x/60)
        
    #4. Convert visitor_type to binary
    if visitor_to_binary:
        if preprocessed_shopping["visitor_type"].dtype == 'object':
            preprocessed_shopping["visitor_type"] = preprocessed_shopping["visitor_type"].str.strip().str.title()
            preprocessed_shopping["visitor_type"] = preprocessed_shopping["visitor_type"].map({"New_Visitor": 1, "Other": 0, "Returning_Visitor": 0})
        
    #5. Combine low-level of categorical observations into single category
    #OS_Level
    if OS_level is not None:
        preprocessed_shopping["operating_systems"] = preprocessed_shopping["operating_systems"].apply(lambda x: x if x in OS_level else "other")
    else:
        preprocessed_shopping["operating_systems"] = preprocessed_shopping["operating_systems"].apply(lambda x: x if preprocessed_shopping["operating_systems"].value_counts()[x] >= 50 else "other")
    #Browser
    if Browser_level is not None:
        preprocessed_shopping["browser"] = preprocessed_shopping["browser"].apply(lambda x: x if x in Browser_level else "Other")
    else: 
        preprocessed_shopping["browser"] = preprocessed_shopping["browser"].apply(lambda x : x if preprocessed_shopping["browser"].value_counts()[x] >= 50 else "other")
    #Region
    if Region_level is not None:
        preprocessed_shopping["region"] = preprocessed_shopping["region"].apply(lambda x : x if x in Region_level else "other")
    else:
        preprocessed_shopping["region"] = preprocessed_shopping["region"].apply(lambda x : x if preprocessed_shopping["region"].value_counts()[x] >= 50 else "other")
         #TrafficType
    if TrafficType_level is not None:
        preprocessed_shopping["traffic_type"] = preprocessed_shopping["traffic_type"].apply(lambda x: x if x in TrafficType_level else "Other")
    else:
        preprocessed_shopping["traffic_type"] = preprocessed_shopping["traffic_type"].apply(lambda x: x if preprocessed_shopping["traffic_type"].value_counts()[x] >= 50 else "other")

    ##Handle Missing and unexpected values in month before mapping
    if preprocessed_shopping['month'].isnull().sum()>0:
        print('Warning: Missing or unexpected values in month before mapping')
        print(preprocessed_shopping['month'].unique())

     #6. Convert month variable to numeric
    if month_to_numeric : 
        if "month_numeric" not in preprocessed_shopping.columns:
            #create the column
            month_mapping = {"Feb": 2, "Mar": 3, "May": 5, "June": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
            preprocessed_shopping["month_numeric"] = preprocessed_shopping["month"].map(month_mapping)

    if preprocessed_shopping["month"].isnull().sum() > 0:
        print("Warning: Missing values in 'month' column after mapping.")
        print(preprocessed_shopping["month"].unique())
        
    #7. Log Transform of Predictors
    if log_xform:
        preprocessed_shopping[["administrative","administrative_duration", "informational","informational_duration","product_related","product_related_duration"]] = np.log(preprocessed_shopping[["administrative","administrative_duration", "informational","informational_duration","product_related","product_related_duration"]] + 1)
     
    #8. Standardize Predictors
    if scaler:
        scaler = MinMaxScaler()
        columns_to_scale = ["administrative","administrative_duration", "informational","informational_duration","product_related","product_related_duration"]
        scaled_data = scaler.fit_transform(preprocessed_shopping[columns_to_scale])
        preprocessed_shopping[columns_to_scale]=pd.DataFrame(scaled_data,columns=columns_to_scale)
    
    cleaned_and_prepd_shopping = preprocessed_shopping.sort_values('month')

     #9. Convert categorical variables to dummy variables and onehot encode
    if encoder:
        cleaned_and_prepd_shopping = pd.get_dummies(preprocessed_shopping, drop_first=True)
    
        
    #9. #Filtering columns for analysis if selected
    if column_selection is not None:
        cleaned_and_prepd_shopping = cleaned_and_prepd_shopping[column_selection]
        cleaned_and_prepd_shopping = cleaned_and_prepd_shopping.reset_index(drop=True)
    else:
        cleaned_and_prepd_shopping = cleaned_and_prepd_shopping.reset_index(drop=True)
        
    print('Number of null values after default preprocessing is',cleaned_and_prepd_shopping.isnull().sum())    
   
    return cleaned_and_prepd_shopping



import re                                                                        
def clean_names(df):
    # Function to convert camel case to snake case
    def to_snake_case(name):
        # Insert underscores before uppercase letters and convert to lowercase
        name_with_underscores = re.sub(r'(?<!^)(?=[A-Z])', '_', name)
        return name_with_underscores.lower()

    # Clean the column names
    df.columns = [to_snake_case(re.sub(r'[^a-zA-Z0-9]+', '_', str(col))) for col in df.columns]
    return df 