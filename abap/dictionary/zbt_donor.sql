@EndUserText.label : 'BiteShare Donor Table'
@AbapCatalog.enhancement.category : #NOT_EXTENSIBLE
@AbapCatalog.tableCategory : #TRANSPARENT
@AbapCatalog.deliveryClass : #A
@AbapCatalog.dataMaintenance : #RESTRICTED
define table zbt_donor {
  key mandt      : mandt not null;
  key donor_id   : char10 not null;
  name           : char80;
  phone          : char20;
  email          : char100;
  address        : char255;
  city           : char50;
  donor_type     : char20; -- Event, Restaurant, Hotel, College, Other
  created_at     : timestampl;
}
