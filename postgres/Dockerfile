FROM postgres:12
# After the entrypoint calls initdb to create the default postgres user and database,
# it will run any *.sql files, run any executable *.sh scripts, and source any non-executable *.sh scripts found
# in the /docker-entry-point-initdb.d directory to do further initialization before starting the service.
COPY create_buses_database.sql /docker-entrypoint-initdb.d