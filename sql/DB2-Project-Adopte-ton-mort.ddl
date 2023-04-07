-- *********************************************
-- * Standard SQL generation                   
-- *--------------------------------------------
-- * DB-MAIN version: 11.0.2              
-- * Generator date: Sep 14 2021              
-- * Generation date: Fri Apr  7 14:07:35 2023 
-- * LUN file: C:\Users\yanni\OneDrive\Documents\GitHub\INFOB212-BD2-project\schema\conceptual-schema.lun 
-- * Schema: physical v4/SQL1 
-- ********************************************* 


-- Database Section
-- ________________ 

create database physical v4;


-- DBSpace Section
-- _______________


-- Tables Section
-- _____________ 

create table ADDRESS (
     street varchar(128) not null,
     number numeric(8) not null,
     postal_code numeric(16) not null,
     city varchar(128) not null,
     land varchar(128) not null,
     id numeric(32) not null,
     constraint ID_ADDRESS_ID primary key (id),
     constraint SID_ADDRESS_ID unique (street, number, postal_code, city, land));

create table ANAESTHETIST (
     id numeric(32) not null,
     inami_number char(32) not null,
     constraint ID_ANAES_STAFF_ID primary key (id));

create table CUSTOMER (
     id numeric(32) not null,
     pseudo varchar(32) not null,
     blood_type varchar(2) not null,
     blood_sign char not null,
     constraint ID_CUSTO_PERSO_ID primary key (id));

create table ORDER (
     id numeric(32) not null,
     Typ_id numeric(32) not null,
     Buy_id numeric(32) not null,
     constraint ID_ORDER_ID primary key (id));

create table ACCOUNTANT (
     id numeric(32) not null,
     constraint ID_ACCOU_STAFF_ID primary key (id));

create table DETAIL (
     BLOOD numeric(32),
     ORGANE numeric(32),
     id numeric(32) not null,
     constraint SID_DETAIL_ID unique (BLOOD, ORGANE, id));

create table DONATOR (
     id numeric(32) not null,
     Giv_id numeric(32) not null,
     gender char not null,
     age_range float(8) not null,
     constraint ID_DONATOR_ID primary key (id),
     constraint SID_DONAT_BLOOD_ID unique (Giv_id));

create table NURSE (
     id numeric(32) not null,
     constraint ID_NURSE_STAFF_ID primary key (id));

create table DELIVERY (
     id numeric(32) not null,
     departure_date date not null,
     arrival_date date not null,
     effective_arrival_date date not null,
     recipent_last_name varchar(64) not null,
     recipent_first_name varchar(64) not null,
     Typ_id varchar(16) not null,
     At_id numeric(32) not null,
     constraint ID_DELIVERY_ID primary key (id));

create table DOCTOR (
     id numeric(32) not null,
     inami_number char(32) not null,
     constraint ID_DOCTO_STAFF_ID primary key (id));

create table ORGANE (
     state char(32) not null,
     functionnal char not null,
     expiration_date date not null,
     expiration_date_transplatation date,
     method_of_preservation varchar(64) not null,
     type varchar(64) not null,
     id numeric(32) not null,
     price float(32) not null,
     Com_id numeric(32) not null,
     constraint ID_ORGANE_ID primary key (id));

create table CEO (
     id numeric(32) not null,
     constraint ID_CEO_STAFF_ID primary key (id));

create table PERSON (
     id numeric(32) not null,
     last_name varchar(64),
     first_name varchar(64),
     email varchar(128) not null,
     phone_number varchar(32),
     born_date date not null,
     password varchar(128) not null,
     Liv_id numeric(32) not null,
     constraint ID_PERSON_ID primary key (id));

create table STAFF (
     id numeric(32) not null,
     salary numeric(32) not null,
     NURSE numeric(32),
     HR numeric(32),
     DOCTOR numeric(32),
     CEO numeric(32),
     ANAESTHETIST numeric(32),
     ACCOUNTANT numeric(32),
     constraint ID_STAFF_PERSO_ID primary key (id));

create table HR (
     id numeric(32) not null,
     constraint ID_HR_STAFF_ID primary key (id));

create table BLOOD (
     id numeric(32) not null,
     type varchar(2) not null,
     signe char not null,
     expiration_date date not null,
     quantity float(4) not null,
     Giv_id numeric(32),
     Nee_id numeric(32),
     constraint ID_BLOOD_ID primary key (id));

create table TRANSPLANTATION (
     date date not null,
     id numeric(32) not null,
     Con_id numeric(32) not null,
     price float(32) not null,
     Rec_id numeric(32) not null,
     D_w_id numeric(32) not null,
     A_w_id numeric(32) not null,
     constraint ID_TRANSPLANTATION_ID primary key (id),
     constraint SID_TRANS_ORGAN_ID unique (Con_id));

create table TYPE_DELIVERY (
     id varchar(16) not null,
     price numeric(4) not null,
     constraint ID_TYPE_DELIVERY_ID primary key (id));

create table N_work_on (
     N_N_id numeric(32) not null,
     id numeric(32) not null,
     constraint ID_N_work_on_ID primary key (N_N_id, id));


-- Constraints Section
-- ___________________ 

alter table ANAESTHETIST add constraint ID_ANAES_STAFF_FK
     foreign key (id)
     references STAFF;

alter table CUSTOMER add constraint ID_CUSTO_PERSO_FK
     foreign key (id)
     references PERSON;

alter table ORDER add constraint REF_ORDER_DELIV_FK
     foreign key (Typ_id)
     references DELIVERY;

alter table ORDER add constraint REF_ORDER_CUSTO_FK
     foreign key (Buy_id)
     references CUSTOMER;

alter table ACCOUNTANT add constraint ID_ACCOU_STAFF_FK
     foreign key (id)
     references STAFF;

alter table DETAIL add constraint EXTONE_DETAIL
     check((ORGANE is not null and BLOOD is null)
           or (ORGANE is null and BLOOD is not null)); 

alter table DETAIL add constraint EQU_DETAI_BLOOD
     foreign key (BLOOD)
     references BLOOD;

alter table DETAIL add constraint EQU_DETAI_ORGAN_FK
     foreign key (ORGANE)
     references ORGANE;

alter table DETAIL add constraint REF_DETAI_ORDER_FK
     foreign key (id)
     references ORDER;

alter table DONATOR add constraint SID_DONAT_BLOOD_FK
     foreign key (Giv_id)
     references BLOOD;

alter table NURSE add constraint ID_NURSE_STAFF_FK
     foreign key (id)
     references STAFF;

alter table DELIVERY add constraint REF_DELIV_TYPE__FK
     foreign key (Typ_id)
     references TYPE_DELIVERY;

alter table DELIVERY add constraint REF_DELIV_ADDRE_FK
     foreign key (At_id)
     references ADDRESS;

alter table DOCTOR add constraint ID_DOCTO_STAFF_FK
     foreign key (id)
     references STAFF;

alter table ORGANE add constraint ID_ORGANE_CHK
     check(exists(select * from DETAIL
                  where DETAIL.ORGANE = id)); 

alter table ORGANE add constraint REF_ORGAN_DONAT_FK
     foreign key (Com_id)
     references DONATOR;

alter table CEO add constraint ID_CEO_STAFF_FK
     foreign key (id)
     references STAFF;

alter table PERSON add constraint REF_PERSO_ADDRE_FK
     foreign key (Liv_id)
     references ADDRESS;

alter table STAFF add constraint EXCL_STAFF
     check((CEO is not null and HR is null and ACCOUNTANT is null and ANAESTHETIST is null and NURSE is null and DOCTOR is null)
           or (CEO is null and HR is not null and ACCOUNTANT is null and ANAESTHETIST is null and NURSE is null and DOCTOR is null)
           or (CEO is null and HR is null and ACCOUNTANT is not null and ANAESTHETIST is null and NURSE is null and DOCTOR is null)
           or (CEO is null and HR is null and ACCOUNTANT is null and ANAESTHETIST is not null and NURSE is null and DOCTOR is null)
           or (CEO is null and HR is null and ACCOUNTANT is null and ANAESTHETIST is null and NURSE is not null and DOCTOR is null)
           or (CEO is null and HR is null and ACCOUNTANT is null and ANAESTHETIST is null and NURSE is null and DOCTOR is not null)
           or (CEO is null and HR is null and ACCOUNTANT is null and ANAESTHETIST is null and NURSE is null and DOCTOR is null)); 

alter table STAFF add constraint ID_STAFF_PERSO_FK
     foreign key (id)
     references PERSON;

alter table HR add constraint ID_HR_STAFF_FK
     foreign key (id)
     references STAFF;

alter table BLOOD add constraint ID_BLOOD_CHK
     check(exists(select * from DETAIL
                  where DETAIL.BLOOD = id)); 

alter table BLOOD add constraint REF_BLOOD_PERSO_FK
     foreign key (Giv_id)
     references PERSON;

alter table BLOOD add constraint REF_BLOOD_TRANS_FK
     foreign key (Nee_id)
     references TRANSPLANTATION;

alter table TRANSPLANTATION add constraint ID_TRANSPLANTATION_CHK
     check(exists(select * from N_work_on
                  where N_work_on.id = id)); 

alter table TRANSPLANTATION add constraint REF_TRANS_CUSTO_FK
     foreign key (Rec_id)
     references CUSTOMER;

alter table TRANSPLANTATION add constraint SID_TRANS_ORGAN_FK
     foreign key (Con_id)
     references ORGANE;

alter table TRANSPLANTATION add constraint REF_TRANS_DOCTO_FK
     foreign key (D_w_id)
     references DOCTOR;

alter table TRANSPLANTATION add constraint REF_TRANS_ANAES_FK
     foreign key (A_w_id)
     references ANAESTHETIST;

alter table N_work_on add constraint EQU_N_wor_TRANS_FK
     foreign key (id)
     references TRANSPLANTATION;

alter table N_work_on add constraint REF_N_wor_NURSE
     foreign key (N_N_id)
     references NURSE;


-- Index Section
-- _____________ 

create unique index ID_ADDRESS_IND
     on ADDRESS (id);

create unique index SID_ADDRESS_IND
     on ADDRESS (street, number, postal_code, city, land);

create unique index ID_ANAES_STAFF_IND
     on ANAESTHETIST (id);

create unique index ID_CUSTO_PERSO_IND
     on CUSTOMER (id);

create unique index ID_ORDER_IND
     on ORDER (id);

create index REF_ORDER_DELIV_IND
     on ORDER (Typ_id);

create index REF_ORDER_CUSTO_IND
     on ORDER (Buy_id);

create unique index ID_ACCOU_STAFF_IND
     on ACCOUNTANT (id);

create index EQU_DETAI_ORGAN_IND
     on DETAIL (ORGANE);

create index REF_DETAI_ORDER_IND
     on DETAIL (id);

create unique index SID_DETAIL_IND
     on DETAIL (BLOOD, ORGANE, id);

create unique index ID_DONATOR_IND
     on DONATOR (id);

create unique index SID_DONAT_BLOOD_IND
     on DONATOR (Giv_id);

create unique index ID_NURSE_STAFF_IND
     on NURSE (id);

create unique index ID_DELIVERY_IND
     on DELIVERY (id);

create index REF_DELIV_TYPE__IND
     on DELIVERY (Typ_id);

create index REF_DELIV_ADDRE_IND
     on DELIVERY (At_id);

create unique index ID_DOCTO_STAFF_IND
     on DOCTOR (id);

create unique index ID_ORGANE_IND
     on ORGANE (id);

create index REF_ORGAN_DONAT_IND
     on ORGANE (Com_id);

create unique index ID_CEO_STAFF_IND
     on CEO (id);

create unique index ID_PERSON_IND
     on PERSON (id);

create index REF_PERSO_ADDRE_IND
     on PERSON (Liv_id);

create unique index ID_STAFF_PERSO_IND
     on STAFF (id);

create unique index ID_HR_STAFF_IND
     on HR (id);

create unique index ID_BLOOD_IND
     on BLOOD (id);

create index REF_BLOOD_PERSO_IND
     on BLOOD (Giv_id);

create index REF_BLOOD_TRANS_IND
     on BLOOD (Nee_id);

create unique index ID_TRANSPLANTATION_IND
     on TRANSPLANTATION (id);

create index REF_TRANS_CUSTO_IND
     on TRANSPLANTATION (Rec_id);

create unique index SID_TRANS_ORGAN_IND
     on TRANSPLANTATION (Con_id);

create index REF_TRANS_DOCTO_IND
     on TRANSPLANTATION (D_w_id);

create index REF_TRANS_ANAES_IND
     on TRANSPLANTATION (A_w_id);

create unique index ID_TYPE_DELIVERY_IND
     on TYPE_DELIVERY (id);

create unique index ID_N_work_on_IND
     on N_work_on (N_N_id, id);

create index EQU_N_wor_TRANS_IND
     on N_work_on (id);

-- Vue Section
-- _____________ 


-- Trigger Section
-- _____________ 
