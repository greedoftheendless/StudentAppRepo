-- Database and user are created by POSTGRES_DB / POSTGRES_USER env vars.
-- This script grants schema permissions.
\c studentdb
GRANT ALL ON SCHEMA public TO studentuser;
