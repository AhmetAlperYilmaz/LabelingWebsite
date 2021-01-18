import os
import sys

import psycopg2 as dbapi2

INIT_STATEMENTS = [
    """CREATE TABLE if not exists USERS
    (
    USERNAME character varying(64) NOT NULL,
    PASSWORD character varying(255) NOT NULL,
    PRIMARY KEY (USERNAME),
    UNIQUE (USERNAME)
    );""",
    """CREATE TABLE if not exists USER_INFO
    (
	EMAIL character varying(64) NOT NULL,
    USERNAME character varying(64) NOT NULL,
	NAME character varying(64) DEFAULT NULL,
    SURNAME character varying(64) DEFAULT NULL,
    PRIMARY KEY (EMAIL),
    UNIQUE (EMAIL),
    CONSTRAINT USERNAME
	FOREIGN KEY (USERNAME)
    REFERENCES USERS(USERNAME) ON DELETE CASCADE
    );""",
    """CREATE TABLE if not exists USER_STATS
    (
    USERNAME character varying(64) NOT NULL,
	UPLOADED_COUNT INTEGER,
    LABELED_COUNT INTEGER,
	DOWNLOADED_COUNT INTEGER,
    PRIMARY KEY (USERNAME),
    FOREIGN KEY (USERNAME)
    REFERENCES USERS(USERNAME) ON DELETE CASCADE
    );"""
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = "dbname='LabelingDB' user='postgres' host='localhost' password='KingHarlaus26'"
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)