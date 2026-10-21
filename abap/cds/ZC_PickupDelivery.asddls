@AccessControl.authorizationCheck: #NOT_REQUIRED
@EndUserText.label: 'BiteShare Pickup Delivery Projection'
define view entity ZC_PickupDelivery
  as projection on ZI_PickupDelivery
{
  key DeliveryId,
      DonationId,
      PickupTime,
      DeliveryTime,
      Status,
      _Donation : redirected to parent ZC_FoodDonation
}
