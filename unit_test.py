import unittest
import mysql.connector
from copy_data_for_test import copy_data


class Test(unittest.TestCase):
    connection1 = None
    connection2 = None

    def setUp(self):
        config1 = {
            'host': 'localhost',
            'user': 'root',
            'password': 'root',
            'database': 'employees',
            'port': 3307
        }
        self.connection1 = mysql.connector.connect(**config1)

        config2 = {
            'host': 'localhost',
            'user': 'root',
            'password': 'root',
            'database': 'employees',
            'port': 3308
        }

        self.connection2 = mysql.connector.connect(**config2)

        create_temp_table1 = 'CREATE TEMPORARY TABLE temp_titles (select * from employees.titles LIMIT 5)'
        cursor1 = self.connection1.cursor()
        cursor1.execute(create_temp_table1)

        create_temp_table2 = 'CREATE TEMPORARY TABLE temp_titles (select * from employees.titles)'
        cursor2 = self.connection2.cursor()
        cursor2.execute(create_temp_table2)

    def tearDown(self):
        if self.connection1 is not None and self.connection1.is_connected():
            self.connection1.close()
        if self.connection2 is not None and self.connection2.is_connected():
            self.connection2.close()

    def test_copy(self):
        copy_data(self.connection1, self.connection2, 'SELECT * FROM temp_titles', 'INSERT INTO temp_titles (emp_no, '
                                                                                   'title, from_date, to_date) VALUES'
                                                                                   ' (%s, %s, %s, %s)')
        query = 'SELECT * FROM temp_titles'

        cursor1 = self.connection1.cursor()
        cursor1.execute(query)
        data1 = cursor1.fetchall()
        print(data1)

        cursor2 = self.connection2.cursor()
        cursor2.execute(query)
        data2 = cursor2.fetchall()
        print(data2)

        self.assertListEqual(data1, data2)


