"""
============
INTRODUCTION
============
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

=====
INPUT
=====
The script necessitates the following arguments:

- geo_type: 'state', 'county', 'zcta'
- census_type: 'acs', 'dec'
- table_name: 'acs1', 'acs5', 'sf1'
- variable_name: The name you want to assign to your derived variable.
- variable_dict: The dictionary that is defined for the variable. We will discuss it in detail below.


======
OUTPUT
======
The script generates CSV files following this naming scheme:

`{variable_name}_{table_name}_{year}_{geo_type}.csv`

For example, for the variable name `pct_owner_occ`, `table_name` `acs5`, `year` `2013`, and `geo_type` `county`,
our file name would be: `pct_owner_occ_acs5_2013_county.csv`

The file would contain the following columns:
county | state | pct_owner_occ | year

"""



"""
====================================
VARIABLE DICTIONARY
====================================

========================
FORMAT OF THE DICTIONARY
========================

Assuming each derived variable is defined as the 

sum of variables in numerator list / sum of variables in denominator list
where:
numerator_list: [variable_1, variable_2]
denominator_list: [variable_3, variable_4]


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


===========================
HOW TO BUILD THE DICTIONARY
===========================

Let say we want to get ACS 5-Year Estimates for percentage of housing units occupied by their owners (pct_owner_occ), for the years 2013 - 2017. 

Using the , we can understand the variables available in each dataset. 
Looking at the variables available, we realize we can calculate this value for the years 2013 as:

Summing up all the values below and saving it as numerator

      - B11012_004E: Estimate!!Total!!Family households!!Married-couple family!!Owner-occupied housing units
      - B11012_008E: Estimate!!Total!!Family households!!Other family!!Male householder, no wife present!!Owner-occupied housing units
      - B11012_011E: Estimate!!Total!!Family households!!Other family!!Female householder, no husband present!!Owner-occupied housing units
      - B11012_014E: Estimate!!Total!!Nonfamily households!!Owner-occupied housing units

Summing up all the values below and saving it as denominator

    -  B11012_001E: Estimate!!Total - HOUSEHOLD TYPE BY TENURE

And finally calculate the pct_owner_occ = numerator/denominator 

We realize we can do this for the years 2013 and 2014, however as per the below documentation that https://www.census.gov/programs-surveys/acs/technical-documentation/table-and-geography-changes/2015/5-year.html

The documentation says: Detailed Tables B10060, B10061 and B11012 have been deleted. Detailed tables B10050 and B11001 are alternatives.

This implies:


"""


#import necessary libraries
import argparse
import requests
import pandas as pd

# insert your census api key here
API_KEY = '0fec0de3c4e525041f1101feb0c3a41be9b4a007'
# API_KEY= <insert your key here> api_key = '0fec0de3c4e525041f1101feb0c3a41be9b4a007'

def get_data(year, geo_type, table_name, variable_list, census_type):

    #helper dictionary for URL creation
    geography_dict = {'county': 'county:*', 'state': 'state:*', 'zcta': 'zip%20code%20tabulation%20area:*'}

    geography = geography_dict[geo_type]
    #structure for api endpoint
    api_endpoint = f'https://api.census.gov/data/{year}/{census_type}/{table_name}'

    # Construct the URL with the parameters
    url = f'{api_endpoint}?get={variable_list}&for={geography}&key={API_KEY}'
    print(url)

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

        return df
    
    else:
        return None

if __name__ == "__main__":

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

    parser = argparse.ArgumentParser(description='Process Census data.')
    
    parser.add_argument('--geo_type', type=str, choices=['county', 'state', 'zcta'], help='Geography type')
    parser.add_argument('--census_type', type=str, help='Type of Census data')
    parser.add_argument('--table_name', type=str, help='Name of the table')
    parser.add_argument('--variable_name', nargs='+', type=str, help='Name of the created variable')

    args = parser.parse_args()

    geo_type = args.geo_type
    census_type = args.census_type
    table_name = args.table_name
    variable_name = args.variable_name
    
    for year in variable_dict:
        df = process_variable_dict(year, geo_type, census_type, table_name, variable_dict[year], variable_name)
        if df is not None:
            file_name = f'{variable_name}_{table_name}_{year}_{geo_type}' + '.csv'
            df.to_csv(file_name)


