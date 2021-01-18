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
	FOREIGN KEY (USERNAME)
    REFERENCES USERS(USERNAME) ON DELETE CASCADE
    );""",
    """CREATE TABLE if not exists USER_STATS
    (
    USERNAME character varying(64) NOT NULL,
	UPLOADED_COUNT INTEGER DEFAULT 0,
    LABELED_COUNT INTEGER DEFAULT 0,
	DOWNLOADED_COUNT INTEGER DEFAULT 0,
    PRIMARY KEY (USERNAME),
    FOREIGN KEY (USERNAME)
    REFERENCES USERS(USERNAME) ON DELETE CASCADE
    );""",
    """CREATE TABLE if not exists LABEL_CATEGORIES
    (
    LABELED_AS character varying(255) NOT NULL,
	TOTAL_COUNT INTEGER,
    TOTAL_DOWNLOAD INTEGER,
    PRIMARY KEY (LABELED_AS),
    UNIQUE(LABELED_AS)
    );""",
    """CREATE TABLE if not exists IMAGES
    (
    IMAGE_ID INTEGER NOT NULL,
	IMAGE_PATH character varying(255) NOT NULL,
    HEIGHT INT NOT NULL,
	WIDTH INT NOT NULL,
    USERNAME character varying(64) NOT NULL,
    PRIMARY KEY (IMAGE_ID),
    UNIQUE (IMAGE_ID),
	FOREIGN KEY (USERNAME)
    REFERENCES USERS(USERNAME) ON DELETE CASCADE
    );""",
    """CREATE TABLE if not exists IMAGE_STATS
    (
    IMAGE_ID INTEGER NOT NULL,
	TOTAL_COUNT_LABEL INTEGER DEFAULT 0,
    TOTAL_COUNT_DOWNLOAD INTEGER DEFAULT 0,
    LABELED_AS character varying(255) NOT NULL,
    PRIMARY KEY (IMAGE_ID),
	FOREIGN KEY (IMAGE_ID)
    REFERENCES IMAGES(IMAGE_ID) ON DELETE CASCADE,
    FOREIGN KEY (LABELED_AS)
    REFERENCES LABEL_CATEGORIES(LABELED_AS) ON DELETE CASCADE
    );"""
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)