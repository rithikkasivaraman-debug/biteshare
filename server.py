import http.server
import socketserver
import json
import urllib.parse
from datetime import datetime, timezone, timedelta
import os

PORT = int(os.environ.get("PORT", 8088))

def get_initial_state():
    return {
        "donors": [
            {"id": "DNR-0001", "name": "Royal Palace Catering", "city": "Dallas", "donor_type": "Event", "email": "catering@royalpalace.com", "phone": "555-0101"},
            {"id": "DNR-0002", "name": "Grand Plaza Hotel", "city": "Dallas", "donor_type": "Hotel", "email": "events@grandplaza.com", "phone": "555-0102"},
            {"id": "DNR-0003", "name": "Bayou City Banquets", "city": "Houston", "donor_type": "Event", "email": "info@bayoubanquets.com", "phone": "555-0103"},
            {"id": "DNR-0004", "name": "Houston Galleria Catering", "city": "Houston", "donor_type": "Restaurant", "email": "contact@galleriacater.com", "phone": "555-0104"},
            {"id": "DNR-0005", "name": "Austin Tech Center Cafe", "city": "Austin", "donor_type": "College", "email": "cafe@austintech.com", "phone": "555-0105"},
            {"id": "DNR-0006", "name": "Magnificent Mile Hotel", "city": "Chicago", "donor_type": "Hotel", "email": "dining@magmilehotel.com", "phone": "555-0106"},
            {"id": "DNR-0007", "name": "Midtown Grand Ballroom", "city": "New York", "donor_type": "Event", "email": "events@midtowngrand.com", "phone": "555-0107"},
            {"id": "DNR-0008", "name": "Seattle Convention Suites", "city": "Seattle", "donor_type": "Event", "email": "suites@seattleconv.com", "phone": "555-0108"},
            {"id": "DNR-0009", "name": "Grand Chola Banquets", "city": "Chennai", "donor_type": "Hotel", "email": "banquets@grandchola.com", "phone": "555-0109"},
            {"id": "DNR-0010", "name": "Whitefield Tech Cafeteria", "city": "Bengaluru", "donor_type": "College", "email": "food@whitefieldtech.com", "phone": "555-0110"}
        ],
        "recipients": [
            # Dallas
            {"id": "RCP-0001", "name": "Hope Community Shelter", "city": "Dallas", "food_type": "Both", "capacity_kg": 500, "is_verified": True, "contact_email": "hope@shelter.org", "phone": "555-0201"},
            {"id": "RCP-0002", "name": "Green Earth Food Bank", "city": "Dallas", "food_type": "Veg", "capacity_kg": 300, "is_verified": True, "contact_email": "green@earthbank.org", "phone": "555-0202"},
            {"id": "RCP-0003", "name": "North Texas Food Rescue", "city": "Dallas", "food_type": "Both", "capacity_kg": 800, "is_verified": True, "contact_email": "ntx@rescue.org", "phone": "555-0203"},
            # Houston
            {"id": "RCP-0004", "name": "Houston Food Mission", "city": "Houston", "food_type": "Both", "capacity_kg": 650, "is_verified": True, "contact_email": "mission@houstonfood.org", "phone": "555-0204"},
            {"id": "RCP-0005", "name": "Star of Hope Haven", "city": "Houston", "food_type": "Veg", "capacity_kg": 400, "is_verified": True, "contact_email": "star@hopehaven.org", "phone": "555-0205"},
            {"id": "RCP-0006", "name": "Gulf Coast Community Pantry", "city": "Houston", "food_type": "Both", "capacity_kg": 1000, "is_verified": True, "contact_email": "gulfcoast@pantry.org", "phone": "555-0206"},
            # Austin
            {"id": "RCP-0007", "name": "Austin Community Kitchen", "city": "Austin", "food_type": "Both", "capacity_kg": 450, "is_verified": True, "contact_email": "kitchen@austinrelief.org", "phone": "555-0207"},
            {"id": "RCP-0008", "name": "Hill Country Relief Center", "city": "Austin", "food_type": "Veg", "capacity_kg": 250, "is_verified": True, "contact_email": "hillcountry@relief.org", "phone": "555-0208"},
            # Chicago
            {"id": "RCP-0009", "name": "Windy City Food Pantry", "city": "Chicago", "food_type": "Both", "capacity_kg": 750, "is_verified": True, "contact_email": "windycity@pantry.org", "phone": "555-0209"},
            {"id": "RCP-0010", "name": "Midwest Care Shelter", "city": "Chicago", "food_type": "Veg", "capacity_kg": 350, "is_verified": True, "contact_email": "midwest@careshelter.org", "phone": "555-0210"},
            # New York
            {"id": "RCP-0011", "name": "City Harvest Outreach", "city": "New York", "food_type": "Both", "capacity_kg": 1200, "is_verified": True, "contact_email": "outreach@cityharvest.org", "phone": "555-0211"},
            {"id": "RCP-0012", "name": "Bowery Mission Haven", "city": "New York", "food_type": "Veg", "capacity_kg": 500, "is_verified": True, "contact_email": "bowery@missionhaven.org", "phone": "555-0212"},
            # Seattle
            {"id": "RCP-0013", "name": "Puget Sound Food Bank", "city": "Seattle", "food_type": "Both", "capacity_kg": 600, "is_verified": True, "contact_email": "puget@foodbank.org", "phone": "555-0213"},
            # Chennai
            {"id": "RCP-0014", "name": "Annam Food Relief Foundation", "city": "Chennai", "food_type": "Veg", "capacity_kg": 800, "is_verified": True, "contact_email": "annam@relief.org", "phone": "555-0214"},
            {"id": "RCP-0015", "name": "Karuna Community Kitchen", "city": "Chennai", "food_type": "Both", "capacity_kg": 500, "is_verified": True, "contact_email": "karuna@kitchen.org", "phone": "555-0215"},
            # Bengaluru
            {"id": "RCP-0016", "name": "Akshaya Food Network", "city": "Bengaluru", "food_type": "Veg", "capacity_kg": 1000, "is_verified": True, "contact_email": "akshaya@foodnet.org", "phone": "555-0216"},
            {"id": "RCP-0017", "name": "Robin Hood Food Volunteers", "city": "Bengaluru", "food_type": "Both", "capacity_kg": 700, "is_verified": True, "contact_email": "robinhood@blrfund.org", "phone": "555-0217"}
        ],
        "volunteers": [
            # Dallas
            {"id": "VOL-0001", "name": "Alex Rivera", "city": "Dallas", "is_available": False, "email": "alex.rivera@volunteer.org", "phone": "555-0301", "deliveries_completed": 3},
            {"id": "VOL-0002", "name": "Samira Khan", "city": "Dallas", "is_available": True, "email": "samira.khan@volunteer.org", "phone": "555-0302", "deliveries_completed": 1},
            {"id": "VOL-0003", "name": "David Chen", "city": "Dallas", "is_available": True, "email": "david.chen@volunteer.org", "phone": "555-0303", "deliveries_completed": 0},
            {"id": "VOL-0004", "name": "Maria Santos", "city": "Dallas", "is_available": True, "email": "maria.santos@volunteer.org", "phone": "555-0304", "deliveries_completed": 2},

            # Houston
            {"id": "VOL-0005", "name": "Liam Johnson", "city": "Houston", "is_available": True, "email": "liam.j@volunteer.org", "phone": "555-0305", "deliveries_completed": 2},
            {"id": "VOL-0006", "name": "Priya Patel", "city": "Houston", "is_available": True, "email": "priya.p@volunteer.org", "phone": "555-0306", "deliveries_completed": 4},
            {"id": "VOL-0007", "name": "Marcus Williams", "city": "Houston", "is_available": True, "email": "marcus.w@volunteer.org", "phone": "555-0307", "deliveries_completed": 1},
            {"id": "VOL-0008", "name": "Elena Rodriguez", "city": "Houston", "is_available": True, "email": "elena.r@volunteer.org", "phone": "555-0308", "deliveries_completed": 0},

            # Austin
            {"id": "VOL-0009", "name": "Carlos Diaz", "city": "Austin", "is_available": True, "email": "carlos.diaz@volunteer.org", "phone": "555-0309", "deliveries_completed": 1},
            {"id": "VOL-0010", "name": "Chloe Bennett", "city": "Austin", "is_available": True, "email": "chloe.b@volunteer.org", "phone": "555-0310", "deliveries_completed": 0},
            {"id": "VOL-0011", "name": "Ryan Miller", "city": "Austin", "is_available": True, "email": "ryan.m@volunteer.org", "phone": "555-0311", "deliveries_completed": 2},

            # Chicago
            {"id": "VOL-0012", "name": "Noah Taylor", "city": "Chicago", "is_available": True, "email": "noah.t@volunteer.org", "phone": "555-0312", "deliveries_completed": 3},
            {"id": "VOL-0013", "name": "Aaliyah Brooks", "city": "Chicago", "is_available": True, "email": "aaliyah.b@volunteer.org", "phone": "555-0313", "deliveries_completed": 1},
            {"id": "VOL-0014", "name": "Ethan Davis", "city": "Chicago", "is_available": True, "email": "ethan.d@volunteer.org", "phone": "555-0314", "deliveries_completed": 0},

            # New York
            {"id": "VOL-0015", "name": "Daniel Kim", "city": "New York", "is_available": True, "email": "daniel.k@volunteer.org", "phone": "555-0315", "deliveries_completed": 5},
            {"id": "VOL-0016", "name": "Olivia Brown", "city": "New York", "is_available": True, "email": "olivia.b@volunteer.org", "phone": "555-0316", "deliveries_completed": 2},
            {"id": "VOL-0017", "name": "Lucas Silva", "city": "New York", "is_available": True, "email": "lucas.s@volunteer.org", "phone": "555-0317", "deliveries_completed": 1},

            # Seattle
            {"id": "VOL-0018", "name": "James Wilson", "city": "Seattle", "is_available": True, "email": "james.w@volunteer.org", "phone": "555-0318", "deliveries_completed": 2},
            {"id": "VOL-0019", "name": "Emily White", "city": "Seattle", "is_available": True, "email": "emily.w@volunteer.org", "phone": "555-0319", "deliveries_completed": 0},

            # Chennai
            {"id": "VOL-0020", "name": "Karthik Raman", "city": "Chennai", "is_available": True, "email": "karthik.r@volunteer.org", "phone": "555-0320", "deliveries_completed": 6},
            {"id": "VOL-0021", "name": "Divya Suresh", "city": "Chennai", "is_available": True, "email": "divya.s@volunteer.org", "phone": "555-0321", "deliveries_completed": 2},
            {"id": "VOL-0022", "name": "Vignesh Kumar", "city": "Chennai", "is_available": True, "email": "vignesh.k@volunteer.org", "phone": "555-0322", "deliveries_completed": 3},

            # Bengaluru
            {"id": "VOL-0023", "name": "Rohan Sharma", "city": "Bengaluru", "is_available": True, "email": "rohan.s@volunteer.org", "phone": "555-0323", "deliveries_completed": 4},
            {"id": "VOL-0024", "name": "Ananya Rao", "city": "Bengaluru", "is_available": True, "email": "ananya.r@volunteer.org", "phone": "555-0324", "deliveries_completed": 1},
            {"id": "VOL-0025", "name": "Arvind Swamy", "city": "Bengaluru", "is_available": True, "email": "arvind.s@volunteer.org", "phone": "555-0325", "deliveries_completed": 2}
        ],
        "donations": [
            {
                "donation_id": "FD-0001",
                "salesforce_id": "a001200000X9A4EAA1",
                "food_type": "Veg",
                "quantity_kg": 100,
                "city": "Dallas",
                "usable_until": (datetime.now() + timedelta(hours=6)).isoformat(),
                "donor_id": "DNR-0001",
                "recipient_id": "RCP-0001",
                "volunteer_id": "VOL-0001",
                "status": "VOL_ASSIGNED",
                "source": "Salesforce Connected App",
                "created_at": datetime.now().strftime("%H:%M:%S")
            }
        ],
        "deliveries": [
            {
                "delivery_id": "PD-0001",
                "donation_id": "FD-0001",
                "pickup_time": None,
                "delivery_time": None,
                "status": "PENDING"
            }
        ],
        "salesforce_sync": {
            "connected": True,
            "org_name": "Salesforce Developer Edition",
            "instance_url": "https://developer.salesforce.com",
            "webhook_endpoint": "https://theaters-eric-portable-recipient.trycloudflare.com/api/salesforce/webhook",
            "total_synced_records": 1,
            "last_sync_time": datetime.now().strftime("%H:%M:%S"),
            "sync_mode": "Bi-Directional Auto-Sync"
        },
        "logs": [
            {
                "time": datetime.now().strftime("%H:%M:%S"),
                "category": "SALESFORCE_BRIDGE",
                "message": "Salesforce Integration Active. Listening for Food_Donation__c webhooks."
            }
        ],
        "next_donation_num": 2,
        "next_delivery_num": 2
    }

STATE = get_initial_state()

def add_log(category, message, details=""):
    timestamp = datetime.now().strftime("%H:%M:%S")
    STATE["logs"].insert(0, {
        "time": timestamp,
        "category": category,
        "message": message,
        "details": details
    })

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>BiteShare | Connected to Salesforce</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    :root {
      --primary: #0284c7;
      --primary-dark: #0369a1;
      --sf-blue: #0176d3;
      --donor-accent: #0284c7;
      --recipient-accent: #7c3aed;
      --volunteer-accent: #16a34a;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --success: #10b981;
      --warning: #f59e0b;
      --radius-sm: 6px;
      --radius-md: 10px;
      --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; }
    body { background-color: var(--bg); color: var(--text-main); display: flex; flex-direction: column; min-height: 100vh; }

    /* Top Connected Bar */
    .sf-sync-banner {
      background: #032d60;
      color: #bae6fd;
      padding: 6px 1.5rem;
      font-size: 0.78rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #0c4a6e;
    }
    .sf-badge { background: #0284c7; color: #fff; padding: 2px 7px; border-radius: 4px; font-weight: 700; font-size: 0.72rem; }

    /* Header */
    header.app-header {
      background: #0f172a;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 1.75rem;
      height: 60px;
      position: sticky;
      top: 0;
      z-index: 50;
      box-shadow: 0 4px 12px rgba(15, 23, 42, 0.12);
    }
    .brand-wrap { display: flex; align-items: center; gap: 12px; }
    .brand-icon {
      background: linear-gradient(135deg, #0176d3, #0284c7);
      width: 36px;
      height: 36px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-size: 1.1rem;
    }
    .brand-title { font-weight: 800; font-size: 1.2rem; letter-spacing: -0.5px; }
    .header-actions { display: flex; align-items: center; gap: 10px; }

    /* Tabs */
    nav.app-nav {
      background: #ffffff;
      border-bottom: 1px solid var(--border);
      display: flex;
      gap: 6px;
      padding: 0 1.5rem;
      overflow-x: auto;
    }
    .nav-item {
      padding: 13px 16px;
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      border-bottom: 2px solid transparent;
      white-space: nowrap;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s;
    }
    .nav-item:hover { color: var(--primary); }
    .nav-item.active { color: var(--primary); border-bottom-color: var(--primary); font-weight: 700; }
    .nav-item.sf.active { color: var(--sf-blue); border-bottom-color: var(--sf-blue); }

    /* Main Container */
    main.main-content { max-width: 1380px; width: 100%; margin: 1.25rem auto; padding: 0 1.25rem; flex: 1; }

    /* KPI Highlights */
    .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1rem; margin-bottom: 1.25rem; }
    .kpi-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 1.15rem;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      position: relative;
      overflow: hidden;
    }
    .kpi-card::before { content:''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px; background: var(--primary); }
    .kpi-card.green::before { background: var(--success); }
    .kpi-card.blue::before { background: var(--sf-blue); }
    .kpi-label { font-size: 0.76rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-value { font-size: 1.95rem; font-weight: 800; color: var(--text-main); margin: 4px 0; letter-spacing: -0.5px; }
    .kpi-subtext { font-size: 0.76rem; color: var(--text-muted); }

    /* Content Cards */
    .content-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-sm);
      margin-bottom: 1.25rem;
      overflow: hidden;
    }
    .card-header {
      padding: 0.95rem 1.3rem;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #fafbfc;
    }
    .card-header h2 { font-size: 1.02rem; font-weight: 700; color: var(--text-main); display: flex; align-items: center; gap: 8px; }
    .card-body { padding: 1.3rem; }

    /* Forms */
    .form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1.15rem; }
    .form-group { display: flex; flex-direction: column; gap: 5px; }
    .form-group label { font-size: 0.8rem; font-weight: 700; color: var(--text-main); }
    .form-control {
      padding: 8px 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 0.88rem;
      outline: none;
      background: #ffffff;
    }
    .form-control:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15); }

    /* Buttons */
    .btn {
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      font-size: 0.83rem;
      font-weight: 700;
      cursor: pointer;
      border: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .btn-primary { background: var(--primary); color: #fff; }
    .btn-primary:hover { background: var(--primary-dark); }
    .btn-sf { background: var(--sf-blue); color: #fff; }
    .btn-sf:hover { background: #014486; }
    .btn-donor { background: var(--donor-accent); color: #fff; }
    .btn-donor:hover { background: #0369a1; }
    .btn-recipient { background: var(--recipient-accent); color: #fff; }
    .btn-recipient:hover { background: #6d28d9; }
    .btn-volunteer { background: var(--volunteer-accent); color: #fff; }
    .btn-volunteer:hover { background: #15803d; }
    .btn-success { background: var(--success); color: #fff; }
    .btn-warning { background: var(--warning); color: #fff; }
    .btn-outline { background: transparent; border: 1px solid var(--border); color: var(--text-main); }
    .btn-outline:hover { background: #f1f5f9; }
    .btn-disabled { background: #f1f5f9; color: #94a3b8; border: 1px solid #e2e8f0; cursor: not-allowed; }
    .btn-sm { padding: 4px 10px; font-size: 0.76rem; border-radius: 5px; }

    /* Tables */
    .data-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.86rem; }
    .data-table th { background: #f8fafc; padding: 11px 13px; border-bottom: 2px solid var(--border); color: var(--text-muted); font-weight: 700; font-size: 0.77rem; text-transform: uppercase; }
    .data-table td { padding: 11px 13px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }
    .data-table tr:hover { background: #fcfcfd; }

    /* Badges */
    .badge-status { display: inline-flex; align-items: center; gap: 4px; padding: 3px 9px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; }
    .badge-submitted { background: #e0f2fe; color: #0369a1; }
    .badge-matched { background: #fef3c7; color: #b45309; }
    .badge-vol_assigned { background: #e0f2fe; color: #0284c7; }
    .badge-picked_up { background: #fef9c3; color: #a16207; }
    .badge-delivered, .badge-completed { background: #dcfce7; color: #166534; }

    /* Stepper Track */
    .stepper-track { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; background: #fafbfc; border-radius: var(--radius-sm); border: 1px solid var(--border); margin-bottom: 1rem; }
    .step-node { display: flex; flex-direction: column; align-items: center; text-align: center; gap: 6px; position: relative; z-index: 2; flex: 1; }
    .step-bubble { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: bold; background: #e2e8f0; color: #64748b; }
    .step-node.done .step-bubble { background: var(--success); color: #fff; }
    .step-node.active .step-bubble { background: var(--primary); color: #fff; }
    .step-label { font-size: 0.75rem; font-weight: 700; color: var(--text-muted); }
    .step-node.done .step-label, .step-node.active .step-label { color: var(--text-main); }
    .step-line { height: 3px; background: #e2e8f0; flex: 1; margin: 0 -10px 18px -10px; z-index: 1; }
    .step-line.done { background: var(--success); }

    /* Terminal Log */
    .log-terminal { max-height: 180px; overflow-y: auto; background: #0f172a; color: #38bdf8; padding: 12px; border-radius: var(--radius-sm); font-family: ui-monospace, "Cascadia Code", monospace; font-size: 0.8rem; line-height: 1.5; }
    .log-item { margin-bottom: 4px; }
    .log-item .time { color: #64748b; }
    .log-item .tag { color: #facc15; font-weight: 700; }
  </style>
</head>
<body>

  <!-- Live Salesforce Sync Banner -->
  <div class="sf-sync-banner">
    <div style="display:flex; align-items:center; gap:8px;">
      <i class="fa-brands fa-salesforce" style="font-size:1.15rem; color:#38bdf8;"></i>
      <span><strong>Salesforce Integration Bridge:</strong> Connected & Listening</span>
      <span class="sf-badge">Bi-Directional</span>
    </div>
    <div style="font-size:0.75rem;">
      <span>Webhook: <code>https://theaters-eric-portable-recipient.trycloudflare.com/api/salesforce/webhook</code></span>
    </div>
  </div>

  <!-- Header -->
  <header class="app-header">
    <div class="brand-wrap">
      <div class="brand-icon"><i class="fa-brands fa-salesforce"></i></div>
      <div>
        <span class="brand-title">BiteShare</span>
        <span class="sf-badge" style="background:#0176d3; margin-left:6px;">Salesforce Connected</span>
      </div>
    </div>
    <div class="header-actions">
      <button class="btn btn-sf btn-sm" onclick="simulateSalesforcePush()"><i class="fa-brands fa-salesforce"></i> Push from Salesforce (Simulate)</button>
      <button class="btn btn-outline btn-sm" style="color:#fff; border-color:#475569;" onclick="resetDemo()"><i class="fa-solid fa-rotate-right"></i> Reset</button>
    </div>
  </header>

  <!-- Navigation Tabs -->
  <nav class="app-nav">
    <div class="nav-item donor active" onclick="switchTab('donor')">
      <i class="fa-solid fa-hand-holding-heart"></i> 1. Donor Section
    </div>
    <div class="nav-item recipient" onclick="switchTab('recipient')">
      <i class="fa-solid fa-building-ngo"></i> 2. Recipient Section (NGOs)
    </div>
    <div class="nav-item volunteer" onclick="switchTab('volunteer')">
      <i class="fa-solid fa-motorcycle"></i> 3. Volunteer Section
    </div>
    <div class="nav-item" onclick="switchTab('tracking')">
      <i class="fa-solid fa-route"></i> 4. Delivery Tracking
    </div>
    <div class="nav-item sf" onclick="switchTab('salesforce')">
      <i class="fa-brands fa-salesforce"></i> 5. Salesforce Integration
    </div>
    <div class="nav-item" onclick="switchTab('volunteers')">
      <i class="fa-solid fa-users"></i> Volunteer Pool (25)
    </div>
    <div class="nav-item" onclick="switchTab('recipients')">
      <i class="fa-solid fa-hotel"></i> NGOs & Shelters (17)
    </div>
    <div class="nav-item" onclick="switchTab('analytics')">
      <i class="fa-solid fa-chart-pie"></i> Impact Analysis
    </div>
  </nav>

  <!-- Main Container -->
  <main class="main-content">

    <!-- KPI Summary Row -->
    <div class="kpi-grid">
      <div class="kpi-card green">
        <span class="kpi-label">Total Food Rescued</span>
        <span class="kpi-value" id="kpi-rescued">0 kg</span>
        <span class="kpi-subtext"><i class="fa-solid fa-leaf" style="color:var(--success)"></i> Synced across SAP & Salesforce</span>
      </div>
      <div class="kpi-card blue">
        <span class="kpi-label">Salesforce Synced</span>
        <span class="kpi-value" id="kpi-sf-synced">1 record</span>
        <span class="kpi-subtext">Real-time webhook active</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-label">Available Volunteers</span>
        <span class="kpi-value" id="kpi-volunteers">25</span>
        <span class="kpi-subtext">Ready for dispatch</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-label">Verified Places / NGOs</span>
        <span class="kpi-value" id="kpi-recipients">17</span>
        <span class="kpi-subtext">Shelters ready to receive</span>
      </div>
    </div>


    <!-- ============================================== -->
    <!-- SECTION 1: DONOR SECTION                       -->
    <!-- ============================================== -->
    <div id="tab-donor" class="tab-pane">
      <div class="content-card">
        <div class="card-header">
          <h2><i class="fa-solid fa-plus-circle" style="color:var(--donor-accent)"></i> Donor Portal: Register Surplus Food</h2>
          <span style="font-size:0.8rem; color:var(--text-muted);">Syncs directly to Salesforce Food_Donation__c</span>
        </div>
        <div class="card-body">
          <form onsubmit="handleCreateDonation(event)">
            <div class="form-grid">
              <div class="form-group">
                <label>Donor Organization (Origin Place)</label>
                <select id="donorSelect" class="form-control" onchange="onDonorChange()"></select>
              </div>
              <div class="form-group">
                <label>City / Operating Metro *</label>
                <select id="citySelect" class="form-control" required onchange="onCityChange()">
                  <option value="Dallas">Dallas, TX</option>
                  <option value="Houston">Houston, TX</option>
                  <option value="Austin">Austin, TX</option>
                  <option value="Chicago">Chicago, IL</option>
                  <option value="New York">New York, NY</option>
                  <option value="Seattle">Seattle, WA</option>
                  <option value="Chennai">Chennai, India</option>
                  <option value="Bengaluru">Bengaluru, India</option>
                </select>
              </div>
              <div class="form-group">
                <label>Food Type *</label>
                <select id="foodType" class="form-control" required>
                  <option value="Veg">Vegetarian Food</option>
                  <option value="Both">Vegetarian & Non-Veg</option>
                  <option value="Non-Veg">Non-Vegetarian Food</option>
                </select>
              </div>
              <div class="form-group">
                <label>Quantity (in kg) *</label>
                <input type="number" id="quantityKg" class="form-control" value="100" min="1" required>
              </div>
              <div class="form-group">
                <label>Usable Until (Date & Time) *</label>
                <input type="datetime-local" id="usableUntil" class="form-control" required>
              </div>
            </div>
            <div style="margin-top: 1.25rem; display: flex; gap: 12px; align-items: center;">
              <button type="submit" class="btn btn-donor"><i class="fa-solid fa-paper-plane"></i> Submit Food Donation</button>
              <span id="formMsg" style="font-size:0.85rem; font-weight:600;"></span>
            </div>
          </form>
        </div>
      </div>

      <!-- Outbound Requests Table -->
      <div class="content-card">
        <div class="card-header">
          <h2><i class="fa-solid fa-clipboard-list"></i> Donor Outbound Food Requests</h2>
          <button class="btn btn-outline btn-sm" onclick="fetchState()"><i class="fa-solid fa-arrows-rotate"></i> Refresh</button>
        </div>
        <div class="card-body" style="padding:0; overflow-x:auto;">
          <table class="data-table">
            <thead>
              <tr>
                <th>Donation ID</th>
                <th>Source</th>
                <th>Donor Place</th>
                <th>City</th>
                <th>Food Type</th>
                <th>Quantity</th>
                <th>Auto-Matched Recipient</th>
                <th>Auto-Assigned Volunteer</th>
                <th>Live Status</th>
              </tr>
            </thead>
            <tbody id="donorRequestsTableBody"></tbody>
          </table>
        </div>
      </div>
    </div>


    <!-- ============================================== -->
    <!-- SECTION 2: RECIPIENT SECTION (NGOs)            -->
    <!-- ============================================== -->
    <div id="tab-recipient" class="tab-pane" style="display:none;">
      <div class="content-card">
        <div class="card-header">
          <h2><i class="fa-solid fa-hand-holding-heart" style="color:var(--recipient-accent)"></i> Recipient / NGO Inbound Feed</h2>
          <span style="font-size:0.8rem; color:var(--text-muted);">Confirm Received is unlocked when volunteer confirms pickup</span>
        </div>
        <div class="card-body" style="padding:0; overflow-x:auto;">
          <table class="data-table">
            <thead>
              <tr>
                <th>Donation ID</th>
                <th>Matched Recipient Shelter</th>
                <th>Origin Place (Donor)</th>
                <th>City</th>
                <th>Quantity</th>
                <th>Assigned Volunteer</th>
                <th>Delivery Stage</th>
                <th>Receipt Confirmation</th>
              </tr>
            </thead>
            <tbody id="recipientTableBody"></tbody>
          </table>
        </div>
      </div>
    </div>


    <!-- ============================================== -->
    <!-- SECTION 3: VOLUNTEER SECTION                   -->
    <!-- ============================================== -->
    <div id="tab-volunteer" class="tab-pane" style="display:none;">
      <div class="content-card">
        <div class="card-header">
          <h2><i class="fa-solid fa-motorcycle" style="color:var(--volunteer-accent)"></i> Volunteer Field Logistics</h2>
          <span style="font-size:0.8rem; color:var(--text-muted);">Pickups conveyed directly to field volunteers</span>
        </div>
        <div class="card-body" style="padding:0; overflow-x:auto;">
          <table class="data-table">
            <thead>
              <tr>
                <th>Donation ID</th>
                <th>Assigned Volunteer</th>
                <th>Operating City</th>
                <th>Pickup Location &rarr; Dropoff Shelter Route</th>
                <th>Quantity</th>
                <th>Mission Status</th>
                <th>Volunteer Action</th>
              </tr>
            </thead>
            <tbody id="volunteerTasksTableBody"></tbody>
          </table>
        </div>
      </div>
    </div>


    <!-- ============================================== -->
    <!-- SECTION 4: DELIVERY TRACKING                   -->
    <!-- ============================================== -->
    <div id="tab-tracking" class="tab-pane" style="display:none;">
      <div class="content-card">
        <div class="card-header">
          <h2><i class="fa-solid fa-route" style="color:var(--primary)"></i> Real-Time Delivery Tracking & Sequential Progress</h2>
        </div>
        <div class="card-body" id="deliveryTrackingContainer"></div>
      </div>
    </div>


    <!-- ============================================== -->
    <!-- SECTION 5: SALESFORCE INTEGRATION DASHBOARD    -->
    <!-- ============================================== -->
    <div id="tab-salesforce" class="tab-pane" style="display:none;">
      <!-- Connection Status Card -->
      <div class="content-card">
        <div class="card-header">
          <h2><i class="fa-brands fa-salesforce" style="color:var(--sf-blue)"></i> Salesforce Live Connection Status</h2>
          <span class="badge-status badge-completed"><i class="fa-solid fa-circle-check"></i> Webhook Active</span>
        </div>
        <div class="card-body">
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:1.25rem;">
            <div style="background:#f8fafc; border:1px solid var(--border); border-radius:var(--radius-sm); padding:1rem;">
              <h3 style="font-size:0.9rem; color:var(--text-muted); margin-bottom:8px;">Live Webhook Endpoint</h3>
              <code style="background:#0f172a; color:#38bdf8; padding:6px 10px; border-radius:4px; font-size:0.8rem; display:block; word-break:break-all;">
                https://theaters-eric-portable-recipient.trycloudflare.com/api/salesforce/webhook
              </code>
              <p style="font-size:0.78rem; color:#64748b; margin-top:8px;">Any JSON POST sent to this URL is immediately ingested into BiteShare.</p>
            </div>

            <div style="background:#f8fafc; border:1px solid var(--border); border-radius:var(--radius-sm); padding:1rem;">
              <h3 style="font-size:0.9rem; color:var(--text-muted); margin-bottom:8px;">Test Salesforce Inbound Event</h3>
              <p style="font-size:0.8rem; color:#64748b; margin-bottom:10px;">Simulate an Apex Trigger firing from your Salesforce Developer Org:</p>
              <button class="btn btn-sf btn-sm" onclick="simulateSalesforcePush()"><i class="fa-brands fa-salesforce"></i> Push Sample Record from Salesforce</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Salesforce Code Snippets -->
      <div class="content-card">
        <div class="card-header">
          <h2><i class="fa-solid fa-code"></i> Setup In Your Salesforce Developer Org (2 Minutes)</h2>
        </div>
        <div class="card-body">
          <p style="font-size:0.85rem; margin-bottom:12px; line-height:1.6;">
            1. In Salesforce Setup, go to <strong>Remote Site Settings</strong> and whitelist <code>https://theaters-eric-portable-recipient.trycloudflare.com</code>.<br>
            2. Open <strong>Developer Console</strong>, create an Apex class named <code>BiteShareCallout</code>, and an Apex Trigger on <code>Food_Donation__c</code>.
          </p>
          <div style="background:#0f172a; color:#38bdf8; padding:12px; border-radius:6px; font-family:monospace; font-size:0.8rem; max-height:200px; overflow-y:auto;">
// Apex Trigger on Food_Donation__c
trigger BiteShareWebhookTrigger on Food_Donation__c (after insert, after update) {
    for (Food_Donation__c fd : Trigger.new) {
        BiteShareCallout.syncDonationToSAP(
            fd.Id, fd.Food_Type__c, fd.Quantity__c, fd.City__c, fd.Usable_Until__c, fd.Status__c
        );
    }
}
          </div>
        </div>
      </div>
    </div>


    <!-- ============================================== -->
    <!-- SECTION 6: VOLUNTEER POOL                      -->
    <!-- ============================================== -->
    <div id="tab-volunteers" class="tab-pane" style="display:none;">
      <div class="content-card">
        <div class="card-header">
          <h2><i class="fa-solid fa-users"></i> Distributed Volunteer Pool (25 Volunteers Across 8 Metros)</h2>
        </div>
        <div class="card-body" style="padding:0; overflow-x:auto;">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Volunteer Name</th>
                <th>Operating City</th>
                <th>Contact Info</th>
                <th>Duty Status</th>
                <th>Deliveries Done</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody id="volunteersPoolTableBody"></tbody>
          </table>
        </div>
      </div>
    </div>


    <!-- ============================================== -->
    <!-- SECTION 7: NGOs DETAILS                        -->
    <!-- ============================================== -->
    <div id="tab-recipients" class="tab-pane" style="display:none;">
      <div class="content-card">
        <div class="card-header">
          <h2><i class="fa-solid fa-building-ngo"></i> Verified Recipient Places & Shelters (17 Registered)</h2>
        </div>
        <div class="card-body" style="padding:0; overflow-x:auto;">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Shelter / NGO Name</th>
                <th>City</th>
                <th>Accepted Type</th>
                <th>Max Capacity</th>
                <th>Contact Email</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody id="ngosDetailsTableBody"></tbody>
          </table>
        </div>
      </div>
    </div>


    <!-- ============================================== -->
    <!-- SECTION 8: IMPACT ANALYSIS                     -->
    <!-- ============================================== -->
    <div id="tab-analytics" class="tab-pane" style="display:none;">
      <div class="content-card">
        <div class="card-header">
          <h2><i class="fa-solid fa-chart-column" style="color:var(--primary)"></i> Surplus Food Impact Analysis</h2>
        </div>
        <div class="card-body">
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem;">
            <div style="border:1px solid var(--border); border-radius:var(--radius-md); padding:1.25rem; background:#fff;">
              <h3 style="font-size:0.9rem; color:var(--text-muted); margin-bottom:12px; font-weight:700;"><i class="fa-solid fa-utensils"></i> Social & Ecological Impact</h3>
              <div style="line-height:2.2; font-size:0.9rem;">
                <div style="display:flex; justify-content:space-between; border-bottom:1px solid #f1f5f9; padding-bottom:4px;">
                  <span>Meals Distributed:</span>
                  <strong style="color:var(--primary);" id="impact-meals">0 meals</strong>
                </div>
                <div style="display:flex; justify-content:space-between; border-bottom:1px solid #f1f5f9; padding-bottom:4px;">
                  <span>CO₂ Offset:</span>
                  <strong style="color:var(--success);" id="impact-co2">0 kg CO₂</strong>
                </div>
              </div>
            </div>

            <div style="border:1px solid var(--border); border-radius:var(--radius-md); padding:1.25rem; background:#fff;">
              <h3 style="font-size:0.9rem; color:var(--text-muted); margin-bottom:12px; font-weight:700;"><i class="fa-solid fa-city"></i> Food Rescued by City</h3>
              <div id="chart-city-content" style="font-size:0.86rem; line-height:2;"></div>
            </div>
          </div>
        </div>
      </div>
    </div>


    <!-- System Event Log -->
    <div class="content-card">
      <div class="card-header">
        <h2><i class="fa-solid fa-terminal" style="color:#38bdf8"></i> Automated System Log (Salesforce Webhooks & Dispatches)</h2>
      </div>
      <div class="card-body">
        <div class="log-terminal" id="logStream"></div>
      </div>
    </div>

  </main>

  <script>
    let CURRENT_STATE = { donations: [], recipients: [], volunteers: [], donors: [], deliveries: [], logs: [], salesforce_sync: {} };

    const d = new Date();
    d.setHours(d.getHours() + 6);
    d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
    document.getElementById('usableUntil').value = d.toISOString().slice(0, 16);

    function switchTab(tabName) {
      document.querySelectorAll('.nav-item').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.style.display = 'none');

      const el = event.currentTarget || event.target.closest('.nav-item');
      if (el) el.classList.add('active');
      document.getElementById('tab-' + tabName).style.display = 'block';
    }

    async function fetchState() {
      const res = await fetch('/api/state');
      CURRENT_STATE = await res.json();
      renderUI(CURRENT_STATE);
    }

    function onDonorChange() {
      const donorId = document.getElementById('donorSelect').value;
      const donor = CURRENT_STATE.donors.find(d => d.id === donorId);
      if (donor) {
        document.getElementById('citySelect').value = donor.city;
      }
    }

    function onCityChange() {
      const city = document.getElementById('citySelect').value;
      const matchedDonor = CURRENT_STATE.donors.find(d => d.city.toLowerCase() === city.toLowerCase());
      if (matchedDonor) {
        document.getElementById('donorSelect').value = matchedDonor.id;
      }
    }

    function renderUI(state) {
      // Donors dropdown
      const donorSel = document.getElementById('donorSelect');
      const curVal = donorSel.value;
      donorSel.innerHTML = state.donors.map(d => `<option value="${d.id}" ${d.id === curVal ? 'selected' : ''}>${d.name} (${d.city})</option>`).join('');

      // Top KPI Cards
      const totalRescued = state.donations
        .filter(d => d.status === 'COMPLETED')
        .reduce((sum, d) => sum + Number(d.quantity_kg), 0);
      document.getElementById('kpi-rescued').innerText = totalRescued + ' kg';
      document.getElementById('kpi-sf-synced').innerText = state.donations.filter(d => d.salesforce_id).length + ' record(s)';

      const availCount = state.volunteers.filter(v => v.is_available).length;
      document.getElementById('kpi-volunteers').innerText = availCount + ' / ' + state.volunteers.length;
      document.getElementById('kpi-recipients').innerText = state.recipients.filter(r => r.is_verified).length;

      // ----------------------------------------------------------------
      // 1. DONOR SECTION TABLE
      // ----------------------------------------------------------------
      document.getElementById('donorRequestsTableBody').innerHTML = state.donations.length === 0 
        ? '<tr><td colspan="9" style="text-align:center; padding:1.5rem; color:#888;">No food requests submitted yet. Use the form above or click "Push from Salesforce".</td></tr>'
        : state.donations.map(d => {
            const donor = state.donors.find(dn => dn.id === d.donor_id);
            const recip = state.recipients.find(r => r.id === d.recipient_id);
            const vol = state.volunteers.find(v => v.id === d.volunteer_id);
            const srcBadge = d.salesforce_id ? '<span class="badge-status" style="background:#e0f2fe; color:#0176d3;"><i class="fa-brands fa-salesforce"></i> Salesforce</span>' : '<span class="badge-status" style="background:#f1f5f9; color:#475569;">BiteShare Web</span>';
            return `
              <tr>
                <td><strong>${d.donation_id}</strong><br><small style="color:#64748b;">${d.salesforce_id || ''}</small></td>
                <td>${srcBadge}</td>
                <td>${donor ? donor.name : d.donor_id}</td>
                <td><span style="font-weight:700; color:var(--primary);"><i class="fa-solid fa-location-dot"></i> ${d.city}</span></td>
                <td>${d.food_type}</td>
                <td><strong>${d.quantity_kg} kg</strong></td>
                <td>${recip ? `<strong style="color:var(--recipient-accent);">${recip.name}</strong>` : '<span style="color:#888;">Matching...</span>'}</td>
                <td>${vol ? `<strong style="color:var(--volunteer-accent);"><i class="fa-solid fa-user"></i> ${vol.name}</strong>` : '<span style="color:#888;">Pending Dispatch</span>'}</td>
                <td><span class="badge-status badge-${d.status.toLowerCase()}">${d.status}</span></td>
              </tr>
            `;
          }).join('');

      // ----------------------------------------------------------------
      // 2. RECIPIENT SECTION TABLE
      // ----------------------------------------------------------------
      document.getElementById('recipientTableBody').innerHTML = state.donations.length === 0
        ? '<tr><td colspan="8" style="text-align:center; padding:1.5rem; color:#888;">No incoming food matches currently.</td></tr>'
        : state.donations.map(d => {
            const donor = state.donors.find(dn => dn.id === d.donor_id);
            const recip = state.recipients.find(r => r.id === d.recipient_id);
            const vol = state.volunteers.find(v => v.id === d.volunteer_id);

            let actionBtn = '';
            if (d.status === 'MATCHED') {
              actionBtn = `<button class="btn btn-recipient btn-sm" onclick="triggerAction('${d.donation_id}', 'accept')"><i class="fa-solid fa-check"></i> Accept Match</button>`;
            } 
            else if (d.status === 'VOL_ASSIGNED') {
              actionBtn = `
                <button class="btn btn-sm btn-disabled" disabled title="Confirm Received is locked until the volunteer arrives at the donor and confirms pickup">
                  <i class="fa-solid fa-lock"></i> Locked (Awaiting Volunteer Pickup)
                </button>
              `;
            } 
            else if (d.status === 'PICKED_UP') {
              actionBtn = `
                <button class="btn btn-success btn-sm" onclick="triggerAction('${d.donation_id}', 'deliver')" title="Food is on the way! Click to confirm safe arrival">
                  <i class="fa-solid fa-clipboard-check"></i> Confirm Received
                </button>
              `;
            } 
            else if (d.status === 'COMPLETED') {
              actionBtn = `<span style="color:var(--success); font-weight:700;"><i class="fa-solid fa-check-double"></i> Received & Confirmed</span>`;
            }

            return `
              <tr>
                <td><strong>${d.donation_id}</strong></td>
                <td><strong>${recip ? recip.name : 'Matched Shelter'}</strong></td>
                <td>${donor ? donor.name : d.city}</td>
                <td>${d.city}</td>
                <td><strong>${d.quantity_kg} kg ${d.food_type}</strong></td>
                <td>${vol ? `<strong>${vol.name}</strong> (${vol.phone})` : '<span style="color:#888;">Awaiting Dispatch</span>'}</td>
                <td><span class="badge-status badge-${d.status.toLowerCase()}">${d.status}</span></td>
                <td>${actionBtn}</td>
              </tr>
            `;
          }).join('');

      // ----------------------------------------------------------------
      // 3. VOLUNTEER SECTION TABLE
      // ----------------------------------------------------------------
      const activeOrDoneVolTasks = state.donations.filter(d => d.volunteer_id);
      document.getElementById('volunteerTasksTableBody').innerHTML = activeOrDoneVolTasks.length === 0
        ? '<tr><td colspan="7" style="text-align:center; padding:1.5rem; color:#888;">No active volunteer delivery tasks.</td></tr>'
        : activeOrDoneVolTasks.map(d => {
            const donor = state.donors.find(dn => dn.id === d.donor_id);
            const recip = state.recipients.find(r => r.id === d.recipient_id);
            const vol = state.volunteers.find(v => v.id === d.volunteer_id);

            let volBtn = '';
            if (d.status === 'VOL_ASSIGNED') {
              volBtn = `<button class="btn btn-warning btn-sm" onclick="triggerAction('${d.donation_id}', 'pickup')"><i class="fa-solid fa-box"></i> Confirm Picked Up</button>`;
            } else if (d.status === 'PICKED_UP') {
              volBtn = `<span style="color:#b45309; font-weight:700;"><i class="fa-solid fa-truck-fast"></i> In Transit (Awaiting NGO Receipt)</span>`;
            } else if (d.status === 'COMPLETED') {
              volBtn = `<span style="color:var(--success); font-weight:700;"><i class="fa-solid fa-check-double"></i> Mission Completed</span>`;
            }

            const route = `${donor ? donor.name : 'Donor'} &rarr; ${recip ? recip.name : 'Shelter'}`;

            return `
              <tr>
                <td><strong>${d.donation_id}</strong></td>
                <td><strong>${vol ? vol.name : '-'}</strong></td>
                <td>${d.city}</td>
                <td><span style="font-weight:600;">${route}</span></td>
                <td><strong>${d.quantity_kg} kg</strong></td>
                <td><span class="badge-status badge-${d.status.toLowerCase()}">${d.status}</span></td>
                <td>${volBtn}</td>
              </tr>
            `;
          }).join('');

      // ----------------------------------------------------------------
      // 4. DELIVERY TRACKING
      // ----------------------------------------------------------------
      const trackContainer = document.getElementById('deliveryTrackingContainer');
      if (state.donations.length === 0) {
        trackContainer.innerHTML = '<div style="text-align:center; padding:2rem; color:#888;">No active deliveries being tracked.</div>';
      } else {
        trackContainer.innerHTML = state.donations.map(d => {
          const donor = state.donors.find(dn => dn.id === d.donor_id);
          const recip = state.recipients.find(r => r.id === d.recipient_id);
          const vol = state.volunteers.find(v => v.id === d.volunteer_id);
          const deliv = state.deliveries.find(del => del.donation_id === d.donation_id);

          const isCreated = true;
          const isMatched = d.recipient_id !== null;
          const isAssigned = d.volunteer_id !== null;
          const isPickedUp = d.status === 'PICKED_UP' || d.status === 'COMPLETED' || d.status === 'DELIVERED';
          const isDelivered = d.status === 'COMPLETED' || d.status === 'DELIVERED';

          return `
            <div style="background:#fff; border:1px solid var(--border); border-radius:var(--radius-md); padding:1.25rem; margin-bottom:1.25rem; box-shadow:var(--shadow-sm);">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; border-bottom:1px solid #f1f5f9; padding-bottom:8px;">
                <div>
                  <strong style="font-size:1.05rem; color:var(--primary);">${d.donation_id}</strong>
                  ${d.salesforce_id ? '<span class="sf-badge" style="margin-left:6px;"><i class="fa-brands fa-salesforce"></i> ' + d.salesforce_id + '</span>' : ''}
                  <span style="margin-left:8px; font-size:0.85rem; color:#64748b;">${d.quantity_kg} kg ${d.food_type} &bull; ${d.city}</span>
                </div>
                <div>
                  <span class="badge-status badge-${d.status.toLowerCase()}">${d.status}</span>
                </div>
              </div>

              <div class="stepper-track">
                <div class="step-node ${isCreated ? 'done' : ''}">
                  <div class="step-bubble"><i class="fa-solid fa-check"></i></div>
                  <span class="step-label">1. Request Created</span>
                </div>
                <div class="step-line ${isMatched ? 'done' : ''}"></div>
                <div class="step-node ${isMatched ? 'done' : ''}">
                  <div class="step-bubble"><i class="fa-solid fa-building-ngo"></i></div>
                  <span class="step-label">2. Recipient Matched</span>
                </div>
                <div class="step-line ${isAssigned ? 'done' : ''}"></div>
                <div class="step-node ${isAssigned ? 'done' : ''}">
                  <div class="step-bubble"><i class="fa-solid fa-motorcycle"></i></div>
                  <span class="step-label">3. Volunteer Conveyed</span>
                </div>
                <div class="step-line ${isPickedUp ? 'done' : ''}"></div>
                <div class="step-node ${isPickedUp ? 'done' : ''}">
                  <div class="step-bubble"><i class="fa-solid fa-box"></i></div>
                  <span class="step-label">4. Food Picked Up</span>
                </div>
                <div class="step-line ${isDelivered ? 'done' : ''}"></div>
                <div class="step-node ${isDelivered ? 'done' : ''}">
                  <div class="step-bubble"><i class="fa-solid fa-clipboard-check"></i></div>
                  <span class="step-label">5. Delivered & Received</span>
                </div>
              </div>

              <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:10px; font-size:0.83rem; background:#f8fafc; padding:10px 14px; border-radius:var(--radius-sm);">
                <div><strong>Origin (Donor):</strong> ${donor ? donor.name : d.donor_id}</div>
                <div><strong>Destination (NGO):</strong> ${recip ? recip.name : 'Matching in progress'}</div>
                <div><strong>Delivery Volunteer:</strong> ${vol ? `${vol.name} (${vol.phone})` : 'Dispatched automatically'}</div>
                <div><strong>Tracking Code:</strong> ${deliv ? deliv.delivery_id : 'PD-Pending'}</div>
              </div>
            </div>
          `;
        }).join('');
      }

      // ----------------------------------------------------------------
      // 5. VOLUNTEERS POOL TABLE
      // ----------------------------------------------------------------
      document.getElementById('volunteersPoolTableBody').innerHTML = state.volunteers.map(v => `
        <tr>
          <td><strong>${v.id}</strong></td>
          <td><strong>${v.name}</strong></td>
          <td><i class="fa-solid fa-location-dot" style="color:#64748b;"></i> ${v.city}</td>
          <td>${v.email} | ${v.phone}</td>
          <td>${v.is_available ? '<span class="badge-status badge-completed">Available</span>' : '<span class="badge-status badge-matched">Busy on Route</span>'}</td>
          <td style="text-align:center; font-weight:700;">${v.deliveries_completed || 0}</td>
          <td>
            <button class="btn btn-outline btn-sm" onclick="toggleVolunteer('${v.id}')">Toggle Availability</button>
          </td>
        </tr>
      `).join('');

      // ----------------------------------------------------------------
      // 6. NGOs DETAILS TABLE
      // ----------------------------------------------------------------
      document.getElementById('ngosDetailsTableBody').innerHTML = state.recipients.map(r => `
        <tr>
          <td><strong>${r.id}</strong></td>
          <td><strong>${r.name}</strong></td>
          <td>${r.city}</td>
          <td>${r.food_type}</td>
          <td><strong>${r.capacity_kg} kg</strong></td>
          <td style="font-size:0.82rem;">${r.contact_email}</td>
          <td>${r.is_verified ? '<span class="badge-status badge-completed"><i class="fa-solid fa-check"></i> Verified</span>' : '<span class="badge-status badge-matched">Pending</span>'}</td>
        </tr>
      `).join('');

      // ----------------------------------------------------------------
      // 7. IMPACT ANALYSIS
      // ----------------------------------------------------------------
      document.getElementById('impact-meals').innerText = (totalRescued * 2.5).toLocaleString() + ' meals';
      document.getElementById('impact-co2').innerText = (totalRescued * 2.5).toLocaleString() + ' kg CO₂';

      const cityTotals = {};
      state.donations.filter(d => d.status === 'COMPLETED').forEach(d => {
        cityTotals[d.city] = (cityTotals[d.city] || 0) + Number(d.quantity_kg);
      });
      document.getElementById('chart-city-content').innerHTML = Object.entries(cityTotals).map(([c, kg]) => `
        <div style="display:flex; justify-content:space-between; margin-bottom:8px; border-bottom:1px solid #f1f5f9; padding-bottom:4px;">
          <span><strong>${c}</strong></span><span style="color:var(--primary); font-weight:700;">${kg} kg rescued</span>
        </div>
      `).join('') || '<span style="color:#888;">No completed deliveries recorded yet.</span>';

      // Logs stream
      document.getElementById('logStream').innerHTML = state.logs.map(l => `
        <div class="log-item">
          <span class="time">[${l.time}]</span>
          <span class="tag">[${l.category}]</span>
          <span>${l.message}</span>
          ${l.details ? `<div style="color:#94a3b8; font-size:0.75rem; margin-left:1.5rem;">${l.details}</div>` : ''}
        </div>
      `).join('');
    }

    async function handleCreateDonation(e) {
      e.preventDefault();
      const msg = document.getElementById('formMsg');
      msg.innerText = '';

      const payload = {
        food_type: document.getElementById('foodType').value,
        quantity_kg: Number(document.getElementById('quantityKg').value),
        city: document.getElementById('citySelect').value,
        usable_until: document.getElementById('usableUntil').value,
        donor_id: document.getElementById('donorSelect').value
      };

      const res = await fetch('/api/donation/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok) {
        msg.style.color = '#ef4444';
        msg.innerText = data.error;
      } else {
        msg.style.color = '#10b981';
        msg.innerText = `Created ${data.donation_id}! Matched to shelter & volunteer dispatched automatically.`;
        fetchState();
      }
    }

    async function triggerAction(donationId, action) {
      const res = await fetch('/api/donation/action', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ donation_id: donationId, action: action })
      });
      if (!res.ok) {
        const err = await res.json();
        alert(err.error || 'Action failed');
      }
      fetchState();
    }

    async function toggleVolunteer(volId) {
      await fetch('/api/volunteer/toggle', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ volunteer_id: volId })
      });
      fetchState();
    }

    async function simulateSalesforcePush() {
      const randomQty = Math.floor(Math.random() * 80) + 100;
      const cities = ["Dallas", "Houston", "Austin", "Chennai"];
      const randomCity = cities[Math.floor(Math.random() * cities.length)];
      const randomSfId = "a001200000" + Math.random().toString(36).substring(2, 9).toUpperCase();

      const sfPayload = {
        salesforce_id: randomSfId,
        food_type: "Veg",
        quantity_kg: randomQty,
        city: randomCity,
        usable_until: new Date(Date.now() + 6 * 3600 * 1000).toISOString(),
        status: "Submitted",
        source: "Salesforce Apex Callout"
      };

      const res = await fetch('/api/salesforce/webhook', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(sfPayload)
      });
      const data = await res.json();
      alert(`Success! Simulated Salesforce Apex Callout received.\nCreated: ${data.donation_id}\nSalesforce ID: ${data.salesforce_id}\nCity: ${data.city} (${data.quantity_kg} kg)`);
      fetchState();
    }

    async function resetDemo() {
      await fetch('/api/demo/reset', { method: 'POST' });
      fetchState();
    }

    fetchState();
    setInterval(fetchState, 3000);
  </script>
</body>
</html>
"""

class BiteShareHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
        elif parsed.path == "/api/state":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(STATE).encode("utf-8"))
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        data = json.loads(body) if body else {}

        # -----------------------------------------------------------------
        # SALESFORCE WEBHOOK LISTENER (Salesforce -> BiteShare Sync)
        # -----------------------------------------------------------------
        if parsed.path == "/api/salesforce/webhook":
            sf_id = data.get("salesforce_id", f"SF-{datetime.now().strftime('%M%S')}")
            qty = data.get("quantity_kg", 100)
            food_type = data.get("food_type", "Veg")
            city = data.get("city", "Dallas")
            usable_until_str = data.get("usable_until", (datetime.now() + timedelta(hours=6)).isoformat())

            don_id = f"FD-{STATE['next_donation_num']:04d}"
            STATE['next_donation_num'] += 1

            donation = {
                "donation_id": don_id,
                "salesforce_id": sf_id,
                "food_type": food_type,
                "quantity_kg": qty,
                "city": city,
                "usable_until": usable_until_str,
                "donor_id": "DNR-0001",
                "recipient_id": None,
                "volunteer_id": None,
                "status": "SUBMITTED",
                "source": "Salesforce Apex Callout",
                "created_at": datetime.now().strftime("%H:%M:%S")
            }
            add_log("SALESFORCE_INBOUND", f"Webhook received from Salesforce record {sf_id}: {qty} kg {food_type} in {city}.")

            # Automatic Matching & Dispatch
            matched_recip = None
            for r in STATE["recipients"]:
                if (r["is_verified"] and 
                    r["city"].lower() == city.lower() and 
                    r["capacity_kg"] >= qty and 
                    (r["food_type"].lower() == food_type.lower() or r["food_type"].lower() == "both")):
                    matched_recip = r
                    break

            if matched_recip:
                donation["recipient_id"] = matched_recip["id"]
                add_log("AUTO_MATCH", f"Salesforce donation {don_id} matched with {matched_recip['name']} in {city}.")

                vols_in_city = [v for v in STATE["volunteers"] if v["is_available"] and v["city"].lower() == city.lower()]
                if vols_in_city:
                    vols_in_city.sort(key=lambda v: v.get("deliveries_completed", 0))
                    chosen_vol = vols_in_city[0]

                    donation["volunteer_id"] = chosen_vol["id"]
                    donation["status"] = "VOL_ASSIGNED"
                    chosen_vol["is_available"] = False

                    del_id = f"PD-{STATE['next_delivery_num']:04d}"
                    STATE['next_delivery_num'] += 1
                    STATE["deliveries"].append({
                        "delivery_id": del_id,
                        "donation_id": don_id,
                        "pickup_time": None,
                        "delivery_time": None,
                        "status": "PENDING"
                    })
                    add_log("VOLUNTEER_DISPATCH", f"Volunteer {chosen_vol['name']} automatically dispatched for Salesforce donation {don_id}.")

            STATE["donations"].append(donation)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(donation).encode("utf-8"))

        elif parsed.path == "/api/donation/create":
            qty = data.get("quantity_kg", 0)
            food_type = data.get("food_type", "")
            city = data.get("city", "")
            usable_until_str = data.get("usable_until", "")

            if qty <= 0:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Validation Rule: Quantity must be greater than 0."}).encode("utf-8"))
                return

            if not food_type or not city:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Validation Rule: Food Type and City are required."}).encode("utf-8"))
                return

            don_id = f"FD-{STATE['next_donation_num']:04d}"
            STATE['next_donation_num'] += 1

            donor = next((d for d in STATE["donors"] if d["id"] == data.get("donor_id")), None)
            donor_name = donor["name"] if donor else "Donor Place"

            donation = {
                "donation_id": don_id,
                "food_type": food_type,
                "quantity_kg": qty,
                "city": city,
                "usable_until": usable_until_str,
                "donor_id": data.get("donor_id", "DNR-0001"),
                "recipient_id": None,
                "volunteer_id": None,
                "status": "SUBMITTED",
                "created_at": datetime.now().strftime("%H:%M:%S")
            }
            add_log("DONATION_CREATE", f"Donation {don_id} created by {donor_name} ({qty} kg {food_type} in {city}).")

            # Auto-Match
            matched_recip = None
            for r in STATE["recipients"]:
                if (r["is_verified"] and 
                    r["city"].lower() == city.lower() and 
                    r["capacity_kg"] >= qty and 
                    (r["food_type"].lower() == food_type.lower() or r["food_type"].lower() == "both")):
                    matched_recip = r
                    break

            if matched_recip:
                donation["recipient_id"] = matched_recip["id"]
                add_log("CONVEY_TO_RECIPIENT", f"ALERT conveyed to {matched_recip['name']} ({matched_recip['contact_email']}): {qty} kg {food_type} matched!")

                vols_in_city = [v for v in STATE["volunteers"] if v["is_available"] and v["city"].lower() == city.lower()]
                if vols_in_city:
                    vols_in_city.sort(key=lambda v: v.get("deliveries_completed", 0))
                    chosen_vol = vols_in_city[0]

                    donation["volunteer_id"] = chosen_vol["id"]
                    donation["status"] = "VOL_ASSIGNED"
                    chosen_vol["is_available"] = False

                    del_id = f"PD-{STATE['next_delivery_num']:04d}"
                    STATE['next_delivery_num'] += 1
                    STATE["deliveries"].append({
                        "delivery_id": del_id,
                        "donation_id": don_id,
                        "pickup_time": None,
                        "delivery_time": None,
                        "status": "PENDING"
                    })
                    add_log("CONVEY_TO_VOLUNTEER", f"DISPATCH conveyed to {chosen_vol['name']} ({chosen_vol['email']}): Pick up {don_id} & deliver to {matched_recip['name']}.")

            STATE["donations"].append(donation)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(donation).encode("utf-8"))

        elif parsed.path == "/api/donation/action":
            don_id = data.get("donation_id")
            action = data.get("action")
            donation = next((d for d in STATE["donations"] if d["donation_id"] == don_id), None)

            if not donation:
                self.send_error(404, "Donation not found")
                return

            if action == "pickup":
                donation["status"] = "PICKED_UP"
                deliv = next((deliv for deliv in STATE["deliveries"] if deliv["donation_id"] == don_id), None)
                if deliv:
                    deliv["status"] = "PICKED_UP"
                    deliv["pickup_time"] = datetime.now().isoformat()
                add_log("PICKUP_CONFIRMED", f"Volunteer confirmed pickup for {don_id}. Syncing status back to Salesforce.")

            elif action == "deliver":
                if donation.get("status") != "PICKED_UP":
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "error": "Sequence Validation Error: The recipient cannot confirm receipt until the delivery volunteer has confirmed pickup from the donor."
                    }).encode("utf-8"))
                    return

                donation["status"] = "COMPLETED"
                if donation["volunteer_id"]:
                    vol = next((v for v in STATE["volunteers"] if v["id"] == donation["volunteer_id"]), None)
                    if vol:
                        vol["is_available"] = True
                        vol["deliveries_completed"] = vol.get("deliveries_completed", 0) + 1

                deliv = next((deliv for deliv in STATE["deliveries"] if deliv["donation_id"] == don_id), None)
                if deliv:
                    deliv["status"] = "DELIVERED"
                    deliv["delivery_time"] = datetime.now().isoformat()

                add_log("DELIVERY_COMPLETE", f"Donation {don_id} confirmed delivered! Status synced to Salesforce as 'Completed'.")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(donation).encode("utf-8"))

        elif parsed.path == "/api/demo/reset":
            STATE.clear()
            STATE.update(get_initial_state())
            add_log("SYSTEM", "State reset to default values.")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
        else:
            self.send_error(404, "Not Found")

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    server_address = ('', PORT)
    httpd = socketserver.TCPServer(server_address, BiteShareHandler)
    print(f"BiteShare Platform with Salesforce Bridge running at http://localhost:{PORT}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
