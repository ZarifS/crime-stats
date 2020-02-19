\copy accident_dimension from 'C:\Users\johan\Desktop\Demo\Data\accident_dimension.csv' with delimiter ',' csv header;

\copy location_dimension from 'C:\Users\johan\Desktop\Demo\Data\location_dimension.csv' with delimiter ',' csv header;

\copy hour_dimension from 'C:\Users\johan\Desktop\Demo\Data\hour_dimension.csv' with delimiter ',' csv header;

\copy weather_dimension from 'C:\Users\johan\Desktop\Demo\Data\weather_dimension.csv' with delimiter ',' csv header;

\copy accident_fact from 'C:\Users\johan\Desktop\Demo\Data\accident_fact.csv' with delimiter ',' csv header;