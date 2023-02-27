import argparse

from sqlalchemy import text, MetaData

from models import Base
from database import db_engine


def drop_table(table: str):
    print(f"Attempting to delete table: {table}")
    db_engine.execute(text(f"DROP table IF EXISTS {table} CASCADE"))
    db_engine.dispose()
    print(f"Deleted table {table}")


def drop_all_tables():
    print("Dropping all tables")
    metadata = MetaData()
    metadata.reflect(bind=db_engine)
    for table in metadata.tables.values():
        drop_table(table)

def make_migrations():
    print("Making migrations")
    pass


def recreate_db():
    print("Recreating database")
    Base.metadata.create_all(bind=db_engine) 


def __get_parser_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)    
    
    group.add_argument("--drop", type=str, help="Drop a specific table from DB")
    group.add_argument("--drop-all", action="store_true", help="Drop all tables")
    group.add_argument("--make-migrations", action="store_true", help="Make DB migratiosn")
    group.add_argument("--recreate", action="store_true", help="Recreate db")

    return parser.parse_args()    

if __name__ == "__main__":
    args = __get_parser_args()
    
    if args.drop:
        drop_table(args.drop)
    elif args.drop_all:
        drop_all_tables()
    elif args.make_migrations:
        make_migrations()
    elif args.recreate:
        recreate_db()
    else:
        print("No specific argument to run")

