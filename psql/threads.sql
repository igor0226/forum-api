CREATE OR REPLACE FUNCTION update_thread_votes_counter() RETURNS TRIGGER AS
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

CREATE OR REPLACE TRIGGER t_votes
AFTER INSERT OR UPDATE ON thread_votes
FOR EACH ROW EXECUTE PROCEDURE update_thread_votes_counter();

CREATE OR REPLACE FUNCTION update_forum_threads_counter() RETURNS TRIGGER AS
$$
    BEGIN
        UPDATE forums
        SET threads = threads + 1
        WHERE slug = NEW.forum;

        RETURN NEW;
    END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER t_threads_counter
AFTER INSERT ON threads
FOR EACH ROW EXECUTE PROCEDURE update_forum_threads_counter();
