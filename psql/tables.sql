DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS forums CASCADE;
DROP TABLE IF EXISTS threads CASCADE;
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS votes CASCADE;

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
