CREATE OR REPLACE FUNCTION get_all_tables_count()
RETURNS TABLE(
    forums_len BIGINT,
    posts_len BIGINT,
    threads_len BIGINT,
    users_len BIGINT
)
AS $$
    BEGIN
        DROP TABLE IF EXISTS temp_all_tables_count;
        CREATE TEMPORARY TABLE temp_all_tables_count(
            p_forums_len BIGINT,
            p_posts_len BIGINT,
            p_threads_len BIGINT,
            p_users_len BIGINT
        );

        INSERT INTO temp_all_tables_count (
            p_forums_len,
            p_posts_len,
            p_threads_len,
            p_users_len
        )
        VALUES (
            (SELECT COUNT(*) FROM forums),
            (SELECT COUNT(*) FROM posts),
            (SELECT COUNT(*) FROM threads),
            (SELECT COUNT(*) FROM users)
        );

        RETURN QUERY SELECT p_forums_len AS forums_len,
            p_posts_len AS posts_len,
            p_threads_len AS threads_len,
            p_users_len AS users_len
        FROM temp_all_tables_count;
    END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION clear_all_tables() RETURNS BOOLEAN
AS $$
    BEGIN
        TRUNCATE posts CASCADE;
        TRUNCATE threads CASCADE;
        TRUNCATE forums CASCADE;
        TRUNCATE users CASCADE;
        TRUNCATE thread_votes CASCADE;

        RETURN TRUE;
    END
$$ LANGUAGE plpgsql;