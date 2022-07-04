import mysql.connector


def copy_data(connection1, connection2, query_stmt, insert_stmt):
    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()
        try:
            cursor1.execute(query_stmt)
            list_of_rows = cursor1.fetchall()

            cursor2.executemany(insert_stmt, list_of_rows)
            connection2.commit()
            return True
        except mysql.connector.Error:
            connection2.rollback()
            print("Failed to insert into MySQL table")
            return False
    except mysql.connector.Error as error:
        print("Failed to connect to database ".format(error))
