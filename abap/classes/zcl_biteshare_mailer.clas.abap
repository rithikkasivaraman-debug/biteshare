CLASS zcl_biteshare_mailer DEFINITION
  PUBLIC
  FINAL
  CREATE PUBLIC .

  PUBLIC SECTION.
    CLASS-METHODS send_recipient_alert
      IMPORTING
        iv_email    TYPE string
        iv_quantity TYPE dec6_0
        iv_type     TYPE string.

    CLASS-METHODS send_volunteer_assignment
      IMPORTING
        iv_email       TYPE string
        iv_donation_id TYPE string.

    CLASS-METHODS send_admin_completion
      IMPORTING
        iv_donation_id TYPE string.
ENDCLASS.

CLASS zcl_biteshare_mailer IMPLEMENTATION.
  METHOD send_recipient_alert.
    " Production implementation using standard SAP cl_bcs
    TRY.
        DATA(lo_send_request) = cl_bcs=>create_persistent( ).
        DATA(lv_subject) = |Surplus food available - { iv_quantity } kg of { iv_type }|.
        DATA(lo_document) = cl_document_bcs=>create_document(
                              i_type    = 'RAW'
                              i_text    = VALUE #( ( |Hello, surplus food has been matched to your organization.| )
                                                   ( |Quantity: { iv_quantity } kg, Type: { iv_type }| )
                                                   ( |Please log in to BiteShare and accept the donation.| ) )
                              i_subject = CONV #( lv_subject ) ).
        lo_send_request->set_document( lo_document ).
        IF iv_email IS NOT INITIAL.
          DATA(lo_recipient) = cl_cam_address_bcs=>create_internet_address( CONV #( iv_email ) ).
          lo_send_request->add_recipient( lo_recipient ).
          lo_send_request->send( ).
        ENDIF.
      CATCH cx_bcs.
        " In sandbox environments without SMTP configured, swallow or log error
    ENDTRY.
  ENDMETHOD.

  METHOD send_volunteer_assignment.
    TRY.
        DATA(lo_send_request) = cl_bcs=>create_persistent( ).
        DATA(lv_subject) = |BiteShare: Pickup Request for Donation { iv_donation_id }|.
        DATA(lo_document) = cl_document_bcs=>create_document(
                              i_type    = 'RAW'
                              i_text    = VALUE #( ( |Hello Volunteer, you have been assigned to food pickup { iv_donation_id }.| )
                                                   ( |Please check BiteShare for pickup details and deliver safely.| ) )
                              i_subject = CONV #( lv_subject ) ).
        lo_send_request->set_document( lo_document ).
        IF iv_email IS NOT INITIAL.
          DATA(lo_recipient) = cl_cam_address_bcs=>create_internet_address( CONV #( iv_email ) ).
          lo_send_request->add_recipient( lo_recipient ).
          lo_send_request->send( ).
        ENDIF.
      CATCH cx_bcs.
    ENDTRY.
  ENDMETHOD.

  METHOD send_admin_completion.
    TRY.
        DATA(lo_send_request) = cl_bcs=>create_persistent( ).
        DATA(lv_subject) = |BiteShare Donation { iv_donation_id } Completed!|.
        DATA(lo_document) = cl_document_bcs=>create_document(
                              i_type    = 'RAW'
                              i_text    = VALUE #( ( |Food donation { iv_donation_id } has been successfully delivered and confirmed.| )
                                                   ( |Thank you for reducing food waste!| ) )
                              i_subject = CONV #( lv_subject ) ).
        lo_send_request->set_document( lo_document ).
        " Default coordinator email
        DATA(lo_recipient) = cl_cam_address_bcs=>create_internet_address( 'coordinator@biteshare.org' ).
        lo_send_request->add_recipient( lo_recipient ).
        lo_send_request->send( ).
      CATCH cx_bcs.
    ENDTRY.
  ENDMETHOD.
ENDCLASS.
