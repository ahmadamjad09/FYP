/**** hosted researcher table****/
create table hosted_researcher(
    hr_id numeric(38) not null primary key,
    hr_generated_id varchar(50),
    hr_name VARCHAR(50) not null,
    hr_dob VARCHAR(50) not null,
    hr_cnic VARCHAR(50) not null UNIQUE,
    hr_qualification VARCHAR(50) not null,
    hr_acedmic_record VARCHAR(50) not null,
    hr_present_status VARCHAR(50) not null,
    hr_designation VARCHAR(50)  null,
    hr_enrollment_no VARCHAR(50) null,
    hr_uni_or_org VARCHAR(50) not null,
    hr_department VARCHAR(50) not null,
    hr_permanent_address VARCHAR(max) not null,
    hr_mailing_address VARCHAR(max) not null,
    hr_landline_no VARCHAR(50) null,
    hr_cell VARCHAR(50) not null UNIQUE,
    hr_email VARCHAR(50) not null UNIQUE,
    hr_category VARCHAR(50) not null,
    hr_department_ncp VARCHAR(50) not null,
    hr_duration_ncp VARCHAR(50) not null,
    hr_supervisor_ncp VARCHAR(50) not null,
    hr_cosupervisor_ncp VARCHAR(50) not null,
    hr_supervisor_name varchar(50) not null,
    hr_supervisor_department varchar(50) not null,
    hr_tentative_date date not null,
    hr_gender varchar(10) not null,
    hr_picture VARCHAR(50) not null,
    hr_picture_path varbinary(max) not null,
   
)
 {% for id,name,dob,cnic,qu,ar,ps,di,uce,po,d,pa,ma,ln,c,em,ca,dn,dan,sn,cn,snn,sd,td,g,pr,ci in row %}

/**** Alter Query ****/

ALTER TABLE dbo.hosted_researcher
drop COLUMN hr_last_degree_path

ALTER TABLE dbo.hosted_researcher
drop COLUMN hr_cv_path

ALTER TABLE dbo.hosted_researcher
drop COLUMN hr_cnic_path

ALTER TABLE dbo.hosted_researcher
drop COLUMN hr_referal_letter_path

ALTER TABLE dbo.hosted_researcher
drop COLUMN hr_picture_path

ALTER TABLE dbo.hosted_researcher
drop COLUMN hr_police_verification_path

ALTER TABLE dbo.hosted_researcher
drop COLUMN hr_security_performa_path

ALTER TABLE dbo.hosted_researcher
ADD hr_last_degree_detail varBinary(max)
ALTER TABLE dbo.hosted_researcher
ADD hr_CV_detail varBinary(max)
ALTER TABLE dbo.hosted_researcher
ADD hr_cnic_detail varBinary(max)
ALTER TABLE dbo.hosted_researcher
ADD hr_referal_letter_detail varBinary(max)
ALTER TABLE dbo.hosted_researcher
ADD hr_picture_detail varBinary(max)
ALTER TABLE dbo.hosted_researcher
ADD hr_police_verification_detail varBinary(max)
ALTER TABLE dbo.hosted_researcher
ADD hr_security_performa_detail varBinary(max)

/**** Request detail ****/

create table request_type(
    rt_id VARCHAR(50) not null primary key,
    rt_request_detail VARCHAR(50) not null UNIQUE
)

/**** Application written ****/

create table application_written (
    aw_id Numeric(50) not null primary key,
    aw_subject VARCHAR(max) not null,
    aw_content VARCHAR(max) null,
    aw_status VARCHAR(50) not null,
    aw_written_by VARCHAR(50) not null,
    aw_forward_to VARCHAR(50) not null,
    aw_insert_date_time VARCHAR(50) not null,
    aw_update_date_time VARCHAR(50) not null,
    aw_request_type VARCHAR(50) not null FOREIGN key REFERENCES request_type (rt_id)
)

/**** Attach Document ****/

create table attach_document(
    ad_id Numeric(38) not null primary key,
    ad_application_id Numeric(38) not null FOREIGN key REFERENCES application_written (aw_id),
    ad_document_name VARCHAR(50) not null,
    ad_document_detail VARbinary(50) not null
)


/**** History Application ****/

create table history_application(
    hp_id Numeric(38) not null primary key,
    hp_application_id Numeric(38) not null FOREIGN key REFERENCES application_written (aw_id),
    hp_comments VARCHAR(max) not null,
    hp_employee_name VARCHAR(50) not null,
    hp_employee_designation varchar(50) not null,
    hp_insert_date_time VARCHAR(50) not null,
    hp_update_date_time VARCHAR(50) not null
)

/**** Login Request ****/

create table login_request(
    lr_id numeric(38) not null primary key,
    lr_application_id numeric(38) not null FOREIGN KEY REFERENCES application_written (aw_id),
    lr_window_login VARCHAR(50) not null,
    lr_email_account VARCHAR(50) not null,
    lr_email_quota VARCHAR(50) not null,
    lr_linux_ldap_account VARCHAR(50) not null,
    lr_building varchar(50) not null,
    lr_room varchar(50) not null,
    lr_floor varchar(50) not null
    lr_from VARCHAR(50) not null,
    lr_to VARCHAR(50) not null,
    lr_mac_address VARCHAR(50) not null,
    lr_purpose_of_account VARCHAR(max) not null,
    lr_assign VARCHAR(50) not null
)

/**** Machine Request ****/

create table machine_request(
    mr_id numeric(38) not null primary key,
    mr_application_id numeric(38) not null FOREIGN key REFERENCES application_written (aw_id),
    mr_operating_system VARCHAR(50) not null,
    mr_linux_flavor VARCHAR(50) null,
    mr_software VARCHAR(max)  null,
    mr_comment VARCHAR(max) null,
    mr_room varchar(50) not null,
    mr_building varchar(50) not null,
    mr_floor varchar(50) not null,
    mr_assign VARCHAR(50) not null

 )

/**** Network Request ****/

create table network_request(
    nr_id numeric(38)not null primary key,
    nr_application_id numeric(38) not null FOREIGN key REFERENCES application_written (aw_id),
    nr_building VARCHAR(50) not null,
    nr_floor VARCHAR(50) not null,
    nr_room VARCHAR(50) not null,
    nr_from VARCHAR(50) not null,
    nr_to VARCHAR(50) not null,
    nr_assign VARCHAR(50) not null
    )

/**** Print Request ****/

create table print_request (
    pr_id Numeric(38) not null primary key,
    pr_application_id Numeric(38) not null FOREIGN key REFERENCES application_written (aw_id),
    pr_pages VARCHAR(50) not null,
    pr_assign VARCHAR(50) not null
)

/**** Mial quota Request ****/

create table mail_quota_request (
    mqr_id numeric(38) not null primary key,
    mqr_application_id numeric(38) not null FOREIGN key REFERENCES application_written (aw_id),
    mqr_mail_quota VARCHAR(50) not null,
    mqr_assign VARCHAR(50) not null
    )

/**** Password Reset Request ****/

create table password_reset_request (
    prr_id numeric(38) not null primary key,
    prr_application_id numeric(38) not null FOREIGN key REFERENCES application_written (aw_id),
    prr_reason VARCHAR(max) not null,
    prr_assign VARCHAR(50) not null
    )

/**** User detail ****/
create table user_detail (
    ud_id numeric(38) not null primasry key,
    ud_name varchar(50) not null,
    ud_username VARCHAR(50) not null Unique,
    ud_email VARCHAR(50) not null Unique,
    us_password VARCHAR(MAX) not null
    )
/****Software Request ****/
create table software_request
(
    sr_id numeric (38) PRIMARY key not null,
    sr_application_id numeric (38) not null,
    sr_software_name varchar(50) not null,
    sr_type VARCHAR(50) not null,
    sr_existing varchar(50) null,
    sr_others VARCHAR(50) null,
    sr_assign VARCHAR not null
)

/*****Cluster Request*****/

create table cluster_request
(
    sr_id numeric (38) PRIMARY key not null,
    sr_application_id numeric (38) not null,
    sr_university varchar(50) not null,
    sr_compiler_required VARCHAR(50) not null,
    sr_Packages_required varchar(50) null,
    sr_from DATETIME not null,
    sr_to DATETIME not null
)

