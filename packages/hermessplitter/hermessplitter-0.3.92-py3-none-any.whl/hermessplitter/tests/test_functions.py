import os
import unittest
from wsqluse.wsqluse import Wsqluse
from hermessplitter import functions


class TestCase(unittest.TestCase):
    sql_shell = Wsqluse(
        dbname=os.environ.get('DBNAME'),
        host=os.environ.get('DBHOST'),
        user=os.environ.get('DBUSER'),
        password=os.environ.get('DBPASS')
    )

    def test_import_clients(self):
        clients = functions.import_clients(self.sql_shell)
        print("CLIENTS", clients)


if __name__ == '__main__':
    unittest.main()
