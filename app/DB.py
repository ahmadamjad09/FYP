import pyodbc
import datetime
from app.ReadProperty import ReadPropety
class Database:
       def __init__(self):
           self.__u=ReadPropety()
           # NCP databae connectivity
           self.__server2=self.__u.getServerName()
           self.__database2 = self.__u.getNCPDatabaseName()
           self.__username2 = self.__u.getNCPUserName()
           self.__password2 = self.__u.getNCPPassword()
           self.__cnxn2 = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.__server2 + ';DATABASE=' + self.__database2 + ';UID=' + self.__username2 + ';PWD=' + self.__password2)
           self.__cursor2 = self.__cnxn2.cursor()
           self.__server = self.__u.getServerName()
           self.__database = self.__u.getEDHDatabaseName()
           self.__username = self.__u.getEDH_UserName()
           self.__password = self.__u.getEDH_Password()
           self.__cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.__server + ';DATABASE=' + self.__database + ';UID=' + self.__username + ';PWD=' + self.__password)
           self.__cursor = self.__cnxn.cursor()
       def getusername(self,id):
           tsql = "select emp_name from dbo.employee where emp_id=?"
           self.__cursor2.execute(tsql,id)
           row = self.__cursor2.fetchall()
           name = None
           for name in row:
               name = name[0]
           if name is None:
               tsql = "select hr_name from dbo.hosted_researcher where hr_id=?"
               self.__cursor.execute(tsql,id)
               row2 = self.__cursor.fetchall()
               for name in row2:
                   name = name[0]
           return name
       def getEmployes(self):
           tsql = "select emp_id,emp_name,designation from dbo.employee where designation='Director' or designation='DG' or designation='Manager'"
           self.__cursor2.execute(tsql)
           row = self.__cursor2.fetchall()
           return row
       def getDocumentCreated(self,id):
           tsql = "SELECT aw_id, aw_subject from dbo.application_written WHERE aw_written_by=? ORDER by aw_id DESC"
           self.__cursor.execute(tsql,id)
           row = self.__cursor.fetchall()
           return row
       def getForwarodToId(self,appid):
           tsql = "select aw_forward_to from dbo.application_written where aw_id=?"
           self.__cursor.execute(tsql,appid)
           row = self.__cursor.fetchall()
           forward_to = None
           for i in row:
               forward_to = i[0]
           return forward_to
       def getApplicationDetail(self,appid):
           tsql = "select aw_id,aw_subject,aw_status,aw_content,aw_written_by from dbo.application_written where aw_id=?"
           self.__cursor.execute(tsql,appid)
           row = self.__cursor.fetchall()
           return row
       def getforwardTodetail(self,appid):
           tsql = "select hp_comments,hp_employee_name, hp_employee_designation from dbo.history_application where hp_application_id=?"
           self.__cursor.execute(tsql,appid)
           row2 = self.__cursor.fetchall()
           return row2
       def getDocumenttoSign(self,id):
           tsql = "SELECT aw_id,aw_subject,aw_update_date_time from dbo.application_written where aw_forward_to=? ORDER by aw_id DESC"
           self.__cursor.execute(tsql,id)
           row = self.__cursor.fetchall()
           return row
       def getMaxAppHistory(self):
           tsql = "select max(hp_id) from dbo.history_application"
           self.__cursor.execute(tsql)
           row = self.__cursor.fetchall()
           id = None
           for i in row:
               id = i[0]
               if id is None:
                   id = 1
               else:
                   id = id + 1
           return id
       def getEmployeeDesignation(self,id):
           tsql = "select designation from dbo.employee where emp_id=?"
           self.__cursor2.execute(tsql,id)
           row = self.__cursor2.fetchall()
           for des in row:
               designation = des[0]
           return designation
       def setCommentHistory(self,appid,comment,forward,action,designation,name):
           id=self.getMaxAppHistory()
           tsql = "insert into dbo.history_application VALUES (?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, id, appid, comment, name, designation,datetime.datetime.now(),datetime.datetime.now())
           self.__cursor.commit()
           tsql = "update dbo.application_written set aw_forward_to=? , aw_update_date_time= ?, aw_status=? where aw_id=?"
           self.__cursor.execute(tsql,forward,datetime.datetime.now(),action,appid)
           self.__cursor.commit()
           return "Record updated"
       def getApplicationMax(self):
           tsql = "select max(aw_id) from dbo.application_written"
           self.__cursor.execute(tsql)
           row = self.__cursor.fetchall()
           id = 0
           for i in row:
               id = i[0]
               if id==0:
                   id = 1
               else:
                   id = id + 1
           return id
       def getLoginRequestMax(self):
           tsql = "SELECT MAX(lr_id) from dbo.login_request"
           self.__cursor.execute(tsql)
           row = self.__cursor.fetchall()
           logid = 0
           for i in row:
               logid = i[0]
               if logid==0:
                   logid = 1
               else:
                   logid = logid + 1
           return logid
       def getAttachDocumentMax(self):
           tsql = "SELECT MAX(ad_id) from dbo.attach_document"
           self.__cursor.execute(tsql)
           row = self.__cursor.fetchall()
           fileid = 0
           for i in row:
               fileid = i[0]
               if fileid==0:
                   fileid = 0
           return fileid
       def getMachineMax(self):
           tsql = "SELECT MAX(mr_id) from dbo.machine_request"
           self.__cursor.execute(tsql)
           row = self.__cursor.fetchall()
           logid = None
           for i in row:
               logid = i[0]
               if logid is None:
                   logid = 1
               else:
                   logid = logid + 1
           return logid
       def setLoginRequest(self,subject,bilding,floor,room,window,emial_account,print_quota,linux_account,fom,to,mac,purpose,content,forward,uid,files):
           id=self.getApplicationMax()
           tsql = "Insert into application_written (aw_id,aw_subject,aw_content,aw_status,aw_written_by,aw_forward_to,aw_request_type,aw_insert_date_time,aw_update_date_time) Values (?,?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql,id,subject,content,'Forward',uid, forward,  '2',datetime.datetime.now(),datetime.datetime.now())
           self.__cnxn.commit()
           logid=self.getLoginRequestMax()
           tsql = "insert into dbo.login_request VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, logid, id, window, emial_account, print_quota, linux_account, bilding, room, floor, fom,to, mac, purpose, 'No')
           self.__cnxn.commit()
           fileid=self.getAttachDocumentMax()
           for file in files:
               fileid = fileid + 1
               tsql = "INSERT INTO attach_document (ad_id,ad_application_id, ad_document_name,ad_document_detail) VALUES (?,?,?,?);"
               self.__cursor.execute(tsql, fileid, id, file.filename, file.read())
               self.__cnxn.commit()
       def getNetworkMax(self):
           tsql = "SELECT MAX(nr_id) from dbo.network_request"
           self.__cursor.execute(tsql)
           row = self.__cursor.fetchall()
           logid = None
           for i in row:
               logid = i[0]
               if logid is None:
                   logid = 1
               else:
                   logid = logid + 1
           return logid
       def setMacineRequest(self,subject,bilding,floor,room,linux_flavour,comment,content,forward,uid,software,os,files):
           id=self.getApplicationMax()
           tsql = "Insert into application_written (aw_id,aw_subject,aw_content,aw_status,aw_written_by,aw_forward_to,aw_request_type,aw_insert_date_time,aw_update_date_time) Values (?,?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, id, subject, content, 'Forward', uid, forward, '3',datetime.datetime.now(),datetime.datetime.now() )
           self.__cnxn.commit()
           fileid=self.getAttachDocumentMax()
           logid=self.getMachineMax()
           tsql = "insert into dbo.machine_request VALUES(?,?,?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, logid, id, os, linux_flavour, software, comment, room, bilding, floor, 'No')
           self.__cnxn.commit()
           for file in files:
               fileid = fileid + 1
               tsql = "INSERT INTO attach_document (ad_id,ad_application_id, ad_document_name,ad_document_detail) VALUES (?,?,?,?);"
               self.__cursor.execute(tsql, fileid, id, file.filename, file.read())
               self.__cnxn.commit()
       def setNetwokRequest(self, subject,bilding, floor,room, fom,to,content,forward,uid):
           id=self.getApplicationMax()
           logid=self.getNetworkMax()
           tsql = "Insert into application_written (aw_id,aw_subject,aw_content,aw_status,aw_written_by,aw_forward_to,aw_request_type,aw_insert_date_time,aw_update_date_time) Values (?,?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, id, subject, content, 'Forward', uid, forward, '4',datetime.datetime.now(),datetime.datetime.now() )
           self.__cnxn.commit()
           tsql = "insert into dbo.network_request VALUES(?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, logid, id, bilding, floor, room, fom, to, 'No')
           self.__cnxn.commit()
       def getPrintMax(self):
           tsql = "SELECT MAX(pr_id) from dbo.print_request"
           self.__cursor.execute(tsql)
           row = self.__cursor.fetchall()
           logid = None
           for i in row:
               logid = i[0]
               if logid is None:
                   logid = 1
               else:
                   logid = logid + 1
           return logid
       def setPrintRequest(self, subject,pages, content,forward,uid):
           id=self.getApplicationMax()
           logid=self.getPrintMax()
           tsql = "Insert into application_written (aw_id,aw_subject,aw_content,aw_status,aw_written_by,aw_forward_to,aw_request_type,aw_insert_date_time,aw_update_date_time) Values (?,?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, id, subject, content, 'Forward', uid, forward, '5',datetime.datetime.now(),datetime.datetime.now() )
           self.__cnxn.commit()
           tsql = "insert into dbo.print_request VALUES(?,?,?,?)"
           self.__cursor.execute(tsql, logid, id, pages, 'No')
           self.__cnxn.commit()
       def getMailMax(self):
           tsql = "SELECT MAX(mqr_id) from dbo.mail_quota_request"
           self.__cursor.execute(tsql)
           row = self.__cursor.fetchall()
           logid = None
           for i in row:
               logid = i[0]
               if logid is None:
                   logid = 1
               else:
                   logid = logid + 1
           return logid
       def setMailRequest(self,subject,gb,content,forward,uid):
           id=self.getApplicationMax()
           logid=self.getMailMax()
           tsql = "Insert into application_written (aw_id,aw_subject,aw_content,aw_status,aw_written_by,aw_forward_to,aw_request_type,aw_insert_date_time,aw_update_date_time) Values (?,?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, id, subject, content, 'Forward', uid, forward,'6', datetime.datetime.now(),datetime.datetime.now())
           self.__cnxn.commit()
           tsql = "insert into dbo.mail_quota_request VALUES(?,?,?,?)"
           self.__cursor.execute(tsql, logid, id, gb, 'No')
           self.__cnxn.commit()
       def getPasswordMax(self):
           tsql = "SELECT MAX(prr_id) from dbo.password_reset_request"
           self.__cursor.execute(tsql)
           row = self.__cursor.fetchall()
           logid = None
           for i in row:
               logid = i[0]
               if logid is None:
                   logid = 1
               else:
                   logid = logid + 1
           return logid
       def setPasswordResetRequest(self,subject,content,forward,uid):
           id=self.getApplicationMax()
           logid=self.getPasswordMax()
           tsql = "Insert into application_written (aw_id,aw_subject,aw_content,aw_status,aw_written_by,aw_forward_to,aw_request_type,aw_insert_date_time,aw_update_date_time) Values (?,?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, id, subject, content, 'Forward', uid, forward, '7',datetime.datetime.now(),datetime.datetime.now() )
           self.__cnxn.commit()
           tsql = "insert into dbo.password_reset_request VALUES(?,?,?,?)"
           self.__cursor.execute(tsql, logid, id, content, 'No')
           self.__cnxn.commit()
       def getMaxhosted(self):
           tsql = "SELECT MAX(hr_id) from dbo.hosted_researcher"
           self.__cursor.execute(tsql)
           row = self.__cursor.fetchall()
           logid = None
           for i in row:
               logid = i[0]
               if logid is None:
                   logid = 1
               else:
                   logid = logid + 1
           return logid
       def setGeneralApplication(self,subject,content,forward,uid,files):
           id=self.getApplicationMax()
           fileid=self.getAttachDocumentMax()
           tsql = "Insert into application_written (aw_id,aw_subject,aw_content,aw_status,aw_written_by,aw_forward_to,aw_request_type,aw_insert_date_time,aw_update_date_time) Values (?,?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, id, subject, content, 'Forward', uid, forward,'1', datetime.datetime.now(),datetime.datetime.now() )
           self.__cnxn.commit()
           for file in files:
               fileid = fileid + 1
               tsql = "INSERT INTO attach_document (ad_id,ad_application_id, ad_document_name,ad_document_detail) VALUES (?,?,?,?);"
               self.__cursor.execute(tsql, fileid, id, file.filename, file.read())
               self.__cnxn.commit()
       def setHostedResearcher(self,id,name,dob,cnic,qualification,academic_record,present_status,designation,enrollemnt_no,uni,department,permanent_address,mailing_address,landline,cell,email,researcher_category,department_NCP,duration_NCP,supervisor_from_NCP,cosupervisor_from_NCP,picture,supervisor_naame,supervisor_departmen,tendate,gender,province,city):
           tsql = "INSERT INTO hosted_researcher (hr_id,hr_name,hr_dob,hr_cnic,hr_qualification,hr_acedmic_record,hr_present_status,hr_designation,hr_enrollment_no,hr_uni_or_org,hr_department,hr_permanent_address,hr_mailing_address,hr_landline_no,hr_cell,hr_email,hr_category,hr_department_ncp,hr_duration_ncp,hr_supervisor_ncp,hr_cosupervisor_ncp,hr_picture,hr_picture_path,hr_supervisor_name,hr_supervisor_department,hr_tentative_date,hr_gender,hr_province,hr_city) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
           self.__cursor.execute(tsql, id, name, dob, cnic, qualification, academic_record, present_status, designation,enrollemnt_no, uni, department, permanent_address, mailing_address, landline, cell, email,researcher_category, department_NCP, duration_NCP, supervisor_from_NCP, cosupervisor_from_NCP,   picture.filename,   picture.read(),supervisor_naame,supervisor_departmen,tendate,gender,province,city)
           self.__cnxn.commit()
       def getUserMax(self):
           tsql = "SELECT MAX(ud_id) from dbo.user_detail"
           self.__cursor.execute(tsql)
           row = self.__cursor.fetchall()
           logid = None
           for i in row:
               logid = i[0]
               if logid is None:
                   logid = 1
               else:
                   logid = logid + 1
           return logid
       def setUserDetail(self,name,username,email,password):
           id=self.getUserMax()
           tsql="INSERT INTO user_detail (ud_id,ud_name,ud_username,ud_email,us_password,ud_verified) VALUES (?,?,?,?,?,?)"
           self.__cursor.execute(tsql,id,name,username,email,password,'No')
           self.__cnxn.commit()
       def loginUser(self,username,password):
           print(password)
           tsql="select ud_id,ud_username, us_password from dbo.user_detail where ud_username=? and us_password=?"
           self.__cursor.execute(tsql,username,password)
           row=self.__cursor.fetchall()
           return row
       def getHostedDetail(self,id):
           tsql="SELECT hr_id, hr_name,hr_dob,hr_cnic,hr_qualification,hr_acedmic_record,hr_present_status,hr_designation,hr_enrollment_no,hr_uni_or_org,hr_department,hr_permanent_address,hr_mailing_address,hr_landline_no,hr_cell,hr_email,hr_category,hr_department_ncp,hr_duration_ncp,hr_supervisor_ncp,hr_cosupervisor_ncp,hr_supervisor_name,hr_supervisor_department,hr_tentative_date,hr_gender,hr_province,hr_city,hr_picture_path from dbo.hosted_researcher where hr_id=?"
           self.__cursor.execute(tsql,id)
           row = self.__cursor.fetchall()
           return row
       def getHostedusername(self,id):
           tsql="select ud_username from dbo.user_detail where ud_id=?"
           self.__cursor.execute(tsql,id)
           row = self.__cursor.fetchall()
           return row
       def getCaadRequest(self):
           tsql = "select hr_id, hr_name,hr_cnic,hr_qualification,hr_category from dbo.hosted_researcher, dbo.caad_request where hr_id=cr_hosted_id"
           self.__cursor.execute(tsql)
           row = self.__cursor.fetchall()
           return row
       def getMaxhostedRequest(self):
           tsql = "SELECT MAX(cr_id) from dbo.caad_request"
           self.__cursor.execute(tsql)
           row = self.__cursor.fetchall()
           logid = None
           for i in row:
               logid = i[0]
               if logid is None:
                   logid = 1
               else:
                   logid = logid + 1
           return logid
       def sethostedRequest(self,id):
           tid=self.getMaxhostedRequest()
           tsql="insert into dbo.caad_request values (?,?)"
           self.__cursor.execute(tsql,tid,id)
           self.__cnxn.commit()
       def sethostedNewid(self,id,newid):
           tsql="update dbo.hosted_researcher set hr_generated_id=? where hr_id=?"
           self.__cursor.execute(tsql,newid,id)
           self.__cnxn.commit()
       def deleteCaadRequest(self,id):
           tsql="delete dbo.caad_request where cr_hosted_id=?"
           self.__cursor.execute(tsql,id)
           self.__cnxn.commit()
       def getSoftwareMax(self):
           tsql = "SELECT MAX(sr_id) from dbo.software_request"
           self.__cursor.execute(tsql)
           row = self.__cursor.fetchall()
           logid = None
           for i in row:
               logid = i[0]
               if logid is None:
                   logid = 1
               else:
                   logid = logid + 1
           return logid
       def setSoftwareRequest(self,subject,content,forward,uid,software_name,type):
           id = self.getApplicationMax()
           tsql = "Insert into application_written (aw_id,aw_subject,aw_content,aw_status,aw_written_by,aw_forward_to,aw_request_type,aw_insert_date_time,aw_update_date_time) Values (?,?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, id, subject, content, 'Forward', uid, forward, '8', datetime.datetime.now(),
                                 datetime.datetime.now())
           self.__cnxn.commit()
           sid=self.getSoftwareMax()
           tsql="insert into dbo.software_request VALUES (?,?,?,?,?)"
           self.__cursor.execute(tsql,sid,id,software_name,type,'No')
           self.__cnxn.commit()
       def getMaxCluster(self):
           tsql = "SELECT MAX(sr_id) from dbo.cluster_request"
           self.__cursor.execute(tsql)
           row = self.__cursor.fetchall()
           logid = None
           for i in row:
               logid = i[0]
               if logid is None:
                   logid = 1
               else:
                   logid = logid + 1
           return logid
       def setClusterRequest(self,subject,content,forward,uid,university,compiler,packages,fom,to,file):
           id = self.getApplicationMax()
           tsql = "Insert into application_written (aw_id,aw_subject,aw_content,aw_status,aw_written_by,aw_forward_to,aw_request_type,aw_insert_date_time,aw_update_date_time) Values (?,?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, id, subject, content, 'Forward', uid, forward, '9', datetime.datetime.now(),
                          datetime.datetime.now())
           self.__cnxn.commit()
           sid = self.getMaxCluster()
           tsql = "insert into dbo.cluster_request VALUES (?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, sid, id,university,compiler,packages,fom,to ,'No')
           self.__cnxn.commit()
           fileid=self.getAttachDocumentMax()
           fileid=fileid+1
           tsql = "INSERT INTO attach_document (ad_id,ad_application_id, ad_document_name,ad_document_detail) VALUES (?,?,?,?);"
           self.__cursor.execute(tsql, fileid, id, file.filename, file.read())
           self.__cnxn.commit()
       def setITClearance(self,subject,content,forward,uid):
           id = self.getApplicationMax()
           tsql = "Insert into application_written (aw_id,aw_subject,aw_content,aw_status,aw_written_by,aw_forward_to,aw_request_type,aw_insert_date_time,aw_update_date_time) Values (?,?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, id, subject, content, 'Forward', uid, forward, '10', datetime.datetime.now(),
                                 datetime.datetime.now())
           self.__cnxn.commit()
       def getMaxitequipments(self):
           tsql = "SELECT MAX(ie_id) from dbo.it_equipments"
           self.__cursor.execute(tsql)
           row = self.__cursor.fetchall()
           logid = None
           for i in row:
               logid = i[0]
               if logid is None:
                   logid = 1
               else:
                   logid = logid + 1
           return logid
       def setITequipments(self,subject,content,forward,uid,location,timefrom,timeto,datefrom,dateto,laptop,mouse,keyboard,speaker,
                           persenter,pointer,projector,microphone,hdmi,tripod):
           id = self.getApplicationMax()
           tsql = "Insert into application_written (aw_id,aw_subject,aw_content,aw_status,aw_written_by,aw_forward_to,aw_request_type,aw_insert_date_time,aw_update_date_time) Values (?,?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, id, subject, content, 'Forward', uid, forward, '11', datetime.datetime.now(),
                                 datetime.datetime.now())
           self.__cnxn.commit()
           sid = self.getMaxitequipments()
           tsql = "insert into dbo.it_equipments VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, sid, id,location,timefrom,timeto,datefrom,dateto,laptop,mouse,keyboard,speaker,persenter,pointer,projector,microphone,hdmi,tripod, 'No')
           self.__cnxn.commit()
       def setwebsiteRequest(self,subject,content,forward,uid):
           id = self.getApplicationMax()
           tsql = "Insert into application_written (aw_id,aw_subject,aw_content,aw_status,aw_written_by,aw_forward_to,aw_request_type,aw_insert_date_time,aw_update_date_time) Values (?,?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, id, subject, content, 'Forward', uid, forward, '12', datetime.datetime.now(),
                                 datetime.datetime.now())
           self.__cnxn.commit()
       def setcolorprintRequest(self,subject,content,forward,uid):
           id = self.getApplicationMax()
           tsql = "Insert into application_written (aw_id,aw_subject,aw_content,aw_status,aw_written_by,aw_forward_to,aw_request_type,aw_insert_date_time,aw_update_date_time) Values (?,?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, id, subject, content, 'Forward', uid, forward, '13', datetime.datetime.now(),
                                 datetime.datetime.now())
           self.__cnxn.commit()
       def getMaxtelephone(self):
           tsql = "SELECT MAX(tr_id) from dbo.telephone_request"
           self.__cursor.execute(tsql)
           row = self.__cursor.fetchall()
           logid = None
           for i in row:
               logid = i[0]
               if logid is None:
                   logid = 1
               else:
                   logid = logid + 1
           return logid
       def settelophone(self,subject,content,forward,uid,building,floor,room,telephone,extension,national,internationl):
           id = self.getApplicationMax()
           tsql = "Insert into application_written (aw_id,aw_subject,aw_content,aw_status,aw_written_by,aw_forward_to,aw_request_type,aw_insert_date_time,aw_update_date_time) Values (?,?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, id, subject, content, 'Forward', uid, forward, '14', datetime.datetime.now(),
                                 datetime.datetime.now())
           self.__cnxn.commit()
           sid = self.getMaxtelephone()
           tsql = "insert into dbo.telephone_request VALUES (?,?,?,?,?,?,?,?,?,?)"
           self.__cursor.execute(tsql, sid, id,building,floor,room,telephone,extension,national,internationl, 'No')
           self.__cnxn.commit()
       def gethoste(self):
           tsql="SELECT TOP (1000)  [hr_id],[hr_name],[hr_uni_or_org],[hr_category],[hr_department_ncp],[hr_gender] FROM [EDH].[dbo].[hosted_researcher]"
           self.__cursor.execute(tsql)
           row = self.__cursor.fetchall()
           return row
       def getEmployeeId(self,name):
           tsql="SELECT  [emp_id] FROM [NCP].[dbo].[employee] where emp_name=?"
           self.__cursor2.execute(tsql,name)
           row=self.__cursor2.fetchall()
           for i in row:
               return i[0]
       def verifiedMail(self,id):
           tsql="update dbo.user_detail set ud_verified=? where ud_id=?"
           self.__cursor.execute(tsql,'Yes',id)
           self.__cnxn.commit()
       def getverifiedMail(self,id):
           tsql = "select ud_verified from dbo.user_detail where ud_id=?"
           self.__cursor.execute(tsql,id)
           row=self.__cursor.fetchall()
           for i in row:
               return i[0]
       def getloginDetail(self,id):
           tsql = "select ud_name,ud_email from dbo.user_detail where ud_id=?"
           self.__cursor.execute(tsql,id)
           row = self.__cursor.fetchall()
           return row
       def getEmployeeDepartment(self,id):
           tsql = "select department from dbo.employee where emp_id=?"
           self.__cursor2.execute(tsql,id)
           row = self.__cursor2.fetchall()
           for i in row:
               return i[0]
       def getDob(self,id):
           tsql = "select hr_dob from dbo.hosted_researcher where hr_id=?"
           self.__cursor.execute(tsql, id)
           row = self.__cursor.fetchall()
           for i in row:
               return i[0]
       def getFile(self,appid):
           tsql="select ad_id,ad_document_name from dbo.attach_document where ad_application_id=?"
           self.__cursor.execute(tsql,appid);
           row=self.__cursor.fetchall()
           return row
       def getFileDetail(self,fileid):
           tsql = "select ad_document_detail from dbo.attach_document where ad_id=?"
           self.__cursor.execute(tsql, fileid);
           row = self.__cursor.fetchall()
           for i in row:
               return i[0]
       def getDesignation(self,id):
           tsql = "select designation from dbo.employee where emp_id=?"
           self.__cursor2.execute(tsql, id);
           row = self.__cursor2.fetchall()
           for i in row:
               return i[0]
       def getEmail(self,id):
           tsql = "select email_address from dbo.employee where emp_id=?"
           self.__cursor2.execute(tsql, id);
           row = self.__cursor2.fetchall()
           for i in row:
               return i[0]




































