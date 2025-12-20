# Ecommerce_Sales_Report_Microsoft_Fabric
![Main Page](https://github.com/tirthvyas95/Ecommerce_Sales_Report_Microsoft_Fabric/blob/cda7ea46ae1dcd814c554691f8d8b9fa15191849/Screenshots/SS_1.png)
## Introduction
This is a full Case Study with a generic Ecommerce Sales Dataset in [Microsoft Fabric](https://www.microsoft.com/en-us/microsoft-fabric) with Report from [Power BI Desktop](https://www.microsoft.com/en-us/power-platform/products/power-bi/desktop) and Integration with [PostgreSQL](https://www.postgresql.org/) by using [Microsoft On-Premises Data Gateway](https://learn.microsoft.com/en-us/power-bi/connect-data/service-gateway-onprem) along with special tips for data cleaning in [Power Query](https://learn.microsoft.com/en-us/power-query/power-query-what-is-power-query). The goal of this project is to demonstrate how one could make a relational database, connect it with power tools analysis tools such as Power BI Desktop and share it on Microsoft Fabric Platform where any stake holder can access it from any corner of the world, and finally connecting the resource in Microsoft Fabric to the same on-premises database for real-time analysis where the interactive visuals in the resource or report on Power Bi service can query directly the data source. Following is the workflow with the steps that we are going to follow as we have a lot of things that need to be done:
1. Select a Dataset
2. Clean and Transform Using Power Query
3. Export to .csv using DAX Studio
4. Set up PostgreSQL
5. Make a Power BI Desktop report in Import Mode
6. Make a Power BI Desktop report in DirectQuery
7. Set up a Microsoft Fabric Workspace
8. Install On-Premises Data Gateway and Set connect to Microsoft Fabric Platform
9. Publish the Reports
10. Security Tips
## Select a Dataset
For this project we need a dataset that resembles a real world transactional database which Ecommerce apps use to manage their orders, customers and products. We have selected this [Dataset](https://www.kaggle.com/datasets/rohiteng/amazon-sales-dataset) from [Kaggle](https://www.kaggle.com/). Kaggle is a popular online platform and community for data science and machine learning, owned by Google, that hosts competitions, provides datasets, and fosters collaboration, allowing users to learn, practice, build skills, and solve real-world problems. Where, a certain [contributer](https://www.kaggle.com/rohiteng) has synthetically designed a database that looks and feels like a genuine database with records that resemble real-world users ordering certain products. For our porposes where we want to demonstrate how data from on-premises computers/servers/backends which power Ecommerce websites moves to Microsoft Fabric Platfrom, this dataset should suffice.
Here the head of this dataset but before we use it in our case study we need to do some transformations with it:
![Image](Image)
## Clean and Transform using Power Query
