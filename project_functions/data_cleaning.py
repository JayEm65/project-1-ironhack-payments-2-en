'''This file groups functions for data cleaning, like dealing with NaN values,
    merging data frames, and formatting dates'''

import pandas as pd

# Load datasets:
#cash_request_data = pd.read_csv('project_dataset/extract - cash request - data analyst.csv')
#fees_data = pd.read_csv('project_dataset/extract - fees - data analyst - .csv')

# Function to convert date columns to European style and remove the time:
def convert_dates(df, date_columns):
    '''This function is for formatting dates'''
    for column in date_columns:
        if column in df.columns:
            # Convert datetime and drop time:
            #df[column] = pd.to_datetime(df[column], errors='coerce').dt.strftime('%d/%m/%Y')
            df[column] = pd.to_datetime(df[column], errors='coerce', dayfirst = True)
            df[column] = df[column].dt.date
            df[column] = pd.to_datetime(df[column])


# List date columns to be formatted:
cash_request_date_columns = ['created_at', 'updated_at', 'moderated_at', 'reimbursement_date', 
                             'cash_request_received_date', 'money_back_date', 'send_at', 'reco_creation', 'reco_last_update']
fees_data_date_columns = ['created_at', 'updated_at', 'paid_at', 'from_date', 'to_date']

# Convert dates:
#cash_request_data = convert_dates(cash_request_data, cash_request_date_columns)
#fees_data = convert_dates(fees_data, fees_data_date_columns)

# Save new datasets:
#cash_request_data.to_csv('project_dataset/extract - cash request - data analyst formatted.csv', index=False)
#fees_data.to_csv('project_dataset/extract - fees - data analyst - formatted.csv', index=False)

# Check:
#print(cash_request_data.head())
#print(fees_data.head())

def remove_nan(data_frame, col_):
    '''This function removes the rows where a specific column has NaN values.
       It also prints the number of rows removed and the list of columns and total NaN values per column.'''
    
    print(f"{data_frame[col_].isna().sum()} rows were removed\n")
    
    return data_frame.dropna(subset = [col_])


def selecting_data_types(data_frame):
    '''This function separates data into numerical and categorical columns.'''

    # Selecting data per type
    numerical_df = data_frame.select_dtypes(include=["number"])
    categorical_df = data_frame.select_dtypes(exclude=["number", "datetime64[ns]"])
    datetime_df = data_frame.select_dtypes(include=["datetime64[ns]"])

    # Correcting categorical and numerical columns based in the amount of unique values
    cat_from_num = numerical_df.loc[:, numerical_df.nunique() < 20]
    cat_df = pd.concat([categorical_df, cat_from_num], axis=1)
    num_df = numerical_df.drop(columns=cat_from_num.columns)
    
    # Droping ID columns
    id_columns = [col for col in num_df.columns if ('id' in col.lower()) and (col.lower() != 'user_id')]
    num_df = num_df.drop(columns=id_columns)

    return (cat_df, num_df, datetime_df)


def merge_df(data_frame_1, data_frame_2, how_, index):
    '''This function merges two data frames.'''

    data = data_frame_1.merge(data_frame_2, on=index, how=how_)
    return data

def rename_col(data_frame, old, new):
    '''This function renames a column.'''

    data_frame.rename(columns={old: new}, inplace=True)
    return data_frame

def rename_col_xy(data_frame):
    '''This function rename columns that have equal number during the merge.'''

    data_frame = data_frame.rename(columns={col: f"CR_{col[:-2]}" for col in data_frame.columns if col.endswith('_x')})
    data_frame = data_frame.rename(columns={col: f"fee_{col[:-2]}" for col in data_frame.columns if col.endswith('_y')})
    return data_frame


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

def clean_text_column(data_frame, column_name):
    '''This function cleans the reason column from numerical data.'''

    data_frame[column_name] = data_frame[column_name].str.replace(r'[\d/-]+', '', regex=True).str.strip()
    return data_frame

def drop_col(data_frame, cols):
    data_frame = data_frame.drop(cols, axis = 1)
    return data_frame

def process_date_columns(df, date_col1, date_col2, new_col_name="days_difference"):
    '''This function substrate two dates columns.'''

    df_cleaned = df.dropna(subset=[date_col1, date_col2]).copy()
    df_cleaned[new_col_name] = (df_cleaned[date_col2] - df_cleaned[date_col1]).dt.days.abs()

    return df_cleaned[[date_col1, date_col2, new_col_name]]

def merge_by_index(data_frame1, data_frame2, how_, col_):
    '''This function merges two data frames by a column.'''

    merged_df = data_frame1.join(data_frame2[col_], how=how_)
    return merged_df

def set_index(data_frame, df, id_column):
    '''This function set a column as index.'''

    data_frame[id_column] = df[id_column]
    data_frame = data_frame.set_index(id_column)
    return data_frame

def move_column(df_from, df_to, column_name):
    '''This function remove a column from a data frame and move it to another data frame.'''

    df_from = df_from.reset_index(drop=True)
    df_to = df_to.reset_index(drop=True)

    df_to[column_name] = df_from[column_name]  
    df_from = df_from.drop(columns=[column_name])
    return (df_from, df_to)
