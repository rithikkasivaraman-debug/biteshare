const cds = require('@sap/cds');

module.exports = cds.service.impl(async function () {
  const { FoodDonations, Recipients, Volunteers, PickupDeliveries } = this.entities;

  // Phase 4: Validation Rules on Food Donation
  this.before(['CREATE', 'UPDATE'], 'FoodDonations', async (req) => {
    const { quantityKg, usableUntil, foodType, city } = req.data;

    if (quantityKg !== undefined && quantityKg <= 0) {
      req.error(400, 'Quantity must be greater than 0.');
    }

    if (usableUntil && new Date(usableUntil) <= new Date()) {
      req.error(400, 'Usable Until must be a future time.');
    }

    if (req.event === 'CREATE') {
      if (!foodType || !city) {
        req.error(400, 'Food Type and City are required.');
      }
    }
  });

  // Phase 5: Flow 1 - Recipient Matching Automation on Creation
  this.before('CREATE', 'FoodDonations', async (req) => {
    // Generate Auto Number FD-000X
    const last = await SELECT.one.from(FoodDonations).orderBy({ ID: 'desc' });
    let nextNum = 1;
    if (last && last.ID && last.ID.startsWith('FD-')) {
      nextNum = parseInt(last.ID.replace('FD-', ''), 10) + 1;
    }
    req.data.ID = `FD-${String(nextNum).padStart(4, '0')}`;

    // Matching Algorithm
    const match = await SELECT.one.from(Recipients).where({
      isVerified: true,
      city: req.data.city,
      capacityKg: { '>=': req.data.quantityKg }
    }).and(
      `foodType = '${req.data.foodType}' or foodType = 'Both'`
    );

    if (match) {
      req.data.recipient_ID = match.ID;
      req.data.status = 'Matched';
      console.log(`[ALERT] Email sent to recipient ${match.contactEmail}: Surplus food available - ${req.data.quantityKg} kg of ${req.data.foodType}`);
    } else {
      req.data.status = 'Submitted';
    }
  });

  // Phase 5: Flow 2 - Accept Donation & Assign Volunteer
  this.on('acceptDonation', 'FoodDonations', async (req) => {
    const donationId = req.params[0].ID || req.params[0];
    const donation = await SELECT.one.from(FoodDonations).where({ ID: donationId });

    if (!donation) return req.error(404, 'Donation not found');

    // Find available volunteer in the same city
    const volunteer = await SELECT.one.from(Volunteers).where({
      isAvailable: true,
      city: donation.city
    });

    if (volunteer) {
      // 1. Assign volunteer and update donation
      await UPDATE(FoodDonations).set({
        volunteer_ID: volunteer.ID,
        status: 'VolunteerAssigned'
      }).where({ ID: donationId });

      // 2. Mark volunteer as busy
      await UPDATE(Volunteers).set({ isAvailable: false }).where({ ID: volunteer.ID });

      // 3. Create child Pickup/Delivery record
      const lastDel = await SELECT.one.from(PickupDeliveries).orderBy({ ID: 'desc' });
      let nextDelNum = 1;
      if (lastDel && lastDel.ID && lastDel.ID.startsWith('PD-')) {
        nextDelNum = parseInt(lastDel.ID.replace('PD-', ''), 10) + 1;
      }
      const deliveryId = `PD-${String(nextDelNum).padStart(4, '0')}`;

      await INSERT.into(PickupDeliveries).entries({
        ID: deliveryId,
        donation_ID: donationId,
        status: 'Pending'
      });

      console.log(`[ALERT] Email sent to volunteer ${volunteer.email}: Pickup assigned for donation ${donationId}`);
    } else {
      await UPDATE(FoodDonations).set({ status: 'Accepted' }).where({ ID: donationId });
    }

    return await SELECT.one.from(FoodDonations).where({ ID: donationId });
  });

  // Flow 3: Complete Donation
  this.on('markDelivered', 'FoodDonations', async (req) => {
    const donationId = req.params[0].ID || req.params[0];
    const donation = await SELECT.one.from(FoodDonations).where({ ID: donationId });

    if (!donation) return req.error(404, 'Donation not found');

    // 1. Update status to Completed
    await UPDATE(FoodDonations).set({ status: 'Completed' }).where({ ID: donationId });

    // 2. Free Volunteer
    if (donation.volunteer_ID) {
      await UPDATE(Volunteers).set({ isAvailable: true }).where({ ID: donation.volunteer_ID });
    }

    // 3. Update Delivery record
    await UPDATE(PickupDeliveries).set({
      status: 'Delivered',
      deliveryTime: new Date().toISOString()
    }).where({ donation_ID: donationId });

    console.log(`[ALERT] Coordinator notified: Donation ${donationId} completed successfully!`);

    return await SELECT.one.from(FoodDonations).where({ ID: donationId });
  });
});
