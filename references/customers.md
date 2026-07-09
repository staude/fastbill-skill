# Kunden & Ansprechpartner (customer.*, contact.*)

## customer.get

Kunden abfragen. Ohne Filter: 10 Kunden, mit `LIMIT` bis 100.

**FILTER:** `CUSTOMER_ID`, `CUSTOMER_NUMBER`, `COUNTRY_CODE` (ISO 3166 ALPHA-2),
`CITY`, `TERM` (Volltextsuche über ORGANIZATION, FIRST_NAME, LAST_NAME, ADDRESS,
ADDRESS_2, ZIPCODE, EMAIL, TAGS)

**RESPONSE-Felder:** CUSTOMER_ID, CUSTOMER_NUMBER, DAYS_FOR_PAYMENT, CREATED,
PAYMENT_TYPE, BANK_NAME, BANK_ACCOUNT_NUMBER, BANK_CODE, BANK_ACCOUNT_OWNER,
BANK_IBAN, BANK_BIC, BANK_ACCOUNT_MANDATE_REFERENCE, SHOW_PAYMENT_NOTICE,
ACCOUNT_RECEIVABLE, CUSTOMER_TYPE, ORGANIZATION, POSITION, ACADEMIC_DEGREE,
SALUTATION, FIRST_NAME, LAST_NAME, ADDRESS, ADDRESS_2, ZIPCODE, CITY,
COUNTRY_CODE, SECONDARY_ADDRESS, PHONE, PHONE_2, FAX, MOBILE, EMAIL, WEBSITE,
VAT_ID, CURRENCY_CODE, LASTUPDATE, BUYER_REFERENCE, GLN, TAGS,
DOCUMENT_HISTORY_URL

```json
{ "SERVICE": "customer.get", "FILTER": { "TERM": "Musterfirma" }, "LIMIT": 100 }
```

## customer.create

Neuen Kunden anlegen.

**DATA – Pflichtfelder:**

| Feld | Bedingung |
|---|---|
| `CUSTOMER_TYPE` | immer – `business` oder `consumer` |
| `ORGANIZATION` | Pflicht bei `business` |
| `LAST_NAME` | Pflicht bei `consumer` (`FIRST_NAME` optional) |
| `BANK_NAME`, `BANK_IBAN` | Pflicht bei `PAYMENT_TYPE = 2` (Lastschrift) |

**DATA – optional:** CUSTOMER_NUMBER, POSITION, ACADEMIC_DEGREE,
SALUTATION (`mr` | `mrs` | `family` | leer), ADDRESS, ADDRESS_2,
SECONDARY_ADDRESS, ZIPCODE, CITY, COUNTRY_CODE (ISO ALPHA-2), PHONE, PHONE_2,
FAX, MOBILE, EMAIL, WEBSITE, ACCOUNT_RECEIVABLE, CURRENCY_CODE, VAT_ID,
DAYS_FOR_PAYMENT (int), SHOW_PAYMENT_NOTICE (0/1), BANK_CODE,
BANK_ACCOUNT_NUMBER, BANK_ACCOUNT_OWNER, BANK_BIC,
BANK_ACCOUNT_MANDATE_REFERENCE, BUYER_REFERENCE, GLN (GS1-validiert), TAGS

**PAYMENT_TYPE-Werte:** 1 Überweisung, 2 Lastschrift, 3 Bar, 4 PayPal,
5 Vorkasse, 6 Kreditkarte

**RESPONSE:** STATUS, CUSTOMER_ID, CUSTOMER_NUMBER

```json
{
  "SERVICE": "customer.create",
  "DATA": {
    "CUSTOMER_TYPE": "business",
    "ORGANIZATION": "Musterfirma GmbH",
    "SALUTATION": "mr",
    "FIRST_NAME": "Max",
    "LAST_NAME": "Muster",
    "ADDRESS": "Musterstr. 1",
    "ZIPCODE": "10115",
    "CITY": "Berlin",
    "COUNTRY_CODE": "DE",
    "EMAIL": "buchhaltung@musterfirma.de",
    "VAT_ID": "DE123456789",
    "PAYMENT_TYPE": 1,
    "DAYS_FOR_PAYMENT": 14
  }
}
```

## customer.update

Wie `customer.create`, zusätzlich Pflichtfeld `CUSTOMER_ID` in `DATA`.
**RESPONSE:** STATUS, CUSTOMER_ID

## customer.delete

`DATA.CUSTOMER_ID` (Pflicht). **RESPONSE:** STATUS

## contact.get

Ansprechpartner eines Kunden abfragen.

**FILTER:** `CUSTOMER_ID`, `CUSTOMER_NUMBER`, `CONTACT_ID`, `TERM`

**RESPONSE-Felder:** CONTACT_ID, CUSTOMER_ID, ORGANIZATION, ACADEMIC_DEGREE,
POSITION, SALUTATION, FIRST_NAME, LAST_NAME, ADDRESS, ADDRESS_2, ZIPCODE, CITY,
COUNTRY_CODE, SECONDARY_ADDRESS, PHONE, PHONE_2, FAX, MOBILE, EMAIL, VAT_ID,
CURRENCY_CODE, CREATED, TAGS

## contact.create

**DATA:** `CUSTOMER_ID` (Pflicht) + dieselben Personen-/Adressfelder wie oben.
**RESPONSE:** STATUS, CONTACT_ID

## contact.update

**DATA:** `CUSTOMER_ID` + `CONTACT_ID` (Pflicht) + zu ändernde Felder.
**RESPONSE:** STATUS, CONTACT_ID

## contact.delete

**DATA:** `CUSTOMER_ID` + `CONTACT_ID` (beide Pflicht). **RESPONSE:** STATUS
