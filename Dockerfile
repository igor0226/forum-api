FROM postgres

RUN useradd igor

ENV POSTGRES_DB=app
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_USER=igor
ENV PGDATA=/var/lib/postgresql/data/pgdata

ADD psql/init.sql /docker-entrypoint-initdb.d
RUN chown -R igor /docker-entrypoint-initdb.d
RUN chown -R igor /var/run/postgresql

EXPOSE 5432:5432
