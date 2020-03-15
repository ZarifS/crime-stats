-- Drill Down (Emeka)

-- Roll Up (Emeka)

-- Slice (Zarif)

-- Dice (Zarif)

-- Combined Operations (Zaid)

SELECT "Custom SQL Query"."neighborhood" AS "neighborhood",
  SUM("Custom SQL Query"."count") AS "sum:count:ok"
FROM (
  SELECT I.neighborhood, count(*)
  FROM t_location_dim as I
  INNER JOIN t_fact_table as a
  ON I.location_key = a.location_key
  GROUP BY neighborhood
) "Custom SQL Query"
GROUP BY 1