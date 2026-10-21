/**
 * @description Master trigger orchestrating the BiteShare Surplus Food Sharing lifecycle.
 */
trigger FoodDonationTrigger on Food_Donation__c (before insert, before update, after insert, after update) {

    if (Trigger.isBefore && Trigger.isInsert) {
        BiteShareEngine.autoMatchRecipient(Trigger.new);
    }

    if (Trigger.isBefore && Trigger.isUpdate) {
        BiteShareEngine.enforceSequentialIntegrity(Trigger.new, Trigger.oldMap);
        BiteShareEngine.handleDonationCompletion(Trigger.new, Trigger.oldMap);
    }

    if (Trigger.isAfter && Trigger.isInsert) {
        BiteShareEngine.assignVolunteerAndCreateDelivery(Trigger.new);
    }

    if (Trigger.isAfter && Trigger.isUpdate) {
        List<Food_Donation__c> needsVolunteer = new List<Food_Donation__c>();
        for (Food_Donation__c d : Trigger.new) {
            Food_Donation__c oldDon = Trigger.oldMap.get(d.Id);
            if (d.Status__c == 'Accepted' && oldDon.Status__c != 'Accepted' && d.Volunteer__c == null) {
                needsVolunteer.add(d);
            }
        }
        if (!needsVolunteer.isEmpty()) {
            BiteShareEngine.assignVolunteerAndCreateDelivery(needsVolunteer);
        }
    }
}
