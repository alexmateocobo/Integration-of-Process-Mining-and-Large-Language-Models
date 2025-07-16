SELECT
  ROW_ID,
  SUBJECT_ID,
  HADM_ID,
  CHARTTIME,
  CHARTDATE,
  CATEGORY,
  DESCRIPTION,
  ISERROR,
  TEXT
FROM
  `physionet-data.mimiciii_notes.noteevents`
WHERE
  -- Retain only relevant categories
  CATEGORY IN ('Discharge summary', 'Echo', 'Radiology')
  -- Exclude notes with ISERROR = '0' (i.e., keep only if error is NOT flagged)
  AND ISERROR IS NULL
  -- Exclude notes without a hospital admission ID
  AND HADM_ID IS NOT NULL
  -- For 'Discharge summary', include only 'Report' descriptions
  AND (
    CATEGORY != 'Discharge summary'
    OR (CATEGORY = 'Discharge summary' AND DESCRIPTION = 'Report')
  )
  -- Filter notes within the specified chartdate window
  AND CHARTDATE BETWEEN '2100-01-01' AND '2100-12-31';