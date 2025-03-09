-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    last_login TIMESTAMP,
    login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP
);

-- Scan Results table
CREATE TABLE scan_results (
    id SERIAL PRIMARY KEY,
    scan_id VARCHAR(50) UNIQUE NOT NULL,
    target_url TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL,
    created_by INTEGER REFERENCES users(id),
    total_findings INTEGER DEFAULT 0
);

-- Findings table
CREATE TABLE findings (
    id SERIAL PRIMARY KEY,
    scan_id INTEGER REFERENCES scan_results(id),
    type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    description TEXT NOT NULL,
    details TEXT,
    discovered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Reports table
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    report_id VARCHAR(50) UNIQUE NOT NULL,
    scan_id INTEGER REFERENCES scan_results(id),
    format VARCHAR(10) NOT NULL,
    file_path TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    encrypted BOOLEAN DEFAULT false,
    encryption_key TEXT
);

-- Audit Logs table
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    details JSONB
);

-- Scan Schedules table
CREATE TABLE scan_schedules (
    id SERIAL PRIMARY KEY,
    target_url TEXT NOT NULL,
    frequency VARCHAR(20) NOT NULL,
    last_run TIMESTAMP,
    next_run TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- API Rate Limits table
CREATE TABLE rate_limits (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    endpoint VARCHAR(100) NOT NULL,
    requests_count INTEGER DEFAULT 0,
    window_start TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_scan_results_timestamp ON scan_results(timestamp);
CREATE INDEX idx_findings_severity ON findings(severity);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_rate_limits_window ON rate_limits(window_start);
GO

-- Create view for high severity findings
CREATE VIEW high_severity_findings AS
SELECT f.*, s.target_url, s.scan_id
FROM findings f
JOIN scan_results s ON f.scan_id = s.id
WHERE f.severity = 'high'
ORDER BY f.discovered_at DESC;
GO

-- Create view for user scan summary
CREATE VIEW user_scan_summary AS
SELECT 
    u.username,
    COUNT(s.id) as total_scans,
    COUNT(f.id) as total_findings,
    MAX(s.timestamp) as last_scan_date
FROM users u
LEFT JOIN scan_results s ON u.id = s.created_by
LEFT JOIN findings f ON s.id = f.scan_id
GROUP BY u.id, u.username;
GO
