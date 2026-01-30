CREATE TABLE IF NOT EXISTS logs (
    timestamp TIMESTAMP,
    ip TEXT,
    user_agent TEXT,
    status INT,
    message TEXT
);
