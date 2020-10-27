### Daily Global & U.S. COVID-19 Cases & Testing Data (Aggregated Data)

The source code outlining how this product gathers, transforms, revises and publishes its datasets is available at [https://github.com/rearc-data/daily-global-and-us-covid-19-cases-and-testing-data-aggregation](https://github.com/rearc-data/daily-global-and-us-covid-19-cases-and-testing-data-aggregation).

## Main Overview
This product provide daily aggregated data related to Covid-19 in different geographical units (countries, US states, US counties). This product can be used to analyze and measure the historical spread, daily trends, and relative impact of Covid-19 in different countries as well as within the U.S.

#### Data Source
There are four data files included with this product in CSV format. README files are also included to offer context on data fields used throughout the dataset files. All files include daily information aggregated across three different data sources:

- covid_19_global.csv - All geographies Combined
- covid_19_us_states.csv - U.S States Only
- covid_19_us_counties.csv - U.S Counties Only
- covid_19_global_countries.csv - Country Level Only

The main fields in the data files include `Date`, `Country / State / County Name`, `FIPS Code / ISO Codes`, `Latitude / Longitude`, `Population`, `number of cases`, `Number of deaths`, and `Number of tests`.

The following data files are also used to map country, U.S. state, and U.s. county names to corresponding FIPS / ISO codes and name abbreviations:
- [country_codes.csv](https://github.com/rearc-data/daily-global-and-us-covid-19-cases-and-testing-data-aggregation/blob/master/pre-processing/pre-processing-code/country_codes.csv)
- [state_codes.csv](https://github.com/rearc-data/daily-global-and-us-covid-19-cases-and-testing-data-aggregation/blob/master/pre-processing/pre-processing-code/state_codes.csv)
- [county_codes.csv](https://github.com/rearc-data/daily-global-and-us-covid-19-cases-and-testing-data-aggregation/blob/master/pre-processing/pre-processing-code/county_codes.csv)

## More Information
- Data Sources:
    - [The New York Times](https://github.com/nytimes/covid-19-data)
    - [Our World in Data](https://github.com/owid/covid-19-data/tree/master/public/data)
    - [The COVID Tracking Project](https://covidtracking.com/api)
- Lisences:
  - [The New York Times](https://github.com/nytimes/covid-19-data/blob/master/LICENSE)
  - [Our World in Data](https://github.com/owid/covid-19-data/tree/master/public/data#license)
  - [The COVID Tracking Project](https://covidtracking.com/about-data/license)
- Frequency: Daily
- Format: CSV

## Contact Details
- If you find any issues with or have enhancement ideas for this product, open up a GitHub [issue](https://github.com/rearc-data/daily-global-and-us-covid-19-cases-and-testing-data-aggregation/issues) and we will gladly take a look at it. Better yet, submit a pull request. Any contributions you make are greatly appreciated :heart:.
- If you are looking for specific open datasets currently not available on ADX, please submit a request on our project board [here](https://github.com/orgs/rearc-data/projects/1).
- If you have questions about the source data, please use contact informations as below:
  - The New York Times: `covid-data@nytimes.com`
  - Our World in Data: `info@ourworldindata.org`
  - The COVID Tracking Project: `https://covidtracking.com/contact`
- If you have any other questions or feedback, send us an email at data@rearc.io.

## About Rearc
Rearc is a cloud, software and services company. We believe that empowering engineers drives innovation. Cloud-native architectures, modern software and data practices, and the ability to safely experiment can enable engineers to realize their full potential. We have partnered with several enterprises and startups to help them achieve agility. Our approach is simple — empower engineers with the best tools possible to make an impact within their industry.