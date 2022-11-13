import pymysql
import os

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

        self.connect()

    def connect(self):
        try:
            self.connection = pymysql.connect(host=os.getenv('HOST_DB', 'localhost'), user=os.getenv('USER_DB', 'root'),
                                              passwd=os.getenv('PASSWORD_DB', '1234'), database="ALERT-ME")
            self.cursor = self.connection.cursor()
        except pymysql.OperationalError as e:
            print(e)