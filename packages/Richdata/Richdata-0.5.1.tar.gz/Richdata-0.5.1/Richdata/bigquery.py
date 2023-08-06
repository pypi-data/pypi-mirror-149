from google.cloud import bigquery
from google.oauth2 import service_account
import os
from abc import ABC, abstractmethod

class Bigquery():
    authentication_strategy = None  # { GOOGLE_ENVIROMENT, JSON_PATH, ENVIROMENT_VAR}
    # GOOGLE_ENVIROMENT: If your application runs inside a Google Cloud environment, your application should use the service account provided by the environment.
    # ENVIROMENT_VAR: Google Cloud Client Libraries will automatically find and use the service account credentials by using the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # JSON_PATH: Google Cloud Client Libraries will find in local file path
    client_bigquery = None
    filepath = None
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    project_id = None

    def __init__(self, authentication_strategy='GOOGLE_ENVIROMENT'):
        self.authentication_strategy = 'GOOGLE_ENVIROMENT'
        self.client_bigquery = self.getClient()

    def getClient(self):
        if self.authentication_strategy == 'GOOGLE_ENVIROMENT':
            self.client_bigquery = bigquery.Client()
        elif self.authentication_strategy == 'JSON_PATH':
            credentials = service_account.Credentials.from_service_account_file(self.filepath, scopes=self.scopes)
            self.client_bigquery = bigquery.Client(credentials=credentials, project=credentials.project_id, )
        elif self.authentication_strategy == 'ENVIROMENT_VAR' and os.environ["GOOGLE_APPLICATION_CREDENTIALS"]:
            credentials = service_account.Credentials.from_service_account_file(self.filepath, scopes=self.scopes)
            self.client_bigquery = bigquery.Client(credentials=credentials, project=credentials.project_id, )
        elif self.authentication_strategy == 'ENVIROMENT_VAR' and not os.environ["GOOGLE_APPLICATION_CREDENTIALS"]:
            raise Exception("set enviroment variable GOOGLE_APPLICATION_CREDENTIALS")
        else:
            raise Exception("authentication_strategy only support  { GOOGLE_ENVIROMENT, JSON_PATH, ENVIROMENT_VAR} ")
        return self.client_bigquery

    def fetchOne(self, sql):
        return next(self.client_bigquery.query(sql).result())[0]

    def fetchAll(self, sql):
        return self.client_bigquery.query(sql).result().to_dataframe()

    def fetchCol(self, sql):
        df = self.fetchAll(sql)
        return df.iloc[:, 0].tolist()

    def execute(self, query):
        client = self.getClient()
        job_config = bigquery.QueryJobConfig(use_legacy_sql=False)
        query_job = client.query(query, job_config=job_config)  # API request
        return query_job.result()  # Waits for statement to finish

    def table_exists(self, table_name, schema,project_id=None):
        if project_id is None:
            project_id = self.project_id
        table_id = f'{project_id}.{schema}.{table_name}'
        return self.client_bigquery.get_table(table_id)


    def load_table_from_dataframe(self,dataframe,table_id,write_disposition="WRITE_EMPTY"):
        """

            WRITE_APPEND    If the table already exists, BigQuery appends the data to the table.
            WRITE_EMPTY     If the table already exists and contains data, a ‘duplicate’ error is returned in the job result.
            WRITE_TRUNCATE  If the table already exists, BigQuery overwrites the table data.

        :param dataframe: dataframe name
        :param table_id:  table name (full path)
        :param write_disposition: WRITE_APPEND, WRITE_EMPTY or WRITE_TRUNCATE
        :return:
        """
        client = self.getClient()
        job_config = bigquery.LoadJobConfig(write_disposition=write_disposition)

        #log.info("Make an Bigquery API request.")
        job = client.load_table_from_dataframe(dataframe, table_id, job_config=job_config)

        #log.info("Wait for the Bigquery job to complete...")
        job.result()

        table = client.get_table(table_id)  # Make an API request.
        #log.info("Loaded {} rows and {} columns to {}".format(table.num_rows, len(table.schema), table_id))
        return table

