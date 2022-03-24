SELECT
    event_begin_time,
    magnitude,
    EXTRACT(MONTH FROM event_begin_time) as month
FROM
    `bigquery-public-data.noaa_historic_severe_storms.storms_*`
WHERE
    state LIKE 'Texas'
    AND cz_name LIKE 'TRAVIS'
    AND event_type LIKE 'hail'
    AND EXTRACT(MONTH FROM event_begin_time) = 3