import logging
from google.cloud import bigquery
from google_auth_oauthlib.flow import InstalledAppFlow

class BigQueryUtils:
    def __init__(self):
        # Configuration
        self.project_id = "integration-of-pm-and-llms"
        self.client_secret_path = "/Users/alejandromateocobo/Documents/PythonProjects/Integration_Of_LLMs_And_Process_Mining/keys/client_secret_316641064865-57id3o26obibotvs226jeevisjdujha5.apps.googleusercontent.com.json"
        self.client = None
        self.credentials = None

    def authenticate(self):
        logging.info("Starting OAuth authentication...")

        SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

        flow = InstalledAppFlow.from_client_secrets_file(
            self.client_secret_path,
            scopes=SCOPES
        )

        self.credentials = flow.run_local_server(port=0)
        self.client = bigquery.Client(credentials=self.credentials, project=self.project_id)

        logging.info("Authentication successful.")
        logging.info("BigQuery client initialized.")

    def run_query(self, query):
        if not self.client:
            raise Exception("BigQuery client not initialized. Run authenticate() first.")

        logging.info("Running user-provided query...")
        job = self.client.query(query)

        logging.info("Waiting for query to complete...")
        df = job.to_dataframe(progress_bar_type='tqdm')

        logging.info(f"Query completed. Retrieved {len(df)} rows.")

        return df