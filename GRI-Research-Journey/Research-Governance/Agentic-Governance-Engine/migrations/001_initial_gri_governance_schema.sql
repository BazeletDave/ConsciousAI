-- GRI governance v2.1 research prototype. Apply only to a dedicated EMPTY test DB.
BEGIN;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE TABLE governance_issuer_keys (
 key_id TEXT PRIMARY KEY,
 public_key_hex CHAR(64) NOT NULL CHECK(public_key_hex ~ '^[0-9a-fA-F]{64}$'),
 revoked BOOLEAN NOT NULL DEFAULT FALSE,
 valid_from TIMESTAMPTZ NOT NULL,
 valid_until TIMESTAMPTZ NOT NULL,
 CHECK(valid_until > valid_from)
);
CREATE TABLE agent_capabilities (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 agent_id VARCHAR(128) NOT NULL,
 issuer_key_id TEXT NOT NULL REFERENCES governance_issuer_keys(key_id),
 capability_digest CHAR(64) NOT NULL UNIQUE CHECK(capability_digest ~ '^[0-9a-f]{64}$'),
 allowed_asset_pair VARCHAR(64) NOT NULL,
 max_single_amount NUMERIC(18,4) NOT NULL CHECK(max_single_amount > 0),
 max_hourly_volume NUMERIC(18,4) NOT NULL CHECK(max_hourly_volume > 0),
 valid_from TIMESTAMPTZ NOT NULL,
 valid_until TIMESTAMPTZ NOT NULL,
 revoked BOOLEAN NOT NULL DEFAULT FALSE,
 CHECK(valid_until > valid_from),
 CHECK(max_single_amount <= max_hourly_volume)
);
CREATE INDEX idx_gri_cap_agent ON agent_capabilities(agent_id);
CREATE TABLE agent_locks (agent_id VARCHAR(128) PRIMARY KEY);
CREATE TABLE authorization_reservations (
 action_id VARCHAR(128) PRIMARY KEY,
 agent_id VARCHAR(128) NOT NULL,
 capability_id UUID NOT NULL REFERENCES agent_capabilities(id),
 amount NUMERIC(18,4) NOT NULL CHECK(amount > 0),
 created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_gri_reservations_agent_time ON authorization_reservations(agent_id,created_at);
CREATE TABLE circuit_breaker_states (
 system_id VARCHAR(64) PRIMARY KEY,
 is_open BOOLEAN NOT NULL DEFAULT FALSE,
 tripped_reason TEXT
);
INSERT INTO circuit_breaker_states(system_id) VALUES ('primary');
CREATE TABLE evidence_chain_heads (
 chain_id TEXT PRIMARY KEY,
 last_index BIGINT NOT NULL DEFAULT 0,
 last_hash CHAR(64) NOT NULL DEFAULT repeat('0',64)
);
INSERT INTO evidence_chain_heads(chain_id) VALUES ('primary');
CREATE TABLE evidence_records (
 chain_id TEXT NOT NULL REFERENCES evidence_chain_heads(chain_id),
 sequence_index BIGINT NOT NULL CHECK(sequence_index > 0),
 timestamp_utc TIMESTAMPTZ NOT NULL,
 action_id VARCHAR(128) NOT NULL UNIQUE,
 agent_id VARCHAR(128) NOT NULL,
 capability_digest CHAR(64) NOT NULL,
 policy_version VARCHAR(32) NOT NULL,
 input_payload_hash CHAR(64) NOT NULL,
 decision_status VARCHAR(32) NOT NULL,
 rejection_reason TEXT,
 amount NUMERIC(18,4) NOT NULL CHECK(amount >= 0),
 previous_record_hash CHAR(64) NOT NULL,
 record_hash CHAR(64) NOT NULL UNIQUE,
 PRIMARY KEY(chain_id,sequence_index)
);
CREATE TABLE idempotency_records (
 agent_id VARCHAR(128) NOT NULL,
 idempotency_key VARCHAR(255) NOT NULL,
 request_hash CHAR(64) NOT NULL,
 response_payload JSONB NOT NULL,
 created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 PRIMARY KEY(agent_id,idempotency_key)
);
CREATE TABLE evidence_checkpoints (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 chain_id TEXT NOT NULL,
 up_to_sequence_index BIGINT NOT NULL,
 chain_head_hash CHAR(64) NOT NULL,
 signer_key_id TEXT NOT NULL REFERENCES governance_issuer_keys(key_id),
 signature_hex CHAR(128) NOT NULL,
 created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 FOREIGN KEY(chain_id,up_to_sequence_index) REFERENCES evidence_records(chain_id,sequence_index)
);
COMMIT;
