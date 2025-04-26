CREATE TABLE weather_searches (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100),
    country VARCHAR(10),
    temperature NUMERIC,
    description TEXT,
    icon TEXT,
    humidity INT,
    wind_speed NUMERIC,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
