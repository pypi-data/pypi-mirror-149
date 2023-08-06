# Hepsiburada Data Science Utilities

This module includes utilities for Hepsiburada Data Science Team.

- Library is available via PyPi. 
- Library can be downloaded using pip as follows: `pip install heps-ds-utils`
- Existing library can be upgraded using pip as follows: `pip install heps-ds-utils --upgrade`

***
## Available Modules

1. Hive Operations

```python
from heps_ds_utils import HiveOperations

# A connection is needed to be generated in a specific runtime.
# There are 3 ways to set credentials for connection.

# 1) Instance try to set default credentials from Environment Variables.
hive_ds = HiveOperations()
hive_ds.connect_to_hive()

# 2) One can pass credentials to instance initiation to override default.
hive_ds = HiveOperations(HIVE_HOST="XXX", HIVE_PORT="YYY", HIVE_USER="ZZZ", HIVE_PASS="WWW", HADOOP_EDGE_HOST="QQQ")
hive_ds.connect_to_hive()

# 3) One can change any of the credentials after initiation using appropriate attribute.
hive_ds = HiveOperations()
hive_ds.hive_username = 'XXX'
hive_ds.connect_to_hive()

# Execute an SQL query to retrieve data.
# Currently Implemented Types: DataFrame, Numpy Array, Dictionary, List.
SQL_QUERY = "SELECT * FROM {db}.{table}"
data, columns = hive_ds.execute_query(SQL_QUERY, return_type="dataframe", return_columns=False)

# Execute an SQL query to create and insert data into table.
SQL_QUERY = "INSERT INTO .."
hive_ds.create_insert_table(SQL_QUERY)

# Send Files to Hive and Create a Table with the Data.
# Currently DataFrame or Numpy Array can be sent to Hive.
# While sending Numpy Array columns have to be provided.
SQL_QUERY = "INSERT INTO .."
hive_ds.send_files_to_hive("{db}.{table}", data, columns=None)

# Close the connection at the end of the runtime.

hive_ds.disconnect_from_hive()

```

2. BigQuery Operations

```python
from heps_ds_utils import BigQueryOperations

# A connection is needed to be generated in a specific runtime.
# There are 3 ways to set credentials for connection.

# 1) Instance try to set default credentials from Environment Variables.
bq_ds = BigQueryOperations()

# 2) One can pass credentials to instance initiation to override default.
bq_ds = BigQueryOperations(gcp_key="/tmp/keys/ds_qos.json")

# Unlike HiveOperations, initiation creates a direct connection. Absence of
# credentials will throw an error.

# Execute an SQL query to retrieve data.
# Currently Implemented Types: DataFrame.
QUERY_STRING = """SELECT * FROM `hb-datalake-prod.production.hpcategory` LIMIT 20"""
data = bq_ds.execute_query(QUERY_STRING, return_type='dataframe')

# Create a Dataset in BigQuery.
bq_ds.create_new_dataset("example_dataset")

# Create a Table under a Dataset in BigQuery.
schema = [
    {"field_name": "id", "field_type": "INTEGER", "field_mode": "REQUIRED"},
    {"field_name": "first_name", "field_type": "STRING", "field_mode": "REQUIRED"},
    {"field_name": "last_name", "field_type": "STRING", "field_mode": "REQUIRED"},
    {"field_name": "email", "field_type": "STRING", "field_mode": "REQUIRED"},
    {"field_name": "gender", "field_type": "STRING", "field_mode": "REQUIRED"},
    {"field_name": "ip_address", "field_type": "STRING", "field_mode": "REQUIRED"}]

bq_ds.create_new_table(dataset='example_dataset', table_name='mock_data', schema=schema)

# Insert into an existing Table from Dataframe.
# There is a Bug in Inserting !!
bq_ds.insert_rows_into_existing_table(dataset='example_dataset', table='mock_data', data=df)

# Delete a Table.
bq_ds.delete_existing_table('example_dataset', 'mock_data')

# Delete a Dataset.
# Trying to delete a dataset consisting of tables will throw an error.
bq_ds.delete_existing_dataset('example_dataset')

# Load Dataframe As a Table. BigQuery will infer the data types.s
bq_ds.load_data_to_table('example_dataset', 'mock_data', df)

```