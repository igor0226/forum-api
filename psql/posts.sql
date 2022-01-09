CREATE OR REPLACE FUNCTION create_post_path() RETURNS TRIGGER AS
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

CREATE OR REPLACE TRIGGER t_path
BEFORE INSERT ON posts
FOR EACH ROW EXECUTE PROCEDURE create_post_path();

CREATE OR REPLACE FUNCTION update_forum_posts_counter() RETURNS TRIGGER AS
$$
    BEGIN
        UPDATE forums
        SET posts = posts + 1
        WHERE slug = NEW.forum;

        RETURN NEW;
    END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER t_posts_counter
AFTER INSERT ON posts
FOR EACH ROW EXECUTE PROCEDURE update_forum_posts_counter();

CREATE OR REPLACE FUNCTION handle_post_is_edited() RETURNS TRIGGER AS
$$
    BEGIN
        IF NEW.message != OLD.message THEN
            NEW.isEdited = TRUE;
        END IF;

        RETURN NEW;
    END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER t_posts_is_edited
BEFORE UPDATE ON posts
FOR EACH ROW EXECUTE PROCEDURE handle_post_is_edited();

CREATE OR REPLACE FUNCTION check_posts_root(parent_post_ids BIGINT[], thread_id BIGINT)
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
            INSERT INTO temp_distinct_ids (post_id) VALUES(i);
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

CREATE OR REPLACE FUNCTION get_post_related_info(post_id_to_find BIGINT)
RETURNS TABLE(
    post_id BIGINT,
    post_created TIMESTAMP WITH TIME ZONE,
    post_isEdited BOOLEAN,
    post_message TEXT,
    post_parent BIGINT,
    post_forum CITEXT,
    post_thread BIGINT,
    post_author CITEXT,

    author_about TEXT,
    author_email CITEXT,
    author_fullname TEXT,
    author_nickname CITEXT,

    forum_id BIGINT,
    forum_posts BIGINT,
    forum_slug CITEXT,
    forum_threads BIGINT,
    forum_title TEXT,
    forum_author CITEXT,

    thread_id BIGINT,
    thread_author CITEXT,
    thread_created TIMESTAMP WITH TIME ZONE,
    thread_forum CITEXT,
    thread_message TEXT,
    thread_slug CITEXT,
    thread_title TEXT,
    thread_votes BIGINT
) AS
$$
    BEGIN
        RETURN QUERY SELECT
            posts.id AS post_id,
            posts.created AS post_created,
            posts.isEdited AS post_isEdited,
            posts.message AS post_message,
            posts.parent AS post_parent,
            posts.forum AS post_forum,
            posts.thread AS post_thread,
            posts.author AS post_author,

            users.about AS author_about,
            users.email AS author_email,
            users.fullname AS author_fullname,
            users.nickname AS author_nickname,

            forums.id AS forum_id,
            forums.posts AS forum_posts,
            forums.slug AS forum_slug,
            forums.threads AS forum_threads,
            forums.title AS forum_title,
            forums.author AS forum_author,

            threads.id AS thread_id,
            threads.author AS thread_author,
            threads.created AS thread_created,
            threads.forum AS thread_forum,
            threads.message AS thread_message,
            threads.slug AS thread_slug,
            threads.title AS thread_title,
            threads.votes AS thread_votes
        FROM posts
        JOIN users ON posts.author = users.nickname
        JOIN forums ON posts.forum = forums.slug
        JOIN threads ON posts.thread = threads.id
        WHERE posts.id = post_id_to_find;
    END
$$ LANGUAGE plpgsql;
