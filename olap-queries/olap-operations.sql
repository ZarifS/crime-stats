-- Drill Down Query 1 - Number of types of crimes per city -> neighbourhood -> location
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

-- Drill Down Query 2 - Number of crimes per location(city -> neighbourhood -> location name) per date (year -> month -> day)
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

-- Roll Up Query 1 - Number of crimes per city per year
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

-- Roll Up Query 2 - Number of crimes that occurr on a holiday per year per city (includes holiday name as well)
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

-- Slice Query 1 - Number of crimes that occurr on March 2016
SELECT "Date_AND_Fact"."city" AS "city",
  SUM(1) AS "number_of_crimes"
FROM (
  select * from
  t_fact_table
  inner join t_date_dim
  on t_fact_table.date_key = t_date_dim.date_key
  inner join t_location_dim
  on t_fact_table.location_key = t_location_dim.location_key
) "Date_AND_Fact"
WHERE (("Date_AND_Fact"."month" = '3') AND ("Date_AND_Fact"."year" = '2016'))
GROUP BY 1

-- Slice Query 2 - Number of crimes that occurr per location
select l.neighborhood, l.city, d.year, SUM(1) AS "number_of_crimes" 
from t_fact_table as f
inner join t_date_dim as d
on f.date_key = d.date_key
inner join t_location_dim as l
on f.location_key = l.location_key
group by (l.neighborhood, l.city, d.year)

-- Dice Query 1 - Number of crimes per location (city -> neighbourhood -> locaiton name) per year in January, February and March
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

-- Dice Query 2: Number of fatal crimes that occured in the following Vancouver neighbourhoods
-- (Central Business District, Grandview-Woodland, Marpole, Mount Pleasant, West End)
-- during the winter months (Jan, Feb and Dec) each year.

SELECT "Location"."city" AS "city",
  "Location"."is_fatal" AS "is_fatal",
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
WHERE (("Location"."city" = 'Vancouver') AND "Location"."is_fatal" AND ("Location"."month" IN ('1', '12', '2')) AND ("Location"."neighborhood" IN ('Central Business District', 'Grandview-Woodland', 'Marpole', 'Mount Pleasant', 'West End')))
GROUP BY 1,
  2,
  3,
  4,
  6

-- Combined Operations

