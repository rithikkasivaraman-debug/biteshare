// Apex Class to send food donation events to the live BiteShare SAP engine
public class BiteShareCallout {
    private static final String ENDPOINT_URL = 'https://theaters-eric-portable-recipient.trycloudflare.com/api/salesforce/webhook';

    @future(callout=true)
    public static void syncDonationToSAP(String donationId, String foodType, Decimal quantity, String city, Datetime usableUntil, String status) {
        try {
            HttpRequest req = new HttpRequest();
            req.setEndpoint(ENDPOINT_URL);
            req.setMethod('POST');
            req.setHeader('Content-Type', 'application/json');

            Map<String, Object> payload = new Map<String, Object>{
                'salesforce_id' => donationId,
                'food_type'     => foodType,
                'quantity_kg'   => quantity,
                'city'          => city,
                'usable_until'  => usableUntil != null ? usableUntil.formatGmt('yyyy-MM-dd\'T\'HH:mm:ss\'Z\'') : null,
                'status'        => status,
                'source'        => 'Salesforce Lightning App'
            };

            req.setBody(JSON.serialize(payload));
            Http http = new Http();
            HttpResponse res = http.send(req);

            System.debug('BiteShare SAP Response: ' + res.getStatusCode() + ' - ' + res.getBody());
        } catch (Exception ex) {
            System.debug('BiteShare Callout Error: ' + ex.getMessage());
        }
    }
}
