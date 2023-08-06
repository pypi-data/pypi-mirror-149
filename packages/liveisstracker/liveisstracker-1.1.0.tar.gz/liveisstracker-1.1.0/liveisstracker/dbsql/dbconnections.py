import mysql.connector
from mysql.connector import errorcode
from mysql.connector import Error
try:
    from mylogger.iss_logging import logger
except ModuleNotFoundError:
    from ..mylogger.iss_logging import logger

#mysql -P 3606 -h localhost -u root --password=root


class MySql:

    config = {
        'user': 'root',
        'password': 'root',
        'host': 'liveisstracker_db_1',
        'port': '3306',
        'database': 'dev'
        }
    def __init__(self,silent=False):
        self.silent = silent
        try:
            self.connection = mysql.connector.connect(**self.config)
            logger.info('DB connection successful') if not self.silent else None
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.error('Incorrect user name or password') 
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.error('Database does not exist')
            elif err.errno == 2003:
                logger.error('Cant connect to Database') if not self.silent else None
            else:
                raise('Unknown Error connecting to Database')
    
    def insert_record(self,table_name,key_values):
        '''
        Function to insert records in the table.
        arg: table_name = Name of the table into which records to be inserted. (str)
        arg: key_values = Dictionary of key value pairs where key is the column name
                        value is the entry corresponding to that key.
        return: None'''

        if key_values == '':
            key_values = {}

        try:
            self.cursor = self.connection.cursor()
            add_record = ("INSERT INTO location "
                    "(lat,lon,datetime_id) "
                    " VALUES (%(lat)s, %(lon)s, %(datetime_id)s)")
            self.cursor.execute(add_record,key_values)
            self.connection.commit()
        except Exception as err:
            logger.error("Unable to insert records: Error: {}".format(err))
        
    def close_connection(self):
        self.cursor.close()
        self.connection.close()
