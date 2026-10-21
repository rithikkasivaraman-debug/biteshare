@EndUserText.label : 'BiteShare Volunteer Table'
@AbapCatalog.enhancement.category : #NOT_EXTENSIBLE
@AbapCatalog.tableCategory : #TRANSPARENT
@AbapCatalog.deliveryClass : #A
@AbapCatalog.dataMaintenance : #RESTRICTED
define table zbt_volunteer {
  key mandt      : mandt not null;
  key volunteer_id : char10 not null;
  name           : char80;
  phone          : char20;
  email          : char100;
  city           : char50;
  is_available   : abap_boolean; -- 'X' or ' '
}
