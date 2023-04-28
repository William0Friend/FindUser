import pandas as pd 
import numpy as np 
#4 Visualize the data using matplotlib and seaborn:
import matplotlib.pyplot as plt
import seaborn as sns 
import math 
from scipy import stats
import re
import csv
import plotly.graph_objs as go
from plotly.subplots import make_subplots



csv_files = [
    'UNdataExportMobileCellularTelephoneSubscriptionsPer100Inhabitants.csv',
    'UNdataExportPercentageOfIndividualsUsingTheInternet.csv',
    'CPIABusinessRegulatoryEnvironmentRating1to6.csv',
    'CPIAMacroeconomicManagementRating1to6.csv',
    'CPIAPropertyRightsAndRuleBasedGovernanceRating1to6.csv',
    'CPIATradeRating1to6.csv'
]

def read_csv_remove_bad_lines(csv_file):
    expected_num_columns = 4

    with open(csv_file, 'r', encoding='utf-8', errors='replace') as file:
        reader = csv.reader(file)

        header = next(reader)
        valid_lines = [header]

        for line in reader:
            if len(line) == expected_num_columns:
                valid_lines.append(line)

    return pd.DataFrame(valid_lines[1:], columns=valid_lines[0])

def read_and_process_csv(csv_file):
    df = read_csv_remove_bad_lines(csv_file)
    df = df.drop(columns=['Value Footnotes'])
    df.columns = ['Country', 'Year', 'Value']
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    df = df.drop_duplicates(subset=['Country', 'Year'])
    df = df[~df['Country'].str.match(r'^\d+$')]
    df = df[df['Country'] != 'footnoteSeqID']
    return df

def get_most_recent_top_100(df):
    most_recent_years = df.groupby('Country')['Year'].max()
    most_recent_data = pd.merge(df, most_recent_years, on=['Country', 'Year'])
    top_100 = most_recent_data.nlargest(100, 'Value')['Country']
    return set(top_100)


# def create_interactive_line_chart(df, common_countries, title):
    # df_filtered = df[df['Country'].isin(common_countries)]
    # df_grouped = df_filtered.groupby(['Country', 'Year'], as_index=False).mean()
    
    # fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # for country in common_countries:
        # country_data = df_grouped[df_grouped['Country'] == country]
        # fig.add_trace(go.Scatter(x=country_data['Year'], y=country_data['Value'],
                                #  mode='lines+markers', name=country))
    
    # fig.update_layout(title=title, hovermode="x unified")
    # fig.show()    
import plotly.express as px

def create_interactive_line_chart(df, common_countries, title):
    df_filtered = df[df['Country'].isin(common_countries)]
    df_grouped = df_filtered.groupby(['Country', 'Year'], as_index=False).mean()
    
    fig = px.line(df_grouped, x='Year', y='Value', color='Country', 
              title=title, hover_name='Country', markers=True,
              category_orders={'Country': df_grouped.loc[df_grouped.groupby('Country')['Value'].idxmax()].sort_values('Value', ascending=False)['Country']})
    fig.show()    

dataframes = [read_and_process_csv(csv_file) for csv_file in csv_files]

top_100_countries_list = [get_most_recent_top_100(df) for df in dataframes]

# Find the intersection of top 100 countries in datasets 1 and 2
common_top_100_datasets_1_and_2 = set.intersection(top_100_countries_list[0], top_100_countries_list[1])

# Find the intersection of top 100 countries in datasets 3, 4, 5, and 6
common_top_100_datasets_3_to_6 = set.intersection(top_100_countries_list[2], top_100_countries_list[3], top_100_countries_list[4], top_100_countries_list[5])

# Print common top 100 countries in datasets 1 and 2
print("Intersection of top 100 countries in datasets % internet users, and mobile subscriptions per 100 residents:")
print(sorted(list(common_top_100_datasets_1_and_2)))
print()

# Print common top 100 countries in datasets 3, 4, 5, and 6
print("Intersection of top 100 countries in datasets 3, 4, 5, and 6:")
print(sorted(list(common_top_100_datasets_3_to_6)))

# Create line charts for the intersection of top 100 countries in datasets 1 and 2
create_interactive_line_chart(pd.concat([dataframes[0], dataframes[1]]),
                              common_top_100_datasets_1_and_2,
                              'Intersection of Top 100 Countries in Datasets 1 and 2')

# Create line charts for the intersection of top 100 countries in datasets 3, 4, 5, and 6
create_interactive_line_chart(pd.concat([dataframes[2], dataframes[3], dataframes[4], dataframes[5]]),
                              common_top_100_datasets_3_to_6,
                              'Intersection of Top 100 Countries in Datasets 3, 4, 5, and 6')