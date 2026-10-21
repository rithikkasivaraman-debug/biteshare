# BiteShare: Step-by-Step SAP Developer Build Guide (SOP)
### Complete Guide for Building BiteShare in SAP Developer Tools (ADT in Eclipse, SAP GUI & SAP BAS)

This guide takes the 8 phases from the Salesforce BiteShare SOP and provides the direct, actionable steps in **SAP Developer Tools**.

---

## Quick Navigation: Phase-by-Phase Mapping

```
Salesforce Phase               -->  SAP Developer Tool Step
------------------------------------------------------------------------------------------
Phase 1: Org Setup             -->  SAP BTP / S/4HANA System Connection & ABAP Package Setup
Phase 2: Create Custom Objects -->  ABAP Dictionary Tables (SE11 / ADT Table Definitions)
Phase 3: Relationships         -->  Core Data Services (CDS) Associations & Compositions
Phase 4: Validation Rules      -->  RAP Behavior Definition Validations (`validateQuantity`, etc.)
Phase 5: Flows (Automations)   -->  RAP Determinations, Actions & `cl_bcs` Email Dispatch
Phase 6: Security & Access     -->  SAP Authorization Objects & PFCG Technical Roles
Phase 7: Reports & Dashboard   -->  CDS Analytical Queries & Fiori Overview Page (OVP)
Phase 8: Test & Demo           -->  Master Data Generator (`F9`) & Fiori Elements UI Test
```

---

## Phase 1: SAP System & Package Setup

1. Open **ABAP Development Tools (ADT)** in Eclipse (or log in to **SAP GUI / SAP BTP ABAP Environment**).
2. Connect to your ABAP Project (e.g., Trial or S/4HANA system).
3. Right-click on your Project -> **New** -> **ABAP Package**:
   - **Name**: `ZBITESHARE`
   - **Description**: `BiteShare Surplus Food Sharing System`
   - **Package Type**: `Development`
   - Choose or create a Transport Request (or `$TMP` for local objects).

---

## Phase 2: Create Database Tables (ABAP Dictionary)

In ADT, right-click `ZBITESHARE` -> **New** -> **Other ABAP Repository Object** -> **Database Table**:

1. **`ZBT_DONOR`** (Donor entity)
   - Paste content from [`abap/dictionary/zbt_donor.sql`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/dictionary/zbt_donor.sql)
   - Press `Ctrl + S`, then `Ctrl + F3` (Activate).

2. **`ZBT_RECIPIENT`** (Recipient Organization entity)
   - Paste content from [`abap/dictionary/zbt_recipient.sql`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/dictionary/zbt_recipient.sql)
   - Activate (`Ctrl + F3`).

3. **`ZBT_VOLUNTEER`** (Volunteer entity)
   - Paste content from [`abap/dictionary/zbt_volunteer.sql`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/dictionary/zbt_volunteer.sql)
   - Activate (`Ctrl + F3`).

4. **`ZBT_DONATION`** (Central Food Donation entity)
   - Paste content from [`abap/dictionary/zbt_donation.sql`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/dictionary/zbt_donation.sql)
   - Activate (`Ctrl + F3`).

5. **`ZBT_DELIVERY`** (Child Delivery entity)
   - Paste content from [`abap/dictionary/zbt_delivery.sql`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/dictionary/zbt_delivery.sql)
   - Activate (`Ctrl + F3`).

---

## Phase 3: Relationships (CDS Views)

Create Core Data Services (CDS) Data Definitions to establish Lookups and Compositions:

1. **Interface Views**:
   - Create `ZI_Donor` from [`abap/cds/ZI_Donor.asddls`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/cds/ZI_Donor.asddls)
   - Create `ZI_Recipient` from [`abap/cds/ZI_Recipient.asddls`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/cds/ZI_Recipient.asddls)
   - Create `ZI_Volunteer` from [`abap/cds/ZI_Volunteer.asddls`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/cds/ZI_Volunteer.asddls)
   - Create `ZI_PickupDelivery` from [`abap/cds/ZI_PickupDelivery.asddls`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/cds/ZI_PickupDelivery.asddls)
   - Create Root View `ZI_FoodDonation` from [`abap/cds/ZI_FoodDonation.asddls`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/cds/ZI_FoodDonation.asddls)
     *(Defines associations to Donor, Recipient, Volunteer and composition of PickupDelivery)*.

2. **Consumption Views & UI Annotations**:
   - Create `ZC_PickupDelivery` from [`abap/cds/ZC_PickupDelivery.asddls`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/cds/ZC_PickupDelivery.asddls)
   - Create `ZC_FoodDonation` from [`abap/cds/ZC_FoodDonation.asddls`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/cds/ZC_FoodDonation.asddls)
   - Create Metadata Extension `ZC_FoodDonation.asddlxs` from [`abap/cds/ZC_FoodDonation.asddlxs`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/cds/ZC_FoodDonation.asddlxs)
   - Activate all CDS entities (`Ctrl + Shift + F3`).

---

## Phase 4 & 5: Validation Rules & Automation Flows (RAP Behavior)

In SAP RAP, Validation Rules and Flows are defined in the **Behavior Definition** and implemented in the **Behavior Pool Class**.

1. **Create Behavior Definition**:
   - Right-click `ZI_FoodDonation` -> **New Behavior Definition**.
   - Paste content from [`abap/bdef/ZI_FoodDonation.asbdef`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/bdef/ZI_FoodDonation.asbdef).
   - Right-click `ZC_FoodDonation` -> **New Behavior Definition** (Projection).
   - Paste content from [`abap/bdef/ZC_FoodDonation.asbdef`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/bdef/ZC_FoodDonation.asbdef).

2. **Create Email Utility Class**:
   - Create ABAP Class `zcl_biteshare_mailer` from [`abap/classes/zcl_biteshare_mailer.clas.abap`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/classes/zcl_biteshare_mailer.clas.abap).
   - Activate (`Ctrl + F3`).

3. **Implement Behavior Pool**:
   - In ADT, on `ZI_FoodDonation.asbdef`, position cursor on `zbp_i_fooddonation` and press `Ctrl + 1` -> **Create Behavior Implementation**.
   - In the **Local Types** tab, paste [`abap/classes/zbp_i_fooddonation.clas.locals_imp.abap`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/classes/zbp_i_fooddonation.clas.locals_imp.abap).
   - This implements:
     - `earlynumbering_create`: Auto numbers `FD-0001` and `PD-0001`.
     - `validateQuantity`: Enforces Quantity > 0.
     - `validateUsableTime`: Enforces Usable Until > Current time.
     - `validateMandatoryFields`: Enforces FoodType and City are non-blank.
     - `matchRecipient`: Automatically finds verified recipient, sets Status = `MATCHED`, sends alert email.
     - `acceptDonation`: Finds available volunteer in city, sets Status = `VOL_ASSIGNED`, sets volunteer busy, creates child delivery record, emails volunteer.
     - `markDelivered`: Sets Status = `COMPLETED`, frees volunteer, confirms delivery, notifies admin.

---

## Phase 6: Service Publishing & Fiori Launchpad Preview

1. **Create Service Definition**:
   - Right-click `ZC_FoodDonation` -> **New** -> **Service Definition**: `ZUI_BITESHARE_O4`.
   - Paste [`abap/srv/ZUI_BITESHARE_O4.assrvds`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/srv/ZUI_BITESHARE_O4.assrvds).
   - Activate.

2. **Create Service Binding**:
   - Right-click `ZUI_BITESHARE_O4` -> **New Service Binding**:
     - **Binding Type**: `OData V4 - UI`
     - **Name**: `ZUI_BITESHARE_O4_UI`
   - Click **Activate**, then click **Publish**.

3. **Launch Fiori App Preview**:
   - Under **Entity Set and Association**, double-click `FoodDonations`.
   - SAP ADT opens the interactive **SAP Fiori Elements List Report & Object Page** directly in your browser!

---

## Phase 7: Seed Master Data & Execute Test Walkthrough

1. **Seed Demo Data (Phase 8 Step 33)**:
   - Create class `zcl_biteshare_data_generator` from [`abap/classes/zcl_biteshare_data_generator.clas.abap`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/abap/classes/zcl_biteshare_data_generator.clas.abap).
   - Press **`F9`** in ADT.
   - The console confirms:
     - 2 Donors inserted (`DNR-0001`, `DNR-0002`)
     - 3 Recipient Orgs inserted (`RCP-0001` Hope Community Shelter in Dallas, etc.)
     - 3 Volunteers inserted (`VOL-0001` Alex Rivera in Dallas, etc.)

2. **Demonstrate Wedding Use Case in Fiori App**:
   - Click **Create** on the Fiori Elements app.
   - Enter:
     - **Quantity**: `100` kg
     - **Food Type**: `VEG`
     - **City**: `Dallas`
     - **Usable Until**: Tomorrow / a few hours ahead
   - Click **Save**:
     - Status immediately becomes **`MATCHED`**.
     - Recipient `RCP-0001` is populated automatically.
   - Click **Recipient Accept**:
     - Status updates to **`VOL_ASSIGNED`**.
     - Volunteer `VOL-0001` (Alex Rivera) is assigned.
     - A new `PickupDelivery` record `PD-0001` appears in the Deliveries tab.
   - Click **Confirm Delivered**:
     - Status updates to **`COMPLETED`**.
     - Volunteer `VOL-0001` is freed back to Available.
     - Analytics query updates Total Rescued Food to `100 kg`.
   - Take screenshots at each step for your project report!
