-- Iceberg Query 1 - Top 5 places in Denver where offences against people occured (most violent areas).
SELECT c.crime_type, l.neighborhood, count(*) as total 
FROM t_location_dim as l INNER JOIN t_fact_table as f
ON l.location_key = f.location_key INNER JOIN t_crime_dim as c ON c.crime_key = f.crime_key 
WHERE l.city = 'Denver' AND c.crime_type = 'Offence Against a Person' 
GROUP BY c.crime_type, l.neighborhood 
ORDER BY total DESC
LIMIT 5;

-- Iceberg Query 2 - Top 5 places in Vancouver where theft occured.
SELECT c.crime_type, l.neighborhood, count(*) as total 
FROM t_location_dim as l INNER JOIN t_fact_table as f
ON l.location_key = f.location_key INNER JOIN t_crime_dim as c ON c.crime_key = f.crime_key 
WHERE l.city = 'Vancouver' AND c.crime_type = 'Theft' 
GROUP BY c.crime_type, l.neighborhood 
ORDER BY total DESC
LIMIT 5;

-- Iceberg Query 3 - Top 5 safest places in Denver (least violent).
SELECT c.crime_type, l.neighborhood, count(*) as total 
FROM t_location_dim as l INNER JOIN t_fact_table as f
ON l.location_key = f.location_key INNER JOIN t_crime_dim as c ON c.crime_key = f.crime_key 
WHERE l.city = 'Denver' AND c.crime_type = 'Offence Against a Person' 
GROUP BY c.crime_type, l.neighborhood 
ORDER BY total ASC
LIMIT 5;

-- Windowing (Zarif)
--window query #1 - avg. # of occurrences per month for each crime_type for each neighbourhood

SELECT CAST (SUM(1) AS FLOAT)/30 AS "avg_ocurrence_per_month",
  "Location"."city" AS "city",
  "Location"."crime_type" AS "crime_type",
  "Location"."month" AS "month",
  "Location"."neighborhood" AS "neighborhood",
  "Location"."year" AS "year"
FROM (
  select * from
  t_fact_table
  inner join t_location_dim
  on t_fact_table.location_key = t_location_dim.location_key
  inner join t_date_dim
  on t_fact_table.date_key = t_date_dim.date_key
  inner join t_crime_dim
  on t_fact_table.crime_key = t_crime_dim.crime_key
  inner join t_event_dim
  on t_fact_table.event_key = t_event_dim.event_key
) "Location"
GROUP BY 2,
  3,
  4,
  5,
  6;

-- window query #2 - avg number of occurrences per season
SELECT (CASE WHEN ((CAST(TRUNC(CAST("Location"."month" AS DOUBLE PRECISION)) AS BIGINT) = 12) OR (CAST(TRUNC(CAST("Location"."month" AS DOUBLE PRECISION)) AS BIGINT) = 1) OR (CAST(TRUNC(CAST("Location"."month" AS DOUBLE PRECISION)) AS BIGINT) = 2)) THEN 'Winter' WHEN ((CAST(TRUNC(CAST("Location"."month" AS DOUBLE PRECISION)) AS BIGINT) = 3) OR (CAST(TRUNC(CAST("Location"."month" AS DOUBLE PRECISION)) AS BIGINT) = 4) OR (CAST(TRUNC(CAST("Location"."month" AS DOUBLE PRECISION)) AS BIGINT) = 5)) THEN 'Spring' WHEN ((CAST(TRUNC(CAST("Location"."month" AS DOUBLE PRECISION)) AS BIGINT) = 6) OR (CAST(TRUNC(CAST("Location"."month" AS DOUBLE PRECISION)) AS BIGINT) = 7) OR (CAST(TRUNC(CAST("Location"."month" AS DOUBLE PRECISION)) AS BIGINT) = 8)) THEN 'Summer' ELSE 'Fall' END) AS "season",
  "Location"."city" AS "city",
  "Location"."crime_type" AS "crime_type",
  "Location"."neighborhood" AS "neighborhood",
  CAST (SUM(1) AS FLOAT)/90 AS "avg_ocurrence_per_season",
  "Location"."year" AS "year"
FROM (
  select * from
  t_fact_table
  inner join t_location_dim
  on t_fact_table.location_key = t_location_dim.location_key
  inner join t_date_dim
  on t_fact_table.date_key = t_date_dim.date_key
  inner join t_crime_dim
  on t_fact_table.crime_key = t_crime_dim.crime_key
  inner join t_event_dim
  on t_fact_table.event_key = t_event_dim.event_key
) "Location"
GROUP BY 1,
  2,
  3,
  4,
  6

-- Utilizing Windowing Clause (Zaid)
-- window query #1
-- compares # of crimes per neighborhood from month to month 
-- uses the window clause 
with init_window as 
(select distinct
	count(day) over w, 
	month, 
	neighborhood, 
	year
from t_fact_table
inner join t_date_dim on t_fact_table.date_key = t_date_dim.date_key
inner join t_location_dim on t_fact_table.location_key = t_location_dim.location_key
WINDOW w AS (PARTITION BY month, neighborhood, year
			 order by neighborhood, month, year)
order by neighborhood, month, year)


select *,
lag(count) over (order by neighborhood, month, year) as previous_year_count,
lead(count) over (order by neighborhood, month, year) as next_year_count
from init_window
window g AS (PARTITION BY month, neighborhood, year)

-- window query #2
-- Number of crimes per city per year
-- This query was separated for both cities
-- Denver window query 
with american_holidays as
	(select distinct
		count(day) over w,
		american_holiday_name,
		year,
		city
	from t_fact_table
	inner join t_date_dim on t_fact_table.date_key = t_date_dim.date_key
	inner join t_crime_dim on t_fact_table.crime_key = t_crime_dim.crime_key
	inner join t_location_dim on t_fact_table.location_key = t_location_dim.location_key
	where city = 'Denver'
	WINDOW w AS (PARTITION BY american_holiday_name, year
				 order by year)
	order by year)
	
select *,
  lag(count) over (order by american_holiday_name, year) as previous_year_count,
  lead(count) over (order by american_holiday_name, year) as next_year_count
from american_holidays
window g AS (PARTITION BY american_holiday_name, year)

--Vancouver window query
with canadian_holidays as
	(select distinct
		count(day) over w,
		canadian_holiday_name,
		year,
		city
	from t_fact_table
	inner join t_date_dim on t_fact_table.date_key = t_date_dim.date_key
	inner join t_crime_dim on t_fact_table.crime_key = t_crime_dim.crime_key
	inner join t_location_dim on t_fact_table.location_key = t_location_dim.location_key
	where city = 'Vancouver'
	WINDOW w AS (PARTITION BY canadian_holiday_name, year
				 order by year)
	order by year)
	
select *,
lag(count) over (order by canadian_holiday_name, year) as previous_year_count,
lead(count) over (order by canadian_holiday_name, year) as next_year_count
from canadian_holidays
window g AS (PARTITION BY canadian_holiday_name, year)