/**
 * @description Central Automation Engine for BiteShare Surplus Food Sharing Platform.
 * Implements Flow 1 (Match Recipient), Flow 2 (Assign Volunteer), Flow 3 (Complete Donation),
 * and the Sequential Delivery Integrity Lock.
 */
public with sharing class BiteShareEngine {

    /**
     * @description Flow 1: Automatically match incoming food donation to verified recipient shelter
     */
    public static void autoMatchRecipient(List<Food_Donation__c> donations) {
        Set<String> cities = new Set<String>();
        for (Food_Donation__c d : donations) {
            if (d.City__c != null) {
                cities.add(d.City__c);
            }
        }

        // Query verified recipient shelters with available capacity in matching cities
        List<Recipient_Organization__c> recips = [
            SELECT Id, Name, City__c, Food_Type_Accepted__c, Capacity_kg__c, Contact_Email__c
            FROM Recipient_Organization__c
            WHERE Verified__c = true AND City__c IN :cities
            ORDER BY Capacity_kg__c DESC
        ];

        for (Food_Donation__c d : donations) {
            if (d.Recipient__c == null) {
                for (Recipient_Organization__c r : recips) {
                    if (r.City__c.equalsIgnoreCase(d.City__c) && r.Capacity_kg__c >= d.Quantity_kg__c) {
                        Boolean typeMatch = (r.Food_Type_Accepted__c == 'Both' || r.Food_Type_Accepted__c == d.Food_Type__c);
                        if (typeMatch) {
                            d.Recipient__c = r.Id;
                            d.Status__c = 'Matched';
                            break;
                        }
                    }
                }
            }
        }
    }

    /**
     * @description Flow 2: Assign available volunteer when donation is Accepted or Matched
     */
    public static void assignVolunteerAndCreateDelivery(List<Food_Donation__c> donations) {
        Set<String> cities = new Set<String>();
        for (Food_Donation__c d : donations) {
            if (d.City__c != null && d.Volunteer__c == null) {
                cities.add(d.City__c);
            }
        }

        List<Volunteer__c> availableVols = [
            SELECT Id, Name, City__c, Available__c, Deliveries_Completed__c
            FROM Volunteer__c
            WHERE Available__c = true AND City__c IN :cities
            ORDER BY Deliveries_Completed__c ASC
        ];

        Map<String, List<Volunteer__c>> volsByCity = new Map<String, List<Volunteer__c>>();
        for (Volunteer__c v : availableVols) {
            String cityKey = v.City__c.toLowerCase();
            if (!volsByCity.containsKey(cityKey)) {
                volsByCity.put(cityKey, new List<Volunteer__c>());
            }
            volsByCity.get(cityKey).add(v);
        }

        List<Pickup_Delivery__c> deliveriesToInsert = new List<Pickup_Delivery__c>();
        List<Volunteer__c> volsToUpdate = new List<Volunteer__c>();

        for (Food_Donation__c d : donations) {
            String cityKey = d.City__c != null ? d.City__c.toLowerCase() : '';
            if (volsByCity.containsKey(cityKey) && !volsByCity.get(cityKey).isEmpty()) {
                Volunteer__c chosenVol = volsByCity.get(cityKey).remove(0);
                d.Volunteer__c = chosenVol.Id;
                d.Status__c = 'Volunteer Assigned';

                chosenVol.Available__c = false;
                volsToUpdate.add(chosenVol);

                deliveriesToInsert.add(new Pickup_Delivery__c(
                    Food_Donation__c = d.Id,
                    Status__c = 'Pending'
                ));
            }
        }

        if (!volsToUpdate.isEmpty()) {
            update volsToUpdate;
        }
        if (!deliveriesToInsert.isEmpty()) {
            insert deliveriesToInsert;
        }
    }

    /**
     * @description Flow 3: Complete donation and release volunteer back to pool
     */
    public static void handleDonationCompletion(List<Food_Donation__c> donations, Map<Id, Food_Donation__c> oldMap) {
        Set<Id> volIdsToRelease = new Set<Id>();
        for (Food_Donation__c d : donations) {
            Food_Donation__c oldDon = oldMap.get(d.Id);
            if ((d.Status__c == 'Delivered' || d.Status__c == 'Completed') && oldDon.Status__c != 'Delivered' && oldDon.Status__c != 'Completed') {
                d.Status__c = 'Completed';
                if (d.Volunteer__c != null) {
                    volIdsToRelease.add(d.Volunteer__c);
                }
            }
        }

        if (!volIdsToRelease.isEmpty()) {
            List<Volunteer__c> vols = [SELECT Id, Available__c, Deliveries_Completed__c FROM Volunteer__c WHERE Id IN :volIdsToRelease];
            for (Volunteer__c v : vols) {
                v.Available__c = true;
                v.Deliveries_Completed__c = (v.Deliveries_Completed__c != null ? v.Deliveries_Completed__c : 0) + 1;
            }
            update vols;
        }
    }

    /**
     * @description Sequential Delivery Lock: Prevents confirming delivery if food was never picked up!
     */
    public static void enforceSequentialIntegrity(List<Food_Donation__c> donations, Map<Id, Food_Donation__c> oldMap) {
        for (Food_Donation__c d : donations) {
            Food_Donation__c oldDon = oldMap.get(d.Id);
            if (d.Status__c == 'Delivered' || d.Status__c == 'Completed') {
                if (oldDon.Status__c != 'Picked Up' && oldDon.Status__c != 'Delivered' && oldDon.Status__c != 'Completed') {
                    d.addError('Sequence Validation Error: The recipient cannot confirm delivery until the assigned volunteer has confirmed food pickup from the donor.');
                }
            }
        }
    }
}
