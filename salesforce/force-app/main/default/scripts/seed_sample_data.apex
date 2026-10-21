// ====================================================================
// BiteShare: Automated Master Data Seed Script for Salesforce
// Paste into Developer Console -> Debug -> Open Execute Anonymous Window
// ====================================================================

// 1. Seed Donors
List<Donor__c> donors = new List<Donor__c>{
    new Donor__c(Name = 'Royal Palace Catering', City__c = 'Dallas', Donor_Type__c = 'Event', Email__c = 'catering@royalpalace.com', Phone__c = '555-0101'),
    new Donor__c(Name = 'Grand Plaza Hotel', City__c = 'Dallas', Donor_Type__c = 'Hotel', Email__c = 'events@grandplaza.com', Phone__c = '555-0102'),
    new Donor__c(Name = 'Bayou City Banquets', City__c = 'Houston', Donor_Type__c = 'Event', Email__c = 'info@bayoubanquets.com', Phone__c = '555-0103'),
    new Donor__c(Name = 'Houston Galleria Catering', City__c = 'Houston', Donor_Type__c = 'Restaurant', Email__c = 'contact@galleriacater.com', Phone__c = '555-0104'),
    new Donor__c(Name = 'Austin Tech Center Cafe', City__c = 'Austin', Donor_Type__c = 'College', Email__c = 'cafe@austintech.com', Phone__c = '555-0105'),
    new Donor__c(Name = 'Magnificent Mile Hotel', City__c = 'Chicago', Donor_Type__c = 'Hotel', Email__c = 'dining@magmilehotel.com', Phone__c = '555-0106'),
    new Donor__c(Name = 'Midtown Grand Ballroom', City__c = 'New York', Donor_Type__c = 'Event', Email__c = 'events@midtowngrand.com', Phone__c = '555-0107'),
    new Donor__c(Name = 'Seattle Convention Suites', City__c = 'Seattle', Donor_Type__c = 'Event', Email__c = 'suites@seattleconv.com', Phone__c = '555-0108'),
    new Donor__c(Name = 'Grand Chola Banquets', City__c = 'Chennai', Donor_Type__c = 'Hotel', Email__c = 'banquets@grandchola.com', Phone__c = '555-0109'),
    new Donor__c(Name = 'Whitefield Tech Cafeteria', City__c = 'Bengaluru', Donor_Type__c = 'College', Email__c = 'food@whitefieldtech.com', Phone__c = '555-0110')
};
insert donors;

// 2. Seed Recipient Organizations
List<Recipient_Organization__c> recips = new List<Recipient_Organization__c>{
    new Recipient_Organization__c(Name = 'Hope Community Shelter', City__c = 'Dallas', Food_Type_Accepted__c = 'Both', Capacity_kg__c = 500, Verified__c = true, Contact_Email__c = 'hope@shelter.org', Phone__c = '555-0201'),
    new Recipient_Organization__c(Name = 'Green Earth Food Bank', City__c = 'Dallas', Food_Type_Accepted__c = 'Veg', Capacity_kg__c = 300, Verified__c = true, Contact_Email__c = 'green@earthbank.org', Phone__c = '555-0202'),
    new Recipient_Organization__c(Name = 'Houston Food Mission', City__c = 'Houston', Food_Type_Accepted__c = 'Both', Capacity_kg__c = 650, Verified__c = true, Contact_Email__c = 'mission@houstonfood.org', Phone__c = '555-0204'),
    new Recipient_Organization__c(Name = 'Star of Hope Haven', City__c = 'Houston', Food_Type_Accepted__c = 'Veg', Capacity_kg__c = 400, Verified__c = true, Contact_Email__c = 'star@hopehaven.org', Phone__c = '555-0205'),
    new Recipient_Organization__c(Name = 'Austin Community Kitchen', City__c = 'Austin', Food_Type_Accepted__c = 'Both', Capacity_kg__c = 450, Verified__c = true, Contact_Email__c = 'kitchen@austinrelief.org', Phone__c = '555-0207'),
    new Recipient_Organization__c(Name = 'Windy City Food Pantry', City__c = 'Chicago', Food_Type_Accepted__c = 'Both', Capacity_kg__c = 750, Verified__c = true, Contact_Email__c = 'windycity@pantry.org', Phone__c = '555-0209'),
    new Recipient_Organization__c(Name = 'City Harvest Outreach', City__c = 'New York', Food_Type_Accepted__c = 'Both', Capacity_kg__c = 1200, Verified__c = true, Contact_Email__c = 'outreach@cityharvest.org', Phone__c = '555-0211'),
    new Recipient_Organization__c(Name = 'Puget Sound Food Bank', City__c = 'Seattle', Food_Type_Accepted__c = 'Both', Capacity_kg__c = 600, Verified__c = true, Contact_Email__c = 'puget@foodbank.org', Phone__c = '555-0213'),
    new Recipient_Organization__c(Name = 'Annam Food Relief Foundation', City__c = 'Chennai', Food_Type_Accepted__c = 'Veg', Capacity_kg__c = 800, Verified__c = true, Contact_Email__c = 'annam@relief.org', Phone__c = '555-0214'),
    new Recipient_Organization__c(Name = 'Akshaya Food Network', City__c = 'Bengaluru', Food_Type_Accepted__c = 'Veg', Capacity_kg__c = 1000, Verified__c = true, Contact_Email__c = 'akshaya@foodnet.org', Phone__c = '555-0216')
};
insert recips;

// 3. Seed Volunteers
List<Volunteer__c> vols = new List<Volunteer__c>{
    new Volunteer__c(Name = 'Alex Morgan', City__c = 'Dallas', Available__c = true, Email__c = 'alex.m@volunteer.org', Phone__c = '555-0301'),
    new Volunteer__c(Name = 'Jordan Lee', City__c = 'Dallas', Available__c = true, Email__c = 'jordan.l@volunteer.org', Phone__c = '555-0302'),
    new Volunteer__c(Name = 'Carlos Mendez', City__c = 'Houston', Available__c = true, Email__c = 'carlos.m@volunteer.org', Phone__c = '555-0304'),
    new Volunteer__c(Name = 'Marcus Johnson', City__c = 'Austin', Available__c = true, Email__c = 'marcus.j@volunteer.org', Phone__c = '555-0308'),
    new Volunteer__c(Name = 'Daniel Kim', City__c = 'New York', Available__c = true, Email__c = 'daniel.k@volunteer.org', Phone__c = '555-0315'),
    new Volunteer__c(Name = 'Karthik Raman', City__c = 'Chennai', Available__c = true, Email__c = 'karthik.r@volunteer.org', Phone__c = '555-0320'),
    new Volunteer__c(Name = 'Rohan Sharma', City__c = 'Bengaluru', Available__c = true, Email__c = 'rohan.s@volunteer.org', Phone__c = '555-0323')
};
insert vols;

System.debug('Successfully seeded BiteShare master data in Salesforce!');
