trigger BiteShareWebhookTrigger on Food_Donation__c (after insert, after update) {
    for (Food_Donation__c fd : Trigger.new) {
        // Prevent recursive triggers on status echoes
        BiteShareCallout.syncDonationToSAP(
            fd.Id,
            fd.Food_Type__c,
            fd.Quantity__c,
            fd.City__c,
            fd.Usable_Until__c,
            fd.Status__c
        );
    }
}
