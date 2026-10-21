# BiteShare: Salesforce Integration Setup (2 Minutes)

Follow these steps in your **Salesforce Developer Edition Org** to connect it to this live BiteShare system:

---

### Step 1: Whitelist the Endpoint in Salesforce
1. In Salesforce Setup, type **Remote Site Settings** in the Quick Find box.
2. Click **New Remote Site**.
3. Enter:
   - **Remote Site Name**: `BiteShare_SAP_Bridge`
   - **Remote Site URL**: `https://theaters-eric-portable-recipient.trycloudflare.com`
   - Active: `[X]` (Checked)
4. Click **Save**.

---

### Step 2: Add the Apex Callout Class
1. Click the Gear Icon ⚙️ -> **Developer Console**.
2. Go to **File** -> **New** -> **Apex Class**.
3. Name: `BiteShareCallout`
4. Paste the contents of [`BiteShareCallout.cls`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/salesforce/BiteShareCallout.cls) and press `Ctrl + S`.

---

### Step 3: Add the Apex Trigger
1. In Developer Console, go to **File** -> **New** -> **Apex Trigger**.
2. Name: `BiteShareWebhookTrigger`
3. sObject: `Food_Donation__c`
4. Paste the contents of [`BiteShareWebhookTrigger.trigger`](file:///C:/Users/G%20S%20RITHIKKA/.gemini/antigravity/scratch/biteshare-sap/salesforce/BiteShareWebhookTrigger.trigger) and press `Ctrl + S`.

---

### That's it!
Whenever you create or edit a `Food_Donation__c` in your Salesforce Lightning App, it will instantly push to this live BiteShare system, auto-match the recipient, dispatch the volunteer, and update the live delivery tracker!
