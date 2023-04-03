-- *********************************************
-- * Standard SQL generation                   
-- *--------------------------------------------
-- * DB-MAIN version: 11.0.2              
-- * Generator date: Sep 14 2021              
-- * Generation date: Mon Apr  3 15:41:35 2023 
-- * LUN file: C:\Users\yanni\OneDrive\Documents\GitHub\INFOB212-BD2-project\schema\conceptual-schema.lun 
-- * Schema: Physique V4/SQL 
-- ********************************************* 


-- Database Section
-- ________________ 

create database Physique_V4;


-- DBSpace Section
-- _______________


-- Tables Section
-- _____________ 

create table ADRESSE (
     Rue varchar(128) not null,
     Numero varchar(8) not null,
     Code_postal numeric(16) not null,
     Ville varchar(128) not null,
     Pays varchar(128) not null,
     ID numeric(32) not null,
     constraint ID_ADRESSE_ID primary key (ID),
     constraint SID_ADRESSE_ID unique (Rue, Numero, Code_postal, Ville, Pays));

create table TYPE_LIVRAISON (
     type_name varchar(16) not null,
     price numeric(4) not null,
     constraint ID_TYPE_LIVRAISON_ID primary key (type_name));

create table Livraison (
     ID numeric(32) not null,
     date_depart date not null,
     date_arrive date not null,
     date_arrive_eff date not null,
     nom_destinataire varchar(64) not null,
     prenom_destinataire varchar(64) not null,
     type_name varchar(16) not null,
     A_ID numeric(32) not null,
     constraint ID_Livraison_ID primary key (ID)
     foreign key (type_name) references TYPE_LIVRAISON
     foreign key (A_ID) references ADRESSE);

create table MEDECIN (
     id numeric(32) not null,
     nb_inami char(32) not null,
     constraint ID_MEDEC_PERSO_ID primary key (id),
     constraint SID_MEDECIN_ID unique (nb_inami));

create table ORGANE (
     etat char(32) not null,
     fonctionnnel char not null,
     date_peremption date not null,
     date_peremption_transplantation date,
     methode_de_conservation varchar(64) not null,
     type varchar(64) not null,
     id_organe numeric(32) not null,
     prix float(64) not null,
     id_donneur numeric(32) not null,
     constraint ID_ORGANE_ID primary key (id_organe));

create table PDG (
     id numeric(32) not null,
     constraint ID_PDG_PERSO_ID primary key (id));

create table PERSONNE (
     id numeric(32) not null,
     Nom varchar(64),
     Prenom varchar(64),
     email varchar(128) not null,
     telephone varchar(32),
     Date_naissance date not null,
     MDP varchar(128) not null,
     Hab_ID numeric(32) not null,
     constraint ID_PERSONNE_ID primary key (id));

create table CLIENT (
     id numeric(32) not null,
     Pseudo varchar(32) not null,
     type_sang varchar(2) not null,
     signe_sang char not null,
     constraint ID_CLIEN_PERSO_ID primary key (id)
     foreign key (id) references PERSONNE);

create table COMMANDE (
     id_commande numeric(32) not null,
     ID numeric(32) not null,
     Ach_id numeric(32) not null,
     constraint ID_COMMANDE_ID primary key (id_commande)
     foreign key (ID) references Livraison
     foreign key (Ach_id) references CLIENT);

create table PERSONNEL (
     id numeric(32) not null,
     salaire numeric(32) not null,
     PDG numeric(32),
     MEDECIN numeric(32),
     INFIRMIER numeric(32),
     COMPTABLE numeric(32),
     ANESTHESISTE numeric(32),
     RH numeric(32),
     constraint ID_PERSO_PERSO_ID primary key (id));

create table INFIRMIER (
     id numeric(32) not null,
     constraint ID_INFIR_PERSO_ID primary key (id)
     foreign key (id) references PERSONNEL);

create table COMPTABLE (
     id numeric(32) not null,
     constraint ID_COMPT_PERSO_ID primary key (id)
     foreign key (id) references PERSONNEL);

create table ANESTHESISTE (
     id numeric(32) not null,
     nb_inami char(32) not null,
     constraint ID_ANEST_PERSO_ID primary key (id),
     constraint SID_ANESTHESISTE_ID unique (nb_inami)
     foreign key (id) references PERSONNEL);


create table Contient (
     id numeric(32) not null,
     R_S_ID numeric(32),
     id_organe numeric(32),
     constraint ID_Contient_ID primary key (id),
     constraint SID_Conti_SANG_ID unique (R_S_ID),
     constraint SID_Conti_ORGAN_ID unique (id_organe));

create table DETAIL (
     id_commande numeric(32) not null,
     id numeric(32) not null,
     constraint SID_DETAI_Conti_ID unique (id),
     constraint ID_DETAIL_ID primary key (id_commande, id)
     foreign key (id) references Contient
     foreign key (id_commande) references COMMANDE);

create table RH (
     id numeric(32) not null,
     constraint ID_RH_PERSO_ID primary key (id));

create table SANG (
     ID numeric(32) not null,
     type varchar(2) not null,
     signe char not null,
     date_peremption_ date not null,
     quantite float(1) not null,
     Don_id numeric(32),
     id_transplantation char(1),
     constraint ID_SANG_ID primary key (ID));

create table DONNEUR (
     id_donneur numeric(32) not null,
     ID numeric(32) not null,
     genre char not null,
     tranche_age float(1) not null,
     constraint ID_DONNEUR_ID primary key (id_donneur),
     constraint SID_DONNE_SANG_ID unique (ID)
     foreign key (ID) references SANG);

create table TRANSPLANTATION (
     date date not null,
     id_transplantation char(1) not null,
     id_organe numeric(32) not null,
     prix_operation float(1) not null,
     id numeric(32) not null,
     A_t_id numeric(32) not null,
     Rec_id numeric(32) not null,
     constraint ID_TRANSPLANTATION_ID primary key (id_transplantation),
     constraint SID_TRANS_ORGAN_ID unique (id_organe));

create table I_travail_sur (
     id numeric(32) not null,
     id_transplantation char(1) not null,
     constraint ID_I_travail_sur_ID primary key (id, id_transplantation)
     foreign key (id_transplantation) references TRANSPLANTATION
     foreign key (id) references INFIRMIER);



-- Constraints Section
-- ___________________ 


alter table MEDECIN add constraint ID_MEDEC_PERSO_FK
     foreign key (id)
     references PERSONNEL;

alter table ORGANE add constraint REF_ORGAN_DONNE_FK
     foreign key (id_donneur)
     references DONNEUR;

alter table PDG add constraint ID_PDG_PERSO_FK
     foreign key (id)
     references PERSONNEL;

alter table PERSONNE add constraint REF_PERSO_ADRES_FK
     foreign key (Hab_ID)
     references ADRESSE;

alter table PERSONNEL add constraint EXCL_PERSONNEL
     check((PDG is not null and RH is null and COMPTABLE is null and ANESTHESISTE is null and INFIRMIER is null and MEDECIN is null)
           or (PDG is null and RH is not null and COMPTABLE is null and ANESTHESISTE is null and INFIRMIER is null and MEDECIN is null)
           or (PDG is null and RH is null and COMPTABLE is not null and ANESTHESISTE is null and INFIRMIER is null and MEDECIN is null)
           or (PDG is null and RH is null and COMPTABLE is null and ANESTHESISTE is not null and INFIRMIER is null and MEDECIN is null)
           or (PDG is null and RH is null and COMPTABLE is null and ANESTHESISTE is null and INFIRMIER is not null and MEDECIN is null)
           or (PDG is null and RH is null and COMPTABLE is null and ANESTHESISTE is null and INFIRMIER is null and MEDECIN is not null)
           or (PDG is null and RH is null and COMPTABLE is null and ANESTHESISTE is null and INFIRMIER is null and MEDECIN is null)); 

alter table PERSONNEL add constraint ID_PERSO_PERSO_FK
     foreign key (id)
     references PERSONNE;

alter table Contient add constraint ID_Contient_CHK
     check(exists(select * from DETAIL
                  where DETAIL.id = id)); 

alter table Contient add constraint SID_Conti_SANG_FK
     foreign key (R_S_ID)
     references SANG;

alter table Contient add constraint SID_Conti_ORGAN_FK
     foreign key (id_organe)
     references ORGANE;

alter table Contient add constraint EXCL_Contient
     check((R_S_ID is not null and id_organe is null)
           or (R_S_ID is null and id_organe is not null)
           or (R_S_ID is null and id_organe is null)); 

alter table RH add constraint ID_RH_PERSO_FK
     foreign key (id)
     references PERSONNEL;

alter table SANG add constraint REF_SANG_PERSO_FK
     foreign key (Don_id)
     references PERSONNE;

alter table SANG add constraint REF_SANG_TRANS_FK
     foreign key (id_transplantation)
     references TRANSPLANTATION;

alter table TRANSPLANTATION add constraint ID_TRANSPLANTATION_CHK
     check(exists(select * from I_travail_sur
                  where I_travail_sur.id_transplantation = id_transplantation)); 

alter table TRANSPLANTATION add constraint REF_TRANS_MEDEC_FK
     foreign key (id)
     references MEDECIN;

alter table TRANSPLANTATION add constraint SID_TRANS_ORGAN_FK
     foreign key (id_organe)
     references ORGANE;

alter table TRANSPLANTATION add constraint REF_TRANS_ANEST_FK
     foreign key (A_t_id)
     references ANESTHESISTE;

alter table TRANSPLANTATION add constraint REF_TRANS_CLIEN_FK
     foreign key (Rec_id)
     references CLIENT;


-- Index Section
-- _____________ 

create unique index ID_ADRESSE_IND
     on ADRESSE (ID);

create unique index SID_ADRESSE_IND
     on ADRESSE (Rue, Numero, Code_postal, Ville, Pays);

create unique index ID_ANEST_PERSO_IND
     on ANESTHESISTE (id);

create unique index SID_ANESTHESISTE_IND
     on ANESTHESISTE (nb_inami);

create unique index ID_CLIEN_PERSO_IND
     on CLIENT (id);

create unique index ID_COMMANDE_IND
     on COMMANDE (id_commande);

create index REF_COMMA_Livra_IND
     on COMMANDE (ID);

create index REF_COMMA_CLIEN_IND
     on COMMANDE (Ach_id);

create unique index ID_COMPT_PERSO_IND
     on COMPTABLE (id);

create unique index SID_DETAI_Conti_IND
     on DETAIL (id);

create unique index ID_DETAIL_IND
     on DETAIL (id_commande, id);

create unique index ID_DONNEUR_IND
     on DONNEUR (id_donneur);

create unique index SID_DONNE_SANG_IND
     on DONNEUR (ID);

create unique index ID_I_travail_sur_IND
     on I_travail_sur (id, id_transplantation);

create index EQU_I_tra_TRANS_IND
     on I_travail_sur (id_transplantation);

create unique index ID_INFIR_PERSO_IND
     on INFIRMIER (id);

create unique index ID_Livraison_IND
     on Livraison (ID);

create index REF_Livra_TYPE__IND
     on Livraison (type_name);

create index REF_Livra_ADRES_IND
     on Livraison (A_ID);

create unique index ID_MEDEC_PERSO_IND
     on MEDECIN (id);

create unique index SID_MEDECIN_IND
     on MEDECIN (nb_inami);

create unique index ID_ORGANE_IND
     on ORGANE (id_organe);

create index REF_ORGAN_DONNE_IND
     on ORGANE (id_donneur);

create unique index ID_PDG_PERSO_IND
     on PDG (id);

create unique index ID_PERSONNE_IND
     on PERSONNE (id);

create index REF_PERSO_ADRES_IND
     on PERSONNE (Hab_ID);

create unique index ID_PERSO_PERSO_IND
     on PERSONNEL (id);

create unique index ID_Contient_IND
     on Contient (id);

create unique index SID_Conti_SANG_IND
     on Contient (R_S_ID);

create unique index SID_Conti_ORGAN_IND
     on Contient (id_organe);

create unique index ID_RH_PERSO_IND
     on RH (id);

create unique index ID_SANG_IND
     on SANG (ID);

create index REF_SANG_PERSO_IND
     on SANG (Don_id);

create index REF_SANG_TRANS_IND
     on SANG (id_transplantation);

create unique index ID_TRANSPLANTATION_IND
     on TRANSPLANTATION (id_transplantation);

create index REF_TRANS_MEDEC_IND
     on TRANSPLANTATION (id);

create unique index SID_TRANS_ORGAN_IND
     on TRANSPLANTATION (id_organe);

create index REF_TRANS_ANEST_IND
     on TRANSPLANTATION (A_t_id);

create index REF_TRANS_CLIEN_IND
     on TRANSPLANTATION (Rec_id);

create unique index ID_TYPE_LIVRAISON_IND
     on TYPE_LIVRAISON (type_name);

