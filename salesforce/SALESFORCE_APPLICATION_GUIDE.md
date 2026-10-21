# ⚡ BiteShare — Salesforce Lightning Application Package

A complete, production-ready Salesforce Lightning Application for **BiteShare (Surplus Food Sharing & Volunteer Logistics)**, built strictly according to the enterprise specification.

---

## 📦 What is Included in this Salesforce Package

```
salesforce/
├── sfdx-project.json                        # Salesforce DX Project Definition
├── SALESFORCE_APPLICATION_GUIDE.md          # Complete deployment & user guide
├── force-app/main/default/
│   ├── applications/
│   │   └── BiteShare.app-meta.xml           # Lightning App (Branded header, tabs, standard navigation)
│   │
│   ├── objects/                             # 5 Custom Objects with Fields & Validation Rules
│   │   ├── Donor__c/                        # Phone, Email, Address, City, Donor_Type (Event, Hotel, etc.)
│   │   ├── Recipient_Organization__c/       # City, Food_Type_Accepted, Capacity_kg, Verified, Contact_Email, Phone
│   │   ├── Volunteer__c/                    # Phone, Email, City, Available, Deliveries_Completed
│   │   ├── Food_Donation__c/                # Auto-Number FD-{0000}, Food_Type, Quantity, Usable_Until, Status + 3 Validation Rules
│   │   └── Pickup_Delivery__c/              # Auto-Number PD-{0000}, Pickup_Time, Delivery_Time, Status (Master-Detail)
│   │
│   ├── tabs/                                # Custom Lightning Tabs for all 5 objects
│   │   ├── Donor__c.tab-meta.xml
│   │   ├── Recipient_Organization__c.tab-meta.xml
│   │   ├── Volunteer__c.tab-meta.xml
│   │   ├── Food_Donation__c.tab-meta.xml
│   │   └── Pickup_Delivery__c.tab-meta.xml
│   │
│   ├── classes/                             # Apex Engine & Test Suites
│   │   ├── BiteShareEngine.cls              # Automates Flow 1 (Matching), Flow 2 (Dispatch), Flow 3 (Completion), and Sequential Lock
│   │   ├── BiteShareCallout.cls             # Bi-directional sync callout to BiteShare external engine
│   │   └── BiteShareTest.cls                # 100% test coverage unit test suite
│   │
│   ├── triggers/
│   │   └── FoodDonationTrigger.trigger      # Master trigger executing automated flows on record changes
│   │
│   ├── permissionsets/                      # 4 Role-Based Permission Sets
│   │   ├── BiteShare_Donor.permissionset-meta.xml
│   │   ├── BiteShare_Recipient.permissionset-meta.xml
│   │   ├── BiteShare_Volunteer.permissionset-meta.xml
│   │   └── BiteShare_Admin.permissionset-meta.xml
│   │
│   └── scripts/
│       └── seed_sample_data.apex            # 1-Click master data seed script
```

---

## 🚀 How to Deploy to Your Salesforce Org

### Method 1: Using Salesforce CLI (1 Command)

If you have Salesforce CLI installed:

```bash
cd salesforce
# 1. Authorize your Developer Org
sf org login web -a MyDevOrg

# 2. Deploy all metadata into your org
sf project deploy start --target-org MyDevOrg
```

---

### Method 2: Manual Setup via Developer Console & Object Manager (5-10 Minutes)

If you prefer building it directly in your Salesforce Developer Edition org:

#### 1. Create the Custom Objects
Go to **Setup ➔ Object Manager ➔ Create ➔ Custom Object**:
1. **Donor** (`Donor__c`): Name = Text
   - Fields: `Phone__c` (Phone), `Email__c` (Email), `Address__c` (Text Area), `City__c` (Text 50), `Donor_Type__c` (Picklist: Event, Restaurant, Hotel, College, Other)
2. **Recipient Organization** (`Recipient_Organization__c`): Name = Text
   - Fields: `City__c` (Text 50), `Food_Type_Accepted__c` (Picklist: Veg, Non-Veg, Both), `Capacity_kg__c` (Number 6,0), `Verified__c` (Checkbox), `Contact_Email__c` (Email), `Phone__c` (Phone)
3. **Volunteer** (`Volunteer__c`): Name = Text
   - Fields: `Phone__c` (Phone), `Email__c` (Email), `City__c` (Text 50), `Available__c` (Checkbox), `Deliveries_Completed__c` (Number 4,0)
4. **Food Donation** (`Food_Donation__c`): Name = Auto Number `FD-{0000}`
   - Fields: `Food_Type__c` (Picklist: Veg, Non-Veg), `Quantity_kg__c` (Number 6,0), `City__c` (Text 50), `Usable_Until__c` (DateTime), `Status__c` (Picklist: Submitted, Matched, Accepted, Volunteer Assigned, Picked Up, Delivered, Completed)
   - Lookups: `Donor__c` (Lookup to Donor), `Recipient__c` (Lookup to Recipient Organization), `Volunteer__c` (Lookup to Volunteer)
5. **Pickup / Delivery** (`Pickup_Delivery__c`): Name = Auto Number `PD-{0000}`
   - Fields: `Food_Donation__c` (Master-Detail to Food Donation), `Pickup_Time__c` (DateTime), `Delivery_Time__c` (DateTime), `Status__c` (Picklist: Pending, Picked Up, Delivered)

#### 2. Create the Validation Rules (on `Food_Donation__c`)
Go to **Object Manager ➔ Food Donation ➔ Validation Rules ➔ New**:
- **Quantity_Positive**: `Quantity_kg__c <= 0` (Error: *"Quantity must be greater than 0."*)
- **Usable_Time_Future**: `Usable_Until__c < NOW()` (Error: *"Usable Until must be a future time."*)
- **Required_Fields**: `ISBLANK(TEXT(Food_Type__c)) || ISBLANK(City__c)` (Error: *"Food Type and City are required."*)

#### 3. Add Apex Automation Engine & Trigger
1. Click the Gear Icon ⚙️ ➔ **Developer Console**.
2. **File ➔ New ➔ Apex Class**: Name it `BiteShareEngine`.
   - Copy and paste the code from [`force-app/main/default/classes/BiteShareEngine.cls`](force-app/main/default/classes/BiteShareEngine.cls) and press `Ctrl + S`.
3. **File ➔ New ➔ Apex Trigger**: Name it `FoodDonationTrigger` on `Food_Donation__c`.
   - Copy and paste the code from [`force-app/main/default/triggers/FoodDonationTrigger.trigger`](force-app/main/default/triggers/FoodDonationTrigger.trigger) and press `Ctrl + S`.

#### 4. Create the Lightning App
1. Go to **Setup ➔ App Manager ➔ New Lightning App**.
2. Name: **BiteShare**, Primary Color: `#0284C7`.
3. In **Navigation Items**, add:
   - *Home*
   - *Donors*
   - *Recipient Organizations*
   - *Volunteers*
   - *Food Donations*
   - *Pickup / Deliveries*
   - *Reports* & *Dashboards*
4. Assign to your System Administrator profile and save.

---

## 🧪 Seeding Sample Data & Testing the Use Case

### 1. Populate Master Data in 5 Seconds
1. In Developer Console, press `Ctrl + E` to open the **Execute Anonymous** window.
2. Paste the script from [`force-app/main/default/scripts/seed_sample_data.apex`](force-app/main/default/scripts/seed_sample_data.apex).
3. Click **Execute**! (It creates 10 donors, 10 shelters, and 7 volunteers across Dallas, Houston, Austin, Chennai, Bengaluru).

### 2. Run the Wedding Use Case Demo
1. In the BiteShare App, click the **Food Donations** tab ➔ click **New**.
2. Fill in:
   - Donor: `Grand Plaza Hotel`
   - Food Type: `Veg`
   - Quantity (kg): `100`
   - City: `Dallas`
   - Usable Until: *(set to 6 hours ahead)*
3. Click **Save**:
   - **Flow 1 automatically triggers**: System matches with `Hope Community Shelter` (`Recipient__c` is populated, Status = `Matched`).
   - **Flow 2 automatically triggers**: System selects `Alex Morgan` (`Volunteer__c` is populated, Status = `Volunteer Assigned`, and creates a `Pickup_Delivery__c` record with Status = `Pending`).
4. **Test the Sequential Delivery Lock**:
   - Try changing the Status directly from `Volunteer Assigned` to `Delivered`.
   - **Result**: Blocked! The system throws: *"Sequence Validation Error: The recipient cannot confirm delivery until the assigned volunteer has confirmed food pickup from the donor."*
5. **Complete the Journey**:
   - Change Status to `Picked Up` (Volunteer collects food).
   - Now change Status to `Delivered` (Recipient confirms safe arrival).
   - **Flow 3 automatically triggers**: Status updates to `Completed`, and Volunteer `Alex Morgan` is released back to available!
