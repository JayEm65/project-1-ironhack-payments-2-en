import pandas as pd

# Load datasets:
cash_request_data = pd.read_csv('project_dataset/extract - cash request - data analyst.csv')
fees_data = pd.read_csv('project_dataset/extract - fees - data analyst - .csv')

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
cash_request_data = convert_dates(cash_request_data, cash_request_date_columns)
fees_data = convert_dates(fees_data, fees_data_date_columns)

# Save new datasets:
cash_request_data.to_csv('project_dataset/extract - cash request - data analyst formatted.csv', index=False)
fees_data.to_csv('project_dataset/extract - fees - data analyst - formatted.csv', index=False)

# Check:
print(cash_request_data.head())
print(fees_data.head())
