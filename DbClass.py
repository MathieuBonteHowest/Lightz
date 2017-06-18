import hashlib
import binascii
import os

class DbClass:
    def __init__(self):
        import mysql.connector as connector

        self.__dsn = {
            "host": "localhost",
            "user": "lightz",
            "passwd": "lightz",
            "db": "lightz"
        }

        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()


    def getUser(self, username, password):
        # Query met parameters
        sqlQuery = "SELECT pwd_hash, pwd_salt FROM tbl_users WHERE username = '{param1}'"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=username)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchone()

        if not result:
            return False

        db_hash_string = result[0]
        db_salt_string = result[1]

        pwd_bytes = password
        db_salt_bytes = binascii.unhexlify(db_salt_string)

        hash_bytes = hashlib.pbkdf2_hmac('sha256', pwd_bytes, db_salt_bytes, 100000)
        hash_string = binascii.hexlify(hash_bytes).decode('utf-8')
        self.__cursor.close()
        return hash_string == db_hash_string

    def getStatus(self):
        sqlQuery = "SELECT StatusID FROM tbl_overzicht ORDER BY ID"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def register(self, username, password, code):
        #Query met parameters
        sqlQuery = "Select * from tbl_users WHERE username = '{param1}'"
        sqlCommand = sqlQuery.format(param1=username)
        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchone()

        if int(code) == 25081998:
            if result:
                message = "Error: Deze gebruiker bestaat al"
            else:
                pwd_bytes = password
                salt_bytes = os.urandom(16)
                hash_bytes = hashlib.pbkdf2_hmac('sha256', pwd_bytes, salt_bytes, 100000)
                salt_string = binascii.hexlify(salt_bytes).decode('utf-8')
                hash_string = binascii.hexlify(hash_bytes).decode('utf-8')

                sqlQuery2 = "INSERT INTO tbl_users (username, pwd_hash, pwd_salt) VALUES ('{param1}', '{param2}', '{param3}')"
                sqlCommand2 = sqlQuery2.format(param1=username, param2=hash_string, param3=salt_string)

                self.__cursor.execute(sqlCommand2)
                self.__connection.commit()
                self.__cursor.close()

                message = "Succesvol geregistreerd"
        else:
            message = "Error: Foute code"

        return message

    def insertSensorValue(self, value):

        sqlQuery = "INSERT INTO tbl_sensor (SensorWaarde, Timestam) VALUES ('{param1}', CURRENT_TIMESTAMP )"
        sqlCommand = sqlQuery.format(param1=value)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def updateStatus(self, id, status):
        if id == 100:
            sqlQuery = "UPDATE tbl_overzicht SET StatusID = '{param2}' WHERE ID = 1 OR ID = 2 OR ID = 3 OR ID = 4 OR ID = 5 OR ID = 6 OR ID = 7"
            sqlCommand = sqlQuery.format(param2=status)
        else:
            sqlQuery = "UPDATE tbl_overzicht SET StatusID =  '{param2}' WHERE ID = '{param1}'"
            sqlCommand = sqlQuery.format(param1=id, param2=status)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()