namespace sap.biteshare;

using { managed, cuid } from '@sap/cds/common';

type FoodTypeEnum : String enum { Veg; NonVeg; Both; };
type DonationStatus : String enum {
  Submitted;
  Matched;
  Accepted;
  VolunteerAssigned;
  PickedUp;
  Delivered;
  Completed;
};

type DeliveryStatus : String enum { Pending; PickedUp; Delivered; };

entity Donors : managed {
  key ID          : String(10);
      name        : String(80);
      phone       : String(20);
      email       : String(100);
      address     : String(255);
      city        : String(50);
      donorType   : String(20); -- Event, Restaurant, Hotel, College, Other
      donations   : Association to many FoodDonations on donations.donor = $self;
}

entity Recipients : managed {
  key ID          : String(10);
      name        : String(80);
      city        : String(50);
      foodType    : FoodTypeEnum;
      capacityKg  : Decimal(6,0);
      isVerified  : Boolean default false;
      contactEmail: String(100);
      phone       : String(20);
}

entity Volunteers : managed {
  key ID          : String(10);
      name        : String(80);
      phone       : String(20);
      email       : String(100);
      city        : String(50);
      isAvailable : Boolean default true;
}

entity FoodDonations : managed {
  key ID          : String(10); // FD-0001
      foodType    : FoodTypeEnum;
      quantityKg  : Decimal(6,0);
      city        : String(50);
      usableUntil : DateTime;
      status      : DonationStatus default 'Submitted';
      donor       : Association to Donors;
      recipient   : Association to Recipients;
      volunteer   : Association to Volunteers;
      deliveries  : Composition of many PickupDeliveries on deliveries.donation = $self;
}

entity PickupDeliveries : managed {
  key ID          : String(10); // PD-0001
      donation    : Association to FoodDonations;
      pickupTime  : DateTime;
      deliveryTime: DateTime;
      status      : DeliveryStatus default 'Pending';
}
