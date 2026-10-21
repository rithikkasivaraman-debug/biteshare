@AccessControl.authorizationCheck: #NOT_REQUIRED
@EndUserText.label: 'BiteShare Pickup Delivery Child View'
define view entity ZI_PickupDelivery
  as select from zbt_delivery
  association to parent ZI_FoodDonation as _Donation on $projection.DonationId = _Donation.DonationId
{
  key delivery_id   as DeliveryId,
      donation_id   as DonationId,
      pickup_time   as PickupTime,
      delivery_time as DeliveryTime,
      status        as Status,
      _Donation
}
