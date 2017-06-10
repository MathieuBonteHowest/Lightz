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


    def getUser(self, username):
        # Query met parameters
        sqlQuery = "SELECT password FROM tbl_users WHERE login = '{param1}'"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=username)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchone()
        self.__cursor.close()
        return result

    def getStatus(self):
        sqlQuery = "SELECT StatusID FROM tbl_overzicht ORDER BY ID"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def register(self, username, password):
        #Query met parameters
        sqlQuery = "Select ID from tbl_users WHERE Login = '{param1}'"
        sqlCommand = sqlQuery.format(param1=username)
        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchone()

        if result:
            message = "Error: Deze gebruiker bestaat al"
        else:
            sqlQuery2 = "INSERT INTO tbl_users (Login, Password) VALUES ('{param1}', '{param2}')"
            sqlCommand2 = sqlQuery2.format(param1=username, param2=password)

            self.__cursor.execute(sqlCommand2)
            self.__connection.commit()
            self.__cursor.close()

            message = "Succesvol geregistreerd"

        return message

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


    # def getDataFromDatabase(self):
    #     # Query zonder parameters
    #     sqlQuery = "SELECT * FROM tablename"
    #
    #     self.__cursor.execute(sqlQuery)
    #     result = self.__cursor.fetchall()
    #     self.__cursor.close()
    #     return result
    #
    # def getDataFromDatabaseMetVoorwaarde(self, voorwaarde):
    #     # Query met parameters
    #     sqlQuery = "SELECT * FROM tablename WHERE columnname = '{param1}'"
    #     # Combineren van de query en parameter
    #     sqlCommand = sqlQuery.format(param1=voorwaarde)
    #
    #     self.__cursor.execute(sqlCommand)
    #     result = self.__cursor.fetchall()
    #     self.__cursor.close()
    #     return result
    #
    # def setDataToDatabase(self, value1):
    #     # Query met parameters
    #     sqlQuery = "INSERT INTO tablename (columnname) VALUES ('{param1}')"
    #     # Combineren van de query en parameter
    #     sqlCommand = sqlQuery.format(param1=value1)
    #
    #     self.__cursor.execute(sqlCommand)
    #     self.__connection.commit()
    #     self.__cursor.close()