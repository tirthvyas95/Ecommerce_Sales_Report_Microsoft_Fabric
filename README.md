# Ecommerce_Sales_Report_Microsoft_Fabric
![Main Page](https://github.com/tirthvyas95/Ecommerce_Sales_Report_Microsoft_Fabric/blob/cda7ea46ae1dcd814c554691f8d8b9fa15191849/Screenshots/SS_1.png)
## Introduction
This is a full Case Study with a generic Ecommerce Sales Dataset in [Microsoft Fabric](https://www.microsoft.com/en-us/microsoft-fabric) with Report from [Power BI Desktop](https://www.microsoft.com/en-us/power-platform/products/power-bi/desktop) and Integration with [PostgreSQL](https://www.postgresql.org/) by using [Microsoft On-Premises Data Gateway](https://learn.microsoft.com/en-us/power-bi/connect-data/service-gateway-onprem) along with special tips for data cleaning in [Power Query](https://learn.microsoft.com/en-us/power-query/power-query-what-is-power-query). 

The goal of this project is to demonstrate how one could make a relational database, connect it with powerful analysis tools such as Power BI Desktop and share it on Microsoft Fabric Platform where any stake holder can access it from any corner of the world, and finally connecting the same resource in Microsoft Fabric to the on-premises database on local machine for real-time analysis where the interactive visuals in the resource or report on Power Bi service can query directly the data source. 

Following is the workflow with the steps that we are going to follow as we have a lot of things that need to be done:
1. Select a Dataset
2. Clean and Transform Using Power Query
3. Export to .csv using DAX Studio
4. Set up PostgreSQL
5. Make a Power BI Desktop report in Import Mode
6. Make a Power BI Desktop report in DirectQuery
7. Install On-Premises Data Gateway and Set up connection to Microsoft Fabric Platform
8. Test the Connection
## Select a Dataset
For this project we need a dataset that resembles a real world transactional database which Ecommerce apps use to manage their orders, customers and products. We have selected this [Dataset](https://www.kaggle.com/datasets/rohiteng/amazon-sales-dataset) from [Kaggle](https://www.kaggle.com/). Kaggle is a popular online platform and community for data science and machine learning, owned by Google, that hosts competitions, provides datasets, and fosters collaboration, allowing users to learn, practice, build skills, and solve real-world problems. Where, a certain [contributer](https://www.kaggle.com/rohiteng) has synthetically designed a database that looks and feels like a genuine database with records that resemble real-world where users ordering certain products. For our porposes where we want to demonstrate how data from on-premises computers/servers/backends which power Ecommerce websites moves to Microsoft Fabric Platfrom, this dataset should suffice.

Here the head of this dataset but before we use it in our case study we need to do some transformations with it:
![Image](https://github.com/tirthvyas95/Ecommerce_Sales_Report_Microsoft_Fabric/blob/eb4ef8a59c441ba75e8d293d91f919583921d3d3/Screenshots/SS_8.png)
## Clean and Transform using Power Query
For this project we are going to clean and transform using Power Query, additionally we will need to make a Date Table or Date Dimention for our model in order to use the time intelligence funcitons. Although, most of them are not available for DirectQuery as this complex funcitons are diffcult to convert into native source queries using QueryFolding, but I will show you even with these fucntions we can furnish very useful insights. First of all download the dataset from Kaggle and open up Power BI and save the Report file first before begining(Good Practice). 

Here is the metadata of the dataset when you download it from Kaggle:
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
11. Discount: Discount provided of each order
12. Tax: Tax imposed
13. ShippingCost: Sipping cost incured
14. TotalAmount: Total amount to be paid by the customer, including discount and tax
15. PaymentMethod: Payment method used by the customer
16. OrderStatus: Status of the order, three distinct values
17. City: City where the customer resides
18. State: State where the customer resides
19. Country: Country where the customer resides
20. SellerID: Unique identification of the seller
An important point to note is that in this project we are transforming the dataset in PowerQuery and importing it inside PostgreSQL but in real world its usually the other way around but as we are trying to simulate a real world data pipeline we can do this, also this demonstrates Data Cleaning skills.
### Open Power BI
Please follow the following steps:
1. Click the get data option to connect to the .csv file that you will have downloaded from Kaggle and once you connect click transfrom data instead of the load option.
2. This will start the PowerQuery window and the data model will be created in Import mode once you click save and apply after finishing your cleaning and transformation
3. First of all on the right side of the window right click on the query(We refer to tables as Queries) and make a new group and name it as 'staging area'
4. Now again right click and click the reference option, this will create a duplicate table with the reference to the original. PowerQuery notes each step/transformation done to the query and you can see it on the right side of the window in applied steps
5. Now, make a group for the referenced query and name it something else like 'model', this way if we make an error we will not need to reconnect to the data source(A good practice)
6. Now, set the column proofing based on the entire dataset on the bottom left side of the window(Very important when cleaning the data)
7. Go to view option and enable Column Distribution, Column Profile and Column Quality
    - Column Distribution: Evaluates data completeness and validity
    - Column Profile: Shows the frequency and spread of values
    - Column Quality:  Provides statistical summaries for a selected column

This is everthing you will ever need for cleaing the dataset, if you have null values in a column you can either replace or remove by right clicking on the column, or if you encounter duplicates in a primary key column you can remove duplicates as well. You can watch the walkthrough video for more details.

Also for the columns OrderID, CustomerID, ProductID and SellerID have values like ORD000123, CUST001504, P00123, and SELL01234 subsequently. We never want to save data like this, there are a couple funcamental problems with storing data like this:
- We will have to save these columns as string/array of characters of varchar, this consumes more space
- By naming primary keys as ABC### you can limiting your range, for example you cannot exceed ABC999
- Moreover, VertiPaq engine which is responsable for storing and compressing data in PowerBI import models performs better with numeric values. That means we can save a lot of space by just changing to one of the numeric data-types

Finally, the reason why we are dividing the dataset into multiple tables is because here also we have an opportunity to reduce the model size, for example in this database there are only 50 products but these products have been ordered over and over again 100000 times which means that details which are same for each product for example attributes of ProductID = 10: Name, Brand, Category and UnitPrice have been repeated each time customer has ordered. While, we only need one identification for each product so we will make a product dimention table.

For instance,
```
ProductID = 7 is ordered 2034 times, so each time someone orders PorductID = 7:
    => ProductName = Dress Shirt, Category = Clothing, Brand = UrbanStyle, ProductID = 7, UnitPrice = 219.81
        => (Values from other columns + 2038*5) values are saved in the Model for that product
```
While, if we have a products dimention table:
```
ProductID = 7 is ordered 2034 times, so each time someone orders ProductID = 7:
    => ProductName = Dress Shirt, Category = Clothing, Brand = UrbanStyle, ProductID = 7 saved once in Products table && ProductID saved 2038 times in Orders table
        => (Values from other columns + 2038 times ProductID in Orders + 1*5 values in Products) values aare saved in the Model for that product
```
The Second option is more optimised and storage efficient, this is like indexing, like makeing a dictionary. If you can expecting your model/dataset to grow substantially in the future then these types of measures are necessary.

We will need to run a command in [M language](https://learn.microsoft.com/en-us/powerquery-m/) which will select and keep only numeric characters and later we will convert the column data-type to Numeric/Decimal.

Click add-column/custom-column and enter this command by substituing your column in [Target Column]:
```
Text.Select([Target Column], {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"})
```
This will create a custom column with just the numbers, change the data type of this column to Decimal, remove the old ID column, and rename this column with that same name. You can check this transformation in Power Query in 'E-Commerce Sales Data Report.pbix' file in the Applied Steps section in PowerQuery.

8. Now, lets make our three tables: Orders, Customers and Products. First we will choose and select the columns for each of these tables:
    - Orders(Fact):
        1. OrderDate
        2. Quantity
        3. Discount
        4. Tax
        5. ShippinCost
        6. TotalAmount
        7. PaymentMethod
        8. OrderStatus
        9. OrderID(Primary Key)
        10. CustomerID(Foreign Key)
        11. ProductID(Foreign Key)
        12. SellerID
    - Customers(Dimension):
        1. CustomerName
        2. City
        3. Country
        4. CustomerID(Primary Key)
        5. State
    - Products(Dimension):
        1. ProductName
        2. Category
        3. Brand
        4. UnitPrice
        5. ProductID(Primary Key)

Our Model will follow a Star Schema where the Dimension tables Connect to the Fact tables, this is the most efficient way to store and query the tables, note that in real world a Data Engineer will already have bifurcated the tables like this to save and optimise the database but here we are doing this on PowerQuery. Also the CustomerID, ProductID act as Foreign Key in the Orders table and they act as primary key in thier subsequent tables.

9. Start by referencing the query in the model group and name it Customer, select the CustomerID column and remove duplicates and now each distinct customer should rest in the table, and finally remove the other unnecessary columns.
10. Similarly, make a reference of the main query in the model group and name it products, here select he ProductsID table and remove duplicates and followed by removing the unnecessary columns.
11. Finally, in the main query in the model group rename it as Orders and remove the columns that are going to be in the dimension tables except the CustomerID and ProductID
12. To end this stage, right click on each query and select which to enable load or not, where disable the option for the query in staging area. Press save and close
13. Now, lets make a date table, go to the model view and press the make a new table on the top, enter this DAX in the field:
```
DateDim = CALENDARAUTO()
```
CALENDATAUTO() function automatically scans your tables and makes a data table by taking minimum date and macimum date, although you can specify them explicitly but for our purposes this should suffice

13. Now, we will add all the columns that we will every need in the data table, add columns and for each column add the following DAXs:
Day of Week:
```
Day of Week = WEEKDAY(DateDim[Date], 2)
```
First Day of Month:
```
First Day of Month = DATE(
                        YEAR(DateDim[Date]),
                        MONTH(DateDim[Date]),
                        1
                    )
```
Day of the Month:
```
Day of the Month = DAY(DateDim[Date])
```
Year:
```
Year = YEAR(DateDim[Date])
```
Day Number:
```
Day Number = 
VAR StartDate =
    CALCULATE ( MIN ( 'DateDim'[Date] ), ALL ( 'DateDim' ) )
RETURN
    DATEDIFF ( StartDate, 'DateDim'[Date], DAY ) + 1
```
Month Name:
```
Month Name = Format(DateDim[Date], "MMMM")
```
Month Number:
```
Month Number = MONTH(DateDim[Date])
```
Keep this in mind that most of time-intelligence functions where this columns are used are not supported in DirectQuery mode so if you wish to make a report with time analysis, it is better to summarize the fact data first and then running the model in Import Mode.

14. Finally we need to make relationships, go to the model view, you can see there all the tables, now click and hold on the ProductID column in the Products table and drag the pointer and place it on the ProductID column in the Orders table, a new window will pop up showing the settings of the relationship, make sure that it is one to many and the filter propogation is one way.
15. Do the same and link CustomerID in Customers tables to CustomerID in orders table, similarly link the Date in the Date Table to OrderDate in the Orders table. Now, your model should look like this:
![Image](https://github.com/tirthvyas95/Ecommerce_Sales_Report_Microsoft_Fabric/blob/eb4ef8a59c441ba75e8d293d91f919583921d3d3/Screenshots/SS_4.png)
## Export to .csv using DAX Studio
To export to .csv we are going to use DAX studio, which can be launched straight from Power BI from the External Tools option. Dax studio is a free open-source tool for Power BI, Excel Power Pivot, and Analysis Services, used for writing, executing, and analysing complex Data Analysis Expressions (DAX) Queries, debugging measures, and optimizing data models and providing a powerful environment for learning and mastering DAX.

Please follow the following steps:
1. You can download DAX Studio from here: [DAX Studio](https://daxstudio.org/)
2. You can open it from the External Tools option which also sends connection details of the model to DAX studio where you can queries which directly queires the VertiPaq engine that compresses and store the model in Power BI
3. Once the DAX studio is open you can see all your tables on the left side and on the center you can write and execute the DAX
4. Go to Advanced option and click on the Export Data, select CSV Files
5. Set the Output Path, Delimiter as Comma, and the file encoding as UTF-8
6. Check all the tables and click export, now you should have 4 exported tables: Orders.csv, Customers.csv, Products.csv, and DateDim.csv

Here is how it should look:
![Image](https://github.com/tirthvyas95/Ecommerce_Sales_Report_Microsoft_Fabric/blob/a2a0de665e0bc06aa236b0ef499eaf8c89c9a7ba/Screenshots/SS_9.png)

Now, we are going to set this data up in PostgreSQL to simulate the real world data flow.
## Set up PostgreSQL
The reason we are using the PostgreSQL is beacuse it is free to use and it is open source, along with the fact that it also supports DirectQuery in Power BI. You can check the supported data sources here. To set up PostgreSQL follow this steps:
1. Download and install the PostgreSQL from here, make sure to remember when you enter the admin credentials when you are prompted
2. Open the pgadmin 4 and make a new database I named it test
3. Make a new login which can be used in Power BI and On-premises data gateway, make sure to assign the role pg_read_all_data
4. Go to Server > test > Schema > Tables, right click on tables and create a new table, we will need to make 4 tables like belows, make sure to use the same datatypes
5. For the Customers use the following settings:
![Image](https://github.com/tirthvyas95/Ecommerce_Sales_Report_Microsoft_Fabric/blob/7d6a0bc88b6c58b09af4f0cf7501a4e69c9f6869/Screenshots/SS_10.png)
6. For the Products table use the following settings:
![Image](https://github.com/tirthvyas95/Ecommerce_Sales_Report_Microsoft_Fabric/blob/a6f335d9444f68ff77aac696271853a770ece4d8/Screenshots/SS_11.png)
7. For the Orders table use the following settings:
![Image](https://github.com/tirthvyas95/Ecommerce_Sales_Report_Microsoft_Fabric/blob/a6f335d9444f68ff77aac696271853a770ece4d8/Screenshots/SS_12.png)
8. For the DateDim table use the following settings:
![Image](https://github.com/tirthvyas95/Ecommerce_Sales_Report_Microsoft_Fabric/blob/a6f335d9444f68ff77aac696271853a770ece4d8/Screenshots/SS_13.png)
9. Before we start importing data to this server we need to a transformation in the .csv files. The dates in the columns came out in the .csv files like "YYYY-MM-DD ##:##:##.###" but we need "YYYY-MM-DD" as set up in the schema
To do this we are going to use a small python script, I am sure you can do the same in Power BI but as long as we reach our goals the questions about which tools we use are inconsequential.
Here is the python script that I used:
```
```
You will have to run this script for three columns 'DateDim.date', 'DateDim.First Day of Month' and 'Orders.OrderDate', also you will need pandas for this, this is how I installed it in Anaconda(More on it in the Test section).
```
conda install pandas
```

10. To import, right click on the table and select Import/Export data option which will pop up a window where toggle to Import mode, give the file path, .csv format, and encoding to UTF8. Also go to options and toggle and enable to header option and the limiter to ','
11. Do the same for Cusotmers, Orders, DateDim and Products tables and run a sample query which should give you an output like below:
![Image](Image)
Now, we are ready to make a Power BI report
## Make a Power BI Desktop report in Import Mode
- Lets open Power BI and go to get data where you can search for PostgreSQL and once select it will ask you for the server IP and the name of the database
- Cick next and it should prompt you for the login credentials, enter in the one we made in PostgreSQL specifiaclly with just the permission to read the data. You can manage you credentials in data source settings File > Options and settings > Login Credintials > Data source settings
- Once it is setup correctly the next windows will show you the tables and thier heads, select all 4 tables and click on load
- Now make the relationships if Power BI has not picked up on them already, your model should look like this:
![Image](Image)
- Now lets add our measures, we are going to use simple measures as complex measures can not be converted to navtive queries in DirectQuery mode where [QueryFolding](https://learn.microsoft.com/en-us/power-query/query-folding-basics) takes place. Most of the Time Intelligence Funcitons are not available in DirectQuery mode for the same reason
- Go to data model view and add this measures one by one, also a good practice is to make a seperate folder for all the measures:
Average Discount:
```
Average Discount = AVERAGE(Orders[Discount])
```
Number of Orders Placed:
```
Number of Orders Placed = COUNTROWS(Orders)
```
Total Product Moved:
```
Total Product Moved = SUM(Products[UnitPrice])
```
Total Revenue:
```
Total Revenue = SUM(Orders[TotalAmount])
```
Total Units Sold:
```
Total Units Sold = SUM(Orders[Quantity])
```
Gross Sales:
```
Gross Sales = [Total Product Moved] * [Total Units Sold]
```
Revenue Lost Due to Discounts:
```
Revenue Lost Due to Discounts = [Gross Sales] * [Average Discount]
```
- We also need to make a select measure where the user can select this measure on which all the values in the visualization will be calculated for this report we will you three measures: Total Revenue, Total Units Sold and Number of Orders Placed
- To make this go to the model view and click New Parameter in Home where select fields and name the measure for my case I did Select Measure, now from the Orders table add these three measures mentioned above
- This will enable us to just put this in the values section of the visualization and it will change according to the selected measure
- Now, you can add visualizations and make your report look something like this:
![Image](Image)
- Finally, publish to report to the choice of your workspace which will create a report file and a semantic model file in the workspace where other users can open the report and use the semantic model in their own reports
Now lets make the same report in DirectQuery mode
## Make a Power BI Desktop report in DirectQuery
Most of the steps that we did in the previous report are similar here but with some changes :
- Open Power BI Desktop and go to get data option and search for PostgreSQL, now when it asks you for the ip of the server enable the radio button beside the DirectQuery mode and load all the tables
- In this case the relationships will not be made automatically as Power BI does not load any data in the model in DirectQuery so it does not have any data to check. Instead, you will have to make the relationships by yourself like follows:
![Image](Image)
- Now, you can add all the measure and make visualizations like just before but the important point to note is that no data has been imported in the model every time you open Power BI or change the select measure or even interact with the visualization the main source which is in our case PostgreSQL is queried be it with some caching ofcourse.
Here is the Report in DirectQuery mode:
![Image](Image)
You can publish the same report to Power BI service/Microsoft Fabric Environment and it will again create two file the semantic model and the report but pay attention to the size of the semantic model you can see it is siginificantly lower:
![Image](Image)
An important point to note is that you need to make sure that to database is able to serve the queries in large amounts if you are planning to share the report with a large audiance, because every time the report is opened in the Power BI service the main data source is queried.
## Install On-Premises Data Gateway and Set up connection to Microsoft Fabric Platform
- The final piece of our puzzle is to set up our On-premises Data Gateway and connect it to Microsoft Fabric Platfrom. On-premises data gateway is a Microsoft Software that can be installed on the system that is hosting the database and it act as a bridge to provide quick and secure data transfer between local machine/system which is hosting the database service and Microsft Fabric Platform. - You can download the On-premises data gateway [here](https://docs.azure.cn/en-us/analysis-services/azure-analysis-services/analysis-services-gateway-install?tabs=azure-portal) and you can find more information [here](https://learn.microsoft.com/en-us/power-bi/connect-data/service-gateway-onprem) and [here](https://docs.azure.cn/en-us/analysis-services/azure-analysis-services/analysis-services-gateway-install?tabs=azure-portal) are the installation steps.
- Some important points to note are, it is must that you remember the passkey for the gateway, you can specify if you have an existing cluster if you do not have one it will create one additionally you can restore a gateway to a system as well but there are seperate steps for that.
- Since we are using PostgreSQL we will need to install a prerequisite the [Npgsql connector](https://learn.microsoft.com/en-us/power-query/connectors/postgresql#prerequisites), once you install this you can set up a dataflow by selecting the get data option in Power BI service.
- Once you set this up, you can go to the settings of the data model and in the Gateway and cloud Connections, you should be able to see your gate way and cluster.
- Try and refresh the model it should be working and finally we will add some rows in the database and see how the change is reflected in the Power BI service.
## Test the Connection
We will test this connection using psycopg2 adapter which is the most widely used PostgreSQL adapter for python. Essentially we will make a script that will communicate with our database and make changes and we will check how the changes reflect in our Report in Microsoft Fabric. This should effectively simulate a Python Backend of a certain application communicating with PostgreSQL to store and we as a Data Analyst we have accessed the same database and build different pipeline that feeds us the most recent data from the database. Also, PostgreSQL is very good at handeling this kind of workloads because of this ACID model and Parallel Query Execution feature.
We will run our Python interpreter in seperate [Anaconda](https://www.anaconda.com/) environment by installing python, psycopg2. We will install this library with Anaconda's own package manager called ['conda'](https://anaconda.org/anaconda/conda) along with creating a seperate environment for out test.
For creating an environment:
```
conda create -- name  test
```
For activating the environment:
```
conda activate test
```
For installing python:
```
conda install python
```
For installing psycopg2:
```
conda install psycopg2
```
Now lets take a look at the python script that we are going to use:
In this script there are 3 options: 
1. You can in insert a row in Orders table with OrderID = 100001 along with some test data in others columns
2. You can in insert another row in Orders table with OrderID = 100002 similarly
3. You can delete every row after OrderID = 100000
We will try and insert a row in Orders table so see how changed reflect in the Dashboard with DirectQuery
```
import psycopg2

hostname = 'localhost'
database = 'Test'
username = 'PyApp'
pwd = 'Test@123'
port_id = 5432
conn = None

try:
    with psycopg2.connect(
            host =  hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id) as conn:
                with conn.cursor() as cur:                
                        case = int(input("1 - Insert \n2 - Insert Another\n0 - DELETE\n"))
                        if case == 1:
                            cur.execute("""
                                            INSERT INTO public."Orders"(
                                                "OrderDate", "Quantity", "Discount", "Tax", "ShippingCost", "TotalAmount", "PaymentMethod", "OrderStatus", "OrderID", "CustomerID", "ProductID", "SellerID")
                                            VALUES ('2024-12-30', 2, 0.15, 77.88, 9.31, 1060.73, 'Debit Card', 'Delivered', 100001, 9034, 41, 1273);
                                        """
                        )
                        if case == 2:
                            cur.execute("""
                                            INSERT INTO public."Orders"(
                                                "OrderDate", "Quantity", "Discount", "Tax", "ShippingCost", "TotalAmount", "PaymentMethod", "OrderStatus", "OrderID", "CustomerID", "ProductID", "SellerID")
                                            VALUES ('2024-12-31', 2, 0.15, 77.88, 9.31, 1060.73, 'Debit Card', 'Delivered', 100002, 9034, 41, 1273);
                                        """
                        )
                        if case == 0:
                            cur.execute("""
                                            DELETE FROM public."Orders" as po
                                            WHERE po."OrderID" > 100000;
                                        """
                        )
                        print("Done")

except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
```
Here are the results:
1. With inserted OrderID = 1000001
![Image](Image)
2. With inserted OrderID = 1000002
![Image](Image)
3. Removing everything after OrderID = 100000

**Thus we have demonstrated that our database installed in the local machine is succesfully being queried by the Report on Power BI Service**
##References
1. Microsoft Learn, Microsoft Learn's Data Analyst Career Path. Retrieved December 26, 2025, from https://learn.microsoft.com/en-us/training/career-paths/data-analyst
2. techFAQ, techFAQ's Youtube Channel, Retieved December 26, 2025, from https://www.youtube.com/watch?v=M2NzvnfS-hI
3. SQLBI, SQLBI's Youtube Channel, Retrieved December 26, 2025. from https://www.youtube.com/watch?v=gZ4JcqFwJfg&list=PLU6II7MW-aiJ3Z-wbUQ0tkqSbAkyiB3uy
## Tools used
1. [Microsoft Azure](https://azure.microsoft.com/en-in)
2. [Microsoft Fabric](https://www.microsoft.com/en-us/microsoft-fabric)
3. [PostgreSQL](https://www.postgresql.org/)
4. [Python](https://www.python.org/)
5. [Anaconda](https://www.anaconda.com/)
6. [Psycopg2](https://pypi.org/project/psycopg2/)
7. [Github](https://github.com/)
8. [Kaggle](https://www.kaggle.com/)
9. [Microsoft Power BI](https://www.microsoft.com/en-us/power-platform/products/power-bi)
10. [DAX STUDIO](https://daxstudio.org/)
