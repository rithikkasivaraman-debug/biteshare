@AbapCatalog.viewEnhancementCategory: [#NONE]
@AccessControl.authorizationCheck: #NOT_REQUIRED
@EndUserText.label: 'BiteShare Impact Analytics Query'
@Analytics.query: true
define view entity ZC_BiteShare_Analytics
  as select from ZI_FoodDonation
{
  @AnalyticsDetails.query.axis: #ROWS
  @EndUserText.label: 'City'
  City,

  @AnalyticsDetails.query.axis: #ROWS
  @EndUserText.label: 'Status'
  Status,

  @AnalyticsDetails.query.axis: #ROWS
  @EndUserText.label: 'Food Type'
  FoodType,

  @AnalyticsDetails.query.axis: #ROWS
  @EndUserText.label: 'Volunteer ID'
  VolunteerId,

  @DefaultAggregation: #SUM
  @EndUserText.label: 'Total Quantity (kg)'
  QuantityKg,

  @DefaultAggregation: #SUM
  @EndUserText.label: 'Total Food Rescued (kg)'
  case when Status = 'COMPLETED' then QuantityKg else 0 end as RescuedQuantityKg,

  @DefaultAggregation: #COUNT
  @EndUserText.label: 'Donation Count'
  1 as DonationCount
}
