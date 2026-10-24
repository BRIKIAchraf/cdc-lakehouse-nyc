CREATE TABLE IF NOT EXISTS public.taxi_trips (
    trip_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    vendor_id SMALLINT,
    pickup_datetime TIMESTAMP NOT NULL,
    dropoff_datetime TIMESTAMP NOT NULL,

    passenger_count NUMERIC(4, 1),
    trip_distance NUMERIC(10, 2),

    pickup_location_id INTEGER,
    dropoff_location_id INTEGER,

    payment_type SMALLINT,
    fare_amount NUMERIC(12, 2),
    total_amount NUMERIC(12, 2),

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT valid_trip_time
        CHECK (dropoff_datetime >= pickup_datetime)
);