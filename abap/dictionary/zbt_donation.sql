@EndUserText.label : 'BiteShare Food Donation Central Table'
@AbapCatalog.enhancement.category : #NOT_EXTENSIBLE
@AbapCatalog.tableCategory : #TRANSPARENT
@AbapCatalog.deliveryClass : #A
@AbapCatalog.dataMaintenance : #RESTRICTED
define table zbt_donation {
  key mandt      : mandt not null;
  key donation_id : char10 not null; -- FD-0001
  food_type      : char10; -- VEG, NON-VEG
  quantity_kg    : dec6_0;
  city           : char50;
  usable_until   : timestampl;
  status         : char20; -- SUBMITTED, MATCHED, ACCEPTED, VOL_ASSIGNED, PICKED_UP, DELIVERED, COMPLETED
  donor_id       : char10;
  recipient_id   : char10;
  volunteer_id   : char10;
  created_by     : syuname;
  created_at     : timestampl;
  last_changed_at : timestampl;
}
