import pandas as pd

# Load datasets:
#cash_request_data = pd.read_csv('project_dataset/extract - cash request - data analyst.csv')
#fees_data = pd.read_csv('project_dataset/extract - fees - data analyst - .csv')

# Function to convert date columns to European style and remove the time:
def convert_dates(df, date_columns):
    for column in date_columns:
        if column in df.columns:
            # Convert datetime and drop time:
            df[column] = pd.to_datetime(df[column], errors='coerce').dt.strftime('%d/%m/%Y')
    return df

# List date columns to be formatted:
cash_request_date_columns = ['created_at', 'updated_at', 'moderated_at', 'reimbursement_date', 
                             'cash_request_received_date', 'money_back_date', 'send_at', 'reco_creation', 'reco_last_update']
fees_data_date_columns = ['created_at', 'updated_at', 'paid_at', 'from_date', 'to_date', 'charge_moment']

# Convert dates:
#cash_request_data = convert_dates(cash_request_data, cash_request_date_columns)
#fees_data = convert_dates(fees_data, fees_data_date_columns)

# Save new datasets:
#cash_request_data.to_csv('project_dataset/extract - cash request - data analyst formatted.csv', index=False)
#fees_data.to_csv('project_dataset/extract - fees - data analyst - formatted.csv', index=False)

# Check:
#print(cash_request_data.head())
#print(fees_data.head())
'''This file groups functions for data cleaning like dealing with NaN values,
    merging data frames, and formatting dates'''

import initial_exploration as explo

def remove_nan(data_frame, col_):
    '''This function removes the rows where a specific column has NaN values.
       It also prints the number of rows removed and the list of columns and total NaN values per column.'''
    print(f"{data_frame[col_].isna().sum()} rows were removed\n")
    return data_frame.dropna(subset = [col_])


def selecting_data_types(data_frame):
    '''This function separates data into numerical and categorical columns.'''
    numerical_df = data_frame.select_dtypes(include=["number"])
    categorical_df = data_frame.select_dtypes(exclude=["number"])
    cat_from_num = numerical_df.loc[:, numerical_df.nunique() < 20]
    cat_df = pd.concat([categorical_df, cat_from_num], axis=1)
    num_df = numerical_df.drop(columns=numerical_df.columns[numerical_df.columns.isin(cat_from_num.columns)])
    return (cat_df, num_df)

def merge_df(data_frame_1, data_frame_2, how_, index_1, index_2):
    '''This function merges two data frames based on given columns and merge type.'''
    data = data_frame_1.merge(data_frame_2, how=how_, left_on=index_1, right_on=index_2)
    return data

# Ensure correct data types:
def ensure_correct_data_types(df, date_columns, numeric_columns=None):
    '''This function ensures that date columns are in datetime format and numeric columns
       are of the correct type.'''
    
    # Ensure date columns are in datetime format:
    for column in date_columns:
        if column in df.columns:
            # Explicitly convert to datetime (coerce errors to NaT):
            df[column] = pd.to_datetime(df[column], errors='coerce', format='%d/%m/%Y')  # Add the date format if necessary
    
    # Ensure numeric columns are of correct type:
    if numeric_columns:
        for column in numeric_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(df[column], errors='coerce')  # Coerce invalid numbers to NaN
    
    # Convert categorical columns to 'category' dtype (optional):
    categorical_columns = df.select_dtypes(exclude=['number', 'datetime']).columns
    for column in categorical_columns:
        df[column] = df[column].astype('category')
    
    return df
