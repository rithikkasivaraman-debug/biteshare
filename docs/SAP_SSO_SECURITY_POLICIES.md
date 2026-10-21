# BiteShare: SAP Single Sign-On (SSO) & Multi-Portal Architecture
### Security Policies & Role-Based Access Control (RBAC) Specification

This document details the Single Sign-On (SSO) and Role-Based Access Control architecture implemented for the **BiteShare Surplus Food Sharing System**, mapping enterprise **SAP Cloud Identity Services (IAS)** policies across the three dedicated user portals.

---

## 1. Enterprise SSO Architecture Overview

```
                                  +------------------------------------+
                                  |   SAP Cloud Identity Services      |
                                  |   (Identity Authentication - IAS)  |
                                  +-----------------+------------------+
                                                    |
                         +--------------------------+--------------------------+
                         | (SAML 2.0 / OIDC Token)  | (MFA & Risk Policies)    |
                         v                          v                          v
       +-------------------------------+ +-------------------------------+ +-------------------------------+
       |       1. DONOR PORTAL         | |     2. RECIPIENT PORTAL       | |     3. VOLUNTEER PORTAL       |
       |  (Hotels, Banquets, Caterers) | |    (Shelters, Food Banks)     | |      (Field Logistics)        |
       +-------------------------------+ +-------------------------------+ +-------------------------------+
       | Role: BiteShare_Donor         | | Role: BiteShare_Recipient     | | Role: BiteShare_Volunteer     |
       | Scope: Donate & Track         | | Scope: Accept & Confirm Rcpt  | | Scope: Pickup & Complete      |
       | Bound: Own Organization ID    | | Bound: Operating City & Cap.  | | Bound: Operating City Geo     |
       +-------------------------------+ +-------------------------------+ +-------------------------------+
```

---

## 2. The Three Dedicated User Portals

### 2.1 Food Donor Portal
- **Target Audience**: Hotel banquet managers, corporate event coordinators, college mess administrators, restaurant owners.
- **SSO Role**: `BiteShare_Donor`
- **Allowed Actions**:
  - Register surplus food with quantity, dietary type (Veg / Non-Veg / Both), city, and expiry timestamp.
  - Live milestone tracking of active donations (`Submitted` $\rightarrow$ `Matched` $\rightarrow$ `Volunteer Assigned` $\rightarrow$ `Picked Up` $\rightarrow$ `Delivered`).
  - View organization impact summary (Total kg rescued, carbon emissions prevented).
- **Security Boundary**: A donor can **only** view donations belonging to their own organization (`donor_id = current_user.org_id`).

### 2.2 Recipient Organization Portal
- **Target Audience**: Verified NGOs, homeless shelters, community kitchens, food banks.
- **SSO Role**: `BiteShare_Recipient`
- **Allowed Actions**:
  - Real-time inbound feed of surplus food automatically matched to their capacity and dietary criteria.
  - **Accept Donation** button (automatically triggers Flow 2 to assign an available field volunteer).
  - View assigned volunteer details (name, phone number, vehicle ETA).
  - **Confirm Receipt** button upon physical delivery.
- **Security Boundary**: An NGO can **only** view donations assigned to their specific organization ID.

### 2.3 Volunteer Field Portal
- **Target Audience**: Field pickup volunteers and logistics coordinators.
- **SSO Role**: `BiteShare_Volunteer`
- **Allowed Actions**:
  - Live pickup and delivery mission route (Origin Donor Address $\rightarrow$ Destination Recipient Shelter).
  - Toggle duty availability (`Available for Pickups` 🟢 vs `Off-Duty / Rest` 🔴).
  - **Confirm Picked Up** button (transitions donation to `PICKED_UP`).
  - **Complete Delivery** button (transitions donation to `COMPLETED`, frees volunteer back to Available, sends coordinator alert).
- **Security Boundary**: Volunteers can only receive task dispatches located in their registered city jurisdiction.

---

## 3. Enforced SAP SSO Security Policies

### Policy 1: Identity Provider (IdP) Authentication & Federation
- User identities are verified through **SAP Cloud Identity Services (IAS)** using standard **SAML 2.0 / OpenID Connect (OIDC)** tokens.
- Authentication tokens contain verified claims:
  - `sub`: User ID
  - `role`: Granted portal role (`DONOR`, `RECIPIENT`, `VOLUNTEER`)
  - `city`: Operating metropolitan boundary
  - `org`: Organization identity

### Policy 2: Zero-Trust Portal Isolation
- Strict role-based isolation is enforced:
  - Donors cannot trigger volunteer assignment or accept donations.
  - Recipients cannot submit donor records or assign volunteers.
  - Volunteers cannot alter recipient capacity or donor specifications.

### Policy 3: Context-Aware City Geo-Fencing
- Volunteers are only allocated to food dispatches within their registered operating city.
- Recipient matching algorithms only match donor food with verified recipient shelters located in the exact same city.

### Policy 4: Multi-Factor Authentication (MFA) & Session Lifecycle
- High-privilege actions (accepting large volume food donations $\ge$ 500 kg and completing deliveries) require active MFA verification status.
- Sessions are constrained to an 8-hour sliding window with instant token revocation upon logout or identity switch.
