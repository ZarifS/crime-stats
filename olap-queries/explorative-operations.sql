-- Iceberg Query 1 - Top 5 places in Denver where offences against people occured (most violent areas).
SELECT c.crime_type, l.neighborhood, count(*) as total 
FROM t_location_dim as l INNER JOIN t_fact_table as f
ON l.location_key = f.location_key INNER JOIN t_crime_dim as c ON c.crime_key = f.crime_key 
WHERE l.city = 'Denver' AND c.crime_type = 'Offence Against a Person' 
GROUP BY c.crime_type, l.neighborhood 
ORDER BY total DESC
LIMIT 5

-- Iceberg Query 2 - Top 5 places in Vancouver where theft occured.
SELECT c.crime_type, l.neighborhood, count(*) as total 
FROM t_location_dim as l INNER JOIN t_fact_table as f
ON l.location_key = f.location_key INNER JOIN t_crime_dim as c ON c.crime_key = f.crime_key 
WHERE l.city = 'Vancouver' AND c.crime_type = 'Theft' 
GROUP BY c.crime_type, l.neighborhood 
ORDER BY total DESC
LIMIT 5

-- Iceberg Query 3 - Top 5 safest places in Denver (least violent).
SELECT c.crime_type, l.neighborhood, count(*) as total 
FROM t_location_dim as l INNER JOIN t_fact_table as f
ON l.location_key = f.location_key INNER JOIN t_crime_dim as c ON c.crime_key = f.crime_key 
WHERE l.city = 'Denver' AND c.crime_type = 'Offence Against a Person' 
GROUP BY c.crime_type, l.neighborhood 
ORDER BY total ASC
LIMIT 5

-- Windowing (Zarif)

-- Utilizing Windowing Clause (Zaid)