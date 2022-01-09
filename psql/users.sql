CREATE OR REPLACE FUNCTION get_all_forum_users(forum_slug CITEXT)
RETURNS SETOF users AS
$$
    BEGIN
        DROP TABLE IF EXISTS temp_nicknames;
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
      END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION check_users_nicknames(authors CITEXT[])
RETURNS BOOLEAN AS
$$
    DECLARE
        author_nickname CITEXT;
        found_users_len INTEGER;
    BEGIN
        DROP TABLE IF EXISTS temp_users;
        CREATE TEMPORARY TABLE temp_users(
            nickname CITEXT
        );

        FOREACH author_nickname IN ARRAY authors LOOP
            INSERT INTO temp_users (nickname) VALUES (author_nickname);
        END LOOP;

        SELECT COUNT(temp_users)
        INTO found_users_len
        FROM temp_users JOIN users
        ON temp_users.nickname = users.nickname;

        IF found_users_len != array_length(authors, 1) THEN
            RETURN FALSE;
        END IF;

        RETURN TRUE;
    END
$$ LANGUAGE plpgsql;
