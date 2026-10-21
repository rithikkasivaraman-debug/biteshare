@AccessControl.authorizationCheck: #NOT_REQUIRED
@EndUserText.label: 'BiteShare Volunteer Interface View'
define view entity ZI_Volunteer
  as select from zbt_volunteer
{
  key volunteer_id as VolunteerId,
      name         as Name,
      phone        as Phone,
      email        as Email,
      city         as City,
      is_available as IsAvailable
}
