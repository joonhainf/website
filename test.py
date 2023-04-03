from app import db, create_app
app = create_app()
with app.app_context():
    print(db.engine.table_names())

from sqlalchemy import create_engine, MetaData

engine = create_engine('sqlite:///messages.db')
metadata = MetaData()

metadata.reflect(bind=engine)
print(metadata.tables.keys())