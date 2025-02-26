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
'''This file group functions for data cleaning like dealing with nan values,
    merging data frames and formating dates'''

import initial_exploration as explo

def remove_nan(data_frame, col_):
    '''This function remove the rows, but only rows where an specific column 
        has NaN values. It also print the number of rows removed and the
        list of columns and total Nan values per column'''
    print(f"{data_frame[col_].isna().sum()} rows were removed\n")
    return data_frame.dropna(subset = [col_])


def selecting_data_types(data_frame):
    numerical_df = data_frame.select_dtypes(include=["number"])
    categorical_df = data_frame.select_dtypes(exclude=["number"])

    cat_from_num = numerical_df.loc[:, numerical_df.nunique() < 20]
    cat_df = pd.concat([categorical_df,cat_from_num], axis = 1)

    num_df = numerical_df.drop(columns=numerical_df.columns[numerical_df.columns.isin(cat_from_num.columns)])
    
    id_columns = [col for col in num_df.columns if 'id' in col.lower()]
    num_df = num_df.drop(columns=id_columns)

    return (cat_df, num_df)

def merge_df(data_frame_1, data_frame_2, how_, index):
    data = data_frame_1.merge(data_frame_2, on=index, how=how_)
    return data

def rename_col(data_frame, old, new):
    data_frame.rename(columns={old: new}, inplace=True)

def rename_col_xy(data_frame):
    data_frame = data_frame.rename(columns={col: f"CR_{col[:-2]}" for col in data_frame.columns if col.endswith('_x')})
    data_frame = data_frame.rename(columns={col: f"fee_{col[:-2]}" for col in data_frame.columns if col.endswith('_y')})
    return data_frame