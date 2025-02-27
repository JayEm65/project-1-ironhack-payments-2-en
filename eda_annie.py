import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

import data_cleaning as cl

# Generate frequency table for category columns
def freq(data_frame, col_):
    
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

# Generate a bar and pie chat for category products
def cat_viz(df, cat, col_):

    output_dir = "plots"
    os.makedirs(output_dir, exist_ok=True)

    fig_bar, ax_bar = plt.subplots(figsize=(7, 5))

    
    formatted_title = col_.replace("CR", "Cash Request").replace("_", " ").title() 
        
    cat.index = cat.index.astype(str).str.replace("_", " ")
    cat.index = cat.index.str.title()
    
    sns.barplot(x=col_,y='absolute_frequency',data=cat,palette='viridis', ax=ax_bar)

    ax_bar.set_title(f'{formatted_title} Absolute Frequency')
    ax_bar.set_xlabel(formatted_title)
    ax_bar.set_ylabel('Absolute Frequency')
    ax_bar.tick_params(axis='x', rotation=45)
    plt.show()
    bar_plot_path = os.path.join(output_dir, f"Bar_plot_{col_}.png")
    fig_bar.savefig(bar_plot_path, bbox_inches='tight')
    plt.close(fig_bar)

    fig_pie, ax_pie = plt.subplots(figsize=(7, 5))

    frequency_table = df[col_].value_counts()
    frequency_table.index = frequency_table.index.astype(str).str.replace("_", " ")
    frequency_table.index = frequency_table.index.str.title()
    frequency_table.plot.pie(autopct='%1.0f%%' ,startangle=90, colors=sns.color_palette('Set2'), ax=ax_pie)

    ax_pie.set_title(f'{formatted_title} Absolute Frequency')
    ax_pie.set_ylabel('')

    pie_plot_path = os.path.join(output_dir, f"Pie_plot_{col_}.png")
    fig_pie.savefig(pie_plot_path, bbox_inches='tight')

    plt.tight_layout()
    plt.show()

# Generate a bar chat for category products
def stat(data_frame, col_):
    df = data_frame[col_].dropna()
    stat_ = df.describe()
    return stat_

def stat_viz(data_frame, col_):

    output_dir = "plots"
    os.makedirs(output_dir, exist_ok=True)
    
    #fig, ax =  plt.subplots(1, 2, figsize=(7, 5))
    fig_box, ax_box = plt.subplots(figsize=(7, 5))

    sns.boxplot(x=data_frame[col_].dropna(), palette="viridis", ax= ax_box)

    ax_box.set_title(f'Box Plot of {col_.replace("CR", "Cash Request").replace("_", " ").title()}', fontsize=14, fontweight="bold")
    ax_box.set_xlabel(col_.replace("CR", "Cash Request").replace("_", " ").title(), fontsize=12)
    ax_box.grid(True, linestyle="--", alpha=0.6)
    plt.show()
    box_plot_path = os.path.join(output_dir, f"Bar_plot_{col_}.png")
    fig_box.savefig(box_plot_path, bbox_inches='tight')
    
    plt.close(fig_box)

    fig_hist, ax_hist = plt.subplots(figsize=(7, 5))




    sns.histplot(data_frame[col_].dropna(), kde=True, color=sns.color_palette("viridis")[3], ax=ax_hist)

    # Set title and labels for the histogram
    ax_hist.set_title(f'Histogram of {col_.replace("CR", "Cash Request").replace("_", " ").title()}', fontsize=14, fontweight="bold")
    ax_hist.set_xlabel(col_.replace("CR", "Cash Request").replace("_", " ").title(), fontsize=12)
    ax_hist.set_ylabel('Frequency', fontsize=12)
    ax_hist.grid(True, linestyle="--", alpha=0.6)



    hist_plot_path = os.path.join(output_dir, f"Pie_plot_{col_}.png")
    fig_hist.savefig(hist_plot_path, bbox_inches='tight')

   
    sns.despine()  # Remove top and right spines

    plt.show()

def revenue_metric(df, _col):
    # Create the cohort (year-month) from the index
    df['cohort_month'] = df.index.to_period('M')
    monthly_totals = df.groupby('cohort_month')[_col].sum().reset_index()
   
    total_amount_sum = monthly_totals['total_amount'].sum()
    monthly_totals['percentage'] = round((monthly_totals['total_amount'] / total_amount_sum) * 100,2)

    total_row = pd.DataFrame({
        'cohort_month': ['Total'],
        'total_amount': [total_amount_sum],
        'percentage': ['100 %']  # The sum of all percentages should be 100%
    })

    monthly_totals = pd.concat([monthly_totals, total_row], ignore_index=True)


    return monthly_totals

def revenue_plot(monthly_totals):

    plt.figure(figsize=(12, 6))

    plot_data = monthly_totals[monthly_totals['cohort_month'] != 'Total']

    sns.barplot(x=plot_data['cohort_month'].astype(str),  # Convert Period to string for plotting
                y=plot_data['total_amount'],
                palette="viridis")

    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Cohort Month", fontsize=12)
    plt.ylabel("Total Amount in Fees", fontsize=12)
    plt.title("Total Amount in Fees per Cohort", fontsize=14, fontweight='bold')

    plt.savefig("plots/revenue_metric_bar_plot.png", dpi=300, bbox_inches='tight')

    plt.show()

def revenue_plot_per_user(df):

    df['cohort_month'] = df.index.to_period('M')

    cohort_data = df.groupby('cohort_month').agg(
        total_fees=('total_amount', 'sum'),
        user_count=('user_id', 'nunique')
    ).reset_index()

    cohort_data['ARPU'] = cohort_data['total_fees'] / cohort_data['user_count']

    all_months = pd.period_range(start=df['cohort_month'].min(), end=df['cohort_month'].max(), freq='M')
    cohort_data = cohort_data.set_index('cohort_month').reindex(all_months).reset_index().rename(columns={'index': 'cohort_month'})
    cohort_data.fillna({'total_fees': 0, 'user_count': 0, 'ARPU': 0}, inplace=True)  

   
    plt.figure(figsize=(12, 6))
    sns.barplot(x=cohort_data['cohort_month'].astype(str), y=cohort_data['ARPU'], palette="mako")

 
    plt.xticks(rotation=45, ha='right')  # Rotate x labels for readability
    plt.xlabel("Cohort Month", fontsize=12)
    plt.ylabel("Average Revenue per User", fontsize=12)
    plt.title("Average revenue per user by cohort", fontsize=14, fontweight='bold')

    plt.savefig("plots/average_revenue_per_user.png", dpi=300, bbox_inches="tight")

    # Show the Plot
    plt.show()