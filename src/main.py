from bigquery_loader import BigQueryEventLogLoader
from process_mining_pipeline import ProcessMiningPipeline

if __name__ == "__main__":
    loader = BigQueryEventLogLoader()
    loader.authenticate()

    # Query MIMIC-III Clinical Dataset with admission filters
    query = """
        SELECT e.*
        FROM `integration-of-pm-and-llms.integration_of_pm_and_llms.filtered_eventlog` e
        INNER JOIN `physionet-data.mimiciii_clinical.admissions` adm
        ON e.subject_id = adm.subject_id AND e.hadm_id = adm.hadm_id
        WHERE adm.admittime BETWEEN '2100-01-01' AND '2100-12-31'
        AND adm.admission_type IN ('EMERGENCY', 'URGENT')
        AND e.subject_id = 72091
    """

    df = loader.run_query(query)

    process_miner = ProcessMiningPipeline(df)
    process_miner.convert_to_event_log()
    process_miner.discover_dfg()