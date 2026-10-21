using { sap.biteshare as my } from '../db/schema';

service BiteShareService @(path: '/biteshare') {
  entity Donors as projection on my.Donors;
  entity Recipients as projection on my.Recipients;
  entity Volunteers as projection on my.Volunteers;

  entity FoodDonations as projection on my.FoodDonations actions {
    action acceptDonation() returns FoodDonations;
    action markPickedUp() returns FoodDonations;
    action markDelivered() returns FoodDonations;
  };

  entity PickupDeliveries as projection on my.PickupDeliveries;

  @readonly
  entity ImpactDashboard as select from my.FoodDonations {
    key ID,
    city,
    foodType,
    status,
    quantityKg,
    case when status = 'Completed' then quantityKg else 0 end as rescuedKg : Decimal(6,0)
  };
}
