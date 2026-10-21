@AccessControl.authorizationCheck: #NOT_REQUIRED
@EndUserText.label: 'BiteShare Donor Interface View'
define view entity ZI_Donor
  as select from zbt_donor
{
  key donor_id   as DonorId,
      name       as Name,
      phone      as Phone,
      email      as Email,
      address    as Address,
      city       as City,
      donor_type as DonorType,
      created_at as CreatedAt
}
