'''This file perform exploratory data analysis and vizualization'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Creating the output directory for the plots if it dosent exist
output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)

def freq(data_frame, col_):
    '''This function generate frequency table for category columns'''
    
    # Generate freuqncy table
    frequency_table = data_frame[col_].value_counts()
    proportion_table = data_frame[col_].value_counts(normalize = True).round(3)
    df = pd.concat([frequency_table, proportion_table], axis=1)
    df.columns = ["absolute_frequency", "relative_frequency"]
    total_absolute = frequency_table.sum()
    total_relative = proportion_table.sum()
    total_row = pd.DataFrame({
        'absolute_frequency': [total_absolute],
        'relative_frequency': [total_relative]
    }, index=['Total'])
    df_f = pd.concat([df,total_row])
    
    return (df_f, df)


def cat_viz(df, cat, col_):
    '''This function generate a bar and pie chart for category columns and save it 
        in the plot folder'''
    
    # Generate a bar chart for category columns

    # Formating column names for visualization    
    formatted_title = col_.replace("CR", "Cash Request").replace("_", " ").title()
    cat.index = cat.index.astype(str).str.replace("_", " ")
    cat.index = cat.index.str.title()
    
    # Bar plot
    fig_bar, ax_bar = plt.subplots(figsize=(7, 5))
    sns.barplot(x=col_,y='absolute_frequency',data=cat,palette='viridis', ax=ax_bar)
    ax_bar.set_title(f'{formatted_title} Absolute Frequency')
    ax_bar.set_xlabel(formatted_title)
    ax_bar.set_ylabel('Absolute Frequency')
    ax_bar.tick_params(axis='x', rotation=45)
    plt.show()

    # Saving and closing the plot
    bar_plot_path = os.path.join(output_dir, f"Bar_plot_{col_}.png")
    fig_bar.savefig(bar_plot_path, bbox_inches='tight')
    plt.close(fig_bar)

    # Generate a pie chart for category columns

    fig_pie, ax_pie = plt.subplots(figsize=(7, 5))

    # Generating the freuqncy tables
    frequency_table = df[col_].value_counts()
    frequency_table.index = frequency_table.index.astype(str).str.replace("_", " ")
    frequency_table.index = frequency_table.index.str.title()

    # Pie plot
    frequency_table.plot.pie(autopct='%1.0f%%' ,startangle=90, colors=sns.color_palette('Set2'), ax=ax_pie)
    ax_pie.set_title(f'{formatted_title} Absolute Frequency')
    ax_pie.set_ylabel('')
    plt.show()

    # Saving the plot
    pie_plot_path = os.path.join(output_dir, f"Pie_plot_{col_}.png")
    fig_pie.savefig(pie_plot_path, bbox_inches='tight')


def stat(data_frame, col_):
    '''This function generate and return a statistical description table for numerical columns'''
    
    df = data_frame[col_].dropna()
    stat_ = df.describe()

    return stat_

def stat_viz(data_frame, col_):
    '''This function generate a box and histogram chart for numerical columns and save it 
        in the plot folder'''

    # Generate a histo for category columns    

    # Box plot    
    fig_box, ax_box = plt.subplots(figsize=(7, 5))
    sns.boxplot(x=data_frame[col_].dropna(), palette="viridis", ax= ax_box)
    ax_box.set_title(f'Box Plot of {col_.replace("CR", "Cash Request").replace("_", " ").title()}', fontsize=14, fontweight="bold")
    ax_box.set_xlabel(col_.replace("CR", "Cash Request").replace("_", " ").title(), fontsize=12)
    ax_box.grid(True, linestyle="--", alpha=0.6)
    plt.show()

    # Saving and closing the plot
    box_plot_path = os.path.join(output_dir, f"Bar_plot_{col_}.png")
    fig_box.savefig(box_plot_path, bbox_inches='tight')
    plt.close(fig_box)

    # Hist
    fig_hist, ax_hist = plt.subplots(figsize=(7, 5))
    sns.histplot(data_frame[col_].dropna(), kde=True, color=sns.color_palette("viridis")[3], ax=ax_hist)
    ax_hist.set_title(f'Histogram of {col_.replace("CR", "Cash Request").replace("_", " ").title()}', fontsize=14, fontweight="bold")
    ax_hist.set_xlabel(col_.replace("CR", "Cash Request").replace("_", " ").title(), fontsize=12)
    ax_hist.set_ylabel('Frequency', fontsize=12)
    ax_hist.grid(True, linestyle="--", alpha=0.6)
    plt.show()

    # Saving the plot
    hist_plot_path = os.path.join(output_dir, f"Pie_plot_{col_}.png")
    fig_hist.savefig(hist_plot_path, bbox_inches='tight')
   
    #sns.despine()  # Remove top and right spines


def revenue_metric(df, _col):
    '''This function generate and return a revenue table by cohort'''
    
    # Create the cohort (year-month) from the index cretaed_at
    df['cohort_month'] = df.index.to_period('M')

    # Calculating monthly totals
    monthly_totals = df.groupby('cohort_month')[_col].sum().reset_index()
    total_amount_sum = monthly_totals['total_amount'].sum()
    monthly_totals['percentage'] = round((monthly_totals['total_amount'] / total_amount_sum) * 100,2)

    # Add a total row
    total_row = pd.DataFrame({
        'cohort_month': ['Total'],
        'total_amount': [total_amount_sum],
        'percentage': ['100 %']  # The sum of all percentages should be 100%
    })

    monthly_totals = pd.concat([monthly_totals, total_row], ignore_index=True)
    monthly_totals.set_index('cohort_month', inplace=True)

    return monthly_totals
   

def revenue_plot(monthly_totals):
    '''This function generate a bar plot of revenue by cohort'''

    # Column renaming and structuring  and cleaning
    monthly_totals.reset_index(inplace=True)
    plot_data = monthly_totals[monthly_totals['cohort_month'] != 'Total']

    # Bar plot
    plt.figure(figsize=(12, 6))
    sns.barplot(x=plot_data['cohort_month'].astype(str), 
                y=plot_data['total_amount'],
                palette="viridis")
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Cohort Month", fontsize=12)
    plt.ylabel("Total Amount in Fees", fontsize=12)
    plt.title("Total Amount in Fees per Cohort", fontsize=14)
    plt.show()

    # Saving the plot
    plt.savefig("plots/revenue_metric_bar_plot.png", dpi=300, bbox_inches='tight')
    

def revenue_plot_per_user(df):
    '''This function generate a bar plot of average revenue per user by cohort'''

    # Create the column with the ARPU and add it to the cohort
    df['cohort_month'] = df.index.to_period('M')
    cohort_data = df.groupby('cohort_month').agg(
        total_fees=('total_amount', 'sum'),
        user_count=('user_id', 'nunique')
    ).reset_index()
    cohort_data['ARPU'] = cohort_data['total_fees'] / cohort_data['user_count']
    all_months = pd.period_range(start=df['cohort_month'].min(), end=df['cohort_month'].max(), freq='M')
    cohort_data = cohort_data.set_index('cohort_month').reindex(all_months).reset_index().rename(columns={'index': 'cohort_month'})
    cohort_data.fillna({'total_fees': 0, 'user_count': 0, 'ARPU': 0}, inplace=True)  
    cohort_data['cohort_month'] = cohort_data['cohort_month'].astype(str)  
    cohort_data['cohort_month'] = pd.to_datetime(cohort_data['cohort_month']).dt.to_period('M')

    # Bar plot
    plt.figure(figsize=(12, 6))
    sns.barplot(x=cohort_data['cohort_month'].astype(str), y=cohort_data['ARPU'], palette="mako")
    plt.xticks(rotation=45, ha='right')  # Rotate x labels for readability
    plt.xlabel("Cohort Month", fontsize=12)
    plt.ylabel("Average Revenue per User", fontsize=12)
    plt.title("Average Revenue per User by Cohort", fontsize=14)
    plt.show()

    # Saving the plot
    plt.savefig("plots/average_revenue_per_user.png", dpi=300, bbox_inches="tight")

    return cohort_data

def incident_metric(data_df):
    '''This function generate a bar plot of incidents by cohort and a frequency table'''

    # Creates the cohort:
    data_df['first_advance_date'] = data_df.groupby('user_id')['CR_created_at'].transform('min')
    data_df['cohort_month'] = data_df['first_advance_date'].dt.to_period('M')

    # Define relevant incident types based on the 'reason' column:
    incident_reasons = ['rejected direct debit', 'month delay on payment']

    # Filter data for rows that have incidents:
    incident_data = data_df[data_df['reason'].isin(incident_reasons)]

    # Group by cohort month and count the number of incidents per cohort:
    incident_counts = incident_data.groupby('cohort_month')['user_id'].nunique()

    # Group by cohort month to count total requests:
    total_requests = data_df.groupby('cohort_month')['user_id'].nunique()

    # Calculate incident rate (number of incidents / total requests per cohort):
    incident_rate = incident_counts / total_requests * 100

    # Frequency table with absolute counts:
    frequency_table = (data_df[data_df['reason'].isin(['rejected direct debit', 'month delay on payment', 'postpone cash request'])]
                    .groupby(['cohort_month', 'reason'])
                    .size()
                    .unstack(fill_value=0))

    # Add total column for each cohort month:
    frequency_table['Total Incidents'] = frequency_table.sum(axis=1)

    # Filter only relevant incidents:
    incident_counts = (data_df[data_df['reason'].isin(['rejected direct debit', 'month delay on payment', 'postpone cash request'])]
                   .groupby(['cohort_month', 'reason'])
                   .size()
                   .unstack(fill_value=0))
  
    # Plot grouped bar chart:
    incident_counts.plot(kind='bar', figsize=(10, 6), width=0.8)

    # Labels and formatting:
    plt.title('Incident Count by Cohort Month')
    plt.ylabel('Number of Incidents')
    plt.xlabel('Cohort Month')
    plt.xticks(rotation=45)
    plt.legend(title="Incident Types", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    # Saving the plot
    plt.savefig("plots/incident_count_per_cohort.png", dpi=300, bbox_inches="tight")

    return incident_rate, frequency_table


def incident_metric_f(data_df, frequency_table):
    '''This function generate a bar plot in % of incidents by cohort and a frequency table'''

    # Frequency table with absolute counts:
    frequency_table = (data_df[data_df['reason'].isin(['rejected direct debit', 'month delay on payment', 'postpone cash request'])]
                    .groupby(['cohort_month', 'reason'])
                    .size()
                    .unstack(fill_value=0))

    # Add total column for each cohort month:
    frequency_table['Total Incidents'] = frequency_table.sum(axis=1)

    # Filter only relevant incidents:
    incident_counts = (data_df[data_df['reason'].isin(['rejected direct debit', 'month delay on payment', 'postpone cash request'])]
                    .groupby(['cohort_month', 'reason'])
                    .size()
                    .unstack(fill_value=0))

    # Compute total requests per cohort:
    total_requests = data_df.groupby('cohort_month').size()

    # Calculate incident rate as a percentage:
    incident_rate = (incident_counts.div(total_requests, axis=0) * 100)

    # Plot stacked bar chart:
    incident_rate.plot(kind='bar', stacked=True, figsize=(10, 6))

    # Labels and formatting:
    plt.title('Incident Rate by Cohort Month')
    plt.ylabel('Incident Rate (%)')
    plt.xlabel('Cohort Month')
    plt.xticks(rotation=45)
    plt.legend(title="Incident Types", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    # Saving the plot
    plt.savefig("plots/incident_count_percent_per_cohort.png", dpi=300, bbox_inches="tight")

    # Display table:
    return frequency_table


def bi_rev_incid(cat_new, num_new):
    '''This function generate a bar plot of revene per incident by cohort and a pivot table'''

    # Creating the cohort and formating the data frame
    cat_new = cat_new.reset_index()
    cat_new = cat_new[['CR_created_at', 'reason']]
    df_grouped = cat_new.pivot_table(index='CR_created_at', columns='reason', aggfunc='size', fill_value=0)
    df_grouped['cohort_month'] = df_grouped.index.to_period('M')
    columns_to_aggregate = ['Instant Payment Cash Request', 'Postpone Cash Request', 'month delay on payment', 'rejected direct debit']
    monthly_totals = df_grouped.groupby('cohort_month')[columns_to_aggregate].sum().reset_index()
    df_merged = monthly_totals.merge(num_new, on='cohort_month', how='inner')
    df_merged = df_merged[["cohort_month", "total_fees","Instant Payment Cash Request", "Postpone Cash Request", "month delay on payment", "rejected direct debit"]]
    df_merged.rename(columns={'month delay on payment': 'Month Delay on Payment'}, inplace=True)
    df_merged.rename(columns={'rejected direct debit': 'Rejected Direct Debit'}, inplace=True)

    df_melted = df_merged.melt(id_vars=["cohort_month", "total_fees"], 
                    value_vars=["Instant Payment Cash Request", "Postpone Cash Request", "Month Delay on Payment", "Rejected Direct Debit"],
                    var_name="incident_reason", 
                    value_name="revenue")
    
    # Bar plot
    plt.figure(figsize=(12, 6))
    sns.barplot(x="cohort_month", y="revenue", hue="incident_reason", data=df_melted, palette="Set2")
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability
    plt.xlabel("Cohort Month", fontsize=12)
    plt.ylabel("Total Revenue", fontsize=12)
    plt.title("Revenue Breakdown by Incident Reason for Each Cohort", fontsize=14)
    plt.legend(title="Incident Reason", loc="upper left")
    plt.tight_layout()
    plt.show()

    # Save the plot
    plt.savefig("plots/bivariant_bar_plot_revenue_incident.png", dpi=300, bbox_inches="tight")
 
    return (df_merged, df_melted)

def restruct(df_new, num_c):
    '''This function different version of the data frame (stacked, unstacked and multiindex)'''

    # Creating the cohort and formating the data frame
    df_new = df_new.reset_index()
    df_new = df_new[['CR_created_at', 'reason']]
    num_c.reset_index(inplace=True)
    df_merged = df_new.merge(num_c, on='CR_created_at', how='inner')
    df_cleaned = df_merged.dropna(subset=['total_amount', 'reason'])
    df_cleaned = df_cleaned[['CR_created_at', 'reason', 'total_amount']]
    df_grouped = df_cleaned.pivot_table(index='CR_created_at', columns='reason', values=["total_amount"])
    df_grouped['cohort_month'] = df_grouped.index.to_period('M')
    monthly_totals = df_grouped.groupby('cohort_month').sum().reset_index()

    # Generating the different versions of the data frame 
    df_multiindex = monthly_totals.set_index(['cohort_month'])
    stacked_data = df_multiindex.stack()
    unstacked_data = stacked_data.unstack('cohort_month')
   
    return (df_multiindex, stacked_data, unstacked_data)

def fee_heat_map(data_df, col1, col2, x, y):
    '''This function generate a heatmap of two cstegorical columns'''

    # Create the crosstab table
    crosstab_table = pd.crosstab(data_df[col1], data_df[col2])

    # Plot the heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(crosstab_table, annot=True, fmt='d', cmap='Blues')
    plt.xlabel(f"{x}")
    plt.ylabel(f"{y}")
    plt.xticks(rotation=45, ha='right')
    plt.title(f'Heatmap of {col2} vs {col1}')
    plt.show()

    # Saving the plot
    plt.savefig(f"plots/bivariant_heatmap_{col1}_vs_{col2}.png", dpi=300, bbox_inches="tight")

    return crosstab_table



def cat_con(cat, num):
    '''This function generate a boxplot of one categorical and one numerical'''

    # Creating the data frame
    df_merged = cat.merge(num, on='CR_created_at', how='inner')
    df_merged = df_merged.reset_index(drop=True)

    # Box plot
    plt.figure(figsize=(12, 6))
    pd.set_option('display.max_columns', None)
    sns.boxplot(data=df_merged, x="reason", y="days_difference_fee_paid", palette="viridis")
    plt.xticks(rotation=45, ha='right')
    plt.title("Box plot between the fee incident and the payment time", fontsize=14)
    plt.ylabel("Times in day to pay the fee", fontsize=12)
    plt.xlabel("Fee reason", fontsize=12)
    plt.show()

    # Saving the plot
    plt.savefig("plots/box_plot_incident_days.png", dpi=300, bbox_inches='tight')
    

def line_plot(cat, num):
    '''This function generate a scatter plot between two numerical columns'''

    # Creating the data frame
    df_merged = cat.merge(num, on='CR_created_at', how='inner')
    df_merged = df_merged.reset_index(drop=True)
    df_merged = df_merged.dropna(subset=["days_difference_CR_back", "days_difference_fee_paid"])

    # Scatter plot
    sns.scatterplot(data=df_merged, x='days_difference_CR_back', y='days_difference_fee_paid', palette="viridis")
    plt.title("Scatter plot between number of days to compleate a CR payment and a Fee payment", fontsize=14)
    plt.ylabel("Number of days for compleated fee incident", fontsize=12)
    plt.xlabel("Number of days for money back from a CR", fontsize=12)
    plt.show()

    # Saving the plot
    plt.savefig("plots/scatter_plot_CR_days_fee_days.png", dpi=300, bbox_inches='tight')

def fre(data_df):
    '''This function generate heatmap and frequency table of service usage'''

    
    #create cohort using dates from the first transactions, and grouping all users according to user id.
    data_df['first_advance_date'] = data_df.groupby('user_id')['CR_created_at'].transform('min')
    data_df['cohort_month'] = data_df['first_advance_date'].dt.to_period('M')

    # extracts month and year from the first advance column and converts it to a period format.
    data_df['cohort_index'] = (data_df['CR_created_at'].dt.year - data_df['first_advance_date'].dt.year) * 12 + \
                     (data_df['CR_created_at'].dt.month - data_df['first_advance_date'].dt.month) + 1


    data_df['cohort_month'] = data_df['first_advance_date'].dt.to_period('M')
    data_df.groupby('cohort_month').size() 

    cohort_table = data_df.groupby(['cohort_month', data_df['CR_created_at'].dt.to_period('M')])['user_id'].count()
    cohort_table = cohort_table.unstack()
    cohort_table = cohort_table.fillna(0)                

    cohort_size = data_df.groupby('cohort_month')['user_id'].nunique()

    # count the number of times each user used the service in each month
    cohort_usage = data_df.groupby(['cohort_month', data_df['CR_created_at'].dt.to_period('M')])['user_id'].count()

    # each row is a cohort, and each column is a month
    cohort_usage = cohort_usage.unstack(fill_value=0)

    # Calculate the frequency of service usage by dividing the usage count by cohort size
    cohort_usage_frequency = cohort_usage.divide(cohort_size, axis=0)  # Divide usage by cohort size

    cohort_usage_percentage = cohort_usage.div(cohort_size, axis=0) * 100
    cohort_usage_percentage.fillna(0, inplace=True)

    data_df['first_advance_date'] = data_df.groupby('user_id')['CR_created_at'].transform('min')
    data_df['cohort_month'] = data_df['first_advance_date'].dt.to_period('M')

    new_users = data_df.groupby('cohort_month')['user_id'].nunique()

    interactions = data_df.groupby('cohort_month')['user_id'].count()

    frequency_of_usage = interactions / new_users
    cohort_usage_matrix = data_df.groupby(['cohort_month', data_df['CR_created_at'].dt.to_period('M')])['user_id'].count().unstack()

    cohort_usage_matrix.fillna(0, inplace=True)

    # Plot the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(cohort_usage_matrix, annot=True, fmt='g', cmap='Blues', cbar=True)
    plt.title('Heatmap of Service Usage by Cohort and Month')
    plt.xlabel('Month of Interaction')
    plt.ylabel('Cohort Month')
    plt.xticks(rotation=45) 
    plt.show()

    # Saving the heatmap
    plt.savefig("plots/freq_heatmap.png", dpi=300, bbox_inches="tight")    

    return cohort_size, cohort_table


def fre_bar(cohort_table):
    '''This function generate barplot of service usage by cohort'''

    frequency_by_month = cohort_table.sum(axis=0) 

    # Plot the barplot
    plt.figure(figsize=(12, 6))
    sns.barplot(x=frequency_by_month.index.astype(str), y=frequency_by_month.values, palette='Blues')

    plt.title('Frequency of Service Usage by Month')
    plt.xlabel('Month')
    plt.ylabel('Number of Interactions')
    plt.xticks(rotation=45)
    plt.show()

    # Saving the plot
    plt.savefig("plots/freq_barplot.png", dpi=300, bbox_inches="tight")    

    frequency_table = cohort_table.sum(axis=0) 
    frequency_table = frequency_table.reset_index() 
    frequency_table.columns = ['Month', 'Total Interactions']

    return frequency_table