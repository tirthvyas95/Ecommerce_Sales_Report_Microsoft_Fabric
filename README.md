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
For this project we are going to clean and transform using Power Query, additionally we will need to make a Date Table or Date Dimention for our model in order to use the time intelligence funcitons. Although, most of them are not available for DirectQuery as this complex funcitons are diffcult to convert into native source queries using QueryFolding, but I will show you are this fucntions can provide very useful insights. First of all download the dataset from Kaggle and open up Power BI and save the Report file first before begining(Good Practice). Here is the metadata of the dataset when you download it from Kaggle:
1. OrderID: Unique Identification number for each record
2. OrderDate: Date on which the order was created
3. CutomerID: Unique Identification number for each customer
4. CustomerName: Name of the customer
5. ProductID: Unique Identification number for each product
6. ProductName: Name of the product
7. Category: The category in which the product belongs to
8. Brand: The Brand of the product
9. Quantity: The amount of product ordered
10. UnitPrice: Unit price of the product added to the order
11. Discount
An important point to note is that in this project we are transforming the dataset in PowerQuery and importing it inside PostgreSQL but in real world its usually the other way around but as we are trying to simulate a real world data pipeline we can do this, also this demonstrates Data Cleaning skills.
Please follow the following steps:
1. Click the get data option to connect to the .csv file that you will have downloaded from Kaggle and once you connect click transfrom data instead of the load option. This will start the PowerQuery window
2. First of all on the right side of the window right click on the query(We refer to tables as Queries) and make a new group and name it as staging area
3. Now again right click and click the reference option, this will create a duplicate table with the reference to the original. PowerQuery notes each step/transformation done to the query and you can see it on the right side of the windows in applied steps
4. Now, make a group for the referenced query and name it something else, this way if we make an error we will not need to reconnect to the data source(A good practice)
5. Now, set the column proofing based on the entire dataset on the bottom left side of the window(Very important when cleaning the data)
6. Go to view option and enable Column Distribution, Column Profile and Column Quality
    - Column Distribution: Evaluates data completeness and validity
    - Column Profile: Shows the frequency and spread of values
    - Column Quality:  Provides statistical summaries for a selected column
   This is everthing you will ever need for cleaing the dataset, if you have null values in a column you can either replace or remove by right clicking on the column, or if you encounter duplicates in a primary key column you can remove duplicates as well. You can watch the walkthrough video for more details
7. Now, lets make our three tables: Orders, Customers and Products. Start by again referencing and renaming the new column Customers 
