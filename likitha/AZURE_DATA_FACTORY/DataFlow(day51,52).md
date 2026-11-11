1. What is a Data Flow?
A Data Flow is a visual data transformation feature in Azure Data Factory (ADF). It allows us to clean, modify, combine, aggregate and prepare data without writing the complete Spark code ourselves.

For example, imagine an e-commerce company has:
- Customer details in one file.
- Order details in another file.
- Product details in a database.
We want to combine these sources, remove invalid records, calculate total sales and load the final result into a data warehouse.

We can design these steps visually using Mapping Data Flow.

Important: Mapping Data Flow runs on a Spark-based cluster. ADF manages the infrastructure and generates the execution logic behind the scenes. We mainly focus on designing the transformation logic.
2. Types of Data Flow in ADF
Type	Meaning
Mapping Data Flow	Visual, code-free data transformation using Spark
Wrangling Data Flow	Power Query-based data preparation experience

For our data engineering syllabus, we mainly focus on Mapping Data Flow.
3. Data Flow Canvas
The Data Flow canvas has three main parts:








learn.microsoft.com


1. Top bar: Contains actions such as saving, debugging and managing the data flow.
2. Graph area: The visual workspace where we connect sources, transformations and sinks.
3. Configuration panel: Displays the settings of whichever source or transformation we select.
4. Three Main Building Blocks
1. SOURCE

Where data comes from

SQL table, CSV, Parquet, JSON, ADLS, etc.


2. TRANSFORMATIONS

What we do with the data

Filter, Join, Aggregate, Derived Column, Sort, etc.


3. SINK

Where the final data goes

SQL table, data lake, warehouse, etc.


Simple example:

Customers.csv → Remove invalid rows → Join with Orders → Calculate total sales → SQL table
5. Dataset vs Inline Dataset
A source or sink can use a normal ADF dataset or an inline dataset.
Dataset object	Inline dataset
Created separately in ADF	Defined inside the Data Flow source/sink
Can be reused	Scoped to that Data Flow transformation
Useful for standard, reusable connections	Useful for flexible or one-off configurations
Dataset holds connection-related format and structure settings	Connection and format settings are configured directly in the transformation

Analogy: A dataset is like saving an address in your address book. An inline dataset is like writing the address directly on one delivery package.

Both approaches can be used with supported data sources and formats. Inline datasets do not automatically make every source schema dynamic; schema drift and projection settings still matter.
6. Important foundational point
ADF does not modify your original source file simply because a Data Flow reads it.

For example, if a CSV file contains an invalid date, ADF may fail while reading or converting that value. The original CSV remains unchanged. The error happens because the incoming data does not match what the transformation expects.

Remember: Reading data and modifying source data are two different things.

Page 2 of 11 – Source, Projection and Common Transformations
1. Source Transformation
The Source is the starting point of a Data Flow. It tells ADF where to read data from and how to understand it.

Examples:
- Azure SQL Database table.
- CSV file in Azure Data Lake Storage.
- Parquet or Avro file.
- JSON file.
The Source configuration commonly contains:
- Source type: Dataset or inline dataset.
- Source options: File paths, wildcard paths and format-specific options.
- Projection: The columns and their expected data types.
- Optimize: Partitioning-related settings.
- Inspect: Metadata information about the incoming stream.
2. What is Projection?
Projection is the schema or column blueprint that ADF uses for a Data Flow source.

Suppose the source contains:
customer_id	name	age
C01	Ravi	22
C02	Priya	24

The projection might describe:
Column	Data type
customer_id	string
name	string
age	integer

ADF uses this information when building downstream transformations.

Important: ADF datasets and Mapping Data Flow projections are not the same thing. You can define or import a projection in the Data Flow Source. A dataset can also contain schema metadata, but you do not manually define a Mapping Data Flow projection in the same way inside a normal dataset.
3. Four Important Schema Options
Option	Meaning
Allow schema drift	Allows incoming columns not present in the defined projection
Infer drifted column types	Tries to detect data types of new columns
Validate schema	Checks whether incoming data matches the expected schema
Use projected schema	Uses the predefined projection rather than repeatedly discovering schema

Example: Your CSV originally contains id, name, age. Next week, the source team adds city.
- If schema drift is disabled, the new column may not flow through as expected.
- If schema drift is enabled, ADF can pass the new column downstream.
- If type inference is disabled, newly detected drifted columns are treated as strings by default.
- If type inference is enabled, ADF attempts to infer their types.
Schema drift provides flexibility, but it also means some column names and types are not known at design time. Critical columns should still be validated. 
Microsoft Learn+1

4. Why Does Projection Import Need Debug Mode?
When you select Import projection, ADF needs to inspect the source and discover its columns and data types.

For Mapping Data Flow, this inspection uses the active Spark debug environment. Therefore, you generally need Debug mode enabled to import or refresh the projection.

Think of it this way:
- Projection = the blueprint.
- Import projection = asking ADF to inspect the actual source and prepare that blueprint.
- Debug cluster = the temporary compute environment helping ADF perform that inspection.
5. CSV vs Parquet vs Avro: Why Are Delimiter Settings Different?
Your doubt about column delimiters is correct.
CSV / Delimited Text

Example file content
id,name,city
1,Ravi,Hyderabad
2,Priya,Vijayawada


ADF needs to know how values are separated.
- Column delimiter: ,
- Row delimiter: newline
- Quote character: "
- Escape character: \
- Encoding: for example, UTF-8
  
  Parquet / Avro
These are structured file formats with schema information stored in the file format itself.

ADF reads their structural metadata. You do not normally configure CSV-style comma delimiters or quote characters for them.

Why do CSV files need these settings?

Consider this value:
101,"Ravi, Kumar",Hyderabad


The comma inside "Ravi, Kumar" is part of the name, not a separator between two columns. The quote character tells ADF how to interpret it.
- Column delimiter separates columns.
- Row delimiter separates records.
- Quote character surrounds values that contain delimiters.
- Escape character handles special characters inside quoted values.
- Encoding determines how characters are represented.
These settings are important for delimited text, not ordinary Parquet or Avro reading. 
Microsoft Learn

6. Common Transformations
A transformation changes the data stream as it moves through the Data Flow.
Transformation	What it does	Simple example
Select	Keeps, removes, renames or reorders columns	Keep only customer ID and name
Derived Column	Creates a new column or modifies an existing one	total = quantity * price
Filter	Keeps rows matching a condition	Keep orders where amount > 1000
Join	Combines two streams using matching columns	Customers + Orders
Aggregate	Groups rows and calculates summaries	Total sales per customer
Sort	Sorts rows based on one or more columns	Sort sales from highest to lowest

Select example

Input:

customer_id, name, age, address, phone

We only need:

customer_id, name

Use Select to remove unnecessary columns.

Derived Column example

Suppose we have:
quantity	price
2	500
3	200

Create:

total_amount = quantity * price

Result:
quantity	price	total_amount
2	500	1000
3	200	600

Filter example

Expression:
amount > 1000


Only rows whose amount is greater than 1000 pass through.

Join example

Customers:
customer_id	name
C01	Ravi
C02	Priya

Orders:
order_id	customer_id
O01	C01
O02	C01
O03	C02

Join using customer_id.

Result:
order_id	customer_id	name
O01	C01	Ravi
O02	C01	Ravi
O03	C02	Priya

Notice that Ravi appears twice because he has two orders. That is expected in a one-to-many relationship.

Aggregate example

Group by customer_id and calculate sum(amount).

This gives total sales per customer instead of one row per order.

Sort example

Sort by amount in descending order to see the highest-value orders first.

Remember: Sorting is not automatically required before a Join in Mapping Data Flow. Do not add Sort transformations unnecessarily just because you are joining two streams. 
Microsoft Learn+1


Page 3 of 11 – Debug Mode, Data Preview and Expression Builder
1. What is Debug Mode?
Debug mode provides an interactive environment to test Mapping Data Flows while developing them.

When you turn on Debug mode, ADF starts or connects to a Spark-based debug cluster.

Think of it as a temporary laboratory:
- You bring sample data into the laboratory.
- You apply transformations.
- You inspect the result after each step.
- You fix mistakes before running the complete pipeline.
2. How to Turn Debug Mode On and Off








learn.microsoft.com


1. Open your Mapping Data Flow.
2. Locate the Data Flow Debug switch in the top bar.
3. Turn it ON.
4. Select the debug compute configuration.
5. Wait for the cluster to become ready.
6. Use Data Preview to inspect the data.
7. When finished, turn Debug mode OFF to release the debug resources.
Important: Debug mode is not the same as running a production pipeline. Debug sessions can keep compute resources active, so avoid leaving them running unnecessarily.
3. What is Data Preview?
Data Preview displays a snapshot of the data at a particular point in the Data Flow.

For example:

Source → Filter → Derived Column → Join → Sink

You can select:
- Source: See the incoming data.
- Filter: See which rows remain after filtering.
- Derived Column: See the newly created column.
- Join: See the combined output.
This helps us identify exactly where something went wrong.
4. Debug Settings: Sampling
You can configure debug settings such as:
- Row limits.
- Data Flow parameters.
- Debug compute settings.
For learning and testing, use small sample files or a reasonable row limit.

Why?

If your source has 10 million records, there is no need to inspect all 10 million records just to check whether a column expression works.

Important: A sample preview is not proof that the full production dataset will work. Test the actual pipeline with realistic data before deployment. 
Microsoft Learn+1

5. Does the Sink Write Data During Debugging?
This needs an important distinction:
- Data Preview: It displays intermediate results. It does not commit the previewed data to your final sink.
- Pipeline Debug run: If you execute a Data Flow activity as part of a pipeline debug run, the Data Flow can execute its sink and write data.
So do not assume that every operation performed while debugging is harmless to the destination. Use a test destination when executing pipeline runs.
6. Quick Actions in Data Preview
When you select a column in Data Preview, ADF provides useful quick actions.
Quick action	Purpose
Typecast	Change the column's data type
Modify	Modify a column
Remove	Remove a column
Statistics	View column statistics
Map Drifted	Generate mappings for detected drifted columns

These actions can generate or help configure transformations such as Select and Derived Column.
7. Data Profiling – The X-Ray of Your Data
Data profiling helps us understand the quality and distribution of values in a column.

It is similar to using describe() in Pandas, although the information and available statistics depend on the data type and preview.

Examples:

For a string column:
- Number of nulls.
- Number of empty values.
- Distinct values.
- Frequency of values.
For a numeric column:
- Minimum.
- Maximum.
- Average.
- Distribution-related statistics.
Example: If the age column contains 500 rows but 100 are null, profiling helps you notice the issue before loading the data.
8. Data Flow Expression Builder
The Expression Builder is where we write expressions used by transformations.

It is similar to writing formulas in Excel, but it has functions designed for data transformation.

Examples:
Function	Purpose
iif()	Conditional logic
isNull()	Checks whether a value is NULL
coalesce()	Returns the first non-NULL value
trim()	Removes leading/trailing spaces
toInteger()	Converts a value to integer
toDate()	Converts a value to date
lower()	Converts text to lowercase
concat()	Combines strings

Examples
iif(amount > 1000, 'High', 'Low')


coalesce(city, 'Unknown')


trim(customer_name)


toInteger(age_text)


concat(first_name, ' ', last_name)


Important: Mapping Data Flow expressions and pipeline expressions are different languages. For example, @pipeline().RunId belongs to the pipeline expression language, while isNull() and toInteger() are Mapping Data Flow expression functions. 
Microsoft Learn+1


Page 4 of 11 – Schema Drift, Null Handling and Data Type Errors
1. What is Schema Drift?
Schema drift happens when the structure of incoming data changes over time.

Example:

Monday's file
id	name	age
1	Ravi	22

Friday's file
id	name	age	city
1	Ravi	22	Hyderabad

The source has added a new column called city.

If our Data Flow expects only the original three columns, we need to decide how to handle the new column.

Allow schema drift lets ADF accept new columns that are not part of the defined projection.

Infer drifted column types attempts to identify the types of those new columns.
2. How Do We Use Drifted Columns?
When columns are not known at design time, we can use:
- byName() – access a column using its name.
- byPosition() – access a column using its position.
- Column patterns – apply logic to columns matching certain conditions.
- Map Drifted – generate mappings for detected drifted columns.
Example:
byName('city')


This references a column named city, even when it is a drifted column.

When should we use schema drift?
- Source files frequently gain new columns.
- We process many files with slightly different structures.
- We are building reusable pipelines for dynamic sources.
When should we avoid blindly enabling it?
- A strict database contract must be followed.
- Important columns must always be present.
- Unexpected columns should cause an alert rather than silently passing through.
3. Null Handling
A NULL means that a value is missing or unknown.

Do not confuse these values:
Value	Meaning
NULL	Missing or unknown value
0	Numeric zero
''	Empty string
'   '	String containing spaces
'null'	Actual text containing the word null
false	Boolean false

They are not interchangeable.

Check for NULL
isNull(city)


Keep non-NULL values
!isNull(city)


Replace NULL with a default value
coalesce(city, 'Unknown')


Handle NULL and empty strings
iif(isNull(city) || trim(city) == '', 'Unknown', trim(city))


Important business rule: Do not replace every missing numeric value with zero automatically.

For example, if salary is NULL, it does not necessarily mean the employee earns zero. It may mean salary information was not provided.
4. Handling Invalid Records
Suppose a customer ID is mandatory.
customer_id	name
C01	Ravi
NULL	Priya
C03	Anu

We should not invent a customer ID for Priya.

Instead:
- Valid records → Continue to the main pipeline.
- Invalid records → Send to a reject/quarantine location.
- Investigate whether the missing value can be corrected using a valid business rule.
A Filter or Conditional Split can help implement this logic.
5. Column Name Mismatch
Suppose the source has:

customer_name

But your Derived Column expression refers to:

customerName

ADF may produce:

DF-Executor-ColumnNotFound

Common reasons:
1. Typo in the expression.
2. Source column was renamed.
3. Projection is outdated.
4. Source schema changed.
5. Wrong column reference after a transformation.
How to debug:
1. Open the source.
2. Check its Projection tab.
3. Refresh/import the projection if required.
4. Open Inspect to verify the available column names.
5. Check every downstream expression.
6. Use Select to rename the column if necessary.
6. Data Type Errors
Every column has a data type.

Examples:
Column	Expected type
age	Integer
salary	Decimal
joining_date	Date
is_active	Boolean
customer_name	String

Suppose your source contains:
age
22
25
Twenty
30

If ADF tries to convert Twenty into an integer, conversion fails.

Safer approach:
1. Read the original value.
2. Clean unnecessary spaces.
3. Validate whether the value is convertible.
4. Convert valid values.
5. Send invalid values to a reject stream.
Useful functions:
isInteger(trim(age_text))


toInteger(trim(age_text))


toDate(joining_date, 'dd-MM-yyyy')


For a date such as 15-08-2026, the format must match the actual input format.

Also remember:
- Decimal precision and scale matter.
- Boolean values should be interpreted according to accepted values.
- Source types and sink types must be compatible.
ADF provides conversion functions and validation functions such as isInteger() and isDate(). 
Microsoft Learn+1

7. Validate Schema: Source vs Sink
- Source Validate Schema: Checks whether incoming source data matches the expected projection.
- Sink Validate Schema: Checks whether the output schema is compatible with the destination's expected structure.
If the source or destination changes, the Data Flow may fail even though you have not modified the original source file.

Golden rule: Check the schema at the source, after important transformations, and at the sink.

Page 5 of 11 – Choosing Between Copy Activity, Data Flow and Spark Notebook
These three tools can all be part of a data engineering pipeline, but they solve different problems.
1. Copy Activity
Copy Activity is mainly used to move data from one location to another.

Think of it as a delivery truck.

Examples:
- SQL Server → Azure Data Lake.
- CSV → Parquet.
- Azure Blob Storage → Azure SQL Database.
It also supports:
- Column mapping.
- Supported data type conversions.
- File format conversion.
- Compression and decompression.
- Parallel copy.
- Staging and supported fault-tolerance options.
Use Copy Activity when the primary requirement is data movement, not complicated transformation logic.
2. Mapping Data Flow
Mapping Data Flow is used for visual transformations.

Examples:
- Join Customers and Orders.
- Remove invalid records.
- Calculate total sales.
- Group records by customer.
- Create multiple output streams.
It runs on Spark-based compute managed by ADF.

Use it when the transformations can be expressed clearly using its visual transformation features.
3. Spark Notebook
A Spark Notebook is useful when we need more control and custom code.

For example:
- Complex PySpark logic.
- Custom algorithms.
- Complicated nested JSON processing.
- Advanced data processing frameworks.
- Machine learning preparation.
In ADF, a Databricks Notebook activity executes a notebook on Databricks compute. It does not execute on the Mapping Data Flow debug cluster.
4. Quick Comparison
Feature	Copy Activity	Mapping Data Flow	Spark Notebook
Main purpose	Move data	Visual transformations	Custom code processing
Coding	Usually minimal	No Spark code required	PySpark/Scala
Compute	Connector/copy infrastructure	Managed Spark	Databricks/Synapse Spark
Best for	Simple ingestion	Joins, filters, aggregates	Complex custom logic
Complexity	Low for simple movement	Medium	Depends on code

5. How Do We Choose?
Ask yourself: What is the actual requirement?
Only moving data?

Choose Copy Activity.

Visual transformations are sufficient?

Choose Mapping Data Flow.

Need complex custom Spark logic?

Choose a Spark Notebook.

Also consider database-side SQL or stored procedures when the data already resides in a database and the required transformations are best performed there.

6. Can We Use All Three in One Pipeline?
Yes. In fact, this is a common design.

Example:

Copy Activity → Mapping Data Flow → Databricks Notebook
1. Copy raw customer files into ADLS.
2. Use Mapping Data Flow to clean, join and aggregate the records.
3. Use a Databricks Notebook for advanced custom processing.
Interview point: We do not select a tool just because it can perform a transformation. We select it based on complexity, maintainability, compute requirements, cost and performance.

Page 6 of 11 – Advanced Transformations: Window, Pivot, Unpivot and Surrogate Key
1. Window Transformation
Window transformation performs calculations over a group of rows without necessarily reducing the number of rows.

Suppose we have:
customer	order_date	amount
Ravi	Jan 1	500
Ravi	Jan 2	700
Ravi	Jan 3	300

We want to calculate the running total for Ravi.
customer	amount	running_total
Ravi	500	500
Ravi	700	1200
Ravi	300	1500

The Window transformation can perform this type of calculation.

Its important configuration areas are:
Setting	Meaning
Over	Defines the grouping/partition columns
Sort	Defines the order of rows inside each group
Range by	Defines the window frame
Window columns	Defines the calculations to perform

Remember:
- over() defines the group or partition.
- sort defines the row order.
- range by defines which rows are included in the calculation.
- Window columns contain the output expressions.
Examples of window functions include:
- rowNumber()
- rank()
- denseRank()
- sum()
- avg()
- lag()
- lead()
- cumeDist()
Cumulative Distribution (CUME_DIST)

It tells us the fraction of rows in a partition whose values are less than or equal to the current row's value, according to the ordering.
\[
CUME\_DIST = \frac{\text{Number of rows up to the current peer group}}{\text{Total rows in the partition}}
\]

For example, if 8 out of 10 rows have a value less than or equal to the current row's value:
\[
CUME\_DIST = \frac{8}{10} = 0.8
\]

It returns a value between 0 and 1.

Important: If the requirement is simply to generate a rank or row number over the entire dataset, check whether the Rank or Surrogate Key transformation is more suitable. A Window transformation is not always the best choice for those tasks. 
Microsoft Learn+1

2. Pivot Transformation
Pivot converts distinct values from rows into separate columns.

Suppose the input is:
department	month	sales
IT	Jan	100
IT	Feb	200
HR	Jan	150
HR	Feb	250

After Pivot:
department	Jan	Feb
IT	100	200
HR	150	250

Important configuration:
- Group by: Columns used to identify each output row.
- Pivot key: Column whose values become output column names.
- Pivot columns: Values or expressions to aggregate into those new columns.
3. Unpivot Transformation
Unpivot does the opposite: it converts multiple columns into rows.

Input:
department	Jan	Feb
IT	100	200
HR	150	250

Output:
department	month	sales
IT	Jan	100
IT	Feb	200
HR	Jan	150
HR	Feb	250

Important configuration:
- Ungroup by: Columns that should remain as identifiers.
- Unpivot key: The output column that holds the original column names.
- Unpivot columns: The columns whose values should be converted into rows.
4. Surrogate Key Transformation
A surrogate key is an artificial identifier created for records.

Example:
customer_name	customer_key
Ravi	1
Priya	2
Anu	3

The key does not carry business meaning. It is mainly used to identify records in dimensional models.

Why use it?
- Business keys may change.
- A source may not provide a suitable unique identifier.
- Data warehouses often use surrogate keys for dimension records.
Important distinction:
- Surrogate key transformation creates an incrementing artificial key.
- guid() creates a globally unique identifier.
- Pipeline RunId identifies a particular pipeline execution.
These are not interchangeable.

A GUID can be used as an identifier if the design requires it, but it is not the same as an incrementing surrogate key.
5. EXISTS Transformation
Exists checks whether a record from one stream has a matching record in another stream.

Example:

Customers:
customer_id
C01
C02
C03

Active customers:
customer_id
C01
C03

If we want customers who exist in the Active Customers stream, use Exists.

Result:
customer_id
C01
C03

The two common conditions are:
- Exists: Keep rows that have a match.
- Doesn't Exist: Keep rows that do not have a match.
Think of it as asking: "Does this customer exist in the other list?"
6. Lookup Transformation
Lookup is used to find matching information from another stream.

Example:

Orders:
product_id	quantity
P01	2
P02	3

Products:
product_id	product_name
P01	Laptop
P02	Mouse

After Lookup, we can attach product names to the order records.

A useful function is:
isMatch()


It tells us whether a Lookup found a matching record. We can use it with Conditional Split to separate matched and unmatched rows.

Difference between Join, Exists and Lookup:
Transformation	Main purpose
Join	Combine columns from two streams
Exists	Check whether a matching record exists
Lookup	Find matching reference information and use it in the output


Microsoft Learn+1

Page 7 of 11 – Conditional Split, Multiple Sinks and Deduplication
1. Conditional Split Transformation
Conditional Split divides one data stream into multiple streams based on conditions.

Imagine we have orders:
order_id	amount
O01	500
O02	5000
O03	10000
O04	200

We want to classify them:
- High value: amount greater than 5000.
- Medium value: amount between 1000 and 5000.
- Low value: amount less than 1000.
We can use Conditional Split.
Orders Source


Conditional Split

High

amount > 5000


Medium

1000–5000


Low

amount < 1000




Two important options:
- First matching condition: A row goes into the first output whose condition matches.
- All matching conditions: A row can go into multiple outputs if multiple conditions match.
Example: If a row satisfies both Condition A and Condition B:
- First matching condition → It goes into the first matching output.
- All matching conditions → It can go into both outputs.
2. Multiple Sinks
A Data Flow can have multiple sinks.

Example: After processing customer records, we want:
- Valid customers → Customer table.
- Invalid customers → Reject file.
- Summary information → Reporting table.
We can create multiple branches and connect each branch to its own sink.

Important sink settings:
- Sink group.
- Execution priority.
- Whether sinks in a group should run in parallel.
- Whether the group should continue after a sink error.
Default behavior:
- Sinks execute sequentially.
- A sink error fails the Data Flow.
- All sinks are initially assigned to the same group.
You can configure different sink groups and execution behavior when required. 
Microsoft Learn

3. Deduplication
Deduplication means removing unwanted duplicate records.

Example:
customer_id	name	updated_at
C01	Ravi	Jan 1
C01	Ravi Kumar	Jan 5
C02	Priya	Jan 3

Suppose we want only the latest record for each customer.

Incorrect approach: Simply use Distinct and assume the latest record will be retained.

Distinct removes duplicate rows based on the selected columns, but it does not automatically mean "keep the latest record."

Better approach:
1. Group or partition by customer_id.
2. Sort by updated_at in descending order.
3. Use a ranking or row-number approach.
4. Keep the first record for each customer.
Conceptually:
Partition by customer_id
Sort by updated_at DESC
Keep row_number = 1


Now we retain the latest version of each customer.

Important: Always decide what makes a record a duplicate before removing anything.
- Same customer ID?
- Same customer ID and email?
- Same complete row?
- Same business key, but different update timestamps?
The correct definition depends on business requirements.
4. Deduplication vs Aggregation
Deduplication	Aggregation
Removes unwanted repeated records	Combines records into summaries
Can retain one selected record	Calculates values such as SUM, COUNT and AVG
Example: Keep latest customer record	Example: Total sales per customer


Page 8 of 11 – Slowly Changing Dimensions (SCD) and Flowlets
1. What is a Slowly Changing Dimension?
In a data warehouse, dimension tables store descriptive information about business entities.

Examples:
- Customer.
- Product.
- Employee.
- Location.
Suppose a customer changes their city from Hyderabad to Bengaluru.

How should the data warehouse handle that change?

That is where Slowly Changing Dimensions (SCD) come in.
2. SCD Type 1
SCD Type 1 overwrites the old value with the new value.

Before:
customer_id	name	city
C01	Ravi	Hyderabad

After:
customer_id	name	city
C01	Ravi	Bengaluru

The old city is not retained.

Use it when: We do not need historical information.

Example: Correcting a spelling mistake in a customer name.
3. SCD Type 2
SCD Type 2 preserves history by creating a new version of the record.

Before:
customer_key	customer_id	city	is_current
101	C01	Hyderabad	true

After the customer moves:
customer_key	customer_id	city	is_current
101	C01	Hyderabad	false
102	C01	Bengaluru	true

We have preserved the previous version.

Common SCD Type 2 columns:
- Surrogate key.
- Business key.
- Effective start date.
- Effective end date.
- Current-record flag.
Example:
customer_key	customer_id	city	start_date	end_date	is_current
101	C01	Hyderabad	Jan 1	Mar 15	false
102	C01	Bengaluru	Mar 16	NULL	true

4. How to Implement SCD Using Mapping Data Flow
A typical SCD process:
1. Read incoming customer records
   
   Read the new customer data from the source.
2. Read existing dimension records
   
   Read the current records from the dimension table.
3. Join using the business key
   
   Match incoming customers with existing customers using customer_id.
4. Compare the columns
   
   Check whether the city, name or other tracked attributes changed.
5. Separate new, changed and unchanged records
   
   Use Derived Column and Conditional Split.
6. Apply the required action
   - New customer → Insert.
   - Unchanged customer → Ignore.
   - Changed customer → Update for Type 1, or expire old version and insert a new version for Type 2.
7. Write to the dimension table
   
   Use appropriate sink mapping and Alter Row policies where supported.

5. What is Alter Row?
Alter Row defines what action should happen to a record at a supported sink.

It can mark rows for:
- Insert.
- Update.
- Delete.
- Upsert.
For example, if an existing customer's city changes and we are implementing SCD Type 1, we can mark the matching row for update.

For SCD Type 2, we need to expire the old version and insert a new version. This requires careful branching and sink logic.

Important: Alter Row defines row policies; it does not automatically build the entire SCD solution for you. The matching, comparison, expiration and insertion logic must be designed correctly. The destination must support the required write behavior. 
Microsoft Learn+1

6. What is a Flowlet?
A Flowlet is a reusable collection of Data Flow transformation logic.

Imagine that three different Data Flows need to perform the same customer-cleaning operation:
- Remove unwanted spaces.
- Normalize email addresses.
- Standardize phone numbers.
- Validate customer IDs.
Instead of building these transformations three times, we can create one Flowlet and reuse it.
Reusable Customer Cleaning Flowlet

Data Flow A


Data Flow B


Data Flow C




Advantages:
- Reuse logic.
- Avoid duplication.
- Maintain consistent business rules.
- Make Data Flows easier to manage.
Remember: A Flowlet is like a reusable function, but for Data Flow transformations.

Page 9 of 11 – Data Flow Monitoring and Performance Analysis
1. Why Do We Need Monitoring?
Creating a Data Flow is only one part of the job.

After execution, we need to understand:
- Did the Data Flow succeed?
- How many rows were read?
- How many rows were written?
- Which transformation took the most time?
- Where did the data volume increase or decrease?
- Are some Spark partitions processing much more data than others?
ADF provides a dedicated Data Flow monitoring view for these questions.
2. Four Major Performance Bottlenecks
Microsoft's performance guidance helps us think about four broad areas:
1. Cluster startup

How long does Spark take to start?

A fresh cluster can take several minutes to become ready.


2. Source reading

How long does it take to read input data?

Could be caused by large files, slow source systems or connectivity.


3. Transformation processing

How long does Spark take to process the data?

Could be caused by joins, aggregations, skew or expensive calculations.


4. Sink writing

How long does it take to write the result?

Could be caused by slow destination systems, excessive output files or write bottlenecks.


Interview tip: Never assume that a slow Data Flow is always caused by insufficient Spark compute. First identify which of these four areas is slow.
3. How to Read the Monitoring View
After a Data Flow activity runs:
1. Open the ADF Monitor section.
2. Find the pipeline run.
3. Open the Data Flow activity details.
4. Select the monitoring/graph view.
5. Inspect the stages and transformations.
The monitoring view provides information such as:
- Stage timings.
- Row counts.
- Transformation execution details.
- Partition statistics.
- Data lineage.
4. Stage Timings
Stage timings tell us how much time is spent in different processing stages.

Suppose:
Stage	Processing time
Source reading	20 seconds
Join	180 seconds
Aggregate	30 seconds
Sink writing	40 seconds

The Join stage is the slowest.

We should investigate the Join first instead of increasing the cluster immediately.

You can sort transformations by processing time to identify the slowest one.
5. Row Counts
Row counts help us understand how records move through the Data Flow.

Example:
Transformation	Rows
Source	100,000
Filter	80,000
Join	120,000
Aggregate	5,000
Sink	5,000

What can we understand?
- Filter removed 20,000 rows.
- Join increased the row count from 80,000 to 120,000.
- Aggregate reduced the rows to 5,000.
The Join output increased. This may be valid, or it may indicate duplicate keys or incorrect join logic.

Never assume that a higher row count is automatically an error. Understand the expected business relationship.
6. Partition Statistics
Spark divides data into partitions so that different tasks can process data in parallel.

Monitoring provides statistics that help us understand how evenly data is distributed.

Two useful terms:
- Skewness: Helps describe asymmetry in a distribution.
- Kurtosis: Helps describe how peaked or heavy-tailed a distribution is.
ADF's monitoring view can show partition statistics including skewness and kurtosis.

If one partition has far more data than the others, that can cause uneven processing.
7. Column Lineage
When you select a Sink in the monitoring view, you can inspect column lineage.
Type	Meaning
Mapped	Column came from the source and is mapped to the sink
Derived	New column created during transformation
Computed	Column used for processing or expressions but not necessarily written to the sink

Example:
- customer_id from source → Mapped.
- total_amount = quantity * price → Derived.
- is_valid used only in a Filter condition → Computed.
Lineage helps us understand where the final output columns originated.

Microsoft Learn+1
8. A Simple Monitoring Example
Suppose a Data Flow normally takes 2 minutes, but today it takes 12 minutes.

My investigation:
1. Check cluster startup time.
2. Check source reading time.
3. Sort transformations by processing time.
4. Inspect row counts before and after Join.
5. Check partition statistics.
6. Inspect sink writing time.
7. Optimize the actual bottleneck.
8. Run again and compare.
Remember: Monitoring is not just checking whether a pipeline succeeded. It is understanding how it performed.

Page 10 of 11 – Runtime Configuration, Cluster Startup and Common Debugging
1. Data Flow Activity Settings
When we add a Data Flow activity inside an ADF pipeline, we can configure execution settings.








learn.microsoft.com


Important settings include:
Setting	Purpose
Integration Runtime	Defines the compute environment used for triggered execution
Compute type	Defines the type of Spark compute
Core count	Defines the compute size where supported
TTL	Keeps a cluster warm for reuse
Checkpoint key	Identifies the CDC checkpoint state
Staging / PolyBase	Supports bulk loading for Synapse
Logging level	Controls the amount of execution telemetry
First row only	Limits cache sink output passed to the pipeline

2. Integration Runtime and Compute Types
Mapping Data Flow uses Spark-based compute.

ADF provides compute configuration options such as:
- General purpose.
- Compute optimized.
- Memory optimized.
Simple meaning:
Compute type	Best suited for
General purpose	Balanced workloads
Compute optimized	Workloads needing more processing power
Memory optimized	Workloads that need more memory

The actual compute options depend on the supported configuration.
3. Cold Start vs Warm Cluster
Cold start: A new Spark cluster needs to be provisioned and started. This can take several minutes.

Warm cluster: An existing cluster is reused instead of starting a fresh one.

This is where TTL (Time to Live) comes in.

Suppose TTL is 10 minutes:
- Data Flow A finishes at 10:00 AM.
- The cluster remains available for reuse.
- Data Flow B starts at 10:05 AM.
- If the same eligible compute environment can be reused, startup overhead can be avoided.
- After the idle TTL expires, the cluster is released.
Important correction: AutoResolve does not automatically mean warm start, and a custom Integration Runtime does not automatically mean cold start. Warm/cold behavior depends on cluster availability and TTL configuration, not simply the name of the Integration Runtime.

The Data Flow activity's Integration Runtime applies to triggered pipeline execution. Debug execution uses the compute environment configured for the debug session. 
Microsoft Learn+1

4. What Is the Default AutoResolve Debug Configuration?
Microsoft documentation describes an AutoResolve debug configuration that provisions an 8-core General compute cluster with a default 60-minute TTL.

The operationalized Data Flow activity has its own compute defaults and configuration.

Do not confuse:
- Debug cluster configuration.
- Triggered pipeline execution configuration.
Also, 8 cores does not mean 8 worker nodes. Cores and nodes are different concepts.
5. PolyBase Staging
Suppose your destination is Azure Synapse Analytics.

Writing millions of rows individually can be slow.

PolyBase staging allows bulk loading through a temporary staging location in Azure Blob Storage or ADLS.

Think of the difference:
- Row-by-row loading = carrying one item at a time.
- Bulk loading = transporting a complete shipment together.
PolyBase is particularly useful for large Synapse loading workloads. It requires a suitable staging linked service and storage path. 
Microsoft Learn

6. Logging Levels
ADF offers logging levels for Data Flow activity execution.
Level	Meaning
Verbose / Fine	Detailed partition-level execution information
Basic / Coarse	Transformation durations
None	Summary of durations

Verbose logging is useful while troubleshooting, but collecting detailed telemetry has overhead.

A practical approach:
- While debugging: Use detailed logging when necessary.
- Normal production execution: Use Basic or None if detailed logs are not required.
7. CDC Checkpoint Key
CDC stands for Change Data Capture.

It allows us to process new or changed records instead of repeatedly processing everything.

Think of a checkpoint as a bookmark.

Example:
- First run processes changes up to a particular point.
- The checkpoint remembers the progress.
- The next run continues from the saved position.
ADF manages checkpoints automatically for supported change-capture scenarios.

The default checkpoint key is a hash of the Data Flow name and pipeline name. If you dynamically process different source tables or folders, you may need to override it with an appropriate key.

Important: Do not confuse these identifiers:
Identifier	Meaning
Pipeline Run ID	Unique identifier for one pipeline execution
GUID	Globally Unique Identifier
CDC checkpoint key	Identifies the checkpoint state
Surrogate key	Artificial key used to identify a dimension record

A pipeline Run ID identifies an execution, not an individual business record. A GUID can be generated with the pipeline expression function guid() when a globally unique identifier is required. It is not the same as a sequential surrogate key.
8. Cache Sink and First Row Only
A Cache sink can write output to the Data Flow activity output so that a subsequent pipeline activity can use it.

The pipeline output has a 2 MB limit.
- First Row Only unchecked: ADF attempts to pass as many rows as possible within the output limit.
- First Row Only checked: ADF returns only the first row.
It does not mean that the Data Flow processes only one row. It limits the output passed from the cache sink into the pipeline.

Use this when you need a small result, such as a control value or a single summary record, rather than passing an entire dataset between pipeline activities. 
Microsoft Learn+1

9. Debug Cluster Not Starting
Possible causes:
- Integration Runtime or region configuration issue.
- Temporary compute provisioning issue.
- Network, firewall or private endpoint problem.
- DNS or connectivity issue.
- Unhealthy or expired debug session.
Troubleshooting order:
1. Read the exact error message.
2. Check the selected debug compute configuration.
3. Check whether the cluster is still provisioning.
4. Verify the Integration Runtime and region.
5. Check network and storage connectivity.
6. Restart an unhealthy debug session if appropriate.
7. Retry with a small test source.
Important: If the cluster is already running but the source preview fails, do not repeatedly restart the cluster. Check the linked service, credentials, permissions, source path and schema instead.
10. Debugging Checklist
Problem	First thing to check
Cluster not starting	Debug compute and IR
Preview fails	Source connection and permissions
Column not found	Projection and expression
Null values	isNull() and business rules
Conversion error	Actual input format and target type
Sink fails	Sink mapping and destination schema
New source column	Schema drift and projection
Debug works, production fails	Runtime, permissions, data size and production settings


Page 11 of 11 – Performance Troubleshooting, Interview Scenarios and Revision
1. Join Explosion
A Join explosion happens when the number of output rows increases unexpectedly after a Join.

Example:

Left table:
customer_id	customer_name
C01	Ravi
C01	Ravi
C02	Priya

Right table:
customer_id	order_id
C01	O01
C01	O02
C02	O03

For C01:
- Left side has 2 matching rows.
- Right side has 2 matching rows.
- Output has 2 × 2 = 4 matching combinations.
This is why duplicate keys on both sides can multiply the output.

What should I check first?
1. Check the Join condition.
2. Check duplicate keys on both sides.
3. Understand the relationship: one-to-one, one-to-many or many-to-many.
4. Check whether the increased row count is expected.
5. If duplicates are unwanted, fix the source or deduplicate using a valid business rule.
Important: Do not immediately increase the Spark cluster. More compute cannot correct incorrect Join logic.
2. Skewed Partitions
Spark divides data into partitions and processes them in parallel.

Ideally, the data should be distributed reasonably evenly.

Suppose we have four partitions:
Partition	Records
P1	10,000
P2	12,000
P3	11,000
P4	500,000

P4 has far more records than the others.

This is called data skew.

The other partitions may finish quickly, while P4 takes much longer.

Why does skew happen?
- A few keys occur very frequently.
- Many records have NULL or default values in the Join key.
- Some customers or products have unusually high activity.
- A Join or Aggregate groups too much data under one key.
How do we fix it?
1. Inspect partition statistics.
2. Identify hot keys.
3. Filter unnecessary records early.
4. Broadcast a genuinely small dataset when appropriate.
5. Consider repartitioning.
6. Isolate unusually frequent keys or use advanced techniques such as salting when justified.
Important: Simply increasing the number of partitions may not solve skew. If the same key continues to go to the same partition, that partition can remain overloaded.
3. Out of Memory (OOM)
OOM means Out of Memory.

Spark needs memory to process data.

Imagine one worker has to process a huge amount of data, but its available memory is insufficient.

The job fails.

Common causes:
- Very large partitions.
- Skewed data.
- Join explosion.
- Large Sort or Aggregate operations.
- Broadcasting a large dataset.
- Too many concurrent workloads.
How to troubleshoot:
1. Identify the transformation where the failure happens.
2. Check whether a Join is multiplying records.
3. Check partition sizes and skew.
4. Check whether a large dataset is being broadcast.
5. Remove unnecessary columns and rows early.
6. Adjust partitioning if needed.
7. Increase compute or use memory-optimized compute if the workload genuinely requires it.
Important: More memory may help a legitimate large workload, but first investigate whether the data is unnecessarily large or incorrectly processed.
4. Timeout
Timeout means an operation did not complete within the allowed time.

But we must identify which timeout occurred.
Timeout type	Possible reason
Cluster startup timeout	Compute provisioning problem
Source timeout	Slow source or connection
Broadcast timeout	Broadcast dataset takes too long
Sink timeout	Destination is slow
Activity timeout	Overall activity exceeded its configured limit

For broadcast joins, Microsoft documents default timeouts of 60 seconds for debug runs and 300 seconds for job runs.

If the broadcast stream is too large, possible fixes include:
- Turn broadcast OFF.
- Broadcast the smaller stream instead.
- Use Auto when appropriate.
- Increase compute where justified.
Do not blindly increase timeout values to hide an inefficient Data Flow. 
Microsoft Learn+1

5. What Should I Change First?
This is one of the most important interview concepts.
Problem	First action
Join output unexpectedly increases	Check Join condition and duplicate keys
One partition is very slow	Investigate skew and hot keys
OOM	Inspect partition size, Join and broadcast
Broadcast timeout	Check broadcast stream size and configuration
Source is slow	Investigate source reading and connectivity
Sink is slow	Investigate destination and write behavior
Cluster starts slowly	Check startup time, IR and TTL

Golden debugging order:
1. Read the exact error message.
2. Check Data Flow monitoring and identify the slow or failed stage.
3. Check row counts before and after important transformations.
4. Check Join conditions, duplicate keys and data distribution.
5. Check partitioning, broadcast and memory usage.
6. Check source and sink connectivity/performance.
7. Increase compute or timeout only when the evidence justifies it.
8. Run again and compare performance and data correctness.

6. Scenario-Based Interview Questions and Simple Answers
These are the questions I would practise before an ADF Data Flow interview.

Q1. Your Mapping Data Flow takes 10 minutes to start. What will you do?

Answer: I will first check cluster startup time in monitoring. If the workload runs frequently, I will check whether a suitable TTL and reusable Integration Runtime configuration can reduce cold-start overhead.

Q2. Your Join output increases from 50,000 to 5 lakh records. What will you check?

Answer: I will check the Join condition and duplicate keys on both sides. I will verify the expected relationship before changing compute settings.

Q3. Your Data Flow works for small files but fails for large files. Why?

Answer: Large data may cause memory pressure, skew or longer processing time. I will inspect partition statistics, transformation timings and the Join/Aggregate operations before increasing compute.

Q4. One Spark partition takes much longer than the others. What could be the reason?

Answer: It may be data skew. I will inspect the distribution of keys and check whether a few keys contain too many records.

Q5. Your source team adds a new column every week. How will you handle it?

Answer: I can enable schema drift and use flexible column references or column patterns. I will still validate important business columns.

Q6. Your Data Flow fails with ColumnNotFound. What will you do?

Answer: I will inspect the source projection and verify the column names used in downstream expressions. I will refresh the projection if the source schema changed.

Q7. Your age column contains values like 20, 25 and Twenty. How will you handle it?

Answer: I will validate the values before converting them. Valid records will be converted into integers, while invalid records will be sent to a reject stream.

Q8. You see NULL customer IDs. Will you replace them with zero?

Answer: No. A missing customer ID is not the same as zero. I will check the business rule and send invalid records to a quarantine stream if the ID is mandatory.

Q9. Your Data Flow succeeds in Debug mode but fails in production. Why?

Answer: Debug mode may use a different compute configuration and sample data. I will compare debug and production runtime settings, permissions, source data size, parameters and sink configuration.

Q10. You need to load a CSV file into Parquet without complex transformations. What will you choose?

Answer: Copy Activity, because the primary requirement is data movement and format conversion.

Q11. You need to join three tables, filter invalid rows and calculate total sales. What will you choose?

Answer: Mapping Data Flow, because it provides visual transformations such as Join, Filter and Aggregate.

Q12. You need complicated custom PySpark logic. What will you choose?

Answer: A Spark Notebook, such as a Databricks Notebook, because it provides more control over custom Spark processing.

Q13. Your Data Flow takes 15 minutes, and monitoring shows the Join consumes 12 minutes. What will you do?

Answer: I will inspect the Join condition, duplicate keys, input sizes and partition distribution. I will optimize the Join before increasing the cluster.

Q14. Your pipeline writes to Synapse very slowly. What can you try?

Answer: I will investigate sink writing time and check whether PolyBase staging can be used for bulk loading.

Q15. Your pipeline output from a Cache sink fails because it is too large. What will you do?

Answer: Data Flow output passed directly into the pipeline is limited to 2 MB. I will avoid passing the full dataset through activity output and store the data in a proper destination instead. If only one result is required, I can consider First Row Only.

Q16. Your Data Flow needs to send valid and invalid customer records to two different destinations. What will you use?

Answer: I will use Conditional Split to separate the records and connect the outputs to separate sinks.

Q17. A customer changes their city. The business wants to retain the previous city. Which SCD type will you use?

Answer: SCD Type 2, because it creates a new record version and preserves historical information.

Q18. Three pipelines need exactly the same customer-cleaning logic. What will you use?

Answer: A Flowlet, because it allows us to reuse transformation logic instead of building it repeatedly.

Q19. A source preview fails, but the debug cluster is already running. What will you check?

Answer: I will check the linked service, credentials, permissions, firewall, source path and projection. Restarting the cluster is not my first step.

Q20. Your Data Flow has too many Sort transformations. Will you keep them before every Join?

Answer: No. Mapping Data Flow Join does not require the input streams to be sorted first. Unnecessary Sort operations can add processing overhead.

7. Important Revision Sheet
Concept	Remember this
Mapping Data Flow	Visual Spark-based transformation
Source	Reads incoming data
Transformation	Changes or processes data
Sink	Writes final output
Projection	Column and type blueprint
Schema drift	Handles changing source schemas
Debug mode	Interactive testing using a Spark debug cluster
Data Preview	Snapshot of data at a transformation
Select	Keep, remove, rename or reorder columns
Derived Column	Create or modify columns
Filter	Remove rows that do not match a condition
Join	Combine streams
Aggregate	Group and calculate
Window	Calculate over related rows
Pivot	Rows into columns
Unpivot	Columns into rows
Surrogate Key	Artificial incrementing identifier
Exists	Check whether a match exists
Lookup	Retrieve matching reference information
Conditional Split	Divide records based on conditions
Flowlet	Reusable transformation logic
SCD Type 1	Overwrite old value
SCD Type 2	Preserve historical versions
TTL	Controls how long an eligible cluster stays available for reuse
PolyBase	Bulk loading into Synapse
CDC Checkpoint	Remembers change-processing progress
Data Skew	Uneven distribution of data
OOM	Insufficient memory
Join Explosion	Unexpected multiplication of Join output

8. Important References and Learning Links
I have kept your original references and added the relevant official Microsoft documentation.

Official Microsoft documentation – primary references
1. Mapping Data Flow overview – Fundamentals, transformations, Debug mode and monitoring.
2. Execute Data Flow activity – Integration Runtime, compute, TTL, PolyBase, logging and sink settings.
3. Source transformation – Source settings and projection.
4. Mapping Data Flow Debug mode – Debug cluster and Data Preview.
5. Schema drift – Flexible schemas and drifted columns.
6. Transformation overview – Complete transformation list.
7. Monitoring Mapping Data Flows – Stage timing, row counts, partition statistics and lineage.
8. Mapping Data Flow performance and tuning – Performance tuning guide.
9. Troubleshoot Mapping Data Flows – Error messages and debugging.
10. Data Flow expression functions – Expression Builder functions.
11. Delimited text format – CSV delimiters, quotes, escapes and encoding.
12. Sink transformation – Sink mapping and Cache sink.
Your original learning references
- Datasets vs Inline Datasets in ADF
- Window, Pivot, Unpivot, Surrogate Key, Exists and Lookup transformations
- Conditional Split transformation
- Additional Data Flow learning video