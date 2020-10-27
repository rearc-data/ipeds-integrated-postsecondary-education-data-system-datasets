<a href="https://www.rearc.io/data/">
    <img src="./rearc_logo_rgb.png" alt="Rearc Logo" title="Rearc Logo" height="52" />
</a>

### Integrated Postsecondary Education Data System (IPEDS) published by the National Center for Education Statistics (NCES)

You can subscribe to the AWS Data Exchange product utilizing the automation featured in this repository by visiting [https://aws.amazon.com/marketplace/pp/prodview-](https://aws.amazon.com/marketplace/pp/prodview-).

## Main Overview
This product provides complete data of the Integrated Postsecondary Education Data System (IPEDS) published by the National Center for Education Statistics (NCES). Use cases include historical analysis of the postsecondary education and the current status of various relevant metrics.

#### Data Source
There are 1115 data files in CSV as well as a meta file for each data file in XSLS format. The data files are organized by survey and year. Provisonal and final data files are included for years where both provisional and final have been released. README files are also included to offer context on data fields used throughout the dataset files. 

For most updated details on availability of provisional and final versions per survey and year please visit the [IPEDS webpage](https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx?goToReportId=7). Below is the status of files as of October 2020. 

Available Data | Provisional Release 	| Final Release 
--- | --- | --- |
Institutional Characteristics (IC) |	2019-20	 | 2008-09 to 2018-19 
Pricing and Tuition (IC) |	2019-20	| 2009-10 to 2011-12
Admissions (ADM) |	2019-20	| 2008-09 to 2018-19
Completions (C) |	2018-19	| 2003-04 to 2017-18
12-month Enrollment | (E12)	2018-19	| 2003-04 to 2017-18
Fall Enrollment (EF) |	2018	| 2004 to 2017
Student Financial Aid (SFA) |	2018-19	| 2003-04 to 2017-18
Graduation Rates (GR) |	2019 |	2004 to 2018
Outcome Measures (OM) |	2019	| 2015 to 2018
Finance (F) |	2017-18	| 2003-04 to 2016-17
Human Resources (HR) |	2018-19	| 2004-05 to 2017-18
Academic Libraries (AL) |	2017-18	| 2014-15 to 2016-17
 
<br />
The timing of the releases can vary somewhat depending on the nature of the internal process, but generally will follow this timetable: 
<br />

Collection Period	| Survey Components	| Collection closes	| Provisional data	| Final (Revised) data
--- | --- | --- | --- | ---
FALL |	IC, C, E12 |	November | See I	| See II
WINTER |	ADM, GR, SFA, OM |	March | See I	| See II
SPRING |	EF, F, HR, AL	| April | See I	| See II
See III | See III | See III |	Yes |	No


- I. Approximately 7 months after collection closes	
- II. Approximately 7 months after institutions have revised their data the following year
- III. WEB Tables and Data Release Memo

## More Information
- Data Source: [IPEDS Complete Data Files](https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx)
- Lisence: [IES Public Access Policy](https://ies.ed.gov/funding/researchaccess.asp)
- Frequency: Annual
- Format: CSV (data files), XLSX(meta files)

## Contact Details
- If you find any issues with or have enhancement ideas for this product, open up a GitHub [issue](https://github.com/rearc-data/ipeds-integrated-postsecondary-education-data-system-datasets/issues) and we will gladly take a look at it. Better yet, submit a pull request. Any contributions you make are greatly appreciated :heart:.
- If you are looking for specific open datasets currently not available on ADX, please submit a request on our project board [here](https://github.com/orgs/rearc-data/projects/1).
- If you have questions about the source data, please refer to the [NCES contact page](https://nces.ed.gov/help/webmail/).
- If you have any other questions or feedback, send us an email at data@rearc.io.

## About Rearc
Rearc is a cloud, software and services company. We believe that empowering engineers drives innovation. Cloud-native architectures, modern software and data practices, and the ability to safely experiment can enable engineers to realize their full potential. We have partnered with several enterprises and startups to help them achieve agility. Our approach is simple — empower engineers with the best tools possible to make an impact within their industry.