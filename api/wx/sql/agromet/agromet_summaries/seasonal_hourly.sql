WITH agg_definitions AS (
    SELECT *
    FROM (VALUES
        ('JFM', ARRAY[1, 2, 3]),
        ('FMA', ARRAY[2, 3, 4]),
        ('MAM', ARRAY[3, 4, 5]),
        ('AMJ', ARRAY[4, 5, 6]),
        ('MJJ', ARRAY[5, 6, 7]),
        ('JJA', ARRAY[6, 7, 8]),
        ('JAS', ARRAY[7, 8, 9]),
        ('ASO', ARRAY[8, 9, 10]),
        ('SON', ARRAY[9, 10, 11]),
        ('OND', ARRAY[10, 11, 12]),
        ('NDJ', ARRAY[11, 12, 13]),
        ('DRY', ARRAY[0, 1, 2, 3, 4, 5]),
        ('WET', ARRAY[6, 7, 8, 9, 10, 11]),
        ('ANNUAL', ARRAY[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]),
        ('DJFM', ARRAY[0, 1, 2, 3])
    ) AS t(agg, months)
)
,filtered_data AS (
    SELECT
        hs.station_id 
        ,hs.variable_id
        ,DATE(hs.datetime) AS day
        ,EXTRACT(MONTH FROM hs.datetime AT TIME ZONE '{{timezone}}') AS month
        ,EXTRACT(YEAR FROM hs.datetime AT TIME ZONE '{{timezone}}') AS year
        ,so.symbol AS sampling_operation
        ,CASE so.symbol
            WHEN 'MIN' THEN hs.min_value
            WHEN 'MAX' THEN hs.max_value
            WHEN 'ACCUM' THEN hs.sum_value
            ELSE hs.avg_value
        END AS value
    FROM hourly_summary hs
    JOIN wx_variable vr ON vr.id = hs.variable_id
    JOIN wx_samplingoperation so ON so.id = vr.sampling_operation_id           
    WHERE hs.station_id = {{station_id}}
      AND hs.variable_id IN ({{variable_ids}})
      AND hs.datetime AT TIME ZONE '{{timezone}}' >= '{{ start_date }}' 
      AND hs.datetime AT TIME ZONE '{{timezone}}' < '{{ end_date }}'
),
extended_data AS(
    SELECT
        station_id
        ,variable_id
        ,day
        ,CASE 
            WHEN month=12 THEN 0
            WHEN month=1 THEN 13
        END as month    
        ,CASE 
            WHEN month=12 THEN year+1
            WHEN month=1 THEN year-1
        END as year
        ,sampling_operation
        ,value       
    FROM filtered_data
    WHERE month in (1,12)
    UNION ALL
    SELECT
        *
    FROM filtered_data
)
,agg_data AS (
    SELECT
        ed.*
        ,ad.agg
    FROM extended_data ed
    CROSS JOIN agg_definitions ad
    WHERE ed.month = ANY(ad.months)
      AND year BETWEEN {{start_year}} AND {{end_year}} 
)
,lagged_data AS (
    SELECT
        *
        ,DATE_PART('day', day::timestamp - LAG(day::timestamp) 
            OVER (PARTITION BY station_id, variable_id, year, agg ORDER BY day)) AS day_diff
    FROM (
        SELECT DISTINCT day, station_id, variable_id, year, agg
        FROM agg_data
    ) AS distinct_entries
)
,validated_data AS (
    SELECT
        st.name AS station
        ,ad.variable_id
        ,ad.year
        ,ad.agg
        ,MAX(ld.day_diff) AS max_day_diff
        ,ROUND(
            CASE ad.sampling_operation
                WHEN 'MIN' THEN MIN(value)::numeric
                WHEN 'MAX' THEN MAX(value)::numeric
                WHEN 'ACCUM' THEN SUM(value)::numeric
                WHEN 'STDV' THEN STDDEV(value)::numeric
                WHEN 'RMS' THEN SQRT(AVG(POW(value, 2)))::numeric
                ELSE AVG(value)::numeric
            END,2
        ) AS value
    FROM agg_data ad
    JOIN wx_station st ON st.id = ad.station_id
    LEFT JOIN lagged_data ld 
      ON (ld.station_id=ad.station_id AND ld.variable_id=ad.variable_id AND ld.day=ad.day AND ld.agg=ad.agg)
    GROUP BY st.name, ad.variable_id, ad.year, ad.agg, ad.sampling_operation 
)
SELECT
    station
    ,variable_id
    ,year
    ,agg
    ,value
FROM validated_data
WHERE max_day_diff < 6
ORDER BY year;