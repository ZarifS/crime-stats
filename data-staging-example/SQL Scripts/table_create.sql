create table accident_dimension(
accident_key int,
accident_time time,
environment varchar,
road_surface varchar,
traffic_control varchar,
visibility varchar,
impact_type varchar,
primary key (accident_key)
);

create table location_dimension(
location_key int,
street_name varchar,
intersection_1 varchar,
intersection_2 varchar,
longitude float,
latiude float,
primary key (location_key)
);

create table hour_dimension(
hour_key int,
hour_start int,
hour_end int,
accident_date timestamp,
month int,
year int,
primary key (hour_key)
);

create table weather_dimension(
weather_key int,
weather_date timestamp,
month varchar,
year int,
station varchar,
temp float,
primary key (weather_key)
);

create table accident_fact(
hour_key int,
location_key int,
accident_key int,
weather_key int,
is_fatal int,
is_intersection int,
/*primary key (hour_key, location_key, accident_key, weather_key), */
foreign key (hour_key) references hour_dimension(hour_key),
foreign key (location_key) references location_dimension(location_key),
foreign key (accident_key) references accident_dimension(accident_key),
foreign key (weather_key) references weather_dimension(weather_key)
);