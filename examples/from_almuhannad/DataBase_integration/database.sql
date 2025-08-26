CREATE TABLE IF NOT EXISTS travel_time_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL,
    distance TEXT,
    distance_value INTEGER,
    is_minimum BOOLEAN DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_source_dest ON travel_time_history(source, destination);
CREATE INDEX IF NOT EXISTS idx_timestamp ON travel_time_history(timestamp);