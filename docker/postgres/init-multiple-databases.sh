!/bin/bash

# set -e
# set -u

# function create_user_and_database() {
#     local database=$1
#     local username=$2
#     local password=$3
#     echo "Creating user '$username' and database '$database'"
#     psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
#         CREATE USER $username WITH PASSWORD '$password';
#         CREATE DATABASE $database;
#         GRANT ALL PRIVILEGES ON DATABASE $database TO $username;
# EOSQL
#     echo "  User '$username' and database '$database' created successfully"
# }

# # Metadata database
# create_user_and_database $METADATA_DATABASE_NAME $METADATA_DATABASE_USERNAME $METADATA_DATABASE_PASSWORD

# # Celery result backend database
# create_user_and_database $CELERY_BACKEND_NAME $CELERY_BACKEND_USERNAME $CELERY_BACKEND_PASSWORD

# # ELT database
# create_user_and_database $ELT_DATABASE_NAME $ELT_DATABASE_USERNAME $ELT_DATABASE_PASSWORD

# echo "All databases and users created successfully"

set -e
set -u
 
# Creates a role (if missing) and a database (if missing).
# Safe to use even when the username is "postgres", which always exists.
create_user_and_database() {
    local database="$1"
    local username="$2"
    local password="$3"
    echo "Setting up database '$database' for user '$username'"
 
    # 1) Role: only create it if it doesn't already exist
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres <<-EOSQL
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '$username') THEN
        CREATE ROLE "$username" LOGIN PASSWORD '$password';
    END IF;
END
\$\$;
EOSQL
 
    # 2) Database: CREATE DATABASE can't run inside a DO block, so check first
    if ! psql --username "$POSTGRES_USER" --dbname postgres -tAc \
        "SELECT 1 FROM pg_database WHERE datname = '$database'" | grep -q 1; then
        psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres \
            -c "CREATE DATABASE \"$database\" OWNER \"$username\""
        echo "  Database '$database' created"
    else
        echo "  Database '$database' already exists"
    fi
}
 
create_user_and_database "$METADATA_DATABASE_NAME" "$METADATA_DATABASE_USERNAME" "$METADATA_DATABASE_PASSWORD"
create_user_and_database "$CELERY_BACKEND_NAME"    "$CELERY_BACKEND_USERNAME"    "$CELERY_BACKEND_PASSWORD"
create_user_and_database "$ELT_DATABASE_NAME"      "$ELT_DATABASE_USERNAME"      "$ELT_DATABASE_PASSWORD"
 
echo "All databases and users are ready"
 