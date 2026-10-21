/**
 * @description Comprehensive unit test suite for BiteShare Salesforce application.
 * Tests Flow 1 (Matching), Flow 2 (Dispatch), Flow 3 (Completion), and Sequential Lock.
 */
@isTest
private class BiteShareTest {

    @testSetup
    static void setupTestData() {
        // 1. Create Donor
        Donor__c donor = new Donor__c(
            Name = 'Grand Palace Hotel',
            City__c = 'Dallas',
            Donor_Type__c = 'Hotel',
            Email__c = 'events@grandpalace.com',
            Phone__c = '555-0101'
        );
        insert donor;

        // 2. Create Recipient Organization
        Recipient_Organization__c recip = new Recipient_Organization__c(
            Name = 'Hope Community Shelter',
            City__c = 'Dallas',
            Food_Type_Accepted__c = 'Both',
            Capacity_kg__c = 500,
            Verified__c = true,
            Contact_Email__c = 'hope@shelter.org',
            Phone__c = '555-0201'
        );
        insert recip;

        // 3. Create Volunteer
        Volunteer__c vol = new Volunteer__c(
            Name = 'Alex Morgan',
            City__c = 'Dallas',
            Available__c = true,
            Email__c = 'alex.m@volunteer.org',
            Phone__c = '555-0301'
        );
        insert vol;
    }

    @isTest
    static void testEndToEndDonationLifecycle() {
        Donor__c donor = [SELECT Id FROM Donor__c LIMIT 1];
        Recipient_Organization__c recip = [SELECT Id FROM Recipient_Organization__c LIMIT 1];
        Volunteer__c vol = [SELECT Id FROM Volunteer__c LIMIT 1];

        Test.startTest();

        // 1. Insert surplus food donation (Wedding use case: 100 kg Veg)
        Food_Donation__c donation = new Food_Donation__c(
            Donor__c = donor.Id,
            City__c = 'Dallas',
            Food_Type__c = 'Veg',
            Quantity_kg__c = 100,
            Usable_Until__c = Datetime.now().addHours(8),
            Status__c = 'Submitted'
        );
        insert donation;

        // Verify Flow 1: Matched to recipient
        Food_Donation__c insertedDon = [SELECT Id, Status__c, Recipient__c, Volunteer__c FROM Food_Donation__c WHERE Id = :donation.Id];
        System.assertEquals(recip.Id, insertedDon.Recipient__c, 'Donation should be auto-matched to Hope Community Shelter');

        // 2. Simulate Volunteer Pickup
        insertedDon.Status__c = 'Picked Up';
        update insertedDon;

        // 3. Recipient Confirms Delivery
        insertedDon.Status__c = 'Delivered';
        update insertedDon;

        Test.stopTest();

        // Verify Flow 3: Donation is Completed and Volunteer is released
        Food_Donation__c finalDon = [SELECT Id, Status__c FROM Food_Donation__c WHERE Id = :donation.Id];
        System.assertEquals('Completed', finalDon.Status__c, 'Donation status should be set to Completed');

        Volunteer__c releasedVol = [SELECT Id, Available__c, Deliveries_Completed__c FROM Volunteer__c WHERE Id = :vol.Id];
        System.assertEquals(true, releasedVol.Available__c, 'Volunteer should be available again');
    }

    @isTest
    static void testSequentialDeliveryLockError() {
        Donor__c donor = [SELECT Id FROM Donor__c LIMIT 1];

        // Create donation
        Food_Donation__c donation = new Food_Donation__c(
            Donor__c = donor.Id,
            City__c = 'Dallas',
            Food_Type__c = 'Veg',
            Quantity_kg__c = 50,
            Usable_Until__c = Datetime.now().addHours(6),
            Status__c = 'Volunteer Assigned'
        );
        insert donation;

        // Attempt to confirm delivery directly without picking up first!
        donation.Status__c = 'Delivered';
        try {
            update donation;
            System.assert(false, 'Expected validation error due to sequential integrity lock');
        } catch (DmlException ex) {
            System.assert(ex.getMessage().contains('Sequence Validation Error'), 'Should block premature delivery confirmation');
        }
    }
}
