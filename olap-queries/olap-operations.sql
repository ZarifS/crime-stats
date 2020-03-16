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

/*
Number of crimes that occurr on a holiday per year per city (includes holiday name as well)
*/

SELECT
  "Date_AND_Fact"."american_holiday_name" AS "american_holiday_name",
  "Date_AND_Fact"."canadian_holiday_name" AS "canadian_holiday_name",
  "Date_AND_Fact"."city" AS "city",
  SUM(1) AS "number_of_crimes",
  "Date_AND_Fact"."year" AS "year"
FROM (
  select * from
  t_fact_table
  inner join t_date_dim
  on t_fact_table.date_key = t_date_dim.date_key
  inner join t_location_dim
  on t_fact_table.location_key = t_location_dim.location_key
) "Date_AND_Fact"
WHERE "Date_AND_Fact"."is_american_holiday"
GROUP BY 1,
  2,
  3,
  5;




-- Slice (Zarif)



-- Dice (Zarif)

/*
Number of crimes per location (city -> neighbourhood -> locaiton name) per year
in January, February and March
*/

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
WHERE ("Location"."month" IN ('1', '2', '3'))
GROUP BY 1,
  2,
  3,
  4,
  5,
  7

-- Combined Operations (Zaid)

