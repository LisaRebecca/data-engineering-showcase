# Project Plan

## Title
<!-- Give your project a short title. -->
Realistic alternatives: Substituting the worst train connections with electrified highways.

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
Which routes between German cities are the fastest by car (in comparison to travel by train) and should be electrified 
for a "quick win" (compared to new train tracks) in climate action?

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->
Travel time is one of the most important factors in the decision for a mode of transportation.
This project aims to give insights into the extent of the advantage of travel by car over travel by train. 
Routes which are significantly faster by car are analysed with respect to their degree of electrification.
A suggestion for improvements to the charging infrastructure will be made. 
Infrastructure projects such as new railways take up years in planning and executing.
With the spirit of "free passage for free citizens" ("Freie Fahrt für freie Bürger"), a reasonable and at the same time 
environmentally friendly alternative is presented: choosing the fast and flexible travel by car, but opting for EVs instead of fossil fuels.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource 1: Connectivity between largest German Cities
* Metadata URL: https://mobilithek.info/offers/573356838940979200
* Data URL: https://mobilithek.info/mdp-api/files/aux/573356838940979200/moin-2022-05-02.1-20220502.131229-1.ttl.bz2
* Data Type: .ttl.bz2 (compressed turtle)

This RDF-Star knowledge graph shows how well the 100 largest (by population) cities in Germany are connected.
It allows to compare travel by train, car and plane with respect to travel time. 

### Datasource 2: List of Electric Vehicle (EV) Charging Points in Germany
* Metadata URL: https://www.bundesnetzagentur.de/DE/Sachgebiete/ElektrizitaetundGas/Unternehmen_Institutionen/E-Mobilitaet/Ladesaeulenkarte/start.html
* Data URL: https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/E_Mobilitaet/Ladesaeulenregister_CSV.csv?__blob=publicationFile&v=54
* Data Type: CSV

Registry of all publicly accessible charging points registered at the German authority for infrastructure (Bundesnetzagentur).
Contains information on location (address and coordinates) and charging point type/capacity.

### Datasource 3: EV Charging Point Infrastructure in Germany
* Metadata URL: https://www.bundesnetzagentur.de/DE/Sachgebiete/ElektrizitaetundGas/Unternehmen_Institutionen/E-Mobilitaet/Ladesaeulenkarte/start.html
* Data URL: https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/E_Mobilitaet/Ladesaeuleninfrastruktur.xlsx?__blob=publicationFile&v=28
* Data Type: XLSX

This overview on the charging point infrastructure in Germany provides information on the number of charging points per 
federal state, city and district, as well as the historical evolution of the infrastructure.

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

This project is structured into six work packages, represented as [milestones in the GitHub repository](https://github.com/LisaRebecca/data-engineering-showcase/milestones?direction=asc&sort=title&state=open).
Each work package contains at least one issue. Issues are structured as follows:
```
1. Dependent on (Optional)
    - ...
2. Tasks
    - ...
3. Deliverables
    - ...
```

The subtasks and deliverables have to be submitted to mark an issue as completed.

1. Goal Formulation and Dataset selection [[WP1](https://github.com/LisaRebecca/data-engineering-showcase/milestone/1)]
    1. Formulate a research question [[issue](https://github.com/LisaRebecca/data-engineering-showcase/issues/13)]
    2. Identify data sources [[issue](https://github.com/LisaRebecca/data-engineering-showcase/issues/14)]
    3. Assess the data sources [[issue](https://github.com/LisaRebecca/data-engineering-showcase/issues/3)]
2. Data Provisioning [[WP2](https://github.com/LisaRebecca/data-engineering-showcase/milestone/2)]
    1. Identifying a suitable data storage format for the goal [[issue](https://github.com/LisaRebecca/data-engineering-showcase/issues/6)]
    2. Transforming the data into a suitable format [[issue](https://github.com/LisaRebecca/data-engineering-showcase/issues/1)]
    3. Making the datasources available to the project [[issue](https://github.com/LisaRebecca/data-engineering-showcase/issues/2)]
3. Data Exploration [[WP3](https://github.com/LisaRebecca/data-engineering-showcase/milestone/3)]
    1. Perform exploratory data analysis and initial visualisation [[issue](https://github.com/LisaRebecca/data-engineering-showcase/issues/4)]
    2. Evaluate the data sources with respect to their ability to answer the initial research question [[issue](https://github.com/LisaRebecca/data-engineering-showcase/issues/7)]
    3. Select appropriate algorithms and approach to analysing the data [[issue](https://github.com/LisaRebecca/data-engineering-showcase/issues/8)]
4. Data Analysis [[WP4](https://github.com/LisaRebecca/data-engineering-showcase/milestone/4)]
    1. Perform Data Analysis [[issue](https://github.com/LisaRebecca/data-engineering-showcase/issues/5)]
5. Evaluation [[WP5](https://github.com/LisaRebecca/data-engineering-showcase/milestone/6)]
    1. Evaluate the analysis results [[issue](https://github.com/LisaRebecca/data-engineering-showcase/issues/9)]
6. Reporting Results [[WP6](https://github.com/LisaRebecca/data-engineering-showcase/milestone/5)]
    1. Create appropriate visualisations [[issue](https://github.com/LisaRebecca/data-engineering-showcase/issues/10)]
    2. Making the repository presentable [[issue](https://github.com/LisaRebecca/data-engineering-showcase/issues/11)]
    3. Create final presentation [[issue](https://github.com/LisaRebecca/data-engineering-showcase/issues/12)]

In general, the work packages are dependent on all previous ones. Therefore, the **work packages will be worked on in a sequential manner**.
Intra-work package dependencies are listed in the respective issues.

Issues are subject to change, therefore the issue-ID is not suitable to identify dependencies. 
Rather, the dependency list in each issue shall be used.



