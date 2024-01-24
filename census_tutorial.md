# Census

## Table of Contents
+ [What This Documentation Is and Is Not?](#item-one)
+ [What Census products does this document focus on?](##item-two)
+ [What is ACS  1-Year Estimates?](##item-three)
+ [What is ACS 5-Year Estimates?](#item-four)
+ [When to use 1-year or 5-year Estimates?](#item-five)
+ [What is Decennial Census?](#item-six)
+ [What is the difference between Decennial and Census?](#item-seven)
+ [What Variables are Available in a Dataset/Table?](#item-eight)
+ [How do I find the geographical coverage of a dataset/table?](#item-nine)
+ [How to Obtain Your Census API Key??](#item-ten)
+ [How can I interact with census data to explore specific variables?](#item-eleven)
+ [Where can I connect with experienced professionals to discuss census data?](#item-twelve)


## What This Documentation Is and Is Not?  
 <a id="item-one"></a>
Welcome to this concise tutorial/documentation, born out of hands-on interactions with various US Census Bureau products and the insights gained while working with them. While specific questions are best directed to the official website, our main aim is to consolidate frequently used information, offering a quick kick-start for your Census journey.

**Acknowledgment:** The resources compiled in this documentation are sourced from the US Census Bureau, and it is important to note that this guide is not intended as a replacement for official Census Bureau materials. For the most accurate and up-to-date information, always refer to the official resources provided by the US Census Bureau.

##  What Census products does this document focus on?
 <a id="item-two"></a>
While there are many survey, programs and census conducted by U.S. Census Bureau, this documentation specifically focuses on some commonly used products:

-   ACS: American Community Survey
    - ACS 1-Year Estimates
    - ACS 5-Year Estimates
-   Decennial Census

## What is ACS  1-Year Estimates?
 <a id="item-three"></a>
The [American Community Survey (ACS) 1-Year Estimate](https://www.census.gov/data/developers/data-sets/acs-1year.html) is an annual survey conducted by the U.S. Census Bureau to provide timely and reliable demographic, social, economic, and housing information for communities across the United States. 

### Key Points:

- Time Period: 2005-present

- Frequency: The ACS 1-Year Estimate is released annually and covers a broad range of topics, allowing for more up-to-date information compared to the traditional decennial census.

- Sample Size: Unlike the full decennial census, which aims to count every person in the United States, the ACS is based on a sample of households. The 1-year estimate is drawn from a one-year sample, providing a snapshot of the population's characteristics during that specific year.

- Geographic Coverage: The ACS 1-Year Estimate provides data for a variety of geographic areas - all 50 states, the District of Columbia, Puerto Rico, every congressional district, every metropolitan area, and all counties and places with populations of 65,000 or more.

- Data Variables: The survey collects information on a wide range of topics, including but not limited to population, age, sex, race, ethnicity, education, employment, income, housing, and commuting patterns.

- Reliability: While the 1-year estimate offers more recent data, it is based on a smaller sample size compared to the 5-year estimate. As a result, caution should be exercised when interpreting data for smaller geographic areas or subpopulations.

### Important Considerations:

- ZCTA Coverage: ZCTA coverage is not included in ACS 1-Year Estimates. 
- Population Threshold: The data is available only for regions with a population of 65,000 or more.
- Hispanic Data Inclusion: Hispanic data was incorporated starting from the 2009 ACS 1-year estimates.
- Impact of COVID-19: Due to the impact of the COVID-19 pandemic on data collection, the Census Bureau did not release its standard 2020 ACS 1-year estimates.
- Variable Changes: Some variable changes occurred; refer to this [link](https://www.census.gov/programs-surveys/acs/technical-documentation/table-and-geography-changes/2015/5-year.html#par_textimage_1) for details.


## What is ACS 5-Year Estimates?
 <a id="item-four"></a>
The American Community Survey (ACS) is an ongoing survey that provides data every year -- giving communities the current information they need to plan investments and services.The [5-year estimates](https://www.census.gov/data/developers/data-sets/acs-5year.html) from the ACS are [period estimates](https://www.census.gov/newsroom/blogs/random-samplings/2022/03/period-estimates-american-community-survey.html) that represent data collected over a period of time. The primary advantage of using multiyear estimates is the increased statistical reliability of the data for less populated areas and small population subgroups.

The below image from the US Census Bureau, effectively illustrates the time period covered by ACS 1-Year and 5-Year estimates.

<p align="center">
 <img src="https://www.census.gov/content/dam/Census/newsroom/blogs/2022/rs-period-estimates-in-the-acs/figure1.jpg" alt="Alt Text" width="500" height="500">
<p align="center">

### Key Points:

- Time Period: 2009 - present

- Frequency: While the ACS 1-Year Estimate provides annual snapshots, the 5-Year Estimate spans a 60-month period, offering a more stable dataset for in-depth analysis. This extended survey period minimizes the impact of yearly fluctuations, making it particularly useful for understanding long-term trends.

- Sample Size: Unlike the full decennial census, the ACS 5-Year Estimate is based on a larger sample size, as it combines data from five years. This results in a more robust dataset, especially beneficial for smaller geographic areas and subpopulations.

- Geographic Coverage: The 5-year estimates are available for all geographies down to the block group level. include the following geographies: nation, all states (including DC and Puerto Rico), all metropolitan areas, all congressional districts (116th congress), all counties, all places, all tracts and block groups.

- Data Variables: Similar to the 1-Year Estimate, the 5-Year Estimate covers a broad range of topics about social, economic, demographic, and housing characteristics of the U.S. population.

- Reliability: The 5-Year Estimate, with its larger sample size, offers increased reliability for smaller geographic areas and subpopulations. However, it's important to note that it may not capture very recent changes, so users should be cautious when interpreting short-term trends.

### Important Considerations:
- ZCTA Coverage: ACS 5-Year Estimates data is available from 2009 onwards; however, ZCTA (ZIP Code Tabulation Area) level information is available from 2011 onwards.
- Comparing ACS 5-Year Estimates: ACS has non-overlapping datasets that allow comparisons of current ACS data to past ACS data. Please refer to the page [here.](https://www.census.gov/programs-surveys/acs/guidance/comparing-acs-data/2021/5-year-comparison.html)

## When to use 1-year or 5-year Estimates?
 <a id="item-five"></a>
For guidance on when to utilize either the 1-Year or 5-Year Estimates, refer to this [resource](https://www.census.gov/programs-surveys/acs/guidance/estimates.html), which provides a clear comparison of the two and offers recommendations on suitable use cases for each.


## What is Decennial Census?
 <a id="item-six"></a>

 Every 10 years, the U.S. Census Bureau conducts a census to determine the number of people living in the United States. 

 Available for the years [2000, 2010, 2020](https://www.census.gov/data/developers/data-sets/decennial-census.2000.html#list-tab-533552149) through the Census API. 

### Important Considerations:
- Data tables from the 1990 census are not available through the census API or data.census.gov. To get tables from any U.S. census back to 1790, you could use nhgis.org, which also has an API.
- The Bureau has redesigned its summary files for the 2020 census. The 2020 DHC (Demographic and Housing Characteristics File) provides most of what was previously available in SF1.

## What is the difference between Decennial and Census?
 <a id="item-seven"></a>

 | Feature             | ACS (American Community Survey)                  | Decennial Census                                 |
|---------------------|-------------------------------------------------|--------------------------------------------------|
| **Frequency**       | Conducted every month, every year               | Conducted every ten years                        |
| **Target Addresses**| Sent to a sample of addresses (about 3.5 million)| Counts every person living in the 50 states, District of Columbia, and the five U.S. territories |
| **Geographic Scope**| 50 states, District of Columbia, Puerto Rico     | 50 states, District of Columbia, five U.S. territories |
| **Survey Topics**   | Topics include education, employment, internet access, transportation | Asks a shorter set of questions, such as age, sex, race, Hispanic origin, and owner/renter status |

For further information refer to this [page.] (https://www.census.gov/programs-surveys/acs/about/acs-and-census.html)


## What Variables are Available in a Dataset/Table?
 <a id="item-eight"></a>
Each data product, in conjunction with its corresponding table or dataset, outlines the variables available for a specific year under the 'Detailed Table Variables' section.

For example, to identify the variables for ACS-5 year estimates in 2017:

-   Navigate to ACS5 Year Estimates.
-   Select the year (2017).
-   Choose the dataset you are interested in, such as the 'Data Profile' table, and then click on 'Detailed Table Variables.'
    
Alternatively, if you already know the specific census product and dataset, you can use the following URL formats:

-  [https://api.census.gov/data/<year>/<product_name>/<dataset>/variables.html](https://api.census.gov/data/%3Cyear%3E/%3Cproduct_name%3E/%3Cdataset%3E/variables.html)
    
-  For our ACS5 2017 example mentioned earlier, you can access the '**Detailed** Table' variables through the following URL: [https://api.census.gov/data/2017/acs/acs5/variables.html](https://api.census.gov/data/2017/acs/acs5/variables.html)


## How do I find the geographical coverage of a dataset/table?
 <a id="item-nine"></a>
**Note: Not all geographies are uniformly supported across all years.** 

Each data product, along with its corresponding table or dataset, specifies its geographical coverage for a particular year in the 'Supported Geography' section.

For instance, if you wish to identify the supported geography for ACS-5 year estimates in 2017:

-   Navigate to ACS5 Year Estimates.
-   Select the year (2017).
-   Choose the dataset you are interested in, such as the '**Detailed** Table', and select 'Supported Geography.'

Alternatively, if you already know the specific census product and dataset, you can use the following URL formats: The below is for '**Detailed** Table':
-   [https://api.census.gov/data/<year>/<product_name>/<dataset>/geography.html](https://api.census.gov/data/%3Cyear%3E/%3Cproduct_name%3E/%3Cdataset%3E/geography.html)
    
-   For our ACS5 2017 example mentioned earlier, you can access the supported geographies for '**Detailed** Table' through the following URL: [https://api.census.gov/data/2017/acs/acs5/geography.html](https://api.census.gov/data/2017/acs/acs5/geography.html). This allows you to determine, for example, that the zip code tabulation area is covered in ACS5 for the year 2017 but not in ACS1 for the same year.

## How to Obtain Your Census API Key?
 <a id="item-ten"></a>

To obtain your Census API Key, follow these steps:

1. Sign up on the Census Bureau's API platform by visiting [this link](https://api.census.gov/data/key_signup.html).
2. Complete the registration process.
3. You will receive an email containing your Census API Key.

Once you have obtained your API key, you can use it to access the Census Bureau's data through their API.


## How can I interact with census data to explore specific variables?
 <a id="item-eleven"></a>
You can navigate census data effortlessly and explore specific variables through the user-friendly interface of [data.census.gov](https://data.census.gov/)

## Where can I connect with experienced professionals to discuss census data?
 <a id="item-twelve"></a>
The Developer’s Forum on [Slack](https://uscensusbureau.slack.com/) - is an active community that proves invaluable for obtaining expert answers to your queries from the knowledgeable professionals at the U.S. Census Bureau.
  
