CREATE TABLE IF NOT EXISTS batch_results (
    id             SERIAL PRIMARY KEY,
    run_at         TIMESTAMP NOT NULL DEFAULT now(),
    file           TEXT NOT NULL,
    row_count      INTEGER,
    null_rate      REAL,
    duplicate_rate REAL,
    cancelled_rate REAL,
    score          REAL,
    verdict        TEXT NOT NULL,
    rule_failures  TEXT
);