import os 
import sys


import psycopg2 as dbapi2

INIT_STATEMENTS = [
    """
    create table if not exists patient(
        id serial primary key,
        name varchar not null,
        mail text not null unique,
        password varchar not null
    )
    """
        ,
    """
    create table if not exists psychologist(
        id serial primary key,
        name varchar not null,
        mail text not null unique,
        address varchar not null unique,
        password varchar not null
    )
    """
        ,
    """
    create table if not exists appointment(
        id serial primary key,
        day varchar not null,
        time varchar not null,
        psychologist_id integer references psychologist(id) on delete set null on update cascade,
        patient_id integer references patient(id ) on delete set null on update cascade
    )
    """
        ,
    """
    create table if not exists point(
        id serial primary key,
        range integer default 0 not null,
        point integer default 0 not null,
        psychologist_id integer references psychologist(id) on delete set null on update cascade,
        patient_id integer references patient(id ) on delete set null on update cascade
    )
    """
        ,
    """
    create table if not exists comment(
        id serial primary key,
        comment varchar not null,
        psychologist_id integer references psychologist(id) on delete set null on update cascade,
        patient_id integer references patient(id ) on delete set null on update cascade
    )
    """
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
        print ("Usage: DATABASE_URL = url python dbinit.py")
        sys.exit(1)
    initialize(url)
