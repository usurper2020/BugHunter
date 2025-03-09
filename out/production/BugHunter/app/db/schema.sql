-- PostgreSQL database initialization for Bug Hunter

-- Drop database if exists (be careful with this in production!)
DROP DATABASE IF EXISTS bughunter_db;
DROP USER IF EXISTS bughunter_user;

-- Create database with proper encoding and timezone
CREATE DATABASE bughunter_db
    WITH 
    ENCODING = 'UTF8'
LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

-- Connect to the database
\c bughunter_db

-- Create extensions
CREATE EXTENSION
IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION
IF NOT EXISTS "pgcrypto";

-- Create user role with proper permissions
CREATE USER bughunter_user
WITH PASSWORD 'your-secure-password-here';
ALTER USER bughunter_user WITH LOGIN;

-- Create schema and set permissions
CREATE SCHEMA
IF NOT EXISTS bughunter;
GRANT USAGE ON SCHEMA bughunter TO bughunter_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA bughunter
GRANT ALL ON TABLES TO bughunter_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA bughunter
GRANT ALL ON SEQUENCES TO bughunter_user;

-- Set search path
SET search_path
TO bughunter, public;

-- Users table (enhanced with authentication fields)
CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP
    WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
    WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    role VARCHAR
    (20) DEFAULT 'user',
    failed_login_attempts INTEGER DEFAULT 0,
    account_locked_until TIMESTAMP
    WITH TIME ZONE,
    password_reset_token VARCHAR
    (255),
    password_reset_expires TIMESTAMP
    WITH TIME ZONE,
    CONSTRAINT valid_role CHECK
    (role IN
    ('admin', 'user', 'viewer'))
);

    -- Fingerprints table for device tracking
    CREATE TABLE fingerprints
    (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        fingerprint_hash VARCHAR(255) NOT NULL,
        device_info JSONB NOT NULL,
        ip_address VARCHAR(45),
        created_at TIMESTAMP
        WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP
        WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    trust_score INTEGER DEFAULT 0,
    UNIQUE
        (user_id, fingerprint_hash)
);

        -- Sessions table for session management
        CREATE TABLE sessions
        (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            session_token VARCHAR(255) UNIQUE NOT NULL,
            fingerprint_hash VARCHAR(255),
            created_at TIMESTAMP
            WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
            WITH TIME ZONE,
    last_activity TIMESTAMP
            WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    ip_address VARCHAR
            (45),
    user_agent TEXT,
    session_data JSONB
);

            -- Login attempts table for security monitoring
            CREATE TABLE login_attempts
            (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                ip_address VARCHAR(45),
                attempt_time TIMESTAMP
                WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN,
    fingerprint_hash VARCHAR
                (255),
    device_info JSONB,
    attempt_type VARCHAR
                (20),
    failure_reason VARCHAR
                (255),
    geolocation JSONB,
    risk_score INTEGER
);

                -- Security events table for audit logging
                CREATE TABLE security_events
                (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    event_type VARCHAR(50) NOT NULL,
                    event_time TIMESTAMP
                    WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    event_data JSONB,
    ip_address VARCHAR
                    (45),
    fingerprint_hash VARCHAR
                    (255),
    severity INTEGER CHECK
                    (severity BETWEEN 1 AND 5),
    is_resolved BOOLEAN DEFAULT false,
    resolution_notes VARCHAR
                    (500),
    resolution_time TIMESTAMP
                    WITH TIME ZONE
);

                    -- Scan Results table
                    CREATE TABLE scan_results
                    (
                        id SERIAL PRIMARY KEY,
                        scan_id UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
                        target_url TEXT NOT NULL,
                        timestamp TIMESTAMP
                        WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR
                        (20) NOT NULL,
    created_by INTEGER REFERENCES users
                        (id) ON
                        DELETE
                        SET NULL
                        ,
    total_findings INTEGER DEFAULT 0,
    scan_duration INTERVAL,
    scan_type VARCHAR
                        (50),
    scan_parameters JSONB,
    CONSTRAINT valid_status CHECK
                        (status IN
                        ('pending', 'running', 'completed', 'failed'))
);

                        -- Findings table
                        CREATE TABLE findings
                        (
                            id SERIAL PRIMARY KEY,
                            scan_id INTEGER REFERENCES scan_results(id) ON DELETE CASCADE,
                            type VARCHAR(50) NOT NULL,
                            severity VARCHAR(20) NOT NULL,
                            description TEXT NOT NULL,
                            details JSONB,
                            discovered_at TIMESTAMP
                            WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    verified BOOLEAN DEFAULT false,
    false_positive BOOLEAN DEFAULT false,
    cvss_score DECIMAL
                            (3,1),
    cve_ids TEXT[],
    CONSTRAINT valid_severity CHECK
                            (severity IN
                            ('critical', 'high', 'medium', 'low', 'info'))
);

                            -- Reports table
                            CREATE TABLE reports
                            (
                                id SERIAL PRIMARY KEY,
                                report_id UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
                                scan_id INTEGER REFERENCES scan_results(id) ON DELETE CASCADE,
                                format VARCHAR(10) NOT NULL,
                                file_path TEXT NOT NULL,
                                created_at TIMESTAMP
                                WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users
                                (id) ON
                                DELETE
                                SET NULL
                                ,
    encrypted BOOLEAN DEFAULT false,
    encryption_key TEXT,
    report_type VARCHAR
                                (50),
    metadata JSONB,
    CONSTRAINT valid_format CHECK
                                (format IN
                                ('pdf', 'html', 'json', 'xml'))
);

                                -- Audit Logs table
                                CREATE TABLE audit_logs
                                (
                                    id SERIAL PRIMARY KEY,
                                    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                                    action VARCHAR(50) NOT NULL,
                                    entity_type VARCHAR(50) NOT NULL,
                                    entity_id INTEGER NOT NULL,
                                    timestamp TIMESTAMP
                                    WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    details JSONB,
    success BOOLEAN DEFAULT true,
    session_id UUID
);

                                    -- Scan Schedules table
                                    CREATE TABLE scan_schedules
                                    (
                                        id SERIAL PRIMARY KEY,
                                        target_url TEXT NOT NULL,
                                        frequency VARCHAR(20) NOT NULL,
                                        last_run TIMESTAMP
                                        WITH TIME ZONE,
    next_run TIMESTAMP
                                        WITH TIME ZONE,
    created_by INTEGER REFERENCES users
                                        (id) ON
                                        DELETE
                                        SET NULL
                                        ,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP
                                        WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    scan_parameters JSONB,
    notification_email TEXT[],
    CONSTRAINT valid_frequency CHECK
                                        (frequency IN
                                        ('daily', 'weekly', 'monthly', 'custom'))
);

                                        -- API Rate Limits table
                                        CREATE TABLE rate_limits
                                        (
                                            id SERIAL PRIMARY KEY,
                                            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                                            endpoint VARCHAR(100) NOT NULL,
                                            requests_count INTEGER DEFAULT 0,
                                            window_start TIMESTAMP
                                            WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    limit_per_window INTEGER NOT NULL,
    window_size INTERVAL NOT NULL
);

                                            -- Create indexes for better query performance
                                            CREATE INDEX idx_users_username ON users(username);
                                            CREATE INDEX idx_users_email ON users(email);
                                            CREATE INDEX idx_users_role ON users(role);

                                            CREATE INDEX idx_fingerprints_user_id ON fingerprints(user_id);
                                            CREATE INDEX idx_fingerprints_hash ON fingerprints(fingerprint_hash);
                                            CREATE INDEX idx_fingerprints_ip ON fingerprints(ip_address);

                                            CREATE INDEX idx_sessions_user_id ON sessions(user_id);
                                            CREATE INDEX idx_sessions_token ON sessions(session_token);
                                            CREATE INDEX idx_sessions_fingerprint ON sessions(fingerprint_hash);

                                            CREATE INDEX idx_login_attempts_user_id ON login_attempts(user_id);
                                            CREATE INDEX idx_login_attempts_time ON login_attempts(attempt_time);
                                            CREATE INDEX idx_login_attempts_ip ON login_attempts(ip_address);

                                            CREATE INDEX idx_security_events_user_id ON security_events(user_id);
                                            CREATE INDEX idx_security_events_type ON security_events(event_type);

                                            CREATE INDEX idx_scan_results_timestamp ON scan_results(timestamp);
                                            CREATE INDEX idx_scan_results_target ON scan_results(target_url);
                                            CREATE INDEX idx_findings_severity ON findings(severity);
                                            CREATE INDEX idx_findings_type ON findings(type);
                                            CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
                                            CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
                                            CREATE INDEX idx_rate_limits_window ON rate_limits(window_start);
                                            CREATE INDEX idx_rate_limits_user_endpoint ON rate_limits(user_id, endpoint);

                                            -- Create views for common queries
                                            CREATE OR REPLACE VIEW high_severity_findings AS
                                            SELECT f.*, s.target_url, s.scan_id
                                            FROM findings f
                                                JOIN scan_results s ON f.scan_id = s.id
                                            WHERE f.severity IN ('critical', 'high')
                                            ORDER BY f.discovered_at DESC;

                                            CREATE OR REPLACE VIEW user_scan_summary AS
                                            SELECT
                                                u.username,
                                                COUNT(s.id) as total_scans,
                                                COUNT(f.id) as total_findings,
                                                MAX(s.timestamp) as last_scan_date,
                                                COUNT(CASE WHEN f.severity = 'critical' THEN 1 END) as critical_findings,
                                                COUNT(CASE WHEN f.severity = 'high' THEN 1 END) as high_findings
                                            FROM users u
                                                LEFT JOIN scan_results s ON u.id = s.created_by
                                                LEFT JOIN findings f ON s.id = f.scan_id
                                            GROUP BY u.id, u.username;

                                            -- Enable row level security
                                            ALTER TABLE users ENABLE ROW LEVEL SECURITY;
                                            ALTER TABLE fingerprints ENABLE ROW LEVEL SECURITY;
                                            ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
                                            ALTER TABLE login_attempts ENABLE ROW LEVEL SECURITY;
                                            ALTER TABLE security_events ENABLE ROW LEVEL SECURITY;

                                            -- Create security policies
                                            CREATE POLICY users_policy ON users 
    FOR ALL TO bughunter_user 
    USING
                                            (true) 
    WITH CHECK
                                            (role != 'admin');

                                            CREATE POLICY fingerprints_policy ON fingerprints 
    FOR ALL TO bughunter_user 
    USING
                                            (true);

                                            CREATE POLICY sessions_policy ON sessions 
    FOR ALL TO bughunter_user 
    USING
                                            (true);

                                            CREATE POLICY login_attempts_policy ON login_attempts 
    FOR ALL TO bughunter_user 
    USING
                                            (true);

                                            CREATE POLICY security_events_policy ON security_events 
    FOR ALL TO bughunter_user 
    USING
                                            (true);

                                            -- Grant necessary permissions
                                            GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA bughunter TO bughunter_user;
                                            GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA bughunter TO bughunter_user;

                                            -- Create default admin user (password: admin123)
                                            INSERT INTO users
                                                (username, password_hash, email, role, is_active)
                                            VALUES
                                                (
                                                    'admin',
                                                    crypt('admin123', gen_salt('bf')),
                                                    'admin@bughunter.local',
                                                    'admin',
                                                    true
);
