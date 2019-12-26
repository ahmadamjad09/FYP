from app.DB import Database
class User:
    def __init__(self):
        self.__db=Database()
    def getName(self,id):
        return self.__db.getusername(id)
    def getEmployes(self):
        return self.__db.getEmployes()
    def getForwardtoDetail(self,appid):
        return self.__db.getforwardTodetail(appid)
    def getEmployeeDesignation(self,id):
        return self.__db.getEmployeeDesignation(id)
    def setHostedResearcher(self,id,name,dob,cnic,qualification,academic_record,present_status,designation,enrollemnt_no,uni,department,permanent_address,mailing_address,landline,cell,email,researcher_category,department_NCP,duration_NCP,supervisor_from_NCP,cosupervisor_from_NCP,picture,supervisor_naame,supervisor_departmen,tendate,gender,province,city):
         self.__db.setHostedResearcher(id,name,dob,cnic,qualification,academic_record,present_status,designation,enrollemnt_no,uni,department,permanent_address,mailing_address,landline,cell,email,researcher_category,department_NCP,duration_NCP,supervisor_from_NCP,cosupervisor_from_NCP,picture,supervisor_naame,supervisor_departmen,tendate,gender,province,city)
    def setUserDetail(self,name,username,email,password):
        self.__db.setUserDetail(name, username, email, password)
    def loginUser(self,username,password):
        return self.__db.loginUser(username,password)
    def getHostedDetail(self,id):
        return self.__db.getHostedDetail(id)
    def getHostedusername(self,id):
        return self.__db.getHostedusername(id)
    def getCaadRequest(self):
        return self.__db.getCaadRequest()
    def sethostedRequest(self,id):
        self.__db.sethostedRequest(id)
    def sethostednewid(self,id,newid):
        self.__db.sethostedNewid(id,newid)
    def deleteCaadRequest(self,id):
        self.__db.deleteCaadRequest(id)
    def gethosted(self):
        row=self.__db.gethoste()
        return row
    def getEmployeeid(self,name):
       return self.__db.getEmployeeId(name)
    def verifirdMail(self,id):
        self.__db.verifiedMail(id)
    def getVerifiedMail(self,id):
        return self.__db.getverifiedMail(id)
    def getLoginDetail(self,id):
        return self.__db.getloginDetail(id)
    def getEmployeeDepartment(self,id):
        return self.__db.getEmployeeDepartment(id)
    def getDob(self,id):
        return self.__db.getDob(id)
    def getDesignation(self,id):
        return self.__db.getDesignation(id)
    def getEmail(self,id):
        return self.__db.getEmail(id)


