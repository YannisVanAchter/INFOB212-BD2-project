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

create database physical_v4;

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
     id numeric(32) unsigned not null AUTO_INCREMENT,
     constraint ID_ADDRESS_ID primary key (id),
     constraint SID_ADDRESS_ID unique (street, number, postal_code, city, land));

create table PERSON (
     id numeric(32) unsigned not null AUTO_INCREMENT,
     last_name varchar(64),
     first_name varchar(64),
     email varchar(128) not null,
     phone_number varchar(32),
     born_date date not null,
     password varchar(128) not null,
     Liv_id numeric(32) not null,
     constraint ID_PERSON_ID primary key (id),
     foreign key (Liv_id) references ADDRESS);

create table CUSTOMER (
     id numeric(32) not null,
     pseudo varchar(32) not null,
     blood_type varchar(2) not null,
     blood_sign char not null,
     constraint ID_CUSTO_PERSO_ID primary key (id),
     foreign key (id) references PERSON);

create table ORDER (
     id numeric(32) unsigned not null AUTO_INCREMENT,
     Typ_id numeric(32) not null,
     Buy_id numeric(32) not null,
     constraint ID_ORDER_ID primary key (id),
     foreign key (Typ_id) references DELIVERY,
     foreign key (Buy_id) references CUSTOMER);

create table STAFF (
     id numeric(32) not null,
     salary numeric(32) not null,
     NURSE numeric(32),
     HR numeric(32),
     DOCTOR numeric(32),
     CEO numeric(32),
     ANAESTHETIST numeric(32),
     ACCOUNTANT numeric(32),
     constraint ID_STAFF_PERSO_ID primary key (id),
     foreign key (id) references PERSON);

create table CEO (
     id numeric(32) not null,
     constraint ID_CEO_STAFF_ID primary key (id),
     foreign key (id) references STAFF);

create table DOCTOR (
     id numeric(32) not null,
     inami_number char(32) not null,
     constraint ID_DOCTO_STAFF_ID primary key (id),
     foreign key (id) references STAFF);

create table NURSE (
     id numeric(32) not null,
     constraint ID_NURSE_STAFF_ID primary key (id),
     foreign key (id) references STAFF);

create table ACCOUNTANT (
     id numeric(32) not null,
     constraint ID_ACCOU_STAFF_ID primary key (id),
     foreign key (id) references STAFF);

create table ANAESTHETIST (
     id numeric(32) not null,
     inami_number char(32) not null,
     constraint ID_ANAES_STAFF_ID primary key (id),
     foreign key (id) references STAFF);

create table HR (
     id numeric(32) not null,
     constraint ID_HR_STAFF_ID primary key (id),
     foreign key (id) references STAFF);

create table TRANSPLANTATION (
     date date not null,
     id numeric(32) unsigned not null AUTO_INCREMENT,
     Con_id numeric(32) not null,
     price float(32) not null,
     Rec_id numeric(32) not null,
     D_w_id numeric(32) not null,
     A_w_id numeric(32) not null,
     constraint ID_TRANSPLANTATION_ID primary key (id),
     constraint SID_TRANS_ORGAN_ID unique (Con_id),
     foreign key (Rec_id) references CUSTOMER,
     foreign key (Con_id) references ORGANE,
     foreign key (D_w_id) references DOCTOR,
     foreign key (A_w_id) references ANAESTHETIST);

create table BLOOD (
     id numeric(32) unsigned not null AUTO_INCREMENT,
     type varchar(2) not null,
     signe char not null,
     expiration_date date not null,
     quantity float(4) not null,
     Giv_id numeric(32),
     Nee_id numeric(32),
     constraint ID_BLOOD_ID primary key (id),
     foreign key (Giv_id) references PERSON,
     foreign key (Nee_id) references TRANSPLANTATION);
     
create table DONATOR (
     id numeric(32) unsigned not null AUTO_INCREMENT,
     Giv_id numeric(32) not null,
     gender char not null,
     age_range float(8) not null,
     constraint ID_DONATOR_ID primary key (id),
     constraint SID_DONAT_BLOOD_ID unique (Giv_id),
     foreign key (Giv_id) references BLOOD);

create table ORGANE (
     state char(32) not null,
     functionnal char not null,
     expiration_date date not null,
     expiration_date_transplatation date,
     method_of_preservation varchar(64) not null,
     type varchar(64) not null,
     id numeric(32) unsigned not null AUTO_INCREMENT,
     price float(32) not null,
     Com_id numeric(32) not null,
     constraint ID_ORGANE_ID primary key (id),
     foreign key (Com_id) references DONATOR,
     foreign key (TRANSPLANTATION.id) references TRANSPLANTATION);

create table DETAIL (
     BLOOD numeric(32),
     ORGANE numeric(32),
     id numeric(32) unsigned not null AUTO_INCREMENT,
     constraint SID_DETAIL_ID unique (BLOOD, ORGANE, id),
     foreign key (BLOOD) references BLOOD,
     foreign key (ORGANE) references ORGANE,
     foreign key (id) references ORDER);

create table TYPE_DELIVERY (
     id varchar(16) unsigned not null AUTO_INCREMENT,
     price numeric(4) not null,
     constraint ID_TYPE_DELIVERY_ID primary key (id));

create table DELIVERY (
     id numeric(32) unsigned not null AUTO_INCREMENT,
     departure_date date not null,
     arrival_date date not null,
     effective_arrival_date date not null,
     recipent_last_name varchar(64) not null,
     recipent_first_name varchar(64) not null,
     Typ_id varchar(16) not null,
     At_id numeric(32) not null,
     constraint ID_DELIVERY_ID primary key (id),
     foreign key (Typ_id) references TYPE_DELIVERY,
     foreign key (At_id) references ADDRESS);

create table N_work_on (
     N_N_id numeric(32) not null,
     id numeric(32) unsigned not null AUTO_INCREMENT,
     constraint ID_N_work_on_ID primary key (N_N_id, id),
     foreign key (id) references TRANSPLANTATION, 
     foreign key (N_N_id) references NURSE);


-- Constraints Section - Checks
-- ____________________________ 

alter table PERSON add constraint MAJOR
     check((DATE.NOW - PERSON.born_date =< 18));

alter table DETAIL add constraint EXTONE_DETAIL
     check((ORGANE is not null and BLOOD is null)
           or (ORGANE is null and BLOOD is not null)); 

alter table ORGANE add constraint ID_ORGANE_CHK
     check(exists(select * from DETAIL
                  where DETAIL.ORGANE = id)); 

alter table STAFF add constraint EXCL_STAFF
     check((CEO is not null and HR is null and ACCOUNTANT is null and ANAESTHETIST is null and NURSE is null and DOCTOR is null)
           or (CEO is null and HR is not null and ACCOUNTANT is null and ANAESTHETIST is null and NURSE is null and DOCTOR is null)
           or (CEO is null and HR is null and ACCOUNTANT is not null and ANAESTHETIST is null and NURSE is null and DOCTOR is null)
           or (CEO is null and HR is null and ACCOUNTANT is null and ANAESTHETIST is not null and NURSE is null and DOCTOR is null)
           or (CEO is null and HR is null and ACCOUNTANT is null and ANAESTHETIST is null and NURSE is not null and DOCTOR is null)
           or (CEO is null and HR is null and ACCOUNTANT is null and ANAESTHETIST is null and NURSE is null and DOCTOR is not null)
           or (CEO is null and HR is null and ACCOUNTANT is null and ANAESTHETIST is null and NURSE is null and DOCTOR is null)); 

alter table BLOOD add constraint ID_BLOOD_CHK
     check(exists(select * from DETAIL
                  where DETAIL.BLOOD = id)); 

alter table TRANSPLANTATION add constraint ID_TRANSPLANTATION_CHK
     check(exists(select * from N_work_on
                  where N_work_on.id = id));

alter table TRANSPLANTATION TYPE_DELIVERY ORGANE add constraint PRICE_POSITIF 
     check((TRANSPLANTATION.price > 0 and TYPE_DELIVERY.price > 0 and ORGANE.price > 0));

alter table ORGANE add constraint LIST_ORGANES
     check((ORGANE.type ))

alter table BLOOD add constraint TYPE_BLOOD
     check((BLOOD.type is A) or (BLOOD.type is B) or (BLOOD.type is AB) or (BLOOD.type is O))

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

create unique index PERSON_email
     on PERSON (email);

create index ORGANES_Types
     on ORGANE (type);

-- Vue Section
-- _____________ 



-- Trigger Section
-- _____________ 

create Trigger TRG_DELIVERY_DATES_EXPIRATION_CONTROL
     -- Trigger goal: Check if the date of delivery is after the date expiration of the organe
     -- Author: Yannis Van Achter
     before insert or update on DELIVERY
     for each row
     begin
          SELECT expiration_date INTO expiration 
               FROM ORGANE 
               WHERE ORGANE.id IN (SELECT DETAIL.organe 
                                   FROM DETAIL 
                                   WHERE DETAIL.id in (SELECT ORDER.id 
                                                       FROM ORDER 
                                                       WHERE ORDER.Typ_id = new.id)
                                   );
          
          if (new.arrival_date < expiration) then
               signal sqlstate '45000'
               set message_text = 'The date of delivery must be after the date expiration of the organe';
          end if;
     end;

create trigger TRG_CHECK_AVAILABILITY_TO_SELL
     -- Trigger goal: Checks if the organ is available before accept to sell it 
     -- Author: Aurélie Genot 
     before insert or update on DETAIL
     for each row 

-- Init Section
-- _____________

insert into TYPE_LIVRAISON values ('normal', 5);
insert into TYPE_LIVRAISON values ('express', 10);
insert into TYPE_LIVRAISON values ('internationnal', 15);
insert into TYPE_LIVRAISON values ('main propre', 3);