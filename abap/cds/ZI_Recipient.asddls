@AccessControl.authorizationCheck: #NOT_REQUIRED
@EndUserText.label: 'BiteShare Recipient Organization View'
define view entity ZI_Recipient
  as select from zbt_recipient
{
  key recipient_id  as RecipientId,
      name          as Name,
      city          as City,
      food_type     as FoodType,
      capacity_kg   as CapacityKg,
      is_verified   as IsVerified,
      contact_email as ContactEmail,
      phone         as Phone
}
