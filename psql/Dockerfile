FROM postgres

RUN useradd igor

ENV POSTGRES_DB=app
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_USER=igor
ENV PGDATA=/var/lib/postgresql/data/pgdata

ADD inits/init.sql /docker-entrypoint-initdb.d
ADD inits/posts.sql /docker-entrypoint-initdb.d
ADD inits/service.sql /docker-entrypoint-initdb.d
ADD inits/tables.sql /docker-entrypoint-initdb.d
ADD inits/threads.sql /docker-entrypoint-initdb.d
ADD inits/users.sql /docker-entrypoint-initdb.d

RUN chown -R igor /docker-entrypoint-initdb.d
RUN mv /docker-entrypoint-initdb.d/init.sql /docker-entrypoint-initdb.d/a.sql
RUN mv /docker-entrypoint-initdb.d/tables.sql /docker-entrypoint-initdb.d/b.sql
RUN chown -R igor /var/run/postgresql

EXPOSE 5432:5432
