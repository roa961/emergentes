CREATE TABLE admin (
    username STRING,
    password STRING
);
CREATE TABLE company (
    ID INT,
    company_name STRING,
    company_api_key STRING
);
CREATE TABLE location(
    ID INT,
    company_id int,
    location_name STRING,
    location_country STRING,
    location_city STRING,
    location_meta STRING,
    foreign key(company_id) references company(ID)
);
CREATE TABLE sensor(
    location_id int,
    sensor_id int,
    sensor_name string,
    sensor_category string,
    sensor_meta string,
    sensor_api_key string,
    foreign key(location_id) references location(ID)
);
