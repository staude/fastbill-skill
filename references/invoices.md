# Rechnungen (invoice.*, item.*)

## Lebenszyklus

```
invoice.create ──► ENTWURF ──invoice.complete──► RECHNUNG (mit Rechnungsnummer)
                     │ update/delete möglich        │ nur noch: sendbyemail/-bypost,
                     ▼                              ▼ setpaid, lock, cancel
                invoice.delete                 invoice.cancel (Storno)
```

- `invoice.create` erzeugt **immer einen Entwurf** – noch keine Rechnungsnummer.
- `invoice.complete` ist **nicht umkehrbar**; danach kein Update/Delete mehr.
- Löschen (`invoice.delete`) funktioniert nur bei Entwürfen; abgeschlossene
  Rechnungen werden storniert (`invoice.cancel`).

## invoice.get

**FILTER:** `INVOICE_ID`, `INVOICE_NUMBER`, `INVOICE_TITLE`, `CUSTOMER_ID`,
`START_DATE`/`END_DATE`, `START_DUE_DATE`/`END_DUE_DATE`,
`START_PAID_DATE`/`END_PAID_DATE`, `START_LASTUPDATE`/`END_LASTUPDATE`
(alle Daten `YYYY-MM-DD`), `TYPE` (`outgoing` = Rechnung, `draft` = Entwurf,
`credit` = Gutschrift). `MONTH`/`YEAR` sind deprecated – Datumsbereiche nutzen.

**RESPONSE-Felder:** INVOICE_ID, TYPE, CUSTOMER_ID, CUSTOMER_NUMBER,
ORGANIZATION, SALUTATION, FIRST_NAME, LAST_NAME, ADDRESS, ADDRESS_2, ZIPCODE,
CITY, COMMENT_, PAYMENT_TYPE, DAYS_FOR_PAYMENT, BANK_*, INVOICE_NUMBER,
INVOICE_TITLE, INVOICE_DATE, DUE_DATE, DELIVERY_DATE, SERVICE_PERIOD_START,
SERVICE_PERIOD_END, CASH_DISCOUNT_PERCENT, CASH_DISCOUNT_DAYS, SUB_TOTAL,
VAT_TOTAL, VAT_ITEMS, ITEMS, TOTAL, PAYMENTS, STATE, DETAILS_URL, DOCUMENT_URL

```json
{
  "SERVICE": "invoice.get",
  "FILTER": { "TYPE": "outgoing", "START_DATE": "2026-04-01", "END_DATE": "2026-06-30" },
  "LIMIT": 100, "OFFSET": 0
}
```

## invoice.create

Erzeugt einen Rechnungs**entwurf**.

**DATA – Pflicht:** `CUSTOMER_ID`, `ITEMS` (Liste, siehe unten)

**DATA – optional:** CUSTOMER_COSTCENTER_ID, CONTACT_ID, CURRENCY_CODE,
TEMPLATE_ID, TEMPLATE_HASH, INTROTEXT, INVOICE_TITLE, INVOICE_DATE,
DELIVERY_DATE, SERVICE_PERIOD_START, SERVICE_PERIOD_END, CASH_DISCOUNT_PERCENT,
CASH_DISCOUNT_DAYS, IS_GROSS (0 = Nettopreise, 1 = Bruttopreise),
CUSTOMER_ACCOUNTING_NOTE, CONTRACT_REFERENCE, CUSTOMER_ORDER_REFERENCE,
ORDER_REFERENCE, VAT_CASE

**VAT_CASE-Werte:** `standard`, `small_business_regulation` (§19 UStG),
`b2c_eu_goods`, `b2c_noneu_goods`, `b2b_eu_goods`, `b2b_eu_services`,
`b2b_noneu_goods`, `b2b_noneu_services`

**RESPONSE:** STATUS, INVOICE_ID

### ITEMS-Struktur (Positionen)

Jede Position ist ein Objekt mit:

| Feld | Beschreibung |
|---|---|
| `DESCRIPTION` | Positionstext |
| `QUANTITY` | Menge |
| `UNIT_PRICE` | Einzelpreis (netto, außer IS_GROSS=1) |
| `VAT_PERCENT` | MwSt-Satz in Prozent (z. B. 19) |
| `ARTICLE_NUMBER` | optional – Artikelnummer aus dem Katalog |
| `SORT_ORDER` | optional – Sortierung |

In Responses zusätzlich: INVOICE_ITEM_ID, INVOICE_ID, CUSTOMER_ID, VAT_VALUE,
COMPLETE_NET, COMPLETE_GROSS, CURRENCY_CODE.

```json
{
  "SERVICE": "invoice.create",
  "DATA": {
    "CUSTOMER_ID": "123456",
    "INVOICE_DATE": "2026-07-09",
    "ITEMS": [
      { "DESCRIPTION": "Beratung Juni 2026", "QUANTITY": 8, "UNIT_PRICE": 120.00, "VAT_PERCENT": 19 },
      { "DESCRIPTION": "Fahrtkosten", "QUANTITY": 1, "UNIT_PRICE": 45.00, "VAT_PERCENT": 19 }
    ]
  }
}
```

## invoice.update

Nur für Entwürfe. **DATA:** `INVOICE_ID` (Pflicht),
`DELETE_EXISTING_ITEMS` (0/1 – bei 1 werden bestehende Positionen ersetzt),
sonst alle Felder aus `invoice.create`. **RESPONSE:** STATUS

## invoice.delete

Nur für Entwürfe. **DATA:** `INVOICE_ID`. **RESPONSE:** STATUS

## invoice.complete

Entwurf → echte Rechnung, vergibt die fortlaufende Rechnungsnummer.
**Nicht umkehrbar.** **DATA:** `INVOICE_ID`. **RESPONSE:** STATUS, INVOICE_NUMBER

## invoice.cancel

Storniert eine abgeschlossene Rechnung. **DATA:** `INVOICE_ID`. **RESPONSE:** STATUS

## invoice.lock

Sperrt eine Rechnung. **DATA:** `INVOICE_ID`. **RESPONSE:** STATUS

## invoice.sendbyemail

Versendet die abgeschlossene Rechnung als PDF-Anhang.
**DATA:** `INVOICE_ID`, `RECIPIENT` (Pflicht); optional `SUBJECT`, `MESSAGE`,
`RECEIPT_CONFIRMATION` (0/1). `RECIPIENT` kann als Objekt mit `TO`/`CC`/`BCC`
angegeben werden. **RESPONSE:** STATUS

## invoice.sendbypost

Postversand (kostenpflichtig). **DATA:** `INVOICE_ID`.
**RESPONSE:** STATUS, REMAINING_CREDITS

## invoice.setpaid

Markiert als bezahlt. **DATA:** `INVOICE_ID` (Pflicht); optional `PAID_DATE`
(`YYYY-MM-DD`), `PAYMENT_METHOD` (frei, z. B. "PayPal", "Überweisung").
**RESPONSE:** STATUS, INVOICE_NUMBER

## item.get / item.delete

- `item.get`: Positionen einer Rechnung – **FILTER:** `INVOICE_ID` (Pflicht)
- `item.delete`: einzelne Position löschen – **DATA:** `INVOICE_ITEM_ID` (Pflicht)
