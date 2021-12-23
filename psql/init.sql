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
  nickname CITEXT COLLATE ucs_basic UNIQUE
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
  pathArray BIGINT[],
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
        parent_post_path_array BIGINT[];
        new_post_path_array BIGINT[];
    BEGIN
        IF NEW.parent IS NOT NULL THEN
            SELECT pathArray
            INTO parent_post_path_array
            FROM POSTS
            WHERE id = NEW.parent;

            IF parent_post_path_array IS NOT NULL THEN
                new_post_path_array := array_append(parent_post_path_array, NEW.id);
            END IF;
        END IF;

        IF parent_post_path_array IS NULL THEN
            new_post_path_array := ARRAY[NEW.id]::BIGINT[];
        END IF;

        NEW.pathArray = new_post_path_array;

        RETURN NEW;
    END
$$ LANGUAGE plpgsql;

CREATE TRIGGER t_path
BEFORE INSERT ON posts
FOR EACH ROW EXECUTE PROCEDURE create_post_path();

CREATE FUNCTION update_forum_threads_counter() RETURNS TRIGGER AS
$$
    BEGIN
        UPDATE forums
        SET threads = threads + 1
        WHERE slug = NEW.forum;

        RETURN NEW;
    END
$$ LANGUAGE plpgsql;

CREATE TRIGGER t_threads_counter
AFTER INSERT ON threads
FOR EACH ROW EXECUTE PROCEDURE update_forum_threads_counter();

CREATE FUNCTION update_forum_posts_counter() RETURNS TRIGGER AS
$$
    BEGIN
        UPDATE forums
        SET posts = posts + 1
        WHERE slug = NEW.forum;

        RETURN NEW;
    END
$$ LANGUAGE plpgsql;

CREATE TRIGGER t_posts_counter
AFTER INSERT ON posts
FOR EACH ROW EXECUTE PROCEDURE update_forum_posts_counter();

CREATE FUNCTION get_all_forum_users(forum_slug CITEXT)
    RETURNS SETOF users AS $$
        BEGIN
            CREATE TEMPORARY TABLE temp_nicknames(
                nickname CITEXT
            );

            INSERT INTO temp_nicknames (nickname)
            SELECT DISTINCT t.author
            FROM threads AS t
            WHERE t.forum = forum_slug;

            INSERT INTO temp_nicknames (nickname)
            SELECT DISTINCT p.author
            FROM posts AS p
            WHERE p.forum = forum_slug;

            RETURN QUERY
            SELECT users.id, users.about, users.email, users.fullname, users.nickname
            FROM users
            INNER JOIN (
                SELECT DISTINCT t.nickname FROM
                temp_nicknames AS t
            ) AS unique_nicknames
            ON users.nickname = unique_nicknames.nickname;

            DROP TABLE temp_nicknames;
          END
    $$ LANGUAGE plpgsql;

CREATE FUNCTION handle_post_is_edited() RETURNS TRIGGER AS
$$
    BEGIN
        IF NEW.message != OLD.message THEN
            NEW.isEdited = TRUE;
        END IF;

        RETURN NEW;
    END
$$ LANGUAGE plpgsql;

CREATE TRIGGER t_posts_is_edited
BEFORE UPDATE ON posts
FOR EACH ROW EXECUTE PROCEDURE handle_post_is_edited();

CREATE FUNCTION check_posts_root(parent_post_ids BIGINT[], thread_id BIGINT)
RETURNS BOOLEAN AS
$$
    DECLARE
        i INTEGER;
        found_posts_len INTEGER;
    BEGIN
        DROP TABLE IF EXISTS temp_distinct_ids;
        CREATE TEMPORARY TABLE temp_distinct_ids (
            post_id BIGINT
        );

        FOREACH i IN ARRAY parent_post_ids LOOP
            INSERT INTO temp_distinct_ids (post_id) values(i);
        END LOOP;

        SELECT COUNT(posts.id)
        INTO found_posts_len
        FROM posts JOIN temp_distinct_ids
        ON posts.id = temp_distinct_ids.post_id
        WHERE posts.thread = thread_id;

        IF found_posts_len != array_length(parent_post_ids, 1) THEN
            RETURN FALSE;
        END IF;

        RETURN TRUE;
    END
$$ LANGUAGE plpgsql;
