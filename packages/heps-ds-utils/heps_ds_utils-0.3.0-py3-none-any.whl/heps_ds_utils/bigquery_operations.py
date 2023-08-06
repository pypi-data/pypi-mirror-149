""" This Module is created to enable Hepsiburada Data Science to communicate with BigQuery. """

import os
import time

from colorama import Fore, init ##Style
from google.cloud import bigquery
from google.oauth2 import service_account

### CREATE DATASET
### CREATE TABLE
### STREAM INSERT INTO TABLE
### DELETE TABLE
### DELETE DATASET

init(autoreset=True)

class BigQueryOperations(bigquery.Client):
    """ This class is created to enable Hepsiburada Data Science to communicate with BigQuery """
    _implemented_returns = ['dataframe']

    def __init__(self, **kwargs) -> None:
        self.gcp_key = kwargs.get('gcp_key_path')
        self.credentials = None
        super().__init__(project=self.credentials.project_id, credentials=self.credentials)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(Project ID: {self.credentials.project_id}, " \
                f"Service Account: {self.credentials._service_account_email.split('@')[0]})"

    def get_bq_table(self, table_name):
        """This function is to get BQ table. """
        return self.get_table(table_name)

    def execute_query(self, query_string, return_type='dataframe', **kwargs):
        """This function is to query BQ. """
        if return_type not in BigQueryOperations._implemented_returns:
            raise NotImplementedError(Fore.RED + f'Return type {return_type} not implemented !!')

        execution_start = time.time()
        query_result = self.query(query_string, **kwargs).result()
        execution_duration = time.time() - execution_start
        print(Fore.YELLOW + f'Query executed in {execution_duration:.2f} seconds !')

        if return_type == 'dataframe':
            return query_result.to_dataframe(progress_bar_type='tqdm')

        return self.query(query_string)

    def create_new_dataset(self, dataset_name):
        """This function is to create dataset. """
        _ = self.create_dataset(dataset_name)

    def delete_existing_dataset(self, dataset_name):
        """This function is to delete dataset. 
        Note: This function will not delete the dataset if there are tables in it. """
        self.delete_dataset(dataset_name)

    def delete_existing_table(self, dataset, table):
        """This function is to delete table. """
        self.delete_table(f'{self.project}.{dataset}.{table}')

    def create_new_table(self, dataset, table_name, schema, **kwargs):
        """This function is to create table. """
        provided_schema = [bigquery.SchemaField(field['field_name'], field['field_type'], field['field_mode']) for field in schema]

        table_reference = bigquery.Table(f'{self.project}.{dataset}.{table_name}',
                                                    schema=provided_schema)
        self.create_table(table_reference, provided_schema, **kwargs)

    def load_data_to_table(self, dataset, table_name, data_frame, **kwargs):
        """This function is to create a table and load data from dataframe into it."""
        if dataset in [dataset.dataset_id for dataset in self.list_datasets()]:
            job = self.load_table_from_dataframe(data_frame, f'{self.project}.{dataset}.{table_name}', **kwargs)
            job.result()
        else:
            raise ValueError(Fore.RED + f'Dataset {dataset} does not exist !')

    def insert_rows_into_existing_table(self, dataset, table, data):
        """This function is to insert rows into existing table. """
        table_reference = self.get_bq_table(f'{self.project}.{dataset}.{table}')
        self.insert_rows_from_dataframe(table_reference, data)

    @property
    def gcp_key(self):
        """This function is to get GCP key. """
        return self._gcp_key

    @gcp_key.setter
    def gcp_key(self, provided_gcp_key):
        """This function is to set GCP key. """
        if provided_gcp_key is not None:
            self._gcp_key = str(provided_gcp_key)
            self.credentials = None
        elif os.environ.get("SERVICE_ACCOUNT_KEY_PATH"):
            self._gcp_key = os.environ.get("SERVICE_ACCOUNT_KEY_PATH")
        else:
            self._gcp_key = None
            print(Fore.RED + "Warning!! GCP Key Path for Service Account is not specified")

    @property
    def credentials(self):
        """This function is to get credentials. """
        return self._credentials

    @credentials.setter
    def credentials(self, provided_credentials):
        """This function is to set credentials. """
        if provided_credentials is not None:
            self._credentials = service_account.Credentials.from_service_account_file(
                self.gcp_key, 
                            scopes=["https://www.googleapis.com/auth/cloud-platform"],)
        elif os.environ.get("SERVICE_ACCOUNT_KEY_PATH"):
            self._credentials = service_account.Credentials.from_service_account_file(
                self.gcp_key, 
                            scopes=["https://www.googleapis.com/auth/cloud-platform"],)
        else:
            self._credentials = None
            print(Fore.RED + "Warning!! Credentials for Service Account is not specified")
