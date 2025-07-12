import logging
from bigquery_utils import BigQueryUtils
from process_mining_utils import ProcessMiningUtils
from langchain_utils import LangChainUtils

if __name__ == "__main__":
    
    # Configure logging globally
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Step 1: Authenticate and load data from BigQuery
    loader = BigQueryUtils()
    loader.authenticate()

    query = """
        SELECT e.*
        FROM `integration-of-pm-and-llms.integration_of_pm_and_llms.filtered_eventlog` e
        INNER JOIN `physionet-data.mimiciii_clinical.icustays` icu
        ON e.icustay_id = icu.icustay_id
        WHERE e.icustay_id IN (211555, 290738, 236225, 213113)
        AND e.linksto = 'datetimeevents'
    """

    df = loader.run_query(query)

    # Step 2: Run the process mining pipeline
    context_dir = "/Users/alejandromateocobo/Documents/PythonProjects/Integration_Of_LLMs_And_Process_Mining/data/context/"
    pipeline = ProcessMiningUtils(df, output_dir=context_dir)
    pipeline.preprocess_dataframe()
    pipeline.discover_dfg()
    # pipeline.view_dfg()
    pipeline.abstract_dfg_to_text()
    pipeline.discover_petri_net()
    # pipeline.view_petri_net()
    pipeline.abstract_petri_net_to_text()

    # Step 3: Embed textual summaries and run a LangChain query
    lc_utils = LangChainUtils(context_dir=context_dir)
    lc_utils.load_and_embed_documents()

    query = "What is the most common workflow for patients in the ICU?"
    answer = lc_utils.query_context(query)
    
    print("\n--- Answer from LLM ---\n")
    print(answer)