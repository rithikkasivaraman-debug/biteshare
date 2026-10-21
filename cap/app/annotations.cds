using { BiteShareService } from '../srv/biteshare-service';

annotate BiteShareService.FoodDonations with @(
  UI.HeaderInfo: {
    TypeName: 'Food Donation',
    TypeNamePlural: 'Food Donations',
    Title: { Value: ID },
    Description: { Value: city }
  },
  UI.SelectionFields: [ foodType, city, status ],
  UI.LineItem: [
    { Value: ID, Label: 'Donation ID' },
    { Value: foodType, Label: 'Food Type' },
    { Value: quantityKg, Label: 'Quantity (kg)' },
    { Value: city, Label: 'City' },
    { Value: usableUntil, Label: 'Usable Until' },
    { Value: status, Label: 'Status' },
    { $Type: 'UI.DataFieldForAction', Action: 'BiteShareService.acceptDonation', Label: 'Accept Donation' },
    { $Type: 'UI.DataFieldForAction', Action: 'BiteShareService.markDelivered', Label: 'Confirm Delivered' }
  ],
  UI.Facets: [
    {
      $Type: 'UI.ReferenceFacet',
      Label: 'Donation Details',
      Target: '@UI.Identification'
    },
    {
      $Type: 'UI.ReferenceFacet',
      Label: 'Deliveries',
      Target: 'deliveries/@UI.LineItem'
    }
  ],
  UI.Identification: [
    { Value: ID },
    { Value: foodType },
    { Value: quantityKg },
    { Value: city },
    { Value: usableUntil },
    { Value: status },
    { Value: donor_ID, Label: 'Donor ID' },
    { Value: recipient_ID, Label: 'Recipient ID' },
    { Value: volunteer_ID, Label: 'Volunteer ID' }
  ]
);

annotate BiteShareService.PickupDeliveries with @(
  UI.LineItem: [
    { Value: ID, Label: 'Delivery ID' },
    { Value: status, Label: 'Status' },
    { Value: pickupTime, Label: 'Pickup Time' },
    { Value: deliveryTime, Label: 'Delivery Time' }
  ]
);
