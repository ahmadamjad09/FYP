
class ReadPropety:
    def __init__(self):
        f = open("/home/ahmad/EDH/file.property", "r")
        for i in range(7):
            line = f.readline()
            linebreak = line.split()
            dump1 = linebreak[0]
            dump2 = linebreak[1]
            if dump2 == "server_Name":
                self.__server = dump1
            if dump2 == "NCP_Database_Name":
                self.__NCP = dump1
            if dump2 == "NCP_UserName":
                self.__NCPUserName = dump1
            if dump2 == "NCP_Password":
                self.__NCPPassword = dump1
            if dump2 == "EDH_Databese_Name":
                self.__EDHDabase_Name = dump1
            if dump2 == "EDH_UserName":
                self.__EDH_UserName = dump1
            if dump2 == "EDH_Password":
                self.__EDH_Password = dump1

    def getServerName(self):
        return self.__server

    def getNCPDatabaseName(self):
        return self.__NCP

    def getNCPUserName(self):
        return self.__NCPUserName

    def getNCPPassword(self):
        return self.__NCPPassword

    def getEDHDatabaseName(self):
        return self.__EDHDabase_Name

    def getEDH_UserName(self):
        return self.__EDH_UserName

    def getEDH_Password(self):
        return self.__EDH_Password
