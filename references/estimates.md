# Angebote (estimate.*)

## estimate.get

**FILTER:** `CUSTOMER_ID`, `ESTIMATE_ID`, `ESTIMATE_NUMBER`,
`START_DATE`/`END_DATE` (`YYYY-MM-DD`)

**RESPONSE-Felder:** ESTIMATE_ID, STATE (Statuscodes a–f), CUSTOMER_ID,
CUSTOMER_NUMBER, ORGANIZATION, SALUTATION, FIRST_NAME, LAST_NAME, ADDRESS,
ADDRESS_2, ZIPCODE, CITY, PAYMENT_TYPE, BANK_*, COUNTRY_CODE, VAT_ID,
CURRENCY_CODE, TEMPLATE_ID, ESTIMATE_NUMBER, INTROTEXT, ESTIMATE_DATE,
DUE_DATE, SUB_TOTAL, VAT_TOTAL, VAT_ITEMS, ITEMS, TOTAL, DOCUMENT_URL

## estimate.create

**DATA – Pflicht:** `CUSTOMER_ID`, `ITEMS` (gleiche Positionsstruktur wie bei
Rechnungen, siehe `references/invoices.md`)

**DATA – optional:** `TEMPLATE_ID`, `TEMPLATE_HASH`

**RESPONSE:** STATUS, ESTIMATE_ID

```json
{
  "SERVICE": "estimate.create",
  "DATA": {
    "CUSTOMER_ID": "123456",
    "ITEMS": [
      { "DESCRIPTION": "Website-Relaunch", "QUANTITY": 1, "UNIT_PRICE": 4800.00, "VAT_PERCENT": 19 }
    ]
  }
}
```

## estimate.sendbyemail

Versand als PDF-Anhang. **DATA:** `ESTIMATE_ID`, `RECIPIENT` (Pflicht);
optional `SUBJECT`, `MESSAGE`, `RECEIPT_CONFIRMATION` (0/1). **RESPONSE:** STATUS

## estimate.createinvoice

Erzeugt aus dem Angebot einen **Rechnungsentwurf**.
**DATA:** `ESTIMATE_ID` (Pflicht). **RESPONSE:** INVOICE_ID
Danach normaler Rechnungs-Lebenszyklus (`invoice.complete` etc.).

## estimate.delete

**DATA:** `ESTIMATE_ID` (Pflicht). **RESPONSE:** STATUS
