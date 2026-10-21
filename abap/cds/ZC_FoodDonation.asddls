@AccessControl.authorizationCheck: #NOT_REQUIRED
@EndUserText.label: 'BiteShare Food Donation Projection'
@Metadata.allowExtensions: true
@Search.searchable: true
define root view entity ZC_FoodDonation
  provider contract transactional_query
  as projection on ZI_FoodDonation
{
  key DonationId,
      FoodType,
      QuantityKg,
      @Search.defaultSearchElement: true
      City,
      UsableUntil,
      Status,
      DonorId,
      RecipientId,
      VolunteerId,
      CreatedBy,
      CreatedAt,
      LastChangedAt,

      _Deliveries : redirected to composition child ZC_PickupDelivery,
      _Donor,
      _Recipient,
      _Volunteer
}
