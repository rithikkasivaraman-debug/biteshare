"""
BiteShare Surplus Food Sharing Application - Multi-Place & Distributed Volunteer Test Suite
Verifies that:
1. Multiple cities/places are supported.
2. Multiple volunteers in the same city are assigned dynamically without bottlenecking.
3. Once a volunteer is assigned to a pickup, subsequent donations in that same city go to the NEXT available volunteer.
"""
from datetime import datetime, timedelta, timezone

class BiteShareEngine:
    def __init__(self):
        # 10 Donors across cities
        self.donors = [
            {"id": "DNR-0001", "name": "Royal Palace Catering", "city": "Dallas", "donor_type": "Event"},
            {"id": "DNR-0002", "name": "Grand Plaza Hotel", "city": "Dallas", "donor_type": "Hotel"},
            {"id": "DNR-0003", "name": "Bayou City Banquets", "city": "Houston", "donor_type": "Event"},
            {"id": "DNR-0004", "name": "Houston Galleria Catering", "city": "Houston", "donor_type": "Restaurant"},
            {"id": "DNR-0005", "name": "Austin Tech Center Cafe", "city": "Austin", "donor_type": "College"}
        ]
        
        # 17 Recipients across cities
        self.recipients = [
            {"id": "RCP-0001", "name": "Hope Community Shelter", "city": "Dallas", "food_type": "Both", "capacity_kg": 500, "is_verified": True},
            {"id": "RCP-0002", "name": "Green Earth Food Bank", "city": "Dallas", "food_type": "Veg", "capacity_kg": 300, "is_verified": True},
            {"id": "RCP-0003", "name": "North Texas Food Rescue", "city": "Dallas", "food_type": "Both", "capacity_kg": 800, "is_verified": True},
            {"id": "RCP-0004", "name": "Houston Food Mission", "city": "Houston", "food_type": "Both", "capacity_kg": 650, "is_verified": True},
            {"id": "RCP-0005", "name": "Star of Hope Haven", "city": "Houston", "food_type": "Veg", "capacity_kg": 400, "is_verified": True},
            {"id": "RCP-0006", "name": "Austin Community Kitchen", "city": "Austin", "food_type": "Both", "capacity_kg": 450, "is_verified": True}
        ]

        # 25 Volunteers (multiple per city)
        self.volunteers = [
            # Dallas (4 volunteers)
            {"id": "VOL-0001", "name": "Alex Rivera", "city": "Dallas", "is_available": True, "deliveries_completed": 0},
            {"id": "VOL-0002", "name": "Samira Khan", "city": "Dallas", "is_available": True, "deliveries_completed": 0},
            {"id": "VOL-0003", "name": "David Chen", "city": "Dallas", "is_available": True, "deliveries_completed": 0},
            {"id": "VOL-0004", "name": "Maria Santos", "city": "Dallas", "is_available": True, "deliveries_completed": 0},
            # Houston (3 volunteers)
            {"id": "VOL-0005", "name": "Liam Johnson", "city": "Houston", "is_available": True, "deliveries_completed": 0},
            {"id": "VOL-0006", "name": "Priya Patel", "city": "Houston", "is_available": True, "deliveries_completed": 0},
            {"id": "VOL-0007", "name": "Marcus Williams", "city": "Houston", "is_available": True, "deliveries_completed": 0},
            # Austin (2 volunteers)
            {"id": "VOL-0008", "name": "Carlos Diaz", "city": "Austin", "is_available": True, "deliveries_completed": 0},
            {"id": "VOL-0009", "name": "Chloe Bennett", "city": "Austin", "is_available": True, "deliveries_completed": 0}
        ]
        
        self.donations = []
        self.deliveries = []
        self._next_donation_num = 1
        self._next_delivery_num = 1

    def create_donation(self, food_type, quantity_kg, city, usable_hours_ahead=6, donor_id=None):
        don_id = f"FD-{self._next_donation_num:04d}"
        self._next_donation_num += 1

        donation = {
            "donation_id": don_id,
            "food_type": food_type,
            "quantity_kg": quantity_kg,
            "city": city,
            "usable_until": datetime.now(timezone.utc) + timedelta(hours=usable_hours_ahead),
            "donor_id": donor_id,
            "recipient_id": None,
            "volunteer_id": None,
            "status": "SUBMITTED"
        }

        # Flow 1: Recipient Matching
        matched = next((r for r in self.recipients if r["is_verified"] and r["city"].lower() == city.lower() and r["capacity_kg"] >= quantity_kg and (r["food_type"].lower() == food_type.lower() or r["food_type"].lower() == "both")), None)
        if matched:
            donation["recipient_id"] = matched["id"]
            donation["status"] = "MATCHED"

        self.donations.append(donation)
        return donation

    def accept_donation(self, donation_id):
        donation = next(d for d in self.donations if d["donation_id"] == donation_id)
        
        # Pick available volunteer in same city with least completed deliveries
        vols_in_city = [v for v in self.volunteers if v["is_available"] and v["city"].lower() == donation["city"].lower()]
        vols_in_city.sort(key=lambda v: v["deliveries_completed"])

        if vols_in_city:
            chosen_vol = vols_in_city[0]
            donation["volunteer_id"] = chosen_vol["id"]
            donation["status"] = "VOL_ASSIGNED"
            chosen_vol["is_available"] = False

            del_id = f"PD-{self._next_delivery_num:04d}"
            self._next_delivery_num += 1
            self.deliveries.append({
                "delivery_id": del_id,
                "donation_id": donation_id,
                "status": "PENDING"
            })
            return chosen_vol
        return None

    def complete_donation(self, donation_id):
        donation = next(d for d in self.donations if d["donation_id"] == donation_id)
        donation["status"] = "COMPLETED"
        if donation["volunteer_id"]:
            vol = next(v for v in self.volunteers if v["id"] == donation["volunteer_id"])
            vol["is_available"] = True
            vol["deliveries_completed"] += 1


def run_tests():
    print("=" * 65)
    print(" MULTI-PLACE & DISTRIBUTED VOLUNTEER VERIFICATION SUITE")
    print("=" * 65)

    engine = BiteShareEngine()

    print("\n--- Test 1: Multiple Concurrent Donations in Dallas ---")
    # Donation 1 in Dallas
    d1 = engine.create_donation("Veg", 100, "Dallas")
    vol1 = engine.accept_donation(d1["donation_id"])
    print(f"Donation 1 (Dallas): Assigned to Volunteer {vol1['name']} ({vol1['id']})")
    assert vol1["id"] == "VOL-0001", "Expected Alex Rivera"

    # Donation 2 in Dallas (Alex is busy, so it should pick Samira Khan!)
    d2 = engine.create_donation("Both", 150, "Dallas")
    vol2 = engine.accept_donation(d2["donation_id"])
    print(f"Donation 2 (Dallas): Assigned to Volunteer {vol2['name']} ({vol2['id']})")
    assert vol2["id"] == "VOL-0002", "Expected Samira Khan (not Alex Rivera!)"

    # Donation 3 in Dallas (Alex and Samira busy -> picks David Chen!)
    d3 = engine.create_donation("Veg", 80, "Dallas")
    vol3 = engine.accept_donation(d3["donation_id"])
    print(f"Donation 3 (Dallas): Assigned to Volunteer {vol3['name']} ({vol3['id']})")
    assert vol3["id"] == "VOL-0003", "Expected David Chen"

    print("\n--- Test 2: Concurrent Donations in Houston & Austin ---")
    # Donation in Houston (picks Liam Johnson)
    dH = engine.create_donation("Both", 200, "Houston")
    volH = engine.accept_donation(dH["donation_id"])
    print(f"Donation in Houston: Assigned to Volunteer {volH['name']} ({volH['id']})")
    assert volH["id"] == "VOL-0005", "Expected Liam Johnson in Houston"

    # Donation in Austin (picks Carlos Diaz)
    dA = engine.create_donation("Both", 120, "Austin")
    volA = engine.accept_donation(dA["donation_id"])
    print(f"Donation in Austin:  Assigned to Volunteer {volA['name']} ({volA['id']})")
    assert volA["id"] == "VOL-0008", "Expected Carlos Diaz in Austin"

    print("\n--- Test 3: Delivery Completion & Workload Balance ---")
    # Complete Donation 1 (frees Alex Rivera)
    engine.complete_donation(d1["donation_id"])
    vol_alex = next(v for v in engine.volunteers if v["id"] == "VOL-0001")
    assert vol_alex["is_available"] == True, "Alex should be available again"
    assert vol_alex["deliveries_completed"] == 1, "Alex should have 1 completed delivery"
    print(f"Donation 1 Completed: Volunteer {vol_alex['name']} freed (Deliveries: {vol_alex['deliveries_completed']})")

    print("\n" + "=" * 65)
    print(" ALL MULTI-PLACE & MULTI-VOLUNTEER TESTS PASSED!")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
