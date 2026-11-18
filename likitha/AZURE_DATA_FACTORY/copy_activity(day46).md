# Copy Activity – Files and Databases

### 1. Configuring Source and Sink

- **Source** means where we are reading the data from.
- **Sink** means where we are writing the data to.
- In Copy Activity, we configure both the source and sink datasets.
- Source can be a file, database table or query.
- Sink can also be a file or database table.
- **Mapping** is used to connect source columns with sink columns.
- If source and sink column names are different, we can manually map them.
- Data types should be compatible between source and sink. Otherwise, the copy may fail.

### 2. File Formats

ADF supports different file formats. Common ones are:

**CSV**
- Stores data in rows and columns.
- Values are separated by a delimiter, usually a comma.
- Important settings:
  - Column delimiter
  - First row as header
  - Encoding (usually UTF-8)
  - Quote character

**JSON**
- Stores data in key-value format.
- Can contain nested objects and arrays.
- ADF supports JSON files, but nested data may need additional transformations.

**Parquet**
- A column-based file format.
- Commonly used in data engineering and analytics.
- Stores schema information and supports compression.
- Useful when working with large datasets.

### 3. Copy Behaviour

These settings control how files are copied from source to destination.

- **Wildcard path:** Used to select multiple files using patterns.
  - `*.csv` – selects all CSV files.
  - `employee*.csv` – selects CSV files starting with employee.
- **Recursive:** Searches for files inside subfolders also.
- **Preserve hierarchy:** Maintains the original folder structure in the destination.
- **Flatten hierarchy:** Copies files into a single destination folder.
- **Merge files:** Combines multiple source files into one output file.

### 4. Checking Copy Activity Results

After running a pipeline, go to:

Monitor → Pipeline runs → Select pipeline → Select Copy Activity.

Important details:

- **Rows read:** Number of rows read from the source.
- **Rows copied:** Number of rows successfully written to the sink.
- **Rows skipped:** Number of rows skipped during copying.
- **Data read:** Amount of data read from the source.
- **Data written:** Amount of data written to the sink.
- **Duration:** Total time taken by the activity.
- **Throughput:** Speed at which data is copied.

These details help us understand whether the copy completed properly and how fast it ran.

### 5. Common Copy Activity Errors

- **No files found:** Check the folder path, file name and wildcard pattern.
- **Schema mismatch:** Check whether source and sink columns match.
- **Data type error:** Check whether the source values can fit into the sink data types.
- **Wrong delimiter:** Check the CSV delimiter. For example, comma and pipe (`|`) are different.
- **Permission denied:** Check whether the linked service has permission to read the source or write to the sink.
- **Timeout:** The source or sink may be slow, or the network may be taking too long.

### 6. Improving Slow Copy Activity

If Copy Activity is slow, first check its execution details in Monitor.

Important settings:

- **Parallel Copies:** Allows multiple copy operations to run at the same time.
- **DIU (Data Integration Units):** Provides compute power for Copy Activity when using Azure Integration Runtime.
- **Partitioning:** Divides source data into smaller parts so they can be read in parallel.

Important points:
- First identify whether the source, sink or network is causing the delay.
- Increase parallel copies only when the source and sink can handle more load.
- Increase DIU when Azure Integration Runtime compute capacity is the bottleneck.
- Change one setting at a time and compare the execution time.

**Quick Revision:**
- Source = Where data comes from.
- Sink = Where data goes.
- Mapping = Connecting source and sink columns.
- Wildcard = Selecting multiple files using a pattern.
- Preserve hierarchy = Keep folder structure.
- Flatten hierarchy = Put files in one folder.
- Merge files = Combine multiple files into one.
- Parallel copies = Run multiple copies at the same time.
- DIU = Compute power for Copy Activity.