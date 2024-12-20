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