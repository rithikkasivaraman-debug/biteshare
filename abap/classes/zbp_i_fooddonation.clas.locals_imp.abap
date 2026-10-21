CLASS lhc_FoodDonation DEFINITION INHERITING FROM cl_abap_behavior_handler.
  PRIVATE SECTION.
    METHODS get_global_authorizations FOR GLOBAL AUTHORIZATION
      IMPORTING REQUEST requested_authorizations FOR FoodDonation RESULT result.

    METHODS earlynumbering_create FOR NUMBERING
      IMPORTING entities FOR CREATE FoodDonation.

    METHODS earlynumbering_cba_Deliveries FOR NUMBERING
      IMPORTING entities FOR CREATE FoodDonation\_Deliveries.

    -- Phase 4: Validation Rules
    METHODS validateQuantity FOR VALIDATE ON SAVE
      IMPORTING keys FOR FoodDonation~validateQuantity.

    METHODS validateUsableTime FOR VALIDATE ON SAVE
      IMPORTING keys FOR FoodDonation~validateUsableTime.

    METHODS validateMandatoryFields FOR VALIDATE ON SAVE
      IMPORTING keys FOR FoodDonation~validateMandatoryFields.

    -- Phase 5: Flow 1
    METHODS matchRecipient FOR DETERMINE ON MODIFY
      IMPORTING keys FOR FoodDonation~matchRecipient.

    -- Phase 5: Actions (Flow 2 & Flow 3)
    METHODS acceptDonation FOR MODIFY
      IMPORTING keys FOR ACTION FoodDonation~acceptDonation RESULT result.

    METHODS markPickedUp FOR MODIFY
      IMPORTING keys FOR ACTION FoodDonation~markPickedUp RESULT result.

    METHODS markDelivered FOR MODIFY
      IMPORTING keys FOR ACTION FoodDonation~markDelivered RESULT result.

ENDCLASS.

CLASS lhc_FoodDonation IMPLEMENTATION.

  METHOD get_global_authorizations.
    " Standard check - allow create/edit for active authorized roles
    result-%create = if_abap_behv=>auth-allowed.
    result-%update = if_abap_behv=>auth-allowed.
    result-%delete = if_abap_behv=>auth-allowed.
  ENDMETHOD.

  METHOD earlynumbering_create.
    SELECT MAX( donation_id ) FROM zbt_donation INTO @DATA(lv_max_id).
    DATA lv_current_num TYPE i.
    IF lv_max_id IS NOT INITIAL AND lv_max_id CP 'FD-*'.
      lv_current_num = lv_max_id+3(4).
    ELSE.
      lv_current_num = 0.
    ENDIF.

    LOOP AT entities INTO DATA(entity) WHERE DonationId IS INITIAL.
      lv_current_num += 1.
      DATA(lv_new_id) = |FD-{ lv_current_num WIDTH = 4 PAD = '0' }|.
      APPEND VALUE #( %cid        = entity-%cid
                      %is_draft   = entity-%is_draft
                      DonationId  = lv_new_id ) TO mapped-fooddonation.
    ENDLOOP.
  ENDMETHOD.

  METHOD earlynumbering_cba_Deliveries.
    SELECT MAX( delivery_id ) FROM zbt_delivery INTO @DATA(lv_max_del).
    DATA lv_del_num TYPE i.
    IF lv_max_del IS NOT INITIAL AND lv_max_del CP 'PD-*'.
      lv_del_num = lv_max_del+3(4).
    ELSE.
      lv_del_num = 0.
    ENDIF.

    LOOP AT entities INTO DATA(entity).
      LOOP AT entity-%target INTO DATA(target) WHERE DeliveryId IS INITIAL.
        lv_del_num += 1.
        DATA(lv_new_del_id) = |PD-{ lv_del_num WIDTH = 4 PAD = '0' }|.
        APPEND VALUE #( %cid        = target-%cid
                        %is_draft   = target-%is_draft
                        DeliveryId  = lv_new_del_id ) TO mapped-delivery.
      ENDLOOP.
    ENDLOOP.
  ENDMETHOD.

  METHOD validateQuantity.
    READ ENTITIES OF ZI_FoodDonation IN LOCAL MODE
      ENTITY FoodDonation
      FIELDS ( QuantityKg )
      WITH CORRESPONDING #( keys )
      RESULT DATA(donations).

    LOOP AT donations INTO DATA(donation).
      IF donation-QuantityKg <= 0.
        APPEND VALUE #( %tky = donation-%tky ) TO failed-fooddonation.
        APPEND VALUE #( %tky = donation-%tky
                        %msg = new_message_with_text(
                                 severity = if_abap_behv_message=>severity-error
                                 text     = 'Quantity must be greater than 0.' )
                      ) TO reported-fooddonation.
      ENDIF.
    ENDLOOP.
  ENDMETHOD.

  METHOD validateUsableTime.
    GET TIME STAMP FIELD DATA(lv_now).
    READ ENTITIES OF ZI_FoodDonation IN LOCAL MODE
      ENTITY FoodDonation
      FIELDS ( UsableUntil )
      WITH CORRESPONDING #( keys )
      RESULT DATA(donations).

    LOOP AT donations INTO DATA(donation).
      IF donation-UsableUntil IS NOT INITIAL AND donation-UsableUntil <= lv_now.
        APPEND VALUE #( %tky = donation-%tky ) TO failed-fooddonation.
        APPEND VALUE #( %tky = donation-%tky
                        %msg = new_message_with_text(
                                 severity = if_abap_behv_message=>severity-error
                                 text     = 'Usable Until must be a future time.' )
                      ) TO reported-fooddonation.
      ENDIF.
    ENDLOOP.
  ENDMETHOD.

  METHOD validateMandatoryFields.
    READ ENTITIES OF ZI_FoodDonation IN LOCAL MODE
      ENTITY FoodDonation
      FIELDS ( FoodType City )
      WITH CORRESPONDING #( keys )
      RESULT DATA(donations).

    LOOP AT donations INTO DATA(donation).
      IF donation-FoodType IS INITIAL OR donation-City IS INITIAL.
        APPEND VALUE #( %tky = donation-%tky ) TO failed-fooddonation.
        APPEND VALUE #( %tky = donation-%tky
                        %msg = new_message_with_text(
                                 severity = if_abap_behv_message=>severity-error
                                 text     = 'Food Type and City are required.' )
                      ) TO reported-fooddonation.
      ENDIF.
    ENDLOOP.
  ENDMETHOD.

  METHOD matchRecipient.
    READ ENTITIES OF ZI_FoodDonation IN LOCAL MODE
      ENTITY FoodDonation
      FIELDS ( City QuantityKg FoodType Status )
      WITH CORRESPONDING #( keys )
      RESULT DATA(donations).

    LOOP AT donations INTO DATA(donation) WHERE Status IS INITIAL OR Status = 'SUBMITTED'.
      " Find verified recipient organization in same city
      SELECT SINGLE recipient_id, contact_email
        FROM zbt_recipient
        WHERE is_verified  = 'X'
          AND city         = @donation-City
          AND capacity_kg >= @donation-QuantityKg
          AND ( food_type  = @donation-FoodType OR food_type = 'BOTH' )
        INTO @DATA(ls_matched).

      IF sy-subrc = 0.
        MODIFY ENTITIES OF ZI_FoodDonation IN LOCAL MODE
          ENTITY FoodDonation
          UPDATE FIELDS ( RecipientId Status )
          WITH VALUE #( ( %tky        = donation-%tky
                          RecipientId = ls_matched-recipient_id
                          Status      = 'MATCHED' ) ).

        zcl_biteshare_mailer=>send_recipient_alert(
          iv_email    = CONV #( ls_matched-contact_email )
          iv_quantity = donation-QuantityKg
          iv_type     = CONV #( donation-FoodType ) ).
      ELSE.
        MODIFY ENTITIES OF ZI_FoodDonation IN LOCAL MODE
          ENTITY FoodDonation
          UPDATE FIELDS ( Status )
          WITH VALUE #( ( %tky   = donation-%tky
                          Status = 'SUBMITTED' ) ).
      ENDIF.
    ENDLOOP.
  ENDMETHOD.

  METHOD acceptDonation.
    READ ENTITIES OF ZI_FoodDonation IN LOCAL MODE
      ENTITY FoodDonation
      ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT DATA(donations).

    LOOP AT donations INTO DATA(donation).
      " Find available volunteer in same city
      SELECT SINGLE volunteer_id, email
        FROM zbt_volunteer
        WHERE is_available = 'X'
          AND city         = @donation-City
        INTO @DATA(ls_vol).

      IF sy-subrc = 0.
        -- Update donation to VOL_ASSIGNED
        MODIFY ENTITIES OF ZI_FoodDonation IN LOCAL MODE
          ENTITY FoodDonation
          UPDATE FIELDS ( VolunteerId Status )
          WITH VALUE #( ( %tky        = donation-%tky
                          VolunteerId = ls_vol-volunteer_id
                          Status      = 'VOL_ASSIGNED' ) ).

        -- Mark volunteer unavailable
        UPDATE zbt_volunteer SET is_available = ' ' WHERE volunteer_id = ls_vol-volunteer_id.

        -- Create child Pickup/Delivery record
        SELECT MAX( delivery_id ) FROM zbt_delivery INTO @DATA(lv_max_del).
        DATA lv_del_num TYPE i.
        IF lv_max_del IS NOT INITIAL AND lv_max_del CP 'PD-*'.
          lv_del_num = lv_max_del+3(4).
        ELSE.
          lv_del_num = 0.
        ENDIF.
        lv_del_num += 1.
        DATA(lv_new_del_id) = |PD-{ lv_del_num WIDTH = 4 PAD = '0' }|.

        INSERT INTO zbt_delivery VALUES @( VALUE #(
          mandt       = sy-mandt
          delivery_id = lv_new_del_id
          donation_id = donation-DonationId
          status      = 'PENDING' ) ).

        zcl_biteshare_mailer=>send_volunteer_assignment(
          iv_email       = CONV #( ls_vol-email )
          iv_donation_id = CONV #( donation-DonationId ) ).
      ENDIF.
    ENDLOOP.

    READ ENTITIES OF ZI_FoodDonation IN LOCAL MODE
      ENTITY FoodDonation
      ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT DATA(updated_donations).

    result = VALUE #( FOR d IN updated_donations ( %tky = d-%tky %param = d ) ).
  ENDMETHOD.

  METHOD markPickedUp.
    GET TIME STAMP FIELD DATA(lv_now).
    READ ENTITIES OF ZI_FoodDonation IN LOCAL MODE
      ENTITY FoodDonation
      ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT DATA(donations).

    LOOP AT donations INTO DATA(donation).
      MODIFY ENTITIES OF ZI_FoodDonation IN LOCAL MODE
        ENTITY FoodDonation
        UPDATE FIELDS ( Status )
        WITH VALUE #( ( %tky   = donation-%tky
                        Status = 'PICKED_UP' ) ).

      UPDATE zbt_delivery
        SET status = 'PICKED_UP', pickup_time = lv_now
        WHERE donation_id = donation-DonationId.
    ENDLOOP.

    READ ENTITIES OF ZI_FoodDonation IN LOCAL MODE
      ENTITY FoodDonation
      ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT DATA(updated_donations).

    result = VALUE #( FOR d IN updated_donations ( %tky = d-%tky %param = d ) ).
  ENDMETHOD.

  METHOD markDelivered.
    GET TIME STAMP FIELD DATA(lv_now).
    READ ENTITIES OF ZI_FoodDonation IN LOCAL MODE
      ENTITY FoodDonation
      ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT DATA(donations).

    LOOP AT donations INTO DATA(donation).
      -- 1. Complete Donation
      MODIFY ENTITIES OF ZI_FoodDonation IN LOCAL MODE
        ENTITY FoodDonation
        UPDATE FIELDS ( Status )
        WITH VALUE #( ( %tky   = donation-%tky
                        Status = 'COMPLETED' ) ).

      -- 2. Free Volunteer
      IF donation-VolunteerId IS NOT INITIAL.
        UPDATE zbt_volunteer SET is_available = 'X' WHERE volunteer_id = donation-VolunteerId.
      ENDIF.

      -- 3. Update Delivery Record
      UPDATE zbt_delivery
        SET status = 'DELIVERED', delivery_time = lv_now
        WHERE donation_id = donation-DonationId.

      -- 4. Notify Admin / Coordinator
      zcl_biteshare_mailer=>send_admin_completion( iv_donation_id = CONV #( donation-DonationId ) ).
    ENDLOOP.

    READ ENTITIES OF ZI_FoodDonation IN LOCAL MODE
      ENTITY FoodDonation
      ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT DATA(updated_donations).

    result = VALUE #( FOR d IN updated_donations ( %tky = d-%tky %param = d ) ).
  ENDMETHOD.

ENDCLASS.
