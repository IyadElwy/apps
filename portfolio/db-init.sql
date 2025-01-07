CREATE TABLE Movies(
    id INTEGER PRIMARY KEY,
    normalized_title TEXT UNIQUE,
    title TEXT UNIQUE,
    year TEXT,
    rated TEXT,
    released TEXT,
    runtime TEXT,
    genre TEXT,
    director TEXT,
    writer TEXT,
    actors TEXT,
    plot TEXT,
    language TEXT
)