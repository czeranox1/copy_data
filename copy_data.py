import mysql.connector


config1 = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'employees',
    'port': 3307
}

config2 = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'employees',
    'port': 3308
}

def copy_data(connection1, connection2, query_stmt, insert_stmt):
    try:
        # create cursor to each database
        cursor1 = connection1.cursor()  # database with data in 'titles'
        cursor2 = connection2.cursor()  # database without data in 'titles'
        try:
            cursor1.execute(query_stmt)  # execute SQL query which extract data to copy
            cursor2.executemany(insert_stmt, cursor1.fetchall())  # prepared command to execute SQL operation (in this case for INSERT, first argument) for sequence of parameters (second argument)

            connection2.commit()  # send COMMIT statement to MySQL server
            # close sessions
            cursor2.close()
            connection2.close()
            cursor1.close()
            connection1.close()
            return True
        except mysql.connector.Error:  # in case of failure undo changes
            connection2.rollback()
            cursor2.close()
            connection2.close()
            cursor1.close()
            connection1.close()
            print("Failed to insert into MySQL table")
            return False
    except mysql.connector.Error as error:
        print("Failed to connect to database ".format(error))


cn1 = mysql.connector.connect(**config1) # database with data in 'titles'
cn2 = mysql.connector.connect(**config2) # database without data in 'titles'
query = 'SELECT * FROM titles'
insert = 'INSERT INTO titles (emp_no, title, from_date, to_date) VALUES (%s, %s, %s, %s)'
copy_data(cn1, cn2, query, insert)
