from app.DB import Database
class Application:
    def __init__(self):
        self.__db=Database()
    def getDocumentsCreated(self, id):
        return self.__db.getDocumentCreated(id)
    def getForwardToId(self,appid):
        return self.__db.getForwarodToId(appid)
    def getApplicationDetail(self,appid):
        return self.__db.getApplicationDetail(appid)
    def getDocumenttoSign(self,id):
        return self.__db.getDocumenttoSign(id)
    def setCommentHistory(self, appid, comment, forward, action, designation, name):
       return self.__db.setCommentHistory(appid,comment,forward,action,designation,name)
    def setLoginRequest(self, subject, bilding, floor, room, window, emial_account, print_quota, linux_account, fom, to, mac, purpose, content,forward,uid,files):
        self.__db.setLoginRequest(subject,bilding,floor,room,window,emial_account,print_quota,linux_account,fom,to,mac,purpose,content,forward,uid,files)
    def setMacineRequest(self, subject, bilding, floor, room, linux_flavour, comment, content, forward, uid, software,os, files):
        self.__db.setMacineRequest(subject, bilding, floor, room, linux_flavour, comment, content, forward, uid, software,os, files)
    def setNetwokRequest(self, subject, bilding, floor, room, fom, to, content, forward, uid):
        self.__db.setNetwokRequest(subject,bilding,forward,room,fom,to,content,forward,uid)
    def setPrintRequest(self, subject, pages, content, forward, uid):
        self.__db.setPrintRequest(subject,pages,content,forward,uid)
    def setMailRequest(self, subject, gb, content, forward, uid):
        self.__db.setMailRequest(subject,gb,content,forward,uid)
    def setPasswordResetRequest(self, subject, content, forward, uid):
        self.__db.setPasswordResetRequest(subject,content,forward,uid)
    def setGeneralApplication(self, subject, content, forward, uid, files):
        self.__db.setGeneralApplication(subject,content,forward,uid,files)
    def setSoftwareRequest(self,subject,content,forward,uid,software_name,type):
        self.__db.setSoftwareRequest(subject,content,forward,uid,software_name,type)
    def setClusterRequest(self, subject, content, forward, uid, university, compiler, packages, fom, to,file):
        self.__db.setClusterRequest(subject,content,forward,uid,university,compiler,packages,fom,to,file)
    def setItClearance(self,subject,conent,forward,uid):
        self.__db.setITClearance(subject,conent,forward,uid)
    def setITequipments(self, subject, content, forward, uid, location, timefrom, timeto, datefrom, dateto, laptop,
                        mouse, keyboard, speaker,
                        persenter, pointer, projector, microphone, hdmi, tripod):
        self.__db.setITequipments(subject,content,forward,uid,location,timefrom,timeto,datefrom,dateto,laptop,mouse,keyboard,speaker,persenter,pointer,projector,microphone,hdmi,tripod)
    def setwebsiteRequest(self,subject,content,forward,uid):
        self.__db.setwebsiteRequest(subject,content,forward,uid)
    def setColorprintRequest(self,subject,content,forward,uid):
        self.__db.setcolorprintRequest(subject,content,forward,uid)
    def settelophone(self, subject, content, forward, uid, building, floor, room, telephone, extension, national,
                     internationl):
        self.__db.settelophone(subject,content,forward,uid,building,floor,room,telephone,extension,national,internationl)
    def getfile(self,appid):
        return self.__db.getFile(appid)
    def getfileDetail(self,fileid):
        return self.__db.getFileDetail(fileid)