import unittest
import sqlalchemy
from hermessplitter.db import init_db
from hermessplitter.db import db_funcs
from hermessplitter.db import tables


class TestCase(unittest.TestCase):
    def test_insert_record(self):
        record_id = 1
        result = db_funcs.create_new_record(record_id=record_id,
                                            clear_gross=5000,
                                            hermes_gross=2000,
                                            final_gross=7000,
                                            clear_cargo=3000,
                                            hermes_cargo=2000,
                                            final_cargo=5000,
                                            tare=2000,
                                            notes='SELLO'
                                            )
        self.assertTrue(isinstance(result.inserted_primary_key[0], int))
        tables.records.delete(tables.records.c.record_id == record_id)

    @unittest.SkipTest
    def test_insert_client(self):
        client_name = 'САХ, ООО'
        kf = 20
        ex_id = 123
        result = db_funcs.create_or_upd_client(name=client_name,
                                               ex_id=ex_id)
        self.assertTrue(isinstance(result.inserted_primary_key[0], int))
        new_kf = 50
        result = db_funcs.create_or_upd_client(name=client_name,
                                               ex_id=ex_id)
        kf_r = db_funcs.get_client_kf_by_name(client_name)
        print('CLIENTS:', db_funcs.get_all_data(tables.clients))
        r = sqlalchemy.delete(tables.clients).where(
            tables.clients.c.name.like(client_name))
        init_db.engine.execute(r)

    def test_settings(self):
        db_funcs.set_settings(active=False)
        ins = tables.settings.select()
        r = init_db.engine.execute(ins)
        activity = db_funcs.get_hermes_activity()
        self.assertEqual(activity[0], '0')

    def test_get_records(self):
        db_funcs.create_new_record(123, 500, 200, 700)
        db_funcs.create_new_record(123, 500, 200, 700)
        records = db_funcs.get_records()
        print("RECORDS", records)


    def test_get_record(self):
        record_info = db_funcs.get_record(1)
        print("RI", record_info)


    def test_get_few_records(self):
        records = [205209, 205208]
        result = db_funcs.get_few_records_dict('1, 123')
        print("RESULT", result)

if __name__ == '__main__':
    unittest.main()
