# Einnahmen & Ausgaben (revenue.*, expense.*)

Einnahmen (`revenue`) sind Umsatzbelege ohne den vollen Rechnungs-Workflow –
z. B. importierte oder extern erstellte Belege. Ausgaben (`expense`) sind
Kosteneinträge/Eingangsrechnungen.

## revenue.get

**FILTER:** wie `invoice.get` (INVOICE_ID, INVOICE_NUMBER, CUSTOMER_ID,
START_DATE/END_DATE, START_PAID_DATE/END_PAID_DATE, TYPE, …)

**RESPONSE-Felder:** INVOICE_ID, TYPE, CUSTOMER_ID, CUSTOMER_NUMBER,
PROJECT_ID, CURRENCY_CODE, DELIVERY_DATE, INVOICE_TITLE, SUB_TOTAL (netto),
VAT_TOTAL (Steuer), TOTAL (brutto), ORGANIZATION, SALUTATION, FIRST_NAME,
LAST_NAME, ADDRESS, ADDRESS_2, ZIPCODE, CITY, COUNTRY_CODE, VAT_ID,
PAYMENT_TYPE, BANK_*, TEMPLATE_ID, INVOICE_NUMBER, INVOICE_DATE, DUE_DATE,
PAID_DATE, IS_CANCELED, INTROTEXT, PAYMENT_INFO, LASTUPDATE, DOCUMENT_URL,
VAT_ITEMS, ITEMS, COMMENTS

## revenue.create

**DATA – Pflicht:** `INVOICE_DATE` (`YYYY-MM-DD`), `CUSTOMER_ID`,
`SUB_TOTAL` (Nettobetrag)

**DATA – optional:** DUE_DATE, INVOICE_NUMBER, COMMENT, VAT_TOTAL,
CURRENCY_CODE, ITEMS

**RESPONSE:** STATUS, INVOICE_ID

### Beleg-Upload

Mit Dateianhang wird der Request als `multipart/form-data` gesendet mit zwei
Teilen: `httpbody` (der JSON-/XML-Request) und `document` (die Datei).

## revenue.setpaid

**DATA:** `INVOICE_ID` (Pflicht), optional `PAID_DATE`.
**RESPONSE:** STATUS, INVOICE_NUMBER

## revenue.delete

**DATA:** `INVOICE_ID` (Pflicht). **RESPONSE:** STATUS

## expense.get

**FILTER:** `INVOICE_ID`, `INVOICE_NUMBER`, `START_DATE`/`END_DATE`,
`START_PAID_DATE`/`END_PAID_DATE` (`YYYY-MM-DD`); `MONTH`/`YEAR` deprecated

**RESPONSE-Felder:** INVOICE_ID, ORGANIZATION, INVOICE_NUMBER, INVOICE_DATE,
SERVICE_PERIOD_START, SERVICE_PERIOD_END, DUE_DATE, PROJECT_ID, CUSTOMER_ID,
SUB_TOTAL, VAT_TOTAL, TOTAL, NOTE, COMMENT, VAT_ITEMS, ITEMS, PAID_DATE,
CURRENCY_CODE, CATEGORY, PAYMENT_INFO, DOCUMENT_URL

## expense.create

**DATA – Pflicht:** `INVOICE_DATE` (`YYYY-MM-DD`), `ORGANIZATION`
(Lieferant/Firma), `SUB_TOTAL` (netto)

**DATA – optional:** SERVICE_PERIOD_START, SERVICE_PERIOD_END, DUE_DATE,
PROJECT_ID, CUSTOMER_ID, INVOICE_NUMBER, COMMENT, VAT_TOTAL, ITEMS

**RESPONSE:** STATUS, INVOICE_ID

Beleg-Upload wie bei `revenue.create` (multipart mit `httpbody` + `document`).
