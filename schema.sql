CREATE TABLE accounts (
    id TEXT NOT NULL,
    secret TEXT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE articles (
    name TEXT NOT NULL,
    id TEXT NOT NULL,
    PRIMARY KEY (name)
);
