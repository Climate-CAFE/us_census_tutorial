"""
============
INTRODUCTION
=============
The script enables the extraction of census variables at various levels of geographical and temporal resolution from the following datasets:

- American Community Survey:
    - ACS 1 Year Estimates: 2005 - 2019
    - ACS 5 Year Estimates: 2005 - 2020
- Decennial Census (SF1): 2000, 2010

========
INPUT
========

The script requires the following input parameters:

year
geo_type: Choose from 'state', 'county', 'zcta'
census_type: Choose from 'acs', 'dec'
table_name: Choose from 'acs1', 'acs5', 'sf1'
variable_list

IMPORTANT NOTE:
Please include your API_KEY in the global variable defined below.

For example, if the goal is to extract variables for the year '2018' from the ACS 1-Year Estimates dataset for all counties, 
specifically targeting the variable 'B01001_001E', the input parameters would be:

year: 2018
geo_type: 'county'
census_type: 'acs'
table_name: 'acs1'
variable_list: ['B01001_001E', 'B11012_008E']

================
RUNNING THE FILE
================

To run the script with the desired arguments, use the following command in your terminal or command prompt:

`python census_script.py --year 2013 --census_type acs --table_name acs5 --variable_list B11012_004E B11012_008E --geo_type zcta`

IMPORTANT: Add your API_KEY in the global variable defined below.

=======
OUTPUT
=======

The script produces CSV files with names adhering to the format: `{table_name}_{year}_{geo_type}.csv`. 
As an illustration, given the variables B01001_001E, census_type 'acs', table_name 'acs5', year '2013', and geo_type 'county',
the corresponding file would be named `acs5_2013_county.csv`. This file includes the following columns:

- county
- state
- B11012_004E 
- B11012_008E

"""

# import necessary libraries
import argparse
import requests
import pandas as pd
import numpy as np

# insert your census api key here
API_KEY = "<insert your key here>"

def get_data(year, geo_type, table_name, variable_list, census_type):

    #helper dictionary for URL creation
    geography_dict = {'county': 'county:*', 'state': 'state:*', 'zcta': 'zip%20code%20tabulation%20area:*'}

    # For all counties
    geography = geography_dict[geo_type]

    #structure for api endpoint
    api_endpoint = f'https://api.census.gov/data/{year}/{census_type}/{table_name}'

    variable = ','.join(variable_list)

    # Construct the URL with the parameters
    url = f'{api_endpoint}?get={variable}&for={geography}&key={API_KEY}'

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
            col_list = [geo_type, 'state'] + variable_list
            df = df[col_list]
            df.set_index([geo_type,'state'], inplace=True)

        if geo_type == 'state':
            col_list = ['state']+ variable_list
            print(col_list)

            df = df[col_list]
            df.set_index('state', inplace=True)

        if geo_type == 'zcta':
            col_list = ['zip code tabulation area']+ variable_list
            df = df[col_list]
            df.set_index('zip code tabulation area')

        # Fill missing values with NaN
        df = df.fillna(np.nan)
    
        numerical_columns = df.select_dtypes(include=[np.number]).columns

        # Replace negative values with NaN in numerical columns
        for column in numerical_columns:
            df[column] = df[column].apply(lambda x: np.nan if pd.notna(x) and x < 0 else x)

        return True,df
    
    else:
        return False, None


if __name__ == "__main__":

    # Set up the command-line argument parser with a description
    parser = argparse.ArgumentParser(description='Process Census data.')

    # Define command-line arguments for the script
    parser.add_argument('--year', type=int, help='Year for the Census data')
    parser.add_argument('--geo_type', type=str, choices=['county', 'state', 'zcta'], help='Geography type')
    parser.add_argument('--census_type', type=str, help='Type of Census data')
    parser.add_argument('--table_name', type=str, help='Name of the table')
    parser.add_argument('--variable_list', nargs='+', type=str, help='List of variables')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Extract values from parsed arguments for easier access
    year = args.year
    geo_type = args.geo_type
    census_type = args.census_type
    table_name = args.table_name
    variable_list = args.variable_list

    print(variable_list)

    # Convert the variable list into a comma-separated string
    #variable_list = ','.join(variable_list)

    # Call the get_data function to retrieve data based on command-line arguments
    status, df = get_data(year, geo_type, table_name, variable_list, census_type)

    # Check if the DataFrame is not empty
    if df is not None:
        # Generate a file name based on table, year, and geography type
        file_name = f'{table_name}_{year}_{geo_type}' + '.csv'
        # Save the DataFrame to a CSV file
        df.to_csv(file_name)
        # Print a message indicating the successful generation of the CSV file
        print(f"GENERATED file = '{table_name}_{year}_{geo_type}.csv'")

    else: 
        # Print a warning message if the DataFrame is empty
        print('WARN: Cannot generate for year:', year)


