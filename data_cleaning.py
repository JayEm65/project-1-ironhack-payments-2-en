'''This file group functions for data cleaning like dealing with nan values,
    merging data frames and formating dates'''

import initial_exploration as explo

def remove_nan(data_frame, col_):
    '''This function remove the rows, but only rows where an specific column 
        has NaN values. It also print the number of rows removed and the
        list of columns and total Nan values per column'''
    print(f"{data_frame[col_].isna().sum()} rows were removed\n")
    explo.chech_null(data_frame)
    return data_frame(subset = [col_])
