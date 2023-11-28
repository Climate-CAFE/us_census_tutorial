"""
This script allows to extarct the census variables for different levels of geographical and time resolution for the following datasets:
- American Community Survey:
    - ACS 1 Year Estimates: 2005 - 2019
    - ACS 5 Year Estimates: 2005-2020
- Decennial Census (SF1): 2000, 2010


For a given year, geography, dataset and the variables the output of the script would be structured as a dataframe with columsn:
<geography> | <variable_name_1> | <variable_name_2>

To illustrate: if we want to extract variables  for the year '2018', dataset - ACS 1-Year Estimates, for all counties. 
Our input would be:
- year: 2018
- geo_type: 'county'
- census_type: 'acs'
- table_name: 'acs1'
- variable: ['B01001_001E']

The resultant dataframe would have the columns: year | county | state | B01001_001E
"""

#import necessary libraries
import requests
import yaml
import pandas as pd
import numpy as np
import argparse

#insert your census api key here
#api_key = '0fec0de3c4e525041f1101feb0c3a41be9b4a007'
#api_key = <insert your key here> api_key = '0fec0de3c4e525041f1101feb0c3a41be9b4a007'

def get_data(year, geo_type, table_name, variable, census_type):

    #helper dictionary for URL creation
    geography_dict = {'county': 'county:*', 'state': 'state:*', 'zcta': 'zip%20code%20tabulation%20area:*'}

    # For all counties
    geography = geography_dict[geo_type]

    #structure for api endpoint
    api_endpoint = f'https://api.census.gov/data/{year}/{census_type}/{table_name}'

    # Construct the URL with the parameters
    url = f'{api_endpoint}?get={variable}&for={geography}&key={api_key}'

    # Make the API request
    response = requests.get(url)


    # Process the response
    if response.status_code == 200:
        status = 200
        #save the response in json 
        data = response.json()
        #convert to dataframe 
        df = pd.DataFrame(data[1:], columns=data[0])
        # The data variable now contains the requested data for all counties.
    else:
        status = -1
        df = None

    if status == 200:

        if geo_type == 'county':

            col_list = [geo_type, 'state', variable]
            df = df[col_list]
            df.set_index([geo_type,'state'], inplace=True)

        if geo_type == 'state':
            col_list = ['state', variable]
            df = df[col_list]
            df.set_index('state', inplace=True)

        if geo_type == 'zcta':
            col_list = ['zip code tabulation area', variable]
            df = df[col_list]
            df.set_index('zip code tabulation area')

    return True,df



def get_df(year, geo_type, census_type, table_name, variable_list):

    #df_list will store all output df's for each variable 
    df_list = []

    #iterate over the list of variables and get the output df (var_df) for each
    for variable in variable_list:
        success, var_df = get_data(year,geo_type, table_name, variable, census_type)
        if success==True:
            df_list.append(var_df)

    #merge all dataframes to create the output dataframe
    df = pd.concat(df_list, axis=1)
    df.reset_index(inplace=True)
    df = df.loc[:,~df.columns.duplicated()]

    # Fill missing values with NaN
    df = df.fillna(np.nan)
    
    numerical_columns = df.select_dtypes(include=[np.number]).columns

    # Replace negative values with NaN in numerical columns
    for column in numerical_columns:
        df[column] = df[column].apply(lambda x: np.nan if pd.notna(x) and x < 0 else x)

    return  df


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process Census data.')
    
    parser.add_argument('--year', type=int, help='Year for the Census data')
    parser.add_argument('--geo_type', type=str, choices=['county', 'state', 'zcta'], help='Geography type')
    parser.add_argument('--census_type', type=str, help='Type of Census data')
    parser.add_argument('--table_name', type=str, help='Name of the table')
    parser.add_argument('--variable_list', nargs='+', type=str, help='List of variables')

    args = parser.parse_args()

    year = args.year
    geo_type = args.geo_type
    census_type = args.census_type
    table_name = args.table_name
    variable_list = args.variable_list

    df = get_df(year, geo_type, census_type, table_name, variable_list)

    print(df)

