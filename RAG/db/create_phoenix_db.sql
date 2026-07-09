SELECT 'CREATE DATABASE phoenix'
WHERE NOT EXISTS (
	SELECT FROM pg_database WHERE datname = 'phoenix'
)\gexec