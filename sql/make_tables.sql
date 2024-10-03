-- Create table to store experiment run metadata (Run Start documents)
CREATE TABLE IF NOT EXISTS run_metadata (
    run_uid TEXT PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    start_document JSONB NOT NULL
);

-- Create table to store event data associated with each run
CREATE TABLE IF NOT EXISTS event_data (
    id SERIAL PRIMARY KEY,
    run_uid TEXT REFERENCES run_metadata(run_uid) ON DELETE CASCADE,
    event_data JSONB NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL
);

-- Create index on timestamp to optimize queries based on time
CREATE INDEX IF NOT EXISTS idx_event_timestamp ON event_data (timestamp);
