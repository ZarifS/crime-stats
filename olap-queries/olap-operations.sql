-- Drill Down (Emeka)
SELECT "Location"."city" AS "city",
  SUM(1) AS "sum:Number of Records:ok",
  "Location"."year" AS "year"
FROM (
  select * from
  t_fact_table
  inner join t_location_dim
  on t_fact_table.location_key = t_location_dim.location_key
  inner join t_date_dim
  on t_fact_table.date_key = t_date_dim.date_key
) "Location"
GROUP BY 1,
  3
-- Roll Up (Emeka)

-- Slice (Zarif)

-- Dice (Zarif)

-- Combined Operations (Zaid)

