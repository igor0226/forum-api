CREATE EXTENSION IF NOT EXISTS CITEXT;
GRANT ALL PRIVILEGES ON DATABASE app TO igor;

DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS forums CASCADE;
DROP TABLE IF EXISTS threads CASCADE;
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS votes CASCADE;
DROP FUNCTION IF EXISTS get_non_existing_posts;

CREATE TABLE users
(
  id BIGSERIAL PRIMARY KEY,
  about TEXT,
  email CITEXT NOT NULL UNIQUE,
  fullname TEXT NOT NULL,
  nickname CITEXT UNIQUE
);

CREATE TABLE forums
(
  id BIGSERIAL PRIMARY KEY,
  posts BIGINT DEFAULT 0,
  slug CITEXT UNIQUE,
  threads BIGINT DEFAULT 0,
  title TEXT,
  author CITEXT NOT NULL,
  FOREIGN KEY (author) REFERENCES users(nickname)
);

CREATE TABLE threads
(
  id BIGSERIAL PRIMARY KEY,
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
  id BIGSERIAL PRIMARY KEY,
  created TIMESTAMP WITH TIME ZONE,
  isEdited BOOLEAN DEFAULT FALSE,
  message TEXT NOT NULL,
  parent BIGINT,
  forum CITEXT,
  thread BIGINT,
  path CITEXT,
  author CITEXT NOT NULL,
  FOREIGN KEY (forum) REFERENCES forums(slug),
  FOREIGN KEY (thread) REFERENCES threads(id),
  FOREIGN KEY (author) REFERENCES users(nickname)
);

CREATE TABLE thread_votes
(
    id BIGSERIAL PRIMARY KEY,
    author CITEXT NOT NULL,
    thread BIGINT NOT NULL,
    vote INT,
    UNIQUE(author, thread),
    FOREIGN KEY (author) REFERENCES users(nickname),
    FOREIGN KEY (thread) REFERENCES threads(id)
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

CREATE FUNCTION update_thread_votes_counter() RETURNS TRIGGER AS
$$
    DECLARE
        old_votes BIGINT;
    BEGIN
        SELECT votes
        INTO old_votes
        FROM threads
        WHERE id = NEW.thread;

        IF TG_OP = 'INSERT' THEN
            UPDATE threads SET votes = old_votes + NEW.vote
            WHERE id = NEW.thread;
        ELSIF TG_OP = 'UPDATE' THEN
            UPDATE threads SET votes = old_votes - OLD.vote + NEW.vote
            WHERE id = NEW.thread;
        END IF;

        RETURN NEW;
    END
$$ LANGUAGE plpgsql;

CREATE TRIGGER t_votes
AFTER INSERT OR UPDATE ON thread_votes
FOR EACH ROW EXECUTE PROCEDURE update_thread_votes_counter();

CREATE FUNCTION create_post_path() RETURNS TRIGGER AS
$$
    DECLARE
        parent_post_path CITEXT;
        new_post_path CITEXT;
    BEGIN
        IF NEW.parent IS NOT NULL THEN
            SELECT path
            INTO parent_post_path
            FROM POSTS
            WHERE id = NEW.parent;

            IF parent_post_path IS NOT NULL THEN
                new_post_path := parent_post_path || '.' || NEW.id::CITEXT;
            END IF;
        END IF;

        IF parent_post_path IS NULL THEN
            new_post_path := NEW.id::CITEXT;
        END IF;

        NEW.path = new_post_path;

        RETURN NEW;
    END
$$ LANGUAGE plpgsql;

CREATE TRIGGER t_path
BEFORE INSERT ON posts
FOR EACH ROW EXECUTE PROCEDURE create_post_path();
