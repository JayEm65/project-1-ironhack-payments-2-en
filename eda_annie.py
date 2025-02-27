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




    sns.histplot(data_frame[col_].dropna(), kde=True, color=sns.color_palette("viridis")[0], ax=ax_hist)

    # Set title and labels for the histogram
    ax_hist.set_title(f'Histogram of {col_.replace("CR", "Cash Request").replace("_", " ").title()}', fontsize=14, fontweight="bold")
    ax_hist.set_xlabel(col_.replace("CR", "Cash Request").replace("_", " ").title(), fontsize=12)
    ax_hist.set_ylabel('Frequency', fontsize=12)
    ax_hist.grid(True, linestyle="--", alpha=0.6)



    hist_plot_path = os.path.join(output_dir, f"Pie_plot_{col_}.png")
    fig_hist.savefig(hist_plot_path, bbox_inches='tight')

   
    sns.despine()  # Remove top and right spines

    plt.show()