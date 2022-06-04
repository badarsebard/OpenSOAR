FROM postgres:14.1

ADD init-user-db.sh /docker-entrypoint-initdb.d/init-user-db.sh