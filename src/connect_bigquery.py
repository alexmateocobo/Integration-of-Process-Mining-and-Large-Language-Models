import os
from dotenv import load_dotenv
from google.cloud import bigquery

# Load environment variables from .env file
load_dotenv()

# Build the dictionary from environment variables (must match the service account JSON structure)
service_account_info = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN")
}

# Initialize BigQuery client using the credentials dictionary
client = bigquery.Client.from_service_account_info(service_account_info)

# List available datasets
print("Datasets in your project:")
datasets = list(client.list_datasets())
if datasets:
    for ds in datasets:
        print(f" - {ds.dataset_id}")
else:
    print("No datasets found.")