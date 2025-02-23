CREATE TABLE IF NOT EXISTS "schema_migrations" (version varchar(128) primary key);
CREATE TABLE playlist (
  id INTEGER PRIMARY KEY,
  name TEXT,
  user TEXT,
  timestamp TEXT
) STRICT;
CREATE TABLE raw_track (
  id INTEGER PRIMARY KEY,
  playlist_id INTEGER,
  -- No JSON type - does this need to be BLOB if using JSONB?
  metadata TEXT,

  FOREIGN KEY (playlist_id) REFERENCES playlist(id)
) STRICT;
CREATE TABLE track (
  id INTEGER PRIMARY KEY,
  playlist_id INTEGER,
  name TEXT,
  link TEXT,
  isrc TEXT,
  artist TEXT,
  album TEXT,
  release_date TEXT,
  duration_ms INTEGER,
  popularity INTEGER,
  added_at TEXT,

  FOREIGN KEY (playlist_id) REFERENCES playlist(id)
) STRICT;
-- Dbmate schema migrations
INSERT INTO "schema_migrations" (version) VALUES
  ('20250223211527');
