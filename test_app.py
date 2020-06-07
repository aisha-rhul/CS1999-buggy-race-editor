import unittest
import app
import sqlite3 as sql


# Unit tests for Buggy project
class MyTestCase(unittest.TestCase):
    # Test function to check return values
    def test_validate_integer(self):
        self.assertEqual(app.validate_integer(5, 3), True)
        self.assertEqual(app.validate_integer(4, 4), True)
        self.assertEqual(app.validate_integer(3, 4), False)
        self.assertEqual(app.validate_integer(-3, 4), False)
        self.assertEqual(app.validate_integer(3, -4), True)
        self.assertEqual(app.validate_integer(0, -4), True)
        self.assertEqual(app.validate_integer(0, 0), True)

    # Test for record retrieval
    def test_get_buggy_record(self):
        con = sql.connect("database.db")
        cur = con.cursor()
        record = []
        cur.execute("SELECT * FROM Buggy WHERE id=1;")
        for row in cur.fetchall():
            record = row

        self.assertEqual(app.get_buggy_record(1), record)

    # Test for value of last buggy id in database
    def test_get_last_buggy_id(self):
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT id FROM Buggy ORDER BY id DESC LIMIT 1")
        for row in cur.fetchall():
            buggy_id = row[0]

        self.assertEqual(app.get_last_buggy_id(), buggy_id)

    # Test for all record retrieval
    def test_get_records(self):
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        
        cur.execute("SELECT * FROM Buggy")
        records = cur.fetchall()

        self.assertEqual(app.get_records(), records)

    # Testing for delete operation
    def test_delete_buggy_message(self):
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute("DELETE FROM Buggy WHERE id = 1")
        con.commit()

        self.assertEqual(app.delete_buggy(1), "Buggy deleted")


if __name__ == '__main__':
    unittest.main()
