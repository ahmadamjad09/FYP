from flask import render_template, request, make_response,session,url_for,send_file
import datetime
from app.Controller import Controller
from app import app
import pdfkit
from base64 import b64encode
import base64
from flask_mail import Mail,Message
import ldap
from io import BytesIO
import json
import easygui
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
s = URLSafeTimedSerializer('this is seceret')
mail = Mail(app)
re=1
from werkzeug.security import generate_password_hash, \
     check_password_hash
control=Controller()
#index page function
@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')
#login
@app.route('/login',methods = ['POST', 'GET'])
def loginuser():
    if request.method == 'POST':
        category=request.form['cat']
        username=request.form['username']
        password=request.form['password']
        row=None
        us=None
        id=None
        dob=None
        if category=="2":
            row=control.loginUser(username,password)
            for i in row:
                id=i[0]
                row=control.getHostedUsername((id))
                for i in row:
                    us=i[0]
                    if username==us:
                        session['id']=str(id)
                        session['name']=us
                        m=control.getVerifiedMail(session['id'])
                        dob=control.getDob(session['id'])
                        if m=='Yes':
                            if dob is None:
                                re=1
                            else:
                                re=2
                            return render_template('home2.html',title='Home',name=session['name'],re=re)
                        else:
                            easygui.msgbox('Email not verified',title='Message')
                            return render_template('index.html')
        else:
            #msg=check_credentials(username,password)
            msg='EMP01'
            if msg=="Wrong username or password":
                easygui.msgbox('Wrong username or password', title='Message')
                return render_template('index.html',title='login')
            elif msg=="AD server not awailable":
                easygui.msgbox('AD server not awailable', title='Message')
                return render_template('index.html', title='login'
                                      )
            else:
                session['id'] = msg
                session['name'] = control.getUser(session['id'])
                easygui.msgbox('Login Successfully', title='Message')
                return render_template('home.html', title='Home', name=session['name'])
    easygui.msgbox('Create Account First', title='Message')
    return render_template('index.html',title='Home')
#it Page function
@app.route('/it')
def it():
    if 'name' in session:
        return render_template('it.html', title='Home', name=session['name'])
    else:
        return render_template('index.html', title='Login')
#General Application page function
@app.route('/general_app')
def application():
    if 'name' in session:
      row=control.getEmpolyees()
      return render_template('writeapp.html', title='General Application' ,id=session['id'],row=row,name=session['name'])
    else:
        return render_template('index.html')
#Register User Page Function
@app.route('/register')
def register_user():
    if 'id' in session:
        m=control.getVerifiedMail(session['id'])
        if m=='Yes':
         row=control.getLoginDetail(session['id'])
         return render_template('register.html', title='Register Researcher',name=session['name'],row=row)
        else:
            easygui.msgbox('Verify Your Email First' ,title='Message')
            return render_template('home2.html', title='Home', name=session['name'],re=re)
    else :
        return render_template('index.html',row1="Login First")
#document Created Detail
@app.route('/document_created')
def document_created():
    if 'name' in session:
       row=control.getDocumentCreated(session['id'])
       return render_template('documentCreated.html', title='Document Created By Me', row=row,name=session['name'])
    else:
       return render_template('index.html')
#document View
@app.route('/document_view',methods = ['POST', 'GET'])
def document_view():
    if 'name' in session:
        if request.method == 'POST':
            appid = request.form['appid']
            name = control.getForwardToName(appid)
            row = control.getApplicationDetail(appid)
            row2 = control.getForwardtodetail(appid)
        return render_template('documentview.html', title='Document Detail', name1=name, row=row, row2=row2,
                               name=session['name'])
    else:
        return render_template('index.html')
#document for sign
@app.route('/document_sign',methods = ['POST', 'GET'])
def document_sign():
    if 'name' in session:
        designation=control.getDesignation(session['id'])
        if designation=='Manager':
            easygui.msgbox('You are not authorized to this page')
            return render_template('home.html', title='Home', name=session['name'])
        else:
         row=control.getDocumentToSign(session['id'])
         return render_template('sign.html', title='Document Sign', row=row,name=session['name'])
    else:
        return render_template('index.html')
@app.route('/manager',methods = ['POST', 'GET'])
def Manager():
    if 'name' in session:
        designation=control.getDesignation(session['id'])
        if designation=='Manager':
            row = control.getDocumentToSign(session['id'])
            return render_template('manager.html', title='Resources Request', row=row, name=session['name'])
        else:
         easygui.msgbox('You are not authorized to this page')
         return render_template('home.html', title='Home', name=session['name'])


    else:
        return render_template('index.html')
@app.route('/back5')
def back5():
    if 'name' in session:
        row = control.getDocumentToSign(session['id'])
        return render_template('sign.html', title='Document Sign', row=row, name=session['name'])
    else:
        return render_template('index.html',title='Login')
@app.route('/back6')
def back6():
    if 'name' in session:
        row = control.getDocumentToSign(session['id'])
        return render_template('manager.html', title='Document Sign', row=row, name=session['name'])
    else:
        return render_template('index.html',title='Login')
#Sign Document
@app.route('/signed_app',methods = ['POST', 'GET'])
def signed_app():
    if 'name' in session:
        if request.method == 'POST':
            appid = request.form['signapp']
            row = control.getApplicationDetail(appid)
            row2 = control.getEmpolyees()
            file = control.getfile(appid)
        return render_template('signed_app.html', title='Signed Document', row=row, row2=row2, name=session['name'],
                               file=file)
    else:
        return render_template('index.html')
@app.route('/assign_res',methods = ['POST', 'GET'])
def assign_res():
    if 'name' in session:
        if request.method == 'POST':
            appid = request.form['signapp']
            row = control.getApplicationDetail(appid)
            row2 = control.getEmpolyees()
            file = control.getfile(appid)
        return render_template('Assign.html', title='Assign Resources', row=row, row2=row2, name=session['name'],
                               file=file)
    else:
        return render_template('index.html')
#save Signed document
@app.route('/signed_document', methods=['POST','GET'])
def document_signed():
   if 'name' in session:
       if request.method == 'POST':
           appid = request.form['appid']
           comment = request.form['signcomment']
           forward = request.form['signforward']
           action = request.form['signaction']
           designation = control.getEmployeeDesignation(session['id'])
           control.setCommentHistory(appid, comment, forward, action, designation, session['name'])
       row = control.getDocumentToSign(session['id'])
       '''email = control.getEmail(forward)
       token = s.dumps(email, salt=None)
       msg = Message('Hello', recipients=[email])
       link = url_for('appsign', token=token, _external=True)
       msg.body = "You Receive an Application For Sign {}".format(link)
       mail.send(msg)'''
       easygui.msgbox('Application Signed and Forward Successfully', title='Message')
       return render_template('sign.html', title='Document Sign', row=row, name=session['name'])
   else:
       return render_template('index.html')
@app.route('/assign', methods=['POST','GET'])
def assign():
   if 'name' in session:
       if request.method == 'POST':
           appid = request.form['appid']
           comment = request.form['signcomment']
           forward = request.form['signforward']
           action = request.form['signaction']
           designation = control.getEmployeeDesignation(session['id'])
           control.setCommentHistory(appid, comment, forward, action, designation, session['name'])
       row = control.getDocumentToSign(session['id'])
       easygui.msgbox('Assignment Details Submit Successfully', title='Message')
       return render_template('manager.html', title='Document Sign', row=row, name=session['name'])
   else:
       return render_template('index.html')
#login Request Form
@app.route('/login_request',methods = ['POST', 'GET'])
def login_request():
    if 'name' in session:
      row=control.getEmpolyees()
      return render_template('loginrequest.html', title='Login Request', row=row, id=session['id'],name=session['name'])
    else:
        return render_template('index.html',title='Login')
#save login Request Form
@app.route('/login_request_save',methods = ['POST', 'GET'])
def save_login_request():
    if 'name' in session:
        if request.method == 'POST':
            subject = "Login Request"
            bilding = request.form['logingbuilding']
            floor = request.form['loginflorr']
            room = request.form['loginroom']
            window = request.form['degree']
            emial_account = request.form['cv']
            print_quota = request.form['cp']
            linux_account = request.form['rl']
            fom = request.form['loginfrom']
            to = request.form['loginto']
            mac = request.form['loginmac']
            purpose = request.form['loginpurpose']
            content = "Request for window login account: '" + window + "' Email Account: '" + emial_account + "' Print Quota: '" + print_quota + "' and linux ldap account: '" + linux_account + "' From: '"+fom+"' To: '"+to+"', MAC Address: '"+mac+"'"
            forward = request.form['appforward']
            files = request.files.getlist("appfile")
            control.setLoginRequest(subject, bilding, floor, room, window, emial_account, print_quota, linux_account,
                                    fom, to, mac, purpose, content, forward, session['id'], files)
            '''email = control.getEmail(forward)
            token = s.dumps(email, salt=None)
            msg = Message('Hello', recipients=[email])
            link = url_for('appsign', token=token, _external=True)
            msg.body = "You Receive an Application For Sign {}".format(link)
            mail.send(msg)'''
            easygui.msgbox('Login Request Submit and Forward Successfully', title='Message')
        return render_template('it.html',title='IT',name=session['name'])
    else:
        return render_template('index.html',title='Login')
#machine request form
@app.route('/machine_request',methods = ['POST', 'GET'])
def machine_request():
    if 'name' in session:
      row=control.getEmpolyees()
      return render_template('machine.html', title='Machine Request', row=row, id=session['id'],name=session['name'])
    else:
        return render_template('index.html',title='Login')
#save machine request
@app.route('/save_machine_request',methods=['POST','GET'])
def machine_request_save():
   if 'name' in session:
       if request.method == 'POST':
           subject = "New Machine Issuance Request"
           bilding = request.form['machinebuilding']
           floor = request.form['machineflorr']
           room = request.form['machineroom']
           os = request.form.get('machineos')
           linux_flavour = request.form.get('machineflavour')
           software = request.form['machinesoftware']
           comment = request.form['machinecomment']
           content = "Request for new machine, with operating system '" + os + "' ', Linux Flavour "+linux_flavour+"' and including softwares: '" + software + "' , Additional Information '"+comment+"'"
           forward = request.form['appforward']
           files = request.files.getlist("appfile")
           control.setMacineRequest(subject, bilding, floor, room, linux_flavour, comment, content, forward,
                                    session['id'], software, os, files)
           '''email = control.getEmail(forward)
           token = s.dumps(email, salt=None)
           msg = Message('Hello', recipients=[email])
           link = url_for('appsign', token=token, _external=True)
           msg.body = "You Receive an Application For Sign {}".format(link)
           mail.send(msg)'''
           easygui.msgbox('Machine Request Submit and Forward Successfully', title='Message')
       return render_template('it.html',title='IT',name=session['name'])
   else:
       return render_template('index.html',title='Login')
#Network Request Form
@app.route('/network_request',methods = ['POST', 'GET'])
def network_request():
    if 'name' in session:
        row=control.getEmpolyees()
        return render_template('networkreq.html', title='Network Request', row=row, id=session['id'],name=session['name'])
    else:
        return render_template('/index.html')
#save network request form
@app.route('/save_network_request',methods=['POST','GET'])
def network_request_save():
    if 'name' in session:
        if request.method == 'POST':
            subject = "Network Connection Request"
            bilding = request.form['logingbuilding']
            floor = request.form['loginflorr']
            room = request.form['loginroom']
            fom = request.form['nfrom']
            to = request.form['nto']
            content = "Netowk Connection Required at Building: '" + bilding + "', Floor: '" + floor + "' and Room: '" + room + "'  From: '" + fom + "' To: '" + to + "'"
            forward = request.form['appforward']
            control.setNetwokRequest(subject, bilding, floor, room, fom, to, content, forward, session['id'])
            email = control.getEmail(forward)
            token = s.dumps(email, salt=None)
            msg = Message('Hello', recipients=[email])
            link = url_for('appsign', token=token, _external=True)
            msg.body = "You Receive an Application For Sign {}".format(link)
            mail.send(msg)
            easygui.msgbox('Network Request Submit and Forward Successfully', title='Message')
        return  render_template('it.html',title='IT',name=session['name'])
    else:
        return render_template('index.html')

#print Quota Request Form
@app.route('/print_request',methods = ['POST', 'GET'])
def print_request():
    if 'name' in session:
        row=control.getEmpolyees()
        return render_template('print.html', title='Print Request', row=row, id=session['id'],name=session['name'])
    else:
        return render_template('index.html')
#print Qouta Request Save
@app.route('/save_print_request',methods=['POST','GET'])
def print_request_save():
   if 'name' in session:
       if request.method == 'POST':
           subject = "Print Quota Request"
           pages = request.form['pages']
           content = "Request to add the '" + pages + "' pages to my account"
           forward = request.form['appforward']
           control.setPrintRequest(subject, pages, content, forward, session['id'])
           email = control.getEmail(forward)
           token = s.dumps(email, salt=None)
           msg = Message('Hello', recipients=[email])
           link = url_for('appsign', token=token, _external=True)
           msg.body = "You Receive an Application For Sign {}".format(link)
           mail.send(msg)
           easygui.msgbox('Print Quota Submit and Forward Successfully', title='Message')
       return  render_template('it.html',title='IT',name=session['name'])
   else:
       return render_template('index.html')
#Mail Request Form
@app.route('/mail_request',methods = ['POST', 'GET'])
def mail_request():
    if 'name' in session:
       row=control.getEmpolyees()
       return render_template('mailqu.html', title='Mail Request', id=session['id'], row=row,name=session['name'])
    else:
        return render_template('index.html')
#Mail Quota Request Form save
@app.route('/save_mail_request',methods=['POST','GET'])
def mail_request_save():
    if 'name' in session:
        if request.method == 'POST':
            subject = "Mail Quota Request"
            gb = request.form['mail']
            content = "Request to add the '" + gb + "' GB to my account for mail."
            forward = request.form['appforward']
            control.setMailRequest(subject, gb, content, forward, session['id'])
            email = control.getEmail(forward)
            token = s.dumps(email, salt=None)
            msg = Message('Hello', recipients=[email])
            link = url_for('appsign', token=token, _external=True)
            msg.body = "You Receive an Application For Sign {}".format(link)
            mail.send(msg)
            easygui.msgbox('Mail Quota Submit and Forward Successfully', title='Message')
        return render_template('it.html',title='IT',name=session['name'])
    else:
        return render_template('index.html')
#Passworf Reset Form
@app.route('/passwordreset_request',methods = ['POST', 'GET'])
def passwordreset_request():
    if 'name' in session:
       row=control.getEmpolyees()
       return render_template('passwordreset.html', title='Password Reset Request', row=row, id=session['id'],name=session['name'])
    else:
        return render_template('index.html')
#Save Password Reset Request
@app.route('/save_password_reset_request',methods=['POST','GET'])
def password_reset_request_save():
   if 'name' in session:
       if request.method == 'POST':
           subject = "Password Reset Request"
           content = request.form['reason']
           forward = request.form['appforward']
           control.setPasswordResetRequest(subject, content, forward, session['id'])
           email = control.getEmail(forward)
           token = s.dumps(email, salt=None)
           msg = Message('Hello', recipients=[email])
           link = url_for('appsign', token=token, _external=True)
           msg.body = "You Receive an Application For Sign {}".format(link)
           mail.send(msg)
           easygui.msgbox('Password Reset Request Submit and Forward Successfully', title='Message')
       return render_template('it.html',title='IT',name=session['name'])
   else:
       return render_template('index.html')
#Save Application function
@app.route('/save_app',methods=['POST', 'GET'])
def save_application():
   if 'name' in session:
       if request.method == 'POST':
           subject = request.form['appsub']
           content = request.form['appcontent']
           forward = request.form['appforward']
           files = request.files.getlist("appfile")
           control.setGeneralApplication(subject, content, forward, session['id'], files)
           '''email = control.getEmail(forward)
           token = s.dumps(email, salt=None)
           msg = Message('Hello', recipients=[email])
           link = url_for('appsign', token=token, _external=True)
           msg.body = "You Receive an Application For Sign {}".format(link)
           mail.send(msg)'''
           easygui.msgbox('Application Submit and Forward Successfully',title='Message')
       return render_template('home.html', name=session['name'], title='Home')
   else:
       return render_template('index.html')
@app.route('/appsign/<token>')
def appsign(token):
    if 'name' in session:
        try:
            email = s.loads(token, salt=None, max_age=172800)
            control.verifiedMail(session['id'])
        except SignatureExpired:
            return "Token expired"
        row = control.getDocumentToSign(session['id'])
        return render_template('sign.html', title='Document Sign', row=row, name=session['name'])
    else:
        return render_template('index.html')
@app.route('/register_hosted', methods=['POST','GET'])
#save hosted researcher record
def hosted_register():
    if 'id' in session:
        if request.method == 'POST':
            name = request.form['regname']
            dob = request.form['regdob']
            cnic = request.form['regcnic']
            qualification = request.form['regqua']
            qualification2=request.form.get('reqqother')
            province = request.form['hrp']
            city = request.form['hrc']
            academic_record = request.form['regacad']
            present_status = request.form['regps']
            present_status2=request.form.get('reqpother')
            designation = request.form['regpd']
            enrollemnt_no = request.form['regpe']
            uni = request.form['reguni']
            department = request.form['regud']
            permanent_address = request.form['regpa']
            mailing_address = request.form['regma']
            landline = request.form['regln']
            cell = request.form['regc']
            email = request.form['regem']
            researcher_category = request.form['regrc']
            department_NCP = request.form['regdncp']
            duration_NCP = request.form['regncpduration']
            supervisor_from_NCP = request.form['regncpsup']
            cosupervisor_from_NCP = request.form['regncpcosup']
            supervisor_name = request.form['hrsn']
            supervisor_department = request.form['hrsnd']
            tendate = request.form['tendate']
            gender = request.form['hrg']
            picture = request.files['regpicture']
            if qualification == "Others" and present_status != "Others":
                control.setHostedResearcher(session['id'],name,dob,cnic,qualification2,academic_record,present_status,designation,enrollemnt_no,uni,designation,permanent_address,mailing_address,landline,cell,email,researcher_category,department_NCP,duration_NCP,supervisor_from_NCP,cosupervisor_from_NCP,picture,supervisor_name,supervisor_department,tendate,gender,province,city)
            elif present_status =="Others" and qualification !="Others":
                control.setHostedResearcher(session['id'], name, dob, cnic, qualification, academic_record,
                                            present_status2, designation, enrollemnt_no, uni, designation,
                                            permanent_address, mailing_address, landline, cell, email,
                                            researcher_category, department_NCP, duration_NCP, supervisor_from_NCP,
                                            cosupervisor_from_NCP, picture, supervisor_name, supervisor_department,
                                            tendate, gender, province, city)
            elif qualification =="Others" and present_status == "Others":
                control.setHostedResearcher(session['id'], name, dob, cnic, qualification2, academic_record,
                                            present_status2, designation, enrollemnt_no, uni, designation,
                                            permanent_address, mailing_address, landline, cell, email,
                                            researcher_category, department_NCP, duration_NCP, supervisor_from_NCP,
                                            cosupervisor_from_NCP, picture, supervisor_name, supervisor_department,
                                            tendate, gender, province, city)
            else:
                control.setHostedResearcher(session['id'], name, dob, cnic, qualification, academic_record,
                                            present_status, designation, enrollemnt_no, uni, designation,
                                            permanent_address, mailing_address, landline, cell, email,
                                            researcher_category, department_NCP, duration_NCP, supervisor_from_NCP,
                                            cosupervisor_from_NCP, picture, supervisor_name, supervisor_department,
                                            tendate, gender, province, city)
            re=2
            control.sethostedRequest(session['id'])
            easygui.msgbox('Request Forward Successfully Kindly Print Form',title='Message')
            return render_template("home2.html", name=session['name'],re=re)
    else:
        return render_template('index.html',title='Home',row='Login First')

#software Form
@app.route('/software_form', methods=['POST', 'GET'])
def softwareForm():
    if 'name' in session:
       row = control.getEmpolyees()
       return render_template('software.html', title='Software Request Form', row=row, id=session['id'],
                           name=session['name'])
    else:
        return render_template('index.html')
@app.route('/cluster_form', methods=['POST', 'GET'])
def clusterForm():
    row = control.getEmpolyees()
    return render_template('cluster.html', title='Cluster Login Request Form', row=row, id=session['id'],
                           name=session['name'])
@app.route('/clearance_form', methods=['POST', 'GET'])
def clearanceform():
    if 'name' in session:
      row = control.getEmpolyees()
      return render_template('clearance.html', title='Clearance Form', row=row, id=session['id'],
                           name=session['name'])
    else:
        return render_template('index.html')
@app.route('/equipment_form', methods=['POST', 'GET'])
def equipmentform():
    if 'name' in session:
      row = control.getEmpolyees()
      return render_template('equipment.html', title='Equipment Form', row=row, id=session['id'],
                           name=session['name'])
    else:
        return render_template('index.html')
@app.route('/web_form', methods=['POST', 'GET'])
def webform():
    if 'name' in session:
       row = control.getEmpolyees()
       return render_template('website.html', title='Website Modification Form', row=row, id=session['id'],
                           name=session['name'])
    else:
        return render_template('index.html')
@app.route('/colorprint_form', methods=['POST', 'GET'])
def colorprintform():
    if 'name' in session:
      row = control.getEmpolyees()
      return render_template('colorprint.html', title='Color Print Form', row=row, id=session['id'],
                           name=session['name'])
    else:
        return render_template('index.html')
@app.route('/telephone_form', methods=['POST', 'GET'])
def telephoneform():
    if 'name' in session:
       row = control.getEmpolyees()
       return render_template('telephone.html', title='Telephone Extension Form', row=row, id=session['id'],
                           name=session['name'])
    else:
        return render_template('index.html')
@app.route('/createaccount', methods=['POST', 'GET'])
def accountcreate():
    return render_template('createaccount.html', title='Registration')

@app.route('/submit_form', methods=['POST', 'GET'])
def form_submit():
    if request.method == 'POST':
        name=request.form['name']
        username=request.form['username']
        email=request.form['email']
        password=request.form['ps']
        token = s.dumps(email, salt=None)
        msg = Message('Hello', recipients=[email])
        link = url_for('mailc', token=token, _external=True)
        msg.body = "Your link is {}".format(link)
        mail.send(msg)
        control.setUserDetail(name,username,email,password)
        row = control.loginUser(username, password)
        for i in row:
            id = i[0]
            row = control.getHostedUsername((id))
            for i in row:
                us = i[0]
            session['id'] = str(id)
            session['name'] = us
        easygui.msgbox('You Registered Successfully, Kindly verify your email')
        return render_template('home2.html', title='Home', name=session['name'],row=row,re=re)
@app.route('/cnfe/<token>')
def mailc(token):
    if 'name' in session:
        try:
            email = s.loads(token, salt=None, max_age=172800)
            control.verifiedMail(session['id'])
        except SignatureExpired:
            return "Token expired"
        easygui.msgbox('Email Verified',title='Message')
        return render_template('home2.html', title='Home', name=session['name'], re=re)
    else:
        return render_template('index.html')
@app.route('/logout')
def logout():
    session.pop('name', None)
    return render_template('index.html')
@app.route('/printregister')
def print_register():
    if 'name' in session:
        row = control.getHostedDeail(session['id'])
        for i in row:
            image = i[27]

            image = b64encode(image).decode("utf-8")
        return render_template('printregister.html', row=row, image=image, title="Hosted Researcher Detail",
                               name=session['name'])
    else:
        return render_template('index.html')
@app.route('/homeview')
def viewhome():
    if 'name' in session:
       return  render_template('home.html',name=session['name'],title='Home')
    else:
        return render_template('index.html')
@app.route('/homeviewedh')
def viewhomeedh():
    if 'name' in session:
        dob=None
        dob = control.getDob(session['id'])
        if dob is None:
            re = 1
        else:
            re = 2
            return render_template('home2.html', title='Home', name=session['name'], re=re)
    else:
        return render_template('index.html')
@app.route('/caad')
def opencadd():
    if 'id' in session:
      department=control.getEmployeeDepartment(session['id'])
      if department=='CAAD':
          return render_template('caad.html',name=session['name'])
      else:
        easygui.msgbox('You are not Authorized to this Page', title='Message')
        return render_template('home.html', name=session['name'],title='Home')
    else:
        return render_template('index.html')
@app.route('/caddreports')
def caadreport():
    if 'name' in session:
      return render_template('caadreports.html',name=session['name'])
    else:
        return render_template('index.html')

@app.route('/request_caad')
def requesttocaad():
    if 'name' in session:
      row=control.getCaadRequest()
      return render_template('requestcaad.html',name=session['name'],row=row)
    else:
      return render_template('index.html')
@app.route('/reportcaadview', methods=['POST','GET'])
def caadreportview():
   if 'name' in session:
       if request.method == 'POST':
           id = request.form['id']
           row = control.getHostedDeail(id)
           for i in row:
               image = i[27]
               image = b64encode(image).decode("utf-8")
       return render_template('caadreportview.html', name=session['name'], row=row, image=image)
   else:
       return render_template('index.html')
@app.route('/requestcaadview', methods=['POST','GET'])
def caadrequesttview():
   if 'name' in session:
       if request.method == 'POST':
           id = request.form['id']
           row = control.getHostedDeail(id)
           for i in row:
               image = i[27]
               image = b64encode(image).decode("utf-8")
       return render_template('caadrequestview.html', name=session['name'], row=row, image=image)
   else:
       return render_template('index.html')
@app.route('/newid', methods=['POST','GET'])
def idnew():
    if 'name' in session:
        if request.method == 'POST':
            id = request.form['id']
            newid = request.form['newid']
            control.sethostednewid(id, newid)
            control.deleteCaadRequest(id)
            row = control.getCaadRequest()
            easygui.msgbox('Id Generated Successfully',title='Message')
            return render_template('requestcaad.html', name=session['name'], row=row)
    else:
        return render_template('index.html')
@app.route('/save_software_request',methods=['POST','GET'])
def software_request_save():
    if 'name' in session:
        if request.method == 'POST':
            subject = "Software Application Request"
            software = request.form['softwarename']
            type = request.form['softtype']
            description = request.form['sofdis']
            content = "Software Name: '" + software + "' type: '" + type + "' Description: '" + description + "'"
            forward = request.form['appforward']
            control.setSoftwareRequest(subject, content, forward, session['id'], software, type)
            email = control.getEmail(forward)
            token = s.dumps(email, salt=None)
            msg = Message('Hello', recipients=[email])
            link = url_for('appsign', token=token, _external=True)
            msg.body = "You Receive an Application For Sign {}".format(link)
            mail.send(msg)
            easygui.msgbox('Software Request Submit and Forward Successfully', title='Message')
        return  render_template('it.html',title='IT',name=session['name'])
    else:
        return render_template('index.html')
@app.route('/save_cluster_request',methods=['POST','GET'])
def cluster_request_save():
    if 'name' in session:
        if request.method == 'POST':
            subject = "Cluster Login Request"
            print("ahmad")
            uni = request.form['cuc']
            thesis = request.form['ctrt']
            compiler = request.form['ccr']
            packages = request.form['cpr']
            fom = request.form['loginfrom']
            to = request.form['loginto']
            file = request.files['appfile']
            content = "Thesis Title: '" + thesis + "' Compiler Required: '" + compiler + "' Packages: '" + packages + "' from: '" + fom + "' to: '" + to + "' University: '"+uni+"'"
            forward = request.form['appforward']
            control.setClusterRequest(subject, content, forward, session['id'], uni, compiler, packages, fom, to, file)
            email = control.getEmail(forward)
            token = s.dumps(email, salt=None)
            msg = Message('Hello', recipients=[email])
            link = url_for('appsign', token=token, _external=True)
            msg.body = "You Receive an Application For Sign {}".format(link)
            mail.send(msg)
            easygui.msgbox('Cluster Login Request Submit and Forward Sucessfully',title='Message')
        return render_template('it.html',title='IT',name=session['name'])
    else:
        return render_template('index.html')

@app.route('/save_clearance_request',methods=['POST','GET'])
def clearance_request_save():
   if 'name' in session:
       if request.method == 'POST':
           subject = "Cluster Login Request"
           content = request.form['comment']
           forward = request.form['appforward']
           control.setItClearance(subject, content, forward, session['id'])
           easygui.msgbox('Clearance Request Submit and Forward Sucessfully', title='Message')
           email = control.getEmail(forward)
           token = s.dumps(email, salt=None)
           msg = Message('Hello', recipients=[email])
           link = url_for('appsign', token=token, _external=True)
           msg.body = "You Receive an Application For Sign {}".format(link)
           mail.send(msg)
       return render_template('it.html',title='IT',name=session['name'])
   else:
       return render_template('index.html')
@app.route('/save_itequipments_request',methods=['POST','GET'])
def save_itequipments_request():
    if 'name' in session:
        if request.method == 'POST':
            subject = "IT Equipments Issuance"
            location = request.form.get('location')
            timefrom = request.form.get('tfrom')
            timeto = request.form.get('tto')
            datefrom = request.form.get('dfrom')
            dateto = request.form.get('dto')
            laptop = request.form.get('checklaptop')
            mouse = request.form.get('checkmouse')
            keyborad = request.form.get('checkkeyboard')
            speaker = request.form.get('checkspeaker')
            presernter = request.form.get('checkPresenter')
            pointer = request.form.get('checkPointer')
            projector = request.form.get('checkProjector')
            micro = request.form.get('checkmicro')
            hdmi = request.form.get('checkhdmi')
            tripord = request.form.get('checktripod')
            content = "Eqiupments Required Keyboard '" + str(keyborad) + "', Mouse: '" + str(
                mouse) + "' , Speaker: '" + str(speaker) + "' , Presenter:  '" + str(presernter) + "' , Laptop/PC:  '"+str(laptop)+"' ,Projector:  '"+str(projector)+"' ,Microphone:  '"+str(micro)+"' ,HDMI:  '"+str(hdmi)+"' ,Tripord:  '"+str(tripord)+"' From: '"+datefrom+"' To: '"+dateto+"'"
            forward = request.form['appforward']
            control.setITequipments(subject, content, forward, session['id'], location, timefrom, timeto, datefrom,
                                    dateto, laptop, mouse, keyborad, speaker, presernter, pointer, projector, micro,
                                    hdmi, tripord)
            email = control.getEmail(forward)
            token = s.dumps(email, salt=None)
            msg = Message('Hello', recipients=[email])
            link = url_for('appsign', token=token, _external=True)
            msg.body = "You Receive an Application For Sign {}".format(link)
            mail.send(msg)
            easygui.msgbox('Equipments Request Submit and Forward Sucessfully', title='Message')
            return render_template('it.html', title='IT', name=session['name'])
    else:
        return render_template('index.html')
@app.route('/save_website_request',methods=['POST','GET'])
def website_request_save():
   if 'name' in session:
       if request.method == 'POST':
           subject = "Website Modification Request"
           type = request.form.get('webtype')
           detail = request.form.get('webdetail')
           content = "Webpage: '" + type + "' Detail: '" + detail + "'"
           forward = request.form['appforward']
           control.setwebsiteRequest(subject, content, forward, session['id'])
           email = control.getEmail(forward)
           token = s.dumps(email, salt=None)
           msg = Message('Hello', recipients=[email])
           link = url_for('appsign', token=token, _external=True)
           msg.body = "You Receive an Application For Sign {}".format(link)
           mail.send(msg)
           easygui.msgbox('Website Request Submit and Forward Sucessfully', title='Message')
       return render_template('it.html', title='IT', name=session['name'])
   else:
       return render_template('index.html')
@app.route('/save_colorprint_request',methods=['POST','GET'])
def colorprint_request_save():
    if 'name' in session:
        if request.method == 'POST':
            subject = "Photocopy/ColorPrint Request"
            pages = request.form.get('pages')
            content = "Kindly Add '" + pages + "' color print pages To My Account"
            forward = request.form['appforward']
            control.setcolorprintRequest(subject, content, forward, session['id'])
            email = control.getEmail(forward)
            token = s.dumps(email, salt=None)
            msg = Message('Hello', recipients=[email])
            link = url_for('appsign', token=token, _external=True)
            msg.body = "You Receive an Application For Sign {}".format(link)
            mail.send(msg)
            easygui.msgbox('Color Print Request Submit and Forward Sucessfully', title='Message')
        return render_template('it.html', title='IT', name=session['name'])
    else:
        return render_template('index.html')
@app.route('/save_telephone_request',methods=['POST','GET'])
def telephone_request_save():
    if 'name' in session:
        if request.method == 'POST':
            subject = "Telephone Extension Requirement"
            biulding = request.form.get('logingbuilding')
            floor = request.form.get('loginflorr')
            room = request.form.get('loginroom')
            telephone = request.form.get('ttype')
            extendion = request.form.get('degree')
            national = request.form.get('cv')
            international = request.form.get('cp')
            content = "Telephone Connection Required in Building '" + biulding + "', floor '" + floor + "' and room '" + room + "', telephone type '"+telephone+"' , extension '"+extendion+"', national: '"+national+"', international '"+international+"'"
            forward = request.form['appforward']
            control.settelophone(subject, content, forward, session['id'], biulding, floor, room, telephone, extendion,
                                 national, international)
            email = control.getEmail(forward)
            token = s.dumps(email, salt=None)
            msg = Message('Hello', recipients=[email])
            link = url_for('appsign', token=token, _external=True)
            msg.body = "You Receive an Application For Sign {}".format(link)
            mail.send(msg)
            easygui.msgbox('Telephone Request Submit and Forward Sucessfully', title='Message')
        return render_template('it.html', title='IT', name=session['name'])
    else:
        return render_template('index.html')
@app.route('/uni')
def uni():
    row=control.gethoste()
    return  render_template('caadreports.html' ,row=row,name=session['name'],title='CAAD Record')
@app.route('/file/<int:i>',methods=['POST','GET'])
def files(i):
    if 'name' in session:
      row=control.getfiledetail(i)
      return  send_file(BytesIO(row), attachment_filename='Flask.pdf',as_attachment=True)
    else:
        return  render_template('index.html')
@app.route('/back')
def Back():
    if 'name' in session:
        return render_template('home.html',title='Home',name=session['name'])
    else:
        return render_template('index.html',title='Login')
@app.route('/back1')
def Back1():
    if 'name' in session:
        return render_template('it.html',title='Home',name=session['name'])
    else:
        return render_template('index.html',title='Login')
@app.route('/back3')
def back3():
    if 'name' in session:
        return render_template('caad.html',title='Home',name=session['name'])
    else:
        return render_template('index.html',title='Login')
@app.route('/back4')
def back4():
    if 'name' in session:
        row = control.getDocumentCreated(session['id'])
        return render_template('documentCreated.html', title='Document Created By Me', row=row, name=session['name'])
    else:
        return render_template('index.html',title='Login')
@app.route('/back8')
def back8():
    return render_template('index.html')

def check_credentials(username, password):

   """Verifies credentials for username and password.
   Returns None on success or a string describing the error on failure
   # Adapt to your needs
   """
   LDAP_SERVER = 'ldap://pdc.ncp.edu.pk'
   # fully qualified AD user name
   LDAP_USERNAME = '%s@ncp.edu.pk' % username
   # your password
   LDAP_PASSWORD = password
   base_dn = 'DC=ncp,DC=edu,DC=pk'
   ldap_filter = 'userPrincipalName=%s@ncp.edu.pk' % username
   attrs = ['employeeID']
   try:
       # build a client
       ldap_client = ldap.initialize(LDAP_SERVER)
       # perform a synchronous bind
       ldap_client.set_option(ldap.OPT_REFERRALS,0)
       ldap_client.simple_bind_s(LDAP_USERNAME, LDAP_PASSWORD)
       #print (ldap_client.search(base_dn,ldap.SCOPE_SUBTREE,"name"))
       dir(ldap_client)
       ab = str(ldap_client.search_s(base_dn, ldap.SCOPE_SUBTREE, ldap_filter, attrs)[0][1]['employeeID'])
       employee_id =  (ab.split("'")[1])
       return employee_id
   except ldap.INVALID_CREDENTIALS:
     #print("wron")
     ldap_client.unbind()
     return 'Wrong username or password'
   except ldap.SERVER_DOWN:
       #print("down")
       return 'AD server not awailable'
   # all is well
   # get all user groups and store it in cerrypy session for future use
   ab = str(ldap_client.search_s(base_dn,
                   ldap.SCOPE_SUBTREE, ldap_filter, attrs)[0][1]['employeeID'])
   #print("ab"+ab)
   ldap_client.unbind()
   return 'success'
