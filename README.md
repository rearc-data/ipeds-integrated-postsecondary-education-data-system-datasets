<a href="https://www.rearc.io/data/">
    <img src="./rearc_logo_rgb.png" alt="Rearc Logo" title="Rearc Logo" height="52" />
</a>

### Integrated Postsecondary Education Data System (IPEDS) published by the National Center for Education Statistics (NCES)

You can subscribe to the AWS Data Exchange product utilizing the automation featured in this repository by visiting [https://aws.amazon.com/marketplace/pp/prodview-](https://aws.amazon.com/marketplace/pp/prodview-).

## Main Overview
This product provides complete datasets of the Integrated Postsecondary Education Data System (IPEDS) published by the National Center for Education Statistics (NCES). Use cases include historical analysis of the postsecondary education and the current status of various metrics.

#### Data Source
There are 1115 data files in CSV as well as a meta file for each data file in XSLS format. README files are also included to offer context on data fields used throughout the dataset files. All files include daily information aggregated across three different data sources:

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