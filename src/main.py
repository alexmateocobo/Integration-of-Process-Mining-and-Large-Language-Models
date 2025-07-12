
from bigquery_event_loader import BigQueryEventLogLoader
from process_mining_pipeline import ProcessMiningPipeline

if __name__ == "__main__":
    # Step 1: Authenticate and load data from BigQuery
    loader = BigQueryEventLogLoader()
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

    # Step 2: Run the simplified inductive miner pipeline
    pipeline = ProcessMiningPipeline(df)
    pipeline.preprocess_dataframe()
    pipeline.discover_dfg()
    pipeline.view_dfg()
    pipeline.discover_petri_net()
    pipeline.view_dfg()