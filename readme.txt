Part I

First, I had to simulate the environment. Because I was working on Windows I prepared two MySQL connections located on other ports. The first database was at port 3307 and contained data in the table ‘titles’, while the second database was at port 3308 and had no data in table ‘titles’. To copy data from one database to another I wrote the script (file copy_data.py) that takes 4 arguments:
- connection1 – this is connection to database that has data in table ‘titles’ and from which we will copy data
- connection2 -  this is connection to database that has no data in table ‘titles’ and to which we will copy data
- query_stmt – this is SQL query executed on database from which we have data to copy. In our case I used ‘SELECT * FROM titles’ to store rows in list 
- insert_stmt – this is SQL query executed on database to which we want to copy data. In this case we need to match query to the structure of the table. 

The logic of this script is as follows:
- first, I connect to both databases (cn1, cn2) with appropriate parameters and create two cursors to be able to perform operations on databases
- next I execute SQL query ‘SELECT * FROM titles’ on first database to fetch all rows and store it in list of tuples
- now with the help of cursor method ‘executemany’ I use it on second database to place data. This method takes two arguments: first is ‘INSERT’ statement and second is list of rows from previous paragraph
- if everything is correct I send all changes to second database with the help of mysql.connector method ‘commit’
- at the end  close both connections

Unit Test

To test validity of the code I used the library ‘unittest’. For this purpose, I decided to connect to my both databases, then before test create two temporary tables, which are deleted at the end of the session, call my script, and compare whether after this when I call SQL ‘SELECT’ statement on both databases both lists will be equal. 
The logic of Unit Test is as follows:
- first I define setUp() method which is executed before each test and tearDown() method which is executed after each test
- in setUp() method I connect to both databases and create temporary tables,  in first database with data from titles, for example with 10 rows and in second database without any data.
- in tearDown() method I am ending sessions of both connections to get rid of temporary tables
- main test is in test_copy(). First, I call my script with both connections and ‘SELECT’ statement and ‘INSERT’ statement accordingly with new temporary tables. Then I create two cursors for both connections and for each database I store all rows in list. At the end I compare two lists whether are equal 

During creating this test, I had two problems. First, when I tried test my main script (copy_data.py) the entire program was executed along with the function call in main script, so test affected the actual databases. For this reason I have function copy_data() to new file ‘copy_data_for_test.py’ without any calling, only with this function. Also, I had problem with sessions management. Because I was using temporary tables which are removed after end of session, I had error with connection to databases. When I start test I initiate new connections to databases in setUp() method. During test I refer to the copy_data() function where after successful commit to database I close sessions. But in test I want to check whether in databases we have the same data, so I need to execute again SQL query. But if I closed sessions in copy_data(), temporary tables have been removed and I have no access to this connections. So in new file to test: ‘copy_data_for_test.py’ I removed part where I close sessions because in test tearDown() method is responsible for close sessions. After this my tests passed. 

Part II
In this part I will try to measure program efficiency. For this reason, I will focus on execution time and memory consumption. 

Execution time

We have large amount of data to copy (443308 rows), so we need to find solution to optimize execution time during storing data in list and inserting data into new database. When I started writing script I found two cursor methods, which allows to insert data into database: ‘execute’ and ‘executemany’. If we use ‘execute’ we insert one rows at one time with these instructions, so we need use ‘for loop’ to loop through list of rows and in each iteration insert row. When I was testing this option execution time of this program was about 2 minutes for this large amount of data. But when I used ‘executemany’, where we pass to parameters, insert statement and list of rows execution time dropped to about 16 seconds.
Also, during production of the code, I had one additional function where I connect to database where I want to fetch data and return list of rows. For example: 

def get_data_to_list(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

And after this I passed this list to function where I inserted this data to new database (of course with ‘executemany’ method). Execution time of program using such logic was about 23 seconds. In my final solution I have one function in which I perform all operations and execution time is 16 second.

Memory consumption

In this case to reduce memory consumption of program I tried to get rid of storage list of rows in variable. For this reason, I placed all procedures in one program. Also, in my final solution first, I placed list of rows in variable and then passed it to ‘executemany’ method. When I passed directly ‘cursor1.fetchall()’ method instead of put it to variable and then pass it to ‘executemany’, then memory consumption dropped from 155MB to 48MB. 
Also, when I checked memory consumption when program was using ‘execute’ method and ‘for loop’, then memory consumption was at the level of 27MB all the time, but program lasted much longer.

Because this program is designed to copy data, often a very large amount of data we need to finding solution which provides us improvements in previously mentioned aspects like execution time and memory consumption. When we write program, we need to consider whether we need faster program or maybe when we transfer data in real time and we do not transmit such a large amount of data at one time we may want reduce hardware load, because during transmit small amount of data execution time is slight.



