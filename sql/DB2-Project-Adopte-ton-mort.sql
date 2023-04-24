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

-- create database db;

-- DBSpace Section
-- _______________


-- Tables Section
-- _____________ 

create table IF NOT EXISTS ADDRESS (
     street varchar(128) not null,
     number numeric(8) not null,
     postal_code numeric(16) not null,
     city varchar(128) not null,
     land varchar(128) not null,
     id INT unsigned not null AUTO_INCREMENT,
     constraint ID_ADDRESS_ID primary key (id),
     constraint SID_ADDRESS_ID unique (street, number, postal_code, city, land));

create table IF NOT EXISTS PERSON (
     id INT unsigned not null AUTO_INCREMENT,
     last_name varchar(64),
     first_name varchar(64),
     email varchar(128) not null,
     phone_number varchar(32),
     born_date date not null, -- check((DATE.NOW - PERSON.born_date) <= 18),
     password varchar(128) not null,
     Liv_id INT unsigned not null,
     constraint ID_PERSON_ID primary key (id),
     constraint FK_PersonAddress foreign key (Liv_id) references ADDRESS(id)
     );

create table IF NOT EXISTS CUSTOMER (
     id INT unsigned not null,
     pseudo varchar(32) not null,
     blood_type varchar(2) not null,
     blood_sign char not null,
     constraint ID_CUSTO_PERSO_ID primary key (id),
     constraint FK_CustomerPerson foreign key (id) references PERSON(id)
     );

create table IF NOT EXISTS TYPE_DELIVERY (
     id varchar(16) not null,
     price numeric(4) not null check(price > 0),
     constraint ID_TYPE_DELIVERY_ID primary key (id));

create table IF NOT EXISTS DELIVERY (
     id INT unsigned not null AUTO_INCREMENT,
     departure_date date not null,
     arrival_date date not null,
     effective_arrival_date date not null,
     recipent_last_name varchar(64) not null,
     recipent_first_name varchar(64) not null,
     Typ_id varchar(16) not null,
     At_id INT unsigned not null,
     constraint ID_DELIVERY_ID primary key (id),
     constraint FK_DeliveryTypeDelivery foreign key (Typ_id) references TYPE_DELIVERY(id),
     constraint FK_DeliveryAddress foreign key (At_id) references ADDRESS(id));

create table IF NOT EXISTS ORDER_ (
     id INT unsigned not null AUTO_INCREMENT,
     Typ_id INT unsigned not null,
     Buy_id INT unsigned not null,
     constraint ID_ORDER_ID primary key (id),
     constraint FK_OrderDelivery foreign key (Typ_id) references DELIVERY(id),
     constraint FK_OrderCustomer foreign key (Buy_id) references CUSTOMER(id));

create table IF NOT EXISTS STAFF ( 
     id INT unsigned not null,
     salary numeric(32) not null,
     job varchar(64),
     NURSE numeric(32),
     HR numeric(32),
     DOCTOR numeric(32),
     CEO numeric(32),
     ANAESTHESIST numeric(32),
     ACCOUNTANT numeric(32),
     constraint ID_STAFF_PERSO_ID primary key (id),
     constraint FK_StaffPerson foreign key (id) references PERSON(id));

create table IF NOT EXISTS CEO (
     id INT unsigned not null,
     constraint ID_CEO_STAFF_ID primary key (id),
     constraint FK_CEOStaff foreign key (id) references STAFF(id));

create table IF NOT EXISTS DOCTOR (
     id INT unsigned not null,
     inami_number char(32) not null,
     constraint ID_DOCTO_STAFF_ID primary key (id),
     constraint FK_DoctorStaff foreign key (id) references STAFF(id));

create table IF NOT EXISTS NURSE (
     id INT unsigned not null,
     constraint ID_NURSE_STAFF_ID primary key (id),
     constraint FK_NurseStaff foreign key (id) references STAFF(id));

create table IF NOT EXISTS ACCOUNTANT (
     id INT unsigned not null,
     constraint ID_ACCOU_STAFF_ID primary key (id),
     constraint FK_AccountantStaff foreign key (id) references STAFF(id));

create table IF NOT EXISTS ANAESTHESIST (
     id INT unsigned not null,
     inami_number char(32) not null,
     constraint ID_ANAES_STAFF_ID primary key (id),
     constraint FK_AnaesthesistStaff foreign key (id) references STAFF(id));

create table IF NOT EXISTS HR (
     id INT unsigned not null,
     constraint ID_HR_STAFF_ID primary key (id),
     constraint FK_HRStaff foreign key (id) references STAFF(id));

create table IF NOT EXISTS BLOOD (
     id INT unsigned not null AUTO_INCREMENT,
     type varchar(2) not null check(type = "A" or type = "B" or type = "O" or type = "AB"),
     signe char not null,
     expiration_date date not null,
     quantity float(4) not null,
     Giv_id INT unsigned,
     Nee_id INT unsigned,
     constraint ID_BLOOD_ID primary key (id),
     constraint FK_BloodPerson foreign key (Giv_id) references PERSON(id));
     
create table IF NOT EXISTS DONATOR (
     id INT unsigned not null AUTO_INCREMENT,
     Giv_id INT unsigned not null,
     gender char not null,
     age_range float(8) not null,
     constraint ID_DONATOR_ID primary key (id),
     constraint SID_DONAT_BLOOD_ID unique (Giv_id),
     constraint FK_DonatorBlood foreign key (Giv_id) references BLOOD(id));

create table IF NOT EXISTS ORGANE (
     state char(32) not null,
     functionnal char not null,
     expiration_date date not null,
     expiration_date_transplatation date,
     method_of_preservation varchar(64) not null,
     type varchar(64) not null,
     id INT unsigned not null AUTO_INCREMENT,
     price float(32) not null check(price > 0),
     Com_id INT unsigned not null,
     constraint ID_ORGANE_ID primary key (id),
     constraint FK_OrganeDonator foreign key (Com_id) references DONATOR(id));
     -- constraint FK_TransplantationTransplantation foreign key (TRANSPLANTATION.id) references TRANSPLANTATION); -- ???

create table IF NOT EXISTS TRANSPLANTATION (
     date date not null,
     id INT unsigned not null AUTO_INCREMENT,
     Con_id INT unsigned not null,
     price float(32) not null check(price > 0),
     Rec_id INT unsigned not null,
     D_w_id INT unsigned not null,
     A_w_id INT unsigned not null,
     constraint ID_TRANSPLANTATION_ID primary key (id),
     constraint SID_TRANS_ORGAN_ID unique (Con_id),
     constraint FK_TransplantationCustomer foreign key (Rec_id) references CUSTOMER(id),
     constraint FK_TransplantationOrgane foreign key (Con_id) references ORGANE(id), -- TODO: have to be done with alter table
     constraint FK_TransplantationDoctor foreign key (D_w_id) references DOCTOR(id),
     constraint FK_TransplantationAnaesthesist foreign key (A_w_id) references ANAESTHESIST(id));

create table IF NOT EXISTS DETAIL (
     BLOOD INT unsigned,
     ORGANE INT unsigned,
     id INT unsigned not null,
     constraint SID_DETAIL_ID unique (BLOOD, ORGANE, id),
     foreign key (BLOOD) references BLOOD(id),
     foreign key (ORGANE) references ORGANE(id),
     foreign key (id) references ORDER_(id),
     constraint EXTONE_DETAIL check(
          (ORGANE is not null and BLOOD is null)
          or (ORGANE is null and BLOOD is not null))
     );

create table IF NOT EXISTS N_work_on (
     N_N_id INT unsigned not null,
     id INT unsigned not null,
     constraint ID_N_work_on_ID primary key (N_N_id, id),
     constraint FK_NWorkOnTransplantation foreign key (id) references TRANSPLANTATION(id), 
     constraint FK_NWorkOnNurse foreign key (N_N_id) references NURSE(id));


-- Constraints Section - Checks
-- ____________________________ 

-- alter table ORGANE add constraint ID_ORGANE_CHK
--      check(exists(select * from DETAIL
--                   where DETAIL.ORGANE = id)); 

alter table STAFF add constraint EXCL_STAFF
     check((CEO is not null and HR is null and ACCOUNTANT is null and ANAESTHESIST is null and NURSE is null and DOCTOR is null)
           or (CEO is null and HR is not null and ACCOUNTANT is null and ANAESTHESIST is null and NURSE is null and DOCTOR is null)
           or (CEO is null and HR is null and ACCOUNTANT is not null and ANAESTHESIST is null and NURSE is null and DOCTOR is null)
           or (CEO is null and HR is null and ACCOUNTANT is null and ANAESTHESIST is not null and NURSE is null and DOCTOR is null)
           or (CEO is null and HR is null and ACCOUNTANT is null and ANAESTHESIST is null and NURSE is not null and DOCTOR is null)
           or (CEO is null and HR is null and ACCOUNTANT is null and ANAESTHESIST is null and NURSE is null and DOCTOR is not null)
           or (CEO is null and HR is null and ACCOUNTANT is null and ANAESTHESIST is null and NURSE is null and DOCTOR is null)); 

-- alter table BLOOD add constraint ID_BLOOD_CHK 
--      check(exists(select * from DETAIL
--                   where DETAIL.BLOOD = id)); 

-- alter table TRANSPLANTATION add constraint ID_TRANSPLANTATION_CHK
--      check(exists(select * from N_work_on
--                   where N_work_on.id = id));

alter table BLOOD add
     constraint FK_BloodTransplantation foreign key (Nee_id) references TRANSPLANTATION(id);

-- alter table ORGANE add constraint LIST_ORGANES
--      check((ORGANE.type));

-- Index Section
-- _____________ 

create unique index ID_ADDRESS_IND
     on ADDRESS (id);

create unique index SID_ADDRESS_IND
     on ADDRESS (street, number, postal_code, city, land);

create unique index ID_ANAES_STAFF_IND
     on ANAESTHESIST (id);

create unique index ID_CUSTO_PERSO_IND
     on CUSTOMER (id);

create unique index ID_ORDER_IND
     on ORDER_ (id);

create index REF_ORDER_DELIV_IND
     on ORDER_ (Typ_id);

create index REF_ORDER_CUSTO_IND
     on ORDER_ (Buy_id);

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

-- create personnal index
create unique index PERSON_email
     on PERSON (email);

create index ORGANES_Types
     on ORGANE (type);

-- View Section
-- _____________ 
-- create view ACCOUNTABLEORGABLO(O.type, O.price, B.type, B.signe)
--      -- View goal : view accountable to view the price of the articles 
--      -- Authors: Aline Boulanger  et Louise Delpierre
--      as  select O.type, B.type, B.signe, O.price
--      from ORGANE O, BLOOD B
--      where O.type = O.price
--      and B.type = B.signe 
--      group by O.type and  B.type

-- create view ACCOUNTABLETRANPLANLIVRAI(PRICE, TYPE)
--      -- View goal : view accountable to view the price of the transplantation and the delivery
--      -- Author: Aline Boulanger et Louise Delpierre
--      as  select TD.price
--      from TRANSPLANTATION T, DELIVERY D, TYPE_DELIVERY TD, CUSTOMER C, ADDRESS A
--      where D.Typ_id = TD.id
--      and C.id = A.id
   

-- create view RH (SALARY, S.DOCTOR, S.NURSE, S.ANAESTHESIST, S.CEO, S.ACCOUNTABLE, S.HR, NAME, FIRST_NAME, EMAIL, PHONE)
--      -- View goal : view RH, to view the staff, the wages, jobs
--      -- Author: Louise DELPIERRE et Aline Boulanger 
--      as  select S.salary, S.DOCTOR, S.NURSE, S.ANAESTHESIST, S.CEO, S.ACCOUNTABLE, S.HR, P.first_name, P.last_name, P.email, P.phone_number  
--      from  STAFF S, PERSON P, DOCTOR D, NURSE N, ANAESTHESIST A, CEO C, ACCOUNTABLE AC, HR H, ADDRESS AD
--      where id.STAFF = id.PERSON
--      and S.NURSE = N.NURSE
--      and S.ANAESTHESIST = A.ANAESTHESIST
--      and S.CEO = C.CEO
--      and S.ACCOUNTABLE = AC.ACCOUNTABLE
--      and S.HR = H.HR
--      and S.DOCTOR = D.DOCTOR
--      and id.PERSON = id.ADDRESS
--      group by S.DOCTOR
--      group by S.NURSE
--      group by S.ANAESTHESIST
--      group by S.CEO
--      group by S.ACCOUNTABLE
--      group by S.HR

-- create view MEDECIN (organe, client, sang, anesthesiste, medecin)
-- -- View goal: view information on the customer and the organ the doctor will have to transplant on him 
-- -- Authors: Eline Mota
-- as select type.ORGANE, Rec_id.TRANSPLANTATION, blood_type.CUSTOMER, id.ANAESTHESIST, id.DOCTOR
-- from ORGANE O, TRANSPLANTATION T, CUSTOMER C, ANAESTHESIST A, DOCTOR M
-- where T.Rec_id = C.id and T.Con_id = O.id and T.D_w_id = M.id and T.A_w_id = A.id




-- Trigger Section
-- _____________ 

-- create trigger TRG_DELIVERY_DATES_EXPIRATION_CONTROL
--      -- Trigger goal: Check if the date of delivery is before the date expiration of the organe
--      -- Author: Yannis Van Achter
--      before insert or update on DELIVERY
--      for each row
--      begin
--           SELECT expiration_date INTO expiration 
--                FROM ORGANE 
--                WHERE ORGANE.id IN (SELECT DETAIL.organe 
--                                    FROM DETAIL 
--                                    WHERE DETAIL.id in (SELECT ORDER.id 
--                                                        FROM ORDER 
--                                                        WHERE ORDER.Typ_id = new.id)
--                                    );
          
--           if (new.arrival_date < expiration) then
--                signal sqlstate '45000'
--                set message_text = 'The date of delivery must be after the date expiration of the organe';
--           end if;
--      end;

-- create trigger TRG_CHECK_AVAILABILITY_ORGAN_TO_SELL
--      -- Trigger goal: Checks if the organ is available before accept to sell it 
--      -- Author: Aurélie Genot 
--      before insert or update on DETAIL
--      for each row 
--      begin 
--           if new.ORGANE not exists ( SELECT *
--                                         FROM ORGANE 
--                                         WHERE NOT EXISTS (SELECT null
--                                                        FROM TRANSPLANTATION
--                                                        WHERE TANSPLANTATION.id = ORGANE.id);)
--           then 
--                signal sqlstate '45000'
--                set message_text = 'The organ that you want to sell is not available anymore';
--           end if; 
--      end; 

     
-- create trigger TRG_CHECK_AVAILABILITY_ORGAN_TO_TRANSPLANT
--      -- Trigger goal: Checks if the organ is available before accept to transplant it 
--      -- Author: Aurélie Genot 
--      before insert or update on TRANSPLANTATION
--      for each row 
--      begin 
--           if new.ORGANE not exists ( SELECT *
--                                         FROM ORGANE 
--                                         WHERE NOT EXISTS (SELECT null
--                                                        FROM DETAIL
--                                                        WHERE DETAIL.id = ORGANE.id);)
--           then 
--                signal sqlstate '45000'
--                set message_text = 'The organ that you want to transplant is not available anymore';
--           end if; 
--      end; 


-- create trigger TRG_CHECK_AVAILABILITY_BLOOD_TO_SELL
--      -- Trigger goal: Checks if the blood is available before accept to sell it 
--      -- Author: Aurélie Genot 
--      before insert or update on DETAIL
--      for each row 
--      begin 
--           if new.BLOOD not exists ( SELECT *
--                                         FROM BLOOD
--                                         WHERE NOT EXISTS (SELECT null
--                                                        FROM TRANSPLANTATION
--                                                        WHERE TANSPLANTATION.id = BLOOD.id);)
--           then 
--                signal sqlstate '45000'
--                set message_text = 'The blood that you want to sell is not available anymore';
--           end if; 
--      end; 
   
-- create trigger TRG_CHECK_AVAILABILITY_BLOOD_TO_TRANSPLANT
--      -- Trigger goal: Checks if the blood is available before accept to transplant it 
--      -- Author: Aurélie Genot 
--      before insert or update on TRANSPLANTATION
--      for each row 
--      begin 
--           if new.BLOOD not exists ( SELECT *
--                                         FROM BLOOD 
--                                         WHERE NOT EXISTS (SELECT null
--                                                        FROM DETAIL
--                                                        WHERE DETAIL.id = BLOOD.id);)
--           then 
--                signal sqlstate '45000'
--                set message_text = 'The blood that you want to transplant is not available anymore';
--           end if; 
--      end; 

-- Init Section
-- _____________

insert into TYPE_DELIVERY values ('normal', 5);
insert into TYPE_DELIVERY values ('express', 10);
insert into TYPE_DELIVERY values ('internationnal', 15);
insert into TYPE_DELIVERY values ('main propre', 3);