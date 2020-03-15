-- Drill Down (Emeka)

-- Number of types of crimes per city -> neighbourhood -> location
SELECT "Custom SQL Query"."city" AS "city",
  "Custom SQL Query"."crime_type" AS "crime_type",
  "Custom SQL Query"."location_name" AS "location_name",
  "Custom SQL Query"."neighborhood" AS "neighborhood",
  SUM(1) AS "sum:Number of Records:ok"
FROM (
  select * from
    t_fact_table
    inner join t_location_dim
    on t_fact_table.location_key = t_location_dim.location_key
    inner join t_crime_dim
    on t_fact_table.crime_key = t_crime_dim.crime_key
) "Custom SQL Query"
GROUP BY 1,
  2,
  3,
  4;

-- Number of crimes per location(city -> neighbourhood -> location name) per date (year -> month -> day)

SELECT "Location"."city" AS "city",
  "Location"."day" AS "day",
  "Location"."location_name" AS "location_name",
  "Location"."month" AS "month",
  "Location"."neighborhood" AS "neighborhood",
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
  2,
  3,
  4,
  5,
  7;

-- Roll Up (Emeka)

/*
Number of crimes per city per year
*/

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
  3;


-- Slice (Zarif)



-- Dice (Zarif)

-- Combined Operations (Zaid)

