CLASS zcl_biteshare_data_generator DEFINITION
  PUBLIC
  FINAL
  CREATE PUBLIC .

  PUBLIC SECTION.
    INTERFACES if_oo_adt_classrun .
ENDCLASS.

CLASS zcl_biteshare_data_generator IMPLEMENTATION.
  METHOD if_oo_adt_classrun~main.
    out->write( 'Seeding BiteShare Multi-City & Distributed Volunteer Master Data...' ).

    -- 1. Clear Existing Data
    DELETE FROM zbt_donor.
    DELETE FROM zbt_recipient.
    DELETE FROM zbt_volunteer.
    DELETE FROM zbt_donation.
    DELETE FROM zbt_delivery.

    -- 2. Populate 10 Donors across Metros
    DATA lt_donors TYPE TABLE OF zbt_donor.
    lt_donors = VALUE #(
      ( mandt = sy-mandt donor_id = 'DNR-0001' name = 'Royal Palace Catering' phone = '555-0101'
        email = 'catering@royalpalace.com' address = '100 Royal Way' city = 'Dallas' donor_type = 'EVENT' )
      ( mandt = sy-mandt donor_id = 'DNR-0002' name = 'Grand Plaza Hotel' phone = '555-0102'
        email = 'events@grandplaza.com' address = '250 Plaza Blvd' city = 'Dallas' donor_type = 'HOTEL' )
      ( mandt = sy-mandt donor_id = 'DNR-0003' name = 'Bayou City Banquets' phone = '555-0103'
        email = 'info@bayoubanquets.com' address = '400 Bayou St' city = 'Houston' donor_type = 'EVENT' )
      ( mandt = sy-mandt donor_id = 'DNR-0004' name = 'Houston Galleria Catering' phone = '555-0104'
        email = 'contact@galleriacater.com' address = '500 Galleria Mall' city = 'Houston' donor_type = 'RESTAURANT' )
      ( mandt = sy-mandt donor_id = 'DNR-0005' name = 'Austin Tech Center Cafe' phone = '555-0105'
        email = 'cafe@austintech.com' address = '700 Congress Ave' city = 'Austin' donor_type = 'COLLEGE' )
      ( mandt = sy-mandt donor_id = 'DNR-0006' name = 'Magnificent Mile Hotel' phone = '555-0106'
        email = 'dining@magmilehotel.com' address = '120 Michigan Ave' city = 'Chicago' donor_type = 'HOTEL' )
      ( mandt = sy-mandt donor_id = 'DNR-0007' name = 'Midtown Grand Ballroom' phone = '555-0107'
        email = 'events@midtowngrand.com' address = '350 5th Ave' city = 'New York' donor_type = 'EVENT' )
      ( mandt = sy-mandt donor_id = 'DNR-0008' name = 'Seattle Convention Suites' phone = '555-0108'
        email = 'suites@seattleconv.com' address = '900 Pike St' city = 'Seattle' donor_type = 'EVENT' )
      ( mandt = sy-mandt donor_id = 'DNR-0009' name = 'Grand Chola Banquets' phone = '555-0109'
        email = 'banquets@grandchola.com' address = '63 Mount Road' city = 'Chennai' donor_type = 'HOTEL' )
      ( mandt = sy-mandt donor_id = 'DNR-0010' name = 'Whitefield Tech Cafeteria' phone = '555-0110'
        email = 'food@whitefieldtech.com' address = 'ITPB Whitefield' city = 'Bengaluru' donor_type = 'COLLEGE' )
    ).
    INSERT zbt_donor FROM TABLE @lt_donors.
    out->write( |Inserted { sy-dbcnt } Donors across 8 Metros.| ).

    -- 3. Populate 17 Verified Recipients / Shelters
    DATA lt_recipients TYPE TABLE OF zbt_recipient.
    lt_recipients = VALUE #(
      ( mandt = sy-mandt recipient_id = 'RCP-0001' name = 'Hope Community Shelter' city = 'Dallas'
        food_type = 'BOTH' capacity_kg = 500 is_verified = 'X' contact_email = 'hope@shelter.org' phone = '555-0201' )
      ( mandt = sy-mandt recipient_id = 'RCP-0002' name = 'Green Earth Food Bank' city = 'Dallas'
        food_type = 'VEG' capacity_kg = 300 is_verified = 'X' contact_email = 'green@earthbank.org' phone = '555-0202' )
      ( mandt = sy-mandt recipient_id = 'RCP-0003' name = 'North Texas Food Rescue' city = 'Dallas'
        food_type = 'BOTH' capacity_kg = 800 is_verified = 'X' contact_email = 'ntx@rescue.org' phone = '555-0203' )
      ( mandt = sy-mandt recipient_id = 'RCP-0004' name = 'Houston Food Mission' city = 'Houston'
        food_type = 'BOTH' capacity_kg = 650 is_verified = 'X' contact_email = 'mission@houstonfood.org' phone = '555-0204' )
      ( mandt = sy-mandt recipient_id = 'RCP-0005' name = 'Star of Hope Haven' city = 'Houston'
        food_type = 'VEG' capacity_kg = 400 is_verified = 'X' contact_email = 'star@hopehaven.org' phone = '555-0205' )
      ( mandt = sy-mandt recipient_id = 'RCP-0006' name = 'Gulf Coast Pantry' city = 'Houston'
        food_type = 'BOTH' capacity_kg = 1000 is_verified = 'X' contact_email = 'gulfcoast@pantry.org' phone = '555-0206' )
      ( mandt = sy-mandt recipient_id = 'RCP-0007' name = 'Austin Community Kitchen' city = 'Austin'
        food_type = 'BOTH' capacity_kg = 450 is_verified = 'X' contact_email = 'kitchen@austinrelief.org' phone = '555-0207' )
      ( mandt = sy-mandt recipient_id = 'RCP-0008' name = 'Hill Country Relief' city = 'Austin'
        food_type = 'VEG' capacity_kg = 250 is_verified = 'X' contact_email = 'hillcountry@relief.org' phone = '555-0208' )
      ( mandt = sy-mandt recipient_id = 'RCP-0009' name = 'Windy City Food Pantry' city = 'Chicago'
        food_type = 'BOTH' capacity_kg = 750 is_verified = 'X' contact_email = 'windycity@pantry.org' phone = '555-0209' )
      ( mandt = sy-mandt recipient_id = 'RCP-0010' name = 'Midwest Care Shelter' city = 'Chicago'
        food_type = 'VEG' capacity_kg = 350 is_verified = 'X' contact_email = 'midwest@careshelter.org' phone = '555-0210' )
      ( mandt = sy-mandt recipient_id = 'RCP-0011' name = 'City Harvest Outreach' city = 'New York'
        food_type = 'BOTH' capacity_kg = 1200 is_verified = 'X' contact_email = 'outreach@cityharvest.org' phone = '555-0211' )
      ( mandt = sy-mandt recipient_id = 'RCP-0012' name = 'Bowery Mission Haven' city = 'New York'
        food_type = 'VEG' capacity_kg = 500 is_verified = 'X' contact_email = 'bowery@missionhaven.org' phone = '555-0212' )
      ( mandt = sy-mandt recipient_id = 'RCP-0013' name = 'Puget Sound Food Bank' city = 'Seattle'
        food_type = 'BOTH' capacity_kg = 600 is_verified = 'X' contact_email = 'puget@foodbank.org' phone = '555-0213' )
      ( mandt = sy-mandt recipient_id = 'RCP-0014' name = 'Annam Food Relief' city = 'Chennai'
        food_type = 'VEG' capacity_kg = 800 is_verified = 'X' contact_email = 'annam@relief.org' phone = '555-0214' )
      ( mandt = sy-mandt recipient_id = 'RCP-0015' name = 'Karuna Community Kitchen' city = 'Chennai'
        food_type = 'BOTH' capacity_kg = 500 is_verified = 'X' contact_email = 'karuna@kitchen.org' phone = '555-0215' )
      ( mandt = sy-mandt recipient_id = 'RCP-0016' name = 'Akshaya Food Network' city = 'Bengaluru'
        food_type = 'VEG' capacity_kg = 1000 is_verified = 'X' contact_email = 'akshaya@foodnet.org' phone = '555-0216' )
      ( mandt = sy-mandt recipient_id = 'RCP-0017' name = 'Robin Hood Volunteers' city = 'Bengaluru'
        food_type = 'BOTH' capacity_kg = 700 is_verified = 'X' contact_email = 'robinhood@blrfund.org' phone = '555-0217' )
    ).
    INSERT zbt_recipient FROM TABLE @lt_recipients.
    out->write( |Inserted { sy-dbcnt } Verified Places across 8 Metros.| ).

    -- 4. Populate 25 Distributed Volunteers (Multiple Volunteers Per City)
    DATA lt_volunteers TYPE TABLE OF zbt_volunteer.
    lt_volunteers = VALUE #(
      -- Dallas
      ( mandt = sy-mandt volunteer_id = 'VOL-0001' name = 'Alex Rivera' phone = '555-0301'
        email = 'alex.rivera@volunteer.org' city = 'Dallas' is_available = 'X' )
      ( mandt = sy-mandt volunteer_id = 'VOL-0002' name = 'Samira Khan' phone = '555-0302'
        email = 'samira.khan@volunteer.org' city = 'Dallas' is_available = 'X' )
      ( mandt = sy-mandt volunteer_id = 'VOL-0003' name = 'David Chen' phone = '555-0303'
        email = 'david.chen@volunteer.org' city = 'Dallas' is_available = 'X' )
      ( mandt = sy-mandt volunteer_id = 'VOL-0004' name = 'Maria Santos' phone = '555-0304'
        email = 'maria.santos@volunteer.org' city = 'Dallas' is_available = 'X' )

      -- Houston
      ( mandt = sy-mandt volunteer_id = 'VOL-0005' name = 'Liam Johnson' phone = '555-0305'
        email = 'liam.j@volunteer.org' city = 'Houston' is_available = 'X' )
      ( mandt = sy-mandt volunteer_id = 'VOL-0006' name = 'Priya Patel' phone = '555-0306'
        email = 'priya.p@volunteer.org' city = 'Houston' is_available = 'X' )
      ( mandt = sy-mandt volunteer_id = 'VOL-0007' name = 'Marcus Williams' phone = '555-0307'
        email = 'marcus.w@volunteer.org' city = 'Houston' is_available = 'X' )
      ( mandt = sy-mandt volunteer_id = 'VOL-0008' name = 'Elena Rodriguez' phone = '555-0308'
        email = 'elena.r@volunteer.org' city = 'Houston' is_available = 'X' )

      -- Austin
      ( mandt = sy-mandt volunteer_id = 'VOL-0009' name = 'Carlos Diaz' phone = '555-0309'
        email = 'carlos.diaz@volunteer.org' city = 'Austin' is_available = 'X' )
      ( mandt = sy-mandt volunteer_id = 'VOL-0010' name = 'Chloe Bennett' phone = '555-0310'
        email = 'chloe.b@volunteer.org' city = 'Austin' is_available = 'X' )
      ( mandt = sy-mandt volunteer_id = 'VOL-0011' name = 'Ryan Miller' phone = '555-0311'
        email = 'ryan.m@volunteer.org' city = 'Austin' is_available = 'X' )

      -- Chicago
      ( mandt = sy-mandt volunteer_id = 'VOL-0012' name = 'Noah Taylor' phone = '555-0312'
        email = 'noah.t@volunteer.org' city = 'Chicago' is_available = 'X' )
      ( mandt = sy-mandt volunteer_id = 'VOL-0013' name = 'Aaliyah Brooks' phone = '555-0313'
        email = 'aaliyah.b@volunteer.org' city = 'Chicago' is_available = 'X' )
      ( mandt = sy-mandt volunteer_id = 'VOL-0014' name = 'Ethan Davis' phone = '555-0314'
        email = 'ethan.d@volunteer.org' city = 'Chicago' is_available = 'X' )

      -- New York
      ( mandt = sy-mandt volunteer_id = 'VOL-0015' name = 'Daniel Kim' phone = '555-0315'
        email = 'daniel.k@volunteer.org' city = 'New York' is_available = 'X' )
      ( mandt = sy-mandt volunteer_id = 'VOL-0016' name = 'Olivia Brown' phone = '555-0316'
        email = 'olivia.b@volunteer.org' city = 'New York' is_available = 'X' )
      ( mandt = sy-mandt volunteer_id = 'VOL-0017' name = 'Lucas Silva' phone = '555-0317'
        email = 'lucas.s@volunteer.org' city = 'New York' is_available = 'X' )

      -- Seattle
      ( mandt = sy-mandt volunteer_id = 'VOL-0018' name = 'James Wilson' phone = '555-0318'
        email = 'james.w@volunteer.org' city = 'Seattle' is_available = 'X' )
      ( mandt = sy-mandt volunteer_id = 'VOL-0019' name = 'Emily White' phone = '555-0319'
        email = 'emily.w@volunteer.org' city = 'Seattle' is_available = 'X' )

      -- Chennai
      ( mandt = sy-mandt volunteer_id = 'VOL-0020' name = 'Karthik Raman' phone = '555-0320'
        email = 'karthik.r@volunteer.org' city = 'Chennai' is_available = 'X' )
      ( mandt = sy-mandt volunteer_id = 'VOL-0021' name = 'Divya Suresh' phone = '555-0321'
        email = 'divya.s@volunteer.org' city = 'Chennai' is_available = 'X' )
      ( mandt = sy-mandt volunteer_id = 'VOL-0022' name = 'Vignesh Kumar' phone = '555-0322'
        email = 'vignesh.k@volunteer.org' city = 'Chennai' is_available = 'X' )

      -- Bengaluru
      ( mandt = sy-mandt volunteer_id = 'VOL-0023' name = 'Rohan Sharma' phone = '555-0323'
        email = 'rohan.s@volunteer.org' city = 'Bengaluru' is_available = 'X' )
      ( mandt = sy-mandt volunteer_id = 'VOL-0024' name = 'Ananya Rao' phone = '555-0324'
        email = 'ananya.r@volunteer.org' city = 'Bengaluru' is_available = 'X' )
      ( mandt = sy-mandt volunteer_id = 'VOL-0025' name = 'Arvind Swamy' phone = '555-0325'
        email = 'arvind.s@volunteer.org' city = 'Bengaluru' is_available = 'X' )
    ).
    INSERT zbt_volunteer FROM TABLE @lt_volunteers.
    out->write( |Inserted { sy-dbcnt } Volunteers distributed across 8 Metros.| ).

    out->write( 'BiteShare Multi-City Master Data initialized successfully!' ).
  ENDMETHOD.
ENDCLASS.
