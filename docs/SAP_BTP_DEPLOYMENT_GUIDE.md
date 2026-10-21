# Deploying BiteShare to SAP BTP (Business Technology Platform)
### How to Host BiteShare with an Official SAP Cloud Public URL (`*.hana.ondemand.com`)

This guide explains how to deploy and host the **BiteShare Surplus Food Sharing Platform** directly on **SAP BTP Cloud Foundry Runtime** to get an official SAP public URL.

---

## 1. What SAP BTP Provides

When deployed on SAP BTP Cloud Foundry:
- **Public Domain**: Hosted on SAP's global infrastructure, e.g.:
  ```
  https://biteshare-food-network.cfapps.<region>.hana.ondemand.com
  ```
- **SSL / TLS**: Pre-configured with official SAP wildcard certificates.
- **High Availability**: Automatic container restarts, auto-scaling, and health checks.
- **Enterprise Integration**: Seamless binding with SAP HANA Cloud, SAP Cloud Identity Services (IAS), and SAP Destination Service.

---

## 2. Prepared Deployment Files in Workspace

The project is already pre-configured for 1-command deployment:

| File | Purpose | Location |
| :--- | :--- | :--- |
| `manifest.yml` | Cloud Foundry deployment descriptor (Memory, Disk, Buildpack, Healthcheck) | [`manifest.yml`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/manifest.yml) |
| `Procfile` | Specifies execution command (`web: python server.py`) | [`Procfile`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/Procfile) |
| `runtime.txt` | Target Python version for SAP BTP buildpack | [`runtime.txt`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/runtime.txt) |
| `requirements.txt`| Dependencies for SAP Cloud Foundry buildpack | [`requirements.txt`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/requirements.txt) |

---

## 3. Step-by-Step Deployment (3 Minutes)

### Step 1: Open Your SAP BTP Cockpit
1. Log in to [SAP BTP Cockpit](https://cockpit.eu10.hana.ondemand.com/cockpit/) (Free Trial or Enterprise Subaccount).
2. Open your **Subaccount** (e.g., `trial` or production subaccount).
3. On the Subaccount Overview page, locate your **Cloud Foundry Environment**:
   - **API Endpoint**: e.g., `https://api.cf.us10-001.hana.ondemand.com`
   - **Org Name**: e.g., `your-org-id`
   - **Space Name**: e.g., `dev`

---

### Step 2: Login via Cloud Foundry CLI (`cf`)
In your terminal (VS Code or PowerShell), run:

```powershell
cf login -a <YOUR_SAP_BTP_API_ENDPOINT>
```

Example:
```powershell
cf login -a https://api.cf.us10-001.hana.ondemand.com
```
Enter your SAP Universal ID email and password, then select your Org and Space (`dev`).

---

### Step 3: Deploy with `cf push`
Navigate to the project root and run:

```powershell
cd "C:\Users\G S RITHIKKA\.gemini\antigravity\scratch\biteshare-sap"
cf push
```

Cloud Foundry will automatically:
1. Upload the application files.
2. Compile and execute using the SAP BTP Python Buildpack.
3. Bind the container port dynamically to `$PORT`.
4. Provision the live public route:
   ```
   routes: biteshare-food-network.cfapps.<region>.hana.ondemand.com
   state:   started
   ```

---

## 4. Hooking the SAP BTP URL to Salesforce

Once deployed to SAP BTP, update your Salesforce Apex Callout ([`BiteShareCallout.cls`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/salesforce/BiteShareCallout.cls)) with your new SAP BTP URL:

```apex
private static final String ENDPOINT_URL = 'https://biteshare-food-network.cfapps.<region>.hana.ondemand.com/api/salesforce/webhook';
```

And update **Remote Site Settings** in Salesforce Setup with your SAP BTP domain!
