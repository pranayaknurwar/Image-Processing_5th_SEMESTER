-- Run this file after connecting to the image_processing_lab database.
CREATE TABLE IF NOT EXISTS experiment_runs (
  id BIGSERIAL PRIMARY KEY,
  experiment_code VARCHAR(20) NOT NULL,
  operation VARCHAR(100) NOT NULL,
  image_name VARCHAR(255),
  performed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_experiment_runs_code
ON experiment_runs(experiment_code);
