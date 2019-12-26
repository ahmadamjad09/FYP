from app.User import User
from app.Application import Application
class Controller:
    def __init__(self):
        self.__user=User()
        self.__application=Application()
    def getUser(self,id):
        return self.__user.getName(id)
    def getEmpolyees(self):
        return self.__user.getEmployes()
    def getDocumentCreated(self,id):
        return self.__application.getDocumentsCreated(id)
    def getForwardToName(self,appid):
        id=self.__application.getForwardToId(appid)
        return self.__user.getName(id)
    def getApplicationDetail(self,appid):
        return self.__application.getApplicationDetail(appid)
    def getForwardtodetail(self,appid):
        return self.__user.getForwardtoDetail(appid)
    def getDocumentToSign(self,id):
        return self.__application.getDocumenttoSign(id)
    def getEmployeeDesignation(self,id):
        return self.__user.getEmployeeDesignation(id)
    def setCommentHistory(self, appid, comment, forward, action, designation, name):
       return self.__application.setCommentHistory(appid,comment,forward,action,designation,name)
    def setLoginRequest(self, subject, bilding, floor, room, window, emial_account, print_quota, linux_account, fom, to, mac, purpose, content,forward,uid,files):
        self.__application.setLoginRequest(subject,bilding,floor,room,window,emial_account,print_quota,linux_account,fom,to,mac,purpose,content,forward,uid,files)
    def setMacineRequest(self, subject, bilding, floor, room, linux_flavour, comment, content, forward, uid, software,os, files):
        self.__application.setMacineRequest(subject, bilding, floor, room, linux_flavour, comment, content, forward, uid, software,os, files)
    def setNetwokRequest(self, subject, bilding, floor, room, fom, to, content, forward, uid):
        self.__application.setNetwokRequest(subject,bilding,forward,room,fom,to,content,forward,uid)
    def setPrintRequest(self, subject, pages, content, forward, uid):
        self.__application.setPrintRequest(subject,pages,content,forward,uid)
    def setMailRequest(self, subject, gb, content, forward, uid):
        self.__application.setMailRequest(subject, gb, content, forward, uid)
    def setPasswordResetRequest(self, subject, content, forward, uid):
        self.__application.setPasswordResetRequest(subject,content,forward,uid)
    def setGeneralApplication(self, subject, content, forward, uid, files):
        self.__application.setGeneralApplication(subject, content, forward, uid, files)
    def setHostedResearcher(self,id,name,dob,cnic,qualification,academic_record,present_status,designation,enrollemnt_no,uni,department,permanent_address,mailing_address,landline,cell,email,researcher_category,department_NCP,duration_NCP,supervisor_from_NCP,cosupervisor_from_NCP,picture,supervisor_naame,supervisor_departmen,tendate,gender,province,city):
         self.__user.setHostedResearcher(id,name,dob,cnic,qualification,academic_record,present_status,designation,enrollemnt_no,uni,department,permanent_address,mailing_address,landline,cell,email,researcher_category,department_NCP,duration_NCP,supervisor_from_NCP,cosupervisor_from_NCP,picture,supervisor_naame,supervisor_departmen,tendate,gender,province,city)
    def setUserDetail(self,name,username,email,password):
        self.__user.setUserDetail(name, username, email, password)
    def loginUser(self,username,password):

        return self.__user.loginUser(username,password)
    def getHostedDeail(self,id):
        return self.__user.getHostedDetail(id)
    def getHostedUsername(self,id):
        return self.__user.getHostedusername(id)
    def getCaadRequest(self):
        return self.__user.getCaadRequest()
    def sethostedRequest(self,id):
        self.__user.sethostedRequest(id)
    def sethostednewid(self,id,newid):
        self.__user.sethostednewid(id,newid)
    def deleteCaadRequest(self,id):
        self.__user.deleteCaadRequest(id)
    def setSoftwareRequest(self,subject,content,forward,uid,software_name,type):
        self.__application.setSoftwareRequest(subject,content,forward,uid,software_name,type)
    def setClusterRequest(self, subject, content, forward, uid, university, compiler, packages, fom, to,file):
        self.__application.setClusterRequest(subject,content,forward,uid,university,compiler,packages,fom,to,file)
    def setItClearance(self,suject,content,forward,uid):
        self.__application.setItClearance(suject,content,forward,uid)
    def setITequipments(self, subject, content, forward, uid, location, timefrom, timeto, datefrom, dateto, laptop,
                        mouse, keyboard, speaker,
                        persenter, pointer, projector, microphone, hdmi, tripod):
        self.__application.setITequipments(subject, content, forward, uid, location, timefrom, timeto, datefrom, dateto, laptop,
                           mouse, keyboard, speaker, persenter, pointer, projector, microphone, hdmi, tripod)
    def setwebsiteRequest(self,subject,content,forward,uid):
        self.__application.setwebsiteRequest(subject,content,forward,uid)
    def setcolorprintRequest(self,sucject,content,forward,uid):
        self.__application.setColorprintRequest(sucject,content,forward,uid)
    def settelophone(self, subject, content, forward, uid, building, floor, room, telephone, extension, national,
                     internationl):
        self.__application.settelophone(subject,content,forward,uid,building,floor,room,telephone,extension,national,internationl)
    def gethoste(self):
        return self.__user.gethosted()
    def getEmployeeid(self,name):
        return self.__user.getEmployeeid(name)
    def verifiedMail(self,id):
        self.__user.verifirdMail(id)
    def getVerifiedMail(self,id):
        return self.__user.getVerifiedMail(id)
    def getLoginDetail(self,id):
        return self.__user.getLoginDetail(id)
    def getEmployeeDepartment(self,id):
        return self.__user.getEmployeeDepartment(id)
    def getDob(self,id):
        return self.__user.getDob(id)
    def getfile(self,appid):
        return self.__application.getfile(appid)
    def getfiledetail(self,fileid):
        return self.__application.getfileDetail(fileid)
    def getDesignation(self,id):
        return self.__user.getDesignation(id)
    def getEmail(self,id):
        return self.__user.getEmail(id)


