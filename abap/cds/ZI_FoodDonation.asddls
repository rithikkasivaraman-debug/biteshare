@AccessControl.authorizationCheck: #NOT_REQUIRED
@EndUserText.label: 'BiteShare Food Donation Interface View'
define root view entity ZI_FoodDonation
  as select from zbt_donation
  composition [0..*] of ZI_PickupDelivery as _Deliveries
  association [0..1] to ZI_Donor          as _Donor     on $projection.DonorId = _Donor.DonorId
  association [0..1] to ZI_Recipient      as _Recipient on $projection.RecipientId = _Recipient.RecipientId
  association [0..1] to ZI_Volunteer      as _Volunteer on $projection.VolunteerId = _Volunteer.VolunteerId
{
  key donation_id     as DonationId,
      food_type       as FoodType,
      quantity_kg     as QuantityKg,
      city            as City,
      usable_until    as UsableUntil,
      status          as Status,
      donor_id        as DonorId,
      recipient_id    as RecipientId,
      volunteer_id    as VolunteerId,
      created_by      as CreatedBy,
      @Semantics.systemDateTime.createdAt: true
      created_at      as CreatedAt,
      @Semantics.systemDateTime.lastChangedAt: true
      last_changed_at as LastChangedAt,

      _Deliveries,
      _Donor,
      _Recipient,
      _Volunteer
}
