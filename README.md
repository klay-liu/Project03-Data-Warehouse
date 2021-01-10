# PROJECT 03: Data Warehouse on AWS

# 1. Overview

The project "Data Warehouse on AWS" is to help Sparkify, a music stream startup, to process the data stored as JSON in AWS S3 buckets into Redshift Cluster. The main purpose is to provide the analytical data to answer the business questions like "what songs do the users listen to?". A ETL pipeline which includes the functionalities like creating tables in Redshift Cluster, copying JSON file from S3 to tables and inserting data into the tables under the star schema in Redshift is built.

# 2. Data
The data set in this project contains two parts with JSON format resided in S3:

**Song data**: s3://udacity-dend/song_data
The song dataset contains metadata about a song and the artist of that song. 
example data:
```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

**Log data**: s3://udacity-dend/log_data
The log dataset consists of log files in JSON format. It stores the app activity logs from an imaginary music streaming app based on configuration settings.
example data:
```
{"artist":null,"auth":"Logged In","firstName":"Walter","gender":"M","itemInSession":0,"lastName":"Frye","length":null,"level":"free","location":"San Francisco-Oakland-Hayward, CA","method":"GET","page":"Home","registration":1540919166796.0,"sessionId":38,"song":null,"status":200,"ts":1541105830796,"userAgent":"\\"Mozilla\\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\\/537.36 (KHTML, like Gecko) Chrome\\/36.0.1985.143 Safari\\/537.36\\"","userId":"39"}
```


# 3. Technologies
- Python3
- Python SDK(boto3) for AWS S3/Redshift
- Redshift SQL
- Jupyter notebook(Optional)

# 4. Database Design
The database design for Sparkify is based on the idea of the data warehouse processing and it has staging tables and analytics tables. The staging tables include staging_events and staging_songs which store the source data reside in S3 buckets. The analytics tables follow the star schema where the fact table songplays contains the business data that can answer the questions like "what songs do the user listen to?" and the dimension tables provide the corresponding data info. Below is the star schema illustration:

![Staging Tables](https://github.com/klay-liu/Project03-Data-Warehouse-On-AWS/blob/master/Staging%20Tables.jpeg)
![Star Schema Design for songplays](https://github.com/klay-liu/Project03-Data-Warehouse-On-AWS/blob/master/Star%20Schema%20Design%20for%20songplays.jpeg)


### Redshift Cluster configuration
- IAM User permission: Amazonadministrator
- Cluster: dc2.large, 2 nodes
- Region: US-West-2

### Staging tables

- **staging_events**: 
Fields: event_id, artist, auth, first_name, gender, item_session, last_name, length, level, location, method, page , registration, session_id, song, status, ts, user_agent, user_id
Table optimization: session_id as the **SORTKEY and DISTKEY**

- **staging_songs**: 
Fields: num_songs, artist_id, artist_latitude, artist_longitude, artist_location, artist_name, song_id, title, duration, year
Table optimization: artist_id as the **SORTKEY and DISTKEY**

### Fact Table

- **songplays**: 
Fields: songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
Table optimization: set the songplay_id as **SORTKEY** and set the user_id as **DISTKEY**

### Dimension Tables

- **users**: 
Fields: user_id, first_name, last_name, gender, level
Table optimization: set the user_id as **SORTKEY** and **distribution all**
- **songs**: 
Fields: song_id, title, artist_id, year, duration
Table optimization: set the song_id as **SORTKEY** and **distribution all**
- **artists**: 
Fields: artist_id, name, location, latitude, longitude
Table optimization: set the artist_id as **SORTKEY** and **distribution all**
- **time**: 
Fields: start_time, hour, day, week, month, year, weekday
Table optimization: set the start_time as **SORTKEY** and **distribution all**

# 5. The project files:

`create_table.py` is to create the fact and dimension tables for the star schema in Redshift.

`etl.py` is to load data from S3 into staging tables on Redshift and then process that data into the analytics tables on Redshift.

`sql_queries.py` to define the **DROP, CREATE, INSERT INTO** SQL statements, which will be imported into the two other files above.

`README.md`  - Description for the project

`dwh.cfg` - A configuration file containing the dependance parameters

`Create Data Warehouse in AWS Redshift.ipynb` - An option to substitute the functionalities of the `create_table.py` and `etl.py` as well as the AWS IAM Role

# 6. Data Process
- 0. Complete the params in dwh.cfg by launching a redshift cluster and creating an IAM role that has read access to S3.
- 1. Design schemas with 2 staging tables and 1 fact table and 4 dimension tables
- 2. Write a SQL DROP,CREATE, COPY, INSERT INTO statement for each of these tables in sql_queries.py
- 3. Write the connection script with psycopg2 package in create_tables.py to connect to the database and create these tables in Redshift Cluster.
- 4. Load data from S3 to staging tables and load data from staging tables to analytics tables on Redshift in etl.py.
- 5. Run the python script file in order to complete the data warehouse: sql_queries.py --> create_tables.py --> etl.py

# 7. Optional
The "Create Data Warehouse in AWS Redshift.ipynb" is an option to create AWS IAM, Redshift cluster and implement the data warehouse building for Sparkify.
