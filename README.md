# 🍲 BiteShare — Surplus Food Sharing & Logistics Network

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![SAP BTP Ready](https://img.shields.io/badge/SAP%20BTP-Cloud%20Foundry-008FD3?style=flat&logo=sap&logoColor=white)](https://www.sap.com/products/technology-platform.html)
[![Salesforce Integrated](https://img.shields.io/badge/Salesforce-Lightning%20%26%20Apex-00A1E0?style=flat&logo=salesforce&logoColor=white)](https://developer.salesforce.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/rithikkasivaraman-debug/biteshare)

> **BiteShare** is an enterprise-grade surplus food management and volunteer logistics automation platform. It bridges commercial food donors (hotels, banquets, restaurants, cafeterias) with verified recipient NGOs and a community-driven volunteer rescue pool, backed by bi-directional Salesforce synchronization and SAP BTP deployment readiness.

---

## 🌟 Key Features

### 1. 👥 Tri-Role Portal Architecture
- **Donor Portal**: Fast submission of surplus food packages with city selection, dietary classification (Vegetarian/Non-Vegetarian/Both), quantity in kilograms, and freshness expiration countdown.
- **Recipient Portal**: Verified NGOs and shelters see incoming dispatched donations in real time.
- **Volunteer Portal**: On-call volunteer network receives automated dispatch alerts with full donor and destination details.

### 2. 🔒 Sequential Delivery Integrity Lock
- **Fraud & Premature Confirmation Prevention**: The recipient's **"Confirm Received"** action is strictly disabled until the assigned delivery volunteer physically confirms pickup from the donor site.

### 3. ⚡ Automated Smart Matching & Conveyance
- **Proximity & Capacity Matching**: Matches surplus donations to the nearest verified NGO shelter in the same city that has sufficient storage capacity.
- **Fair-Share Volunteer Dispatch**: Automatically selects the nearest available volunteer with the fewest completed deliveries to balance workload across the fleet.

### 4. 📍 Multi-Step Live Delivery Tracker
- Interactive visual progress tracker displaying the 4-stage lifecycle:
  `REQUESTED` ➔ `VOLUNTEER ASSIGNED` ➔ `PICKED UP` ➔ `DELIVERED & VERIFIED`

### 5. ☁️ Bi-Directional Salesforce Integration
- Built-in webhook listener at `/api/salesforce/webhook`.
- Production-ready Apex Callout class (`BiteShareCallout.cls`) and Trigger (`FoodDonationTrigger.trigger`) to sync donations created in Salesforce CRM directly to the BiteShare network.

### 6. 📊 Real-Time Impact Analytics
- Live tracking of:
  - 🍱 Total Meals Rescued & Served
  - 🌍 $\text{CO}_2$ Carbon Emissions Mitigated
  - 🤝 Active Donors & Volunteer Pool Hours

### 7. 🏢 Comprehensive Pre-Seeded Master Data
- **10 Enterprise Donors** (Hotels, Event Venues, Tech Cafeterias) across Dallas, Houston, Austin, Chicago, New York, Seattle, Chennai, Bengaluru.
- **17 Verified Shelters & Food Banks** with dietary capacities.
- **25 Certified Volunteers** with real-time status and delivery histories.

---

## 🏗️ Repository Architecture

```
biteshare-sap/
├── server.py                        # Core BiteShare Web Engine & REST API (Zero-dependency)
├── manifest.yml                     # SAP BTP Cloud Foundry deployment manifest
├── Procfile                         # Cloud Foundry process declaration
├── runtime.txt                      # Python runtime specification (python-3.11.9)
├── requirements.txt                 # Python dependencies
├── test_biteshare_scenario.py       # Automated test suite
│
├── salesforce/                      # Salesforce Integration Package
│   ├── BiteShareCallout.cls         # Apex Future Callout Class
│   └── FoodDonationTrigger.trigger  # Apex Trigger on Food_Donation__c
│
├── docs/                            # Architecture & Deployment Guides
│   ├── SAP_BTP_DEPLOYMENT_GUIDE.md  # Step-by-step SAP BTP Cloud Foundry guide
│   └── SAP_DEVELOPER_BUILD_GUIDE.md # SAP RAP / ABAP Development SOP
│
├── abap/                            # SAP S/4HANA RAP Artifacts
│   ├── dictionary/                  # Transparent DB Tables (SE11)
│   ├── cds/                         # Core Data Services views & projections
│   ├── bdef/                        # RAP Behavior Definitions
│   └── classes/                     # ABAP Behavior Implementation classes
│
└── cap/                             # SAP Cloud Application Programming (CAP) Model
    ├── schema.cds                   # CDS Entity Definitions
    └── srv/                         # OData Services & Handlers
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Git

### Local Installation & Launch
```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/biteshare.git
cd biteshare

# 2. Run the application
python server.py
```

Open your browser and navigate to:
```
http://localhost:8088
```

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/state` | Returns the entire live platform state (donors, recipients, volunteers, donations, metrics) |
| `POST` | `/api/donation/create` | Creates a new surplus donation and automatically runs matching and volunteer dispatch |
| `POST` | `/api/donation/action` | Executes a lifecycle transition (`pickup` or `deliver`) with sequence validation |
| `POST` | `/api/salesforce/webhook` | Receives live webhook payloads from Salesforce CRM |
| `POST` | `/api/demo/reset` | Resets all state and metrics back to initial baseline data |

---

## ☁️ SAP BTP Cloud Foundry Deployment

The project is pre-configured for one-command deployment to SAP BTP:

```bash
# 1. Target your SAP BTP Cloud Foundry endpoint
cf api https://api.cf.eu10-004.hana.ondemand.com

# 2. Login to SAP BTP
cf login --sso

# 3. Push to SAP BTP Cloud Foundry
cf push
```

---

## 🤝 Salesforce Integration Setup

1. Copy [`salesforce/BiteShareCallout.cls`](salesforce/BiteShareCallout.cls) into your Salesforce Org via **Developer Console** or **VS Code Salesforce Extensions**.
2. Add your BiteShare public domain to **Setup ➔ Remote Site Settings**.
3. Deploy [`salesforce/FoodDonationTrigger.trigger`](salesforce/FoodDonationTrigger.trigger) to automatically dispatch donations created in Salesforce into BiteShare.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
