@EndUserText.label : 'BiteShare Pickup Delivery Child Table'
@AbapCatalog.enhancement.category : #NOT_EXTENSIBLE
@AbapCatalog.tableCategory : #TRANSPARENT
@AbapCatalog.deliveryClass : #A
@AbapCatalog.dataMaintenance : #RESTRICTED
define table zbt_delivery {
  key mandt      : mandt not null;
  key delivery_id : char10 not null; -- PD-0001
  donation_id    : char10 not null;
  pickup_time    : timestampl;
  delivery_time  : timestampl;
  status         : char20; -- PENDING, PICKED_UP, DELIVERED
}
