import sqlalchemy.exc
from sqlalchemy import create_engine
from hermessplitter.db import tables
import os

dbpath = os.environ.get('HDBPATH')
print('DBPATH', dbpath)
dbpath = f"sqlite:///{dbpath}"
#dbpath = 'sqlite:///'
if not os.path.exists(dbpath):
    engine = create_engine(dbpath)
    engine.connect()
    tables.metadata.create_all(engine)

try:
    ins = tables.settings.insert().values(
        key='active',
        value=True
    )
    engine.execute(ins)
except sqlalchemy.exc.IntegrityError:
    pass

try:
    ins = tables.settings.insert().values(
        key='test_mode',
        value=True
    )
    engine.execute(ins)
except sqlalchemy.exc.IntegrityError:
    pass

