"""
================
1. INTRODUCTION
================
In many instances, the data required for our studies often demands standardization or proportional adjustments for further analysis.

While we previously explored the extraction of raw variables from the census API using `<script_name>`, 
this script empowers us to define custom variables tailored to our specific requirements derived from the raw data.


Note: This script facilitates the extraction of variables based on geographical and time resolutions:

Time:
- American Community Survey:
    - ACS 1 Year Estimates: 2005 - 2019
    - ACS 5 Year Estimates: 2005-2020
- Decennial Census (SF1): 2000, 2010

Geography:
- State
- County
- ZCTA (Zip Code Tabulation Area)

=========
2. INPUT
=========
The script necessitates the following arguments:

- geo_type: 'state', 'county', 'zcta'
- census_type: 'acs', 'dec'
- table_name: 'acs1', 'acs5', 'sf1'
- variable_name: The name you want to assign to your derived variable. (for example: pct_owner_occ)
- variable_dict: The dictionary that is defined for the variable. We will discuss it in detail below.

IMPORTANT NOTE: 
- ADD YOUR API_KEY in the global variable defined below.
- YOU WILL NEED TO REPLACE THE VARIABLE DICT WITH YOUR DEFINED VARIABLE DICTIONARY IN THE MAIN FUNCTION


==========
3. OUTPUT
==========
The script generates CSV files following this naming scheme:

`{variable_name}_{table_name}_{year}_{geo_type}.csv`

For example, for the variable name `pct_owner_occ`, `table_name` `acs5`, `year` `2013`, and `geo_type` `county`,
our file name would be: `pct_owner_occ_acs5_2013_county.csv`

The file would contain the following columns:
county | state | pct_owner_occ | year

=======================
4. RUNNING THE FILE
=======================

To run the script with the desired arguments, use the following command in your terminal or command prompt:

`python census_custom_variable_script.py --year 2018 --geo_type county --census_type acs --table_name acs1 --variable_name pct_owner_occ`

IMPORTANT: Add your API_KEY in the global variable defined below.

===========================
5. VARIABLE DICTIONARY
===========================

=============================
5.1 FORMAT OF THE DICTIONARY
=============================

Each derived variable is defined as the sum of variables in the numerator list divided by the sum of variables in the denominator list. 

The structure is as follows:

numerator_list: [variable_1, variable_2]
denominator_list: [variable_3, variable_4]

Note:
- If you do not have any denominators, you can remove the 'den' key from the dictionary for that year.
- If your numerators have only one variable, you can add it as [variable_1].

The example below illustrates the required format for the variable dictionary, we define the numberator and denominator list for each year:


    variable_dict = {
    2013: {
        'num': [ 'B11012_004E', 'B11012_008E', 'B11012_011E', 'B11012_014E'],
        'den': [ 'B11012_001E']
    },
    2014: {
        'num': [ 'B11012_004E', 'B11012_008E', 'B11012_011E', 'B11012_014E'],
        'den': [ 'B11012_001E']
    },
    2015: {
        'num': [ 'B25011_002E'],
        'den': [ 'B25011_001E']
    },
    2016: {
        'num': [ 'B25011_002E'],
        'den': [ 'B25011_001E']
    },
    2017: {
        'num': [ 'B25011_002E'],
        'den': [ 'B25011_001E']
    }
}


================================
5.2 HOW TO BUILD THE DICTIONARY
================================

Let's illustrate the process of building a dictionary for obtaining ACS 5-Year Estimates for the percentage of housing units occupied by their owners (pct_owner_occ) for the years 2013 - 2017.

Firstly, we explore the available variables in each dataset to understand their structure. Upon inspecting the variables, we define `pct_owner_occ` as follows for the year 2013:

- Numerator List: ['B11012_004E', 'B11012_008E', 'B11012_011E', 'B11012_014E']
- Denominator List: ['B11012_001E']

Where the variables represent:
  - B11012_004E: Estimate!!Total!!Family households!!Married-couple family!!Owner-occupied housing units
  - B11012_008E: Estimate!!Total!!Family households!!Other family!!Male householder, no wife present!!Owner-occupied housing units
  - B11012_011E: Estimate!!Total!!Family households!!Other family!!Female householder, no husband present!!Owner-occupied housing units
  - B11012_014E: Estimate!!Total!!Nonfamily households!!Owner-occupied housing units
  - B11012_001E: Estimate!!Total - HOUSEHOLD TYPE BY TENURE

Finally, we compute as :

pct_owner_occ = ('B11012_004E' + 'B11012_008E'  + 'B11012_011E' + 'B11012_014E') / ('B11012_001E')

However, starting from 2015, detailed tables B10060, B10061, and B11012 have been deleted. 
With alternatives being detailed tables B10050 and B11001, as stated in the documentation available at: 
https://www.census.gov/programs-surveys/acs/technical-documentation/table-and-geography-changes/2015/5-year.html.

This implies the need to reidentify and redefine the variables required to calculate 'pct_owner_occ' from the year 2015 onwards.

Based on our needs, we redefine the variable for the years 2015-2017 as:

pct_owner_occ = ('B25011002') / ('B25011001')

Additionally, when constructing your variable dictionary, consider the following:

Some variables might not be available for certain years. For instance, a variable added only in 2015 may not be available prior to that.
Some variables available in ACS 5-Year Estimates might not be accessible for ACS 1-Year Estimates.

"""


#import necessary libraries
import argparse
import requests
import pandas as pd
import numpy as np

# insert your census api key here
API_KEY= '<insert your key here> '

def get_data(year, geo_type, table_name, variable_list, census_type):

    #helper dictionary for URL creation
    geography_dict = {'county': 'county:*', 'state': 'state:*', 'zcta': 'zip%20code%20tabulation%20area:*'}

    #extract the required geography for URL creation
    geography = geography_dict[geo_type]

    #structure for api endpoint
    api_endpoint = f'https://api.census.gov/data/{year}/{census_type}/{table_name}'

    # Construct the URL with the parameters
    url = f'{api_endpoint}?get={variable_list}&for={geography}&key={API_KEY}'
    #print(url)

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

            col_list = [geo_type, 'state'] + variable_list.split(',')
            df = df[col_list]
            df.set_index([geo_type,'state'], inplace=True)

        if geo_type == 'state':
            col_list = ['state']+ variable_list.split(',')
            df = df[col_list]
            df.set_index('state', inplace=True)

        if geo_type == 'zcta':
            col_list = ['zip code tabulation area'] + variable_list.split(',')
            df = df[col_list]
            df.set_index('zip code tabulation area', inplace=True)

        return True,df
    
    else:
        return False, None


def process_variable_dict(year, geo_type, census_type, table_name, year_variables, variable_name ):

    if 'den' in year_variables: 
        den_list = year_variables['den']
        num_list = year_variables['num']
        if den_list is None and num_list is None:
            return None
        all_var_list = den_list + num_list
    
    else:
        num_list = year_variables['num']
        all_var_list = num_list

    variables = ','.join(all_var_list)

    if variables is None:
        return None

    status, df = get_data(year, geo_type, table_name, variables, census_type)

    if status == True:
        df = df.apply(pd.to_numeric, errors='coerce')
        if 'den' in year_variables:
            df[variable_name] = df[num_list].sum(axis=1) / df[den_list].sum(axis=1)
        else:
            df[variable_name] = df[num_list].sum(axis=1)

        df['year'] = year
        df.drop(columns=all_var_list, inplace=True)

        # Fill missing values with NaN
        df = df.fillna(np.nan)
    
        numerical_columns = df.select_dtypes(include=[np.number]).columns

        # Replace negative values with NaN in numerical columns
        for column in numerical_columns:
            df[column] = df[column].apply(lambda x: np.nan if pd.notna(x) and x < 0 else x)

        return df
    
    else:
        return None

if __name__ == "__main__":

    # Create the dictionary based on the instructions above 
    # Replace the below dictionary with your own


    variable_dict = {
    2013: {
        'num': [ 'B11012_004E', 'B11012_008E', 'B11012_011E', 'B11012_014E'],
        'den': [ 'B11012_001E']
    },
    2014: {
        'num': [ 'B11012_004E', 'B11012_008E', 'B11012_011E', 'B11012_014E'],
        'den': [ 'B11012_001E']
    },
    2015: {
        'num': [ 'B25011_002E'],
        'den': [ 'B25011_001E']
    },
    2016: {
        'num': [ 'B25011_002E'],
        'den': [ 'B25011_001E']
    },
    2017: {
        'num': [ 'B25011_002E'],
        'den': [ 'B25011_001E']
    }
}
    # Set up command-line argument parser       
    parser = argparse.ArgumentParser(description='Process Census data.')

    # Define command-line arguments    
    parser.add_argument('--geo_type', type=str, choices=['county', 'state', 'zcta'], help='Geography type')
    parser.add_argument('--census_type', type=str, help='Type of Census data')
    parser.add_argument('--table_name', type=str, help='Name of the table')
    parser.add_argument('--variable_name', type=str, help='Name of the created variable')

    # Parse command-line arguments
    args = parser.parse_args()

    # Extract values from command-line arguments
    geo_type = args.geo_type
    census_type = args.census_type
    table_name = args.table_name
    variable_name = args.variable_name

    # Iterate through years in the variable_dict
    for year in variable_dict:
        df = process_variable_dict(year, geo_type, census_type, table_name, variable_dict[year], variable_name)
        # Check if the DataFrame is not empty
        if df is not None:
            # Generate a file name based on variable, table, year, and geography type
            file_name = f'{variable_name}_{table_name}_{year}_{geo_type}' + '.csv'
            # Save the DataFrame to a CSV file
            df.to_csv(file_name)
            print(f"GENERATED file = '{variable_name}_{table_name}_{year}_{geo_type}.csv'")

        else: 
            print('WARN: Cannot generate for year:', year)


