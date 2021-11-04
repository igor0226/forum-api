CREATE EXTENSION IF NOT EXISTS CITEXT;
GRANT ALL PRIVILEGES ON DATABASE app TO igor;

DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS forums CASCADE;
DROP TABLE IF EXISTS threads CASCADE;
DROP TABLE IF EXISTS posts CASCADE;
DROP FUNCTION IF EXISTS get_non_existing_posts;

CREATE TABLE users
(
  id BIGSERIAL PRIMARY KEY NOT NULL,
  about TEXT,
  email CITEXT NOT NULL UNIQUE,
  fullname TEXT NOT NULL,
  nickname CITEXT UNIQUE
);

CREATE TABLE forums
(
  id BIGSERIAL PRIMARY KEY NOT NULL,
  posts BIGINT DEFAULT 0,
  slug CITEXT UNIQUE,
  threads BIGINT DEFAULT 0,
  title TEXT,
  author CITEXT NOT NULL,
  FOREIGN KEY (author) REFERENCES users(nickname)
);

CREATE TABLE threads
(
  id BIGSERIAL PRIMARY KEY NOT NULL,
  author CITEXT NOT NULL,
  created TIMESTAMP WITH TIME ZONE,
  forum CITEXT NOT NULL,
  message TEXT NOT NULL,
  slug CITEXT UNIQUE,
  title TEXT NOT NULL,
  votes BIGINT DEFAULT 0,
  FOREIGN KEY (author) REFERENCES users(nickname),
  FOREIGN KEY (forum) REFERENCES forums(slug)
);

CREATE TABLE posts
(
  id BIGSERIAL PRIMARY KEY NOT NULL,
  created TIMESTAMP WITH TIME ZONE,
  isEdited BOOLEAN DEFAULT FALSE,
  message TEXT NOT NULL,
  parent BIGINT,
  forum CITEXT,
  thread BIGINT,
  author CITEXT NOT NULL,
  FOREIGN KEY (forum) REFERENCES forums(slug),
  FOREIGN KEY (thread) REFERENCES threads(id),
  FOREIGN KEY (author) REFERENCES users(nickname),
  UNIQUE(parent, forum, thread)
);

CREATE FUNCTION
  get_non_existing_posts(post_ids BIGINT[])
  RETURNS TABLE(id BIGINT) AS $$
      DECLARE
        i INTEGER;
      BEGIN
        CREATE TEMPORARY TABLE temp_posts(
          id BIGINT
        );

        FOREACH i IN ARRAY post_ids LOOP
          INSERT INTO temp_posts (id) values(i);
        END LOOP;

        RETURN QUERY SELECT temp_posts.id FROM
        temp_posts
        LEFT JOIN posts
        ON temp_posts.id = posts.id
        WHERE posts.id IS NULL;

        DROP TABLE temp_posts;
      END;
  $$ LANGUAGE plpgsql;
