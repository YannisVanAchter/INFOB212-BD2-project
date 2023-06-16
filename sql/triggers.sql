-- To Execute in Datagrip, for some reason they work there but doesn't when added to the sql file sent to the Docker container

create trigger TRG_DELIVERY_DATES_EXPIRATION_CONTROL_INSERT
     -- Trigger goal: Check if the date of delivery is before the date expiration of the organe
     -- Author: Yannis Van Achter
     before insert on DELIVERY
     for each row
     begin
          DECLARE expiration DATE;
          SELECT expiration_date INTO expiration
               FROM ORGANE
               WHERE ORGANE.id IN (SELECT DETAIL.organe
                                   FROM DETAIL
                                   WHERE DETAIL.id in (SELECT id
                                                       FROM ORDER_
                                                       WHERE Typ_id = new.id)
                                   );

          if (new.arrival_date < expiration) then
               signal sqlstate '45000'
               set message_text = 'The date of delivery must be after the date expiration of the organe';
          end if;
     end;

create trigger TRG_DELIVERY_DATES_EXPIRATION_CONTROL_UPDATE
     -- Trigger goal: Check if the date of delivery is before the date expiration of the organe
     -- Author: Yannis Van Achter
     before update on DELIVERY
     for each row
     begin
          DECLARE expiration DATE;
          SELECT expiration_date INTO expiration 
               FROM ORGANE 
               WHERE ORGANE.id IN (SELECT DETAIL.organe 
                                   FROM DETAIL 
                                   WHERE DETAIL.id in (SELECT id
                                                       FROM ORDER_ 
                                                       WHERE Typ_id = new.id)
                                   );
          
          if (new.arrival_date < expiration) then
               signal sqlstate '45000'
               set message_text = 'The date of delivery must be after the date expiration of the organe';
          end if;
     end;


create trigger TRG_CHECK_AVAILABILITY_ORGAN_TO_SELL_INSERT
     -- Trigger goal: Checks if the organ is available before accept to sell it
     -- Author: Aurélie Genot
     before insert on DETAIL
     for each row
     begin
          if (new.ORGANE IS NOT NULL AND (new.ORGANE in (SELECT Con_id
                                                       FROM TRANSPLANTATION
                                                       WHERE Con_id = new.ORGANE)) OR (new.ORGANE in 
                                                            (SELECT ORGANE
                                                            FROM DETAIL 
                                                            WHERE ORGANE = new.ORGANE)))
          then
               signal sqlstate '45000'
               set message_text = 'The organ that you want to sell is not available anymore';
          end if;
     end;

create trigger TRG_CHECK_AVAILABILITY_ORGAN_TO_SELL_UPDATE
     -- Trigger goal: Checks if the organ is available before accept to sell it
     -- Author: Aurélie Genot
     before update on DETAIL
     for each row
     begin
          if (new.ORGANE IS NOT NULL AND (new.ORGANE in (SELECT Con_id
                                                       FROM TRANSPLANTATION
                                                       WHERE Con_id = new.ORGANE)) OR (new.ORGANE in 
                                                            (SELECT ORGANE
                                                            FROM DETAIL 
                                                            WHERE ORGANE = new.ORGANE)))
          then
               signal sqlstate '45000'
               set message_text = 'The organ that you want to sell is not available anymore';
          end if;
     end;
     
create trigger TRG_CHECK_AVAILABILITY_ORGAN_TO_TRANSPLANT_INSERT
     -- Trigger goal: Checks if the organ is available before accept to transplant it
     -- Author: Aurélie Genot
     before insert on TRANSPLANTATION
     for each row
     begin
          if (new.Con_id IS NOT NULL AND (new.Con_id in (SELECT ORGANE
                                                       FROM DETAIL
                                                       WHERE ORGANE = new.Con_id) OR new.Con_id in 
                                                            (SELECT Con_id
                                                            FROM TRANSPLANTATION
                                                            WHERE Con_id = new.Con_id)))
          then
               signal sqlstate '45000'
               set message_text = 'The organ that you want to transplant is not available anymore';
          end if;
     end;

create trigger TRG_CHECK_AVAILABILITY_ORGAN_TO_TRANSPLANT_UPDATE
     -- Trigger goal: Checks if the organ is available before accept to transplant it
     -- Author: Aurélie Genot
     before update on TRANSPLANTATION
     for each row
     begin
          if (new.Con_id IS NOT NULL AND (new.Con_id in (SELECT ORGANE
                                                       FROM DETAIL
                                                       WHERE ORGANE = new.Con_id) OR new.Con_id in 
                                                            (SELECT Con_id
                                                            FROM TRANSPLANTATION
                                                            WHERE Con_id = new.Con_id)))
          then
               signal sqlstate '45000'
               set message_text = 'The organ that you want to transplant is not available anymore';
          end if;
     end;

create trigger TRG_CHECK_AVAILABILITY_BLOOD_TO_SELL_INSERT
     -- Trigger goal: Checks if the blood is available before accept to sell it
     -- Author: Aurélie Genot
    before insert on DETAIL
    for each row
    begin
          if (new.BLOOD is not null and (new.BLOOD in 
               (SELECT id 
               FROM BLOOD 
               WHERE Nee_id is not null) OR new.BLOOD in 
                    (SELECT BLOOD
                    FROM DETAIL
                    WHERE BLOOD = new.BLOOD)))
          then
               signal sqlstate '45000'
               set message_text = 'The blood that you want to sell is not available anymore';
          end if;
    end;

create trigger TRG_CHECK_AVAILABILITY_BLOOD_TO_SELL_UPDATE
     -- Trigger goal: Checks if the blood is available before accept to sell it
     -- Author: Aurélie Genot
     before update on DETAIL
     for each row
     begin
          if (new.BLOOD is not null and (new.BLOOD in 
               (SELECT id 
               FROM BLOOD 
               WHERE Nee_id is not null) OR new.BLOOD in 
                    (SELECT BLOOD
                    FROM DETAIL
                    WHERE BLOOD = new.BLOOD)))
          then
               signal sqlstate '45000'
               set message_text = 'The blood that you want to sell is not available anymore';
          end if;
     end;

create trigger TRG_CHECK_AVAILABILITY_BLOOD_TO_TRANSPLANT_INSERT
     -- Trigger goal: Checks if the blood is available before accept to use it during tranplant
     -- Author: Youlan Collard
     before update on BLOOD
     for each row
     begin
          if (old.Nee_id is null and new.Nee_id is not null and (
               new.id in (SELECT BLOOD 
                         FROM DETAIL
                         WHERE BLOOD = new.id)))
          then
               signal sqlstate '45000'
               set message_text = 'The blood that you wish to transplant is not available';
          end if;
     end;
   

create trigger TRG_UPDATE_MEDECINS
  -- Trigger goal: Before update a medecin checks if this employee has to do a transplantation (in the future)
  -- Author: Aurélie Genot
  before update on DOCTOR
  for each row
     begin
          DECLARE transplantation_in_future INT;
          SELECT count(date_) into transplantation_in_future
               FROM TRANSPLANTATION
               WHERE D_w_id = new.id and date_ > CURRENT_DATE()
               ORDER BY date_ DESC
               LIMIT 1;
          if (transplantation_in_future > 0) then
               signal sqlstate '45000'
               set message_text = 'This person cannot be deleted because she has to do a transplatation';
          end if;
     end;


create trigger TRG_CHECK_STAFF_NOT_OPERATING_THEMSELF_INSERT
     -- Tigger goal: Checks if the receiver of an organ is not operating themself
     -- Author: Youlan Collard
     before insert on TRANSPLANTATION
     for each row
     begin
          if (new.Rec_id = new.D_w_id or new.Rec_id = new.A_w_id or exists (
               SELECT * FROM N_work_on
               WHERE id = new.id and N_N_id = new.Rec_id
          ))
          then
               signal sqlstate '45000'
               set message_text = 'The receiver of an organ can not be in the transplant team';
          end if;
     end;

create trigger TRG_CHECK_STAFF_NOT_OPERATING_THEMSELF_UPDATE
     -- Tigger goal: Checks if the receiver of an organ is not operating themself
     -- Author: Youlan Collard
     before update on TRANSPLANTATION
     for each row
     begin
          if (new.Rec_id = new.D_w_id or new.Rec_id = new.A_w_id or exists (
               SELECT * FROM N_work_on
               WHERE id = new.id and N_N_id = new.Rec_id
          ))
          then
               signal sqlstate '45000'
               set message_text = 'The receiver of an organ can not be in the transplant team';
          end if;
     end;