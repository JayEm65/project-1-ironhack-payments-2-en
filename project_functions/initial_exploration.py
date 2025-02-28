'''This file perform and initial exploration and output important details
from the data'''

def initial_chk(data_frame):
    '''This function check for the number of columns and rows, 
        the data types, unique values, posble categorial values
        and unique values count for categorical columns'''
       
    print(f"Number of columns: {data_frame.shape[1]} amd rows: {data_frame.shape[0]}")

    print("\nData types:")
    print(data_frame.dtypes)

    # Unique values count
    print("\nUnique values count:")
    unique_values_count = data_frame.nunique()
    print(unique_values_count)

    # Let's identify categorical columns 
    categorical_columns = unique_values_count[unique_values_count < 10].index
    print(f"\nThis columns apear to be categroical:\n {categorical_columns}")

    print("\nUnique value count for categorical columns:")
    for col_ in data_frame.columns:
        if col_ in categorical_columns:
            print(f"{data_frame[col_].value_counts()}\n")

def check_null(data_frame):
    '''Check for NaN values in each column and print the total per column'''
    print("Count of null values:")
    print(data_frame.isnull().sum())

def check_duplicated(data_frame):
    '''Check for duplicated values in the data frame and print the total'''
    print("\nCount of duplicated values:")
    print(data_frame.duplicated().sum())

def check(data_frame):
    '''A function to call all the function for the data cleaning'''
    initial_chk(data_frame)
    check_null(data_frame)
    check_duplicated(data_frame)

    
