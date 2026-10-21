@EndUserText.label : 'BiteShare Recipient Organization Table'
@AbapCatalog.enhancement.category : #NOT_EXTENSIBLE
@AbapCatalog.tableCategory : #TRANSPARENT
@AbapCatalog.deliveryClass : #A
@AbapCatalog.dataMaintenance : #RESTRICTED
define table zbt_recipient {
  key mandt      : mandt not null;
  key recipient_id : char10 not null;
  name           : char80;
  city           : char50;
  food_type      : char10; -- VEG, NON-VEG, BOTH
  capacity_kg    : dec6_0;
  is_verified    : abap_boolean; -- 'X' or ' '
  contact_email  : char100;
  phone          : char20;
}
