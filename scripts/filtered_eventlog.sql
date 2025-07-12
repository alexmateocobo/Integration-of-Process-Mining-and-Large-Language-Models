-- Prepare chartevents
WITH chartevents_prepared AS (
    SELECT
        ce.itemid,
        ce.subject_id,
        ce.hadm_id,
        ce.icustay_id,
        ce.charttime AS event_timestamp,
        di.label,
        di.category,
        di.linksto
    FROM
        `physionet-data.mimiciii_clinical.chartevents` ce
    LEFT JOIN
        `physionet-data.mimiciii_clinical.d_items` di
    ON
        ce.itemid = di.itemid
),

-- Prepare datetimeevents
datetimeevents_prepared AS (
    SELECT
        de.itemid,
        de.subject_id,
        de.hadm_id,
        de.icustay_id,
        de.value AS event_timestamp,
        di.label,
        di.category,
        di.linksto
    FROM
        `physionet-data.mimiciii_clinical.datetimeevents` de
    LEFT JOIN
        `physionet-data.mimiciii_clinical.d_items` di
    ON
        de.itemid = di.itemid
),

-- Prepare inputevents_mv
inputevents_prepared AS (
    SELECT
        ie.itemid,
        ie.subject_id,
        ie.hadm_id,
        ie.icustay_id,
        ie.starttime AS event_timestamp,
        di.label,
        di.category,
        di.linksto
    FROM
        `physionet-data.mimiciii_clinical.inputevents_mv` ie
    LEFT JOIN
        `physionet-data.mimiciii_clinical.d_items` di
    ON
        ie.itemid = di.itemid
),

-- Prepare outputevents
outputevents_prepared AS (
    SELECT
        oe.itemid,
        oe.subject_id,
        oe.hadm_id,
        oe.icustay_id,
        oe.charttime AS event_timestamp,
        di.label,
        di.category,
        di.linksto
    FROM
        `physionet-data.mimiciii_clinical.outputevents` oe
    LEFT JOIN
        `physionet-data.mimiciii_clinical.d_items` di
    ON
        oe.itemid = di.itemid
),

-- Prepare procedureevents_mv
procedureevents_prepared AS (
    SELECT
        pe.itemid,
        pe.subject_id,
        pe.hadm_id,
        pe.icustay_id,
        pe.starttime AS event_timestamp,
        di.label,
        di.category,
        di.linksto
    FROM
        `physionet-data.mimiciii_clinical.procedureevents_mv` pe
    LEFT JOIN
        `physionet-data.mimiciii_clinical.d_items` di
    ON
        pe.itemid = di.itemid
),

-- Unified event log (removed microbio_spec, microbio_org, microbio_ab, labevents)
eventlog AS (
    SELECT * FROM chartevents_prepared
    UNION ALL
    SELECT * FROM datetimeevents_prepared
    UNION ALL
    SELECT * FROM inputevents_prepared
    UNION ALL
    SELECT * FROM outputevents_prepared
    UNION ALL
    SELECT * FROM procedureevents_prepared
),

-- Apply category mapping
eventlog_with_mapped_category AS (
    SELECT
        e.itemid,
        e.subject_id,
        e.hadm_id,
        e.icustay_id,
        e.event_timestamp,
        e.label,
        COALESCE(cm.standardized_category, e.category) AS category,
        e.linksto
    FROM
        eventlog e
    LEFT JOIN
        `integration-of-pm-and-llms.integration_of_pm_and_llms.category_mapping` cm
    ON
        e.category = cm.original_category
)

-- Final output: filter out events without labels
SELECT *
FROM eventlog_with_mapped_category
WHERE label IS NOT NULL
AND event_timestamp IS NOT NULL
AND icustay_id IS NOT NULL