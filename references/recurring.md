# Wiederkehrende Rechnungen (recurring.*)

Abo-/Dauerrechnungen: FastBill erzeugt nach Zeitplan automatisch Rechnungen
(als Entwurf oder direkt abgeschlossen, je nach `OUTPUT_TYPE`).

## recurring.get

**FILTER:** `INVOICE_ID`

**RESPONSE-Felder:** INVOICE_ID, TYPE, CUSTOMER_ID, CUSTOMER_COSTCENTER_ID,
CURRENCY_CODE, TEMPLATE_ID, INTROTEXT, INVOICE_NUMBER, PAID_DATE,
IS_CANCELED (0/1), INVOICE_DATE, DUE_DATE, DELIVERY_DATE,
CASH_DISCOUNT_PERCENT, CASH_DISCOUNT_DAYS, SUB_TOTAL, VAT_TOTAL, TOTAL,
VAT_ITEMS, ITEMS

## recurring.create

**DATA – Pflicht:**

| Feld | Werte |
|---|---|
| `CUSTOMER_ID` | Kundennummer |
| `START_DATE` | erster Lauf, `YYYY-MM-DD` |
| `FREQUENCY` | `weekly`, `2 weeks`, `4 weeks`, `monthly`, `2 months`, `3 months`, `6 months`, `yearly`, `2 years` |
| `OUTPUT_TYPE` | `draft` (Entwurf) oder `outgoing` (direkt abgeschlossen) |
| `ITEMS` | Positionsliste (Struktur siehe `references/invoices.md`) |

**DATA – optional:** CUSTOMER_COSTCENTER_ID, CURRENCY_CODE, TEMPLATE_ID,
TEMPLATE_HASH, INTROTEXT, `OCCURENCES` (Anzahl Läufe, 0 = unbegrenzt;
Achtung: API-Schreibweise mit einem R), `EMAIL_NOTIFY` (0/1), DELIVERY_DATE,
CASH_DISCOUNT_PERCENT, CASH_DISCOUNT_DAYS, VAT_CASE

**RESPONSE:** STATUS, INVOICE_ID

```json
{
  "SERVICE": "recurring.create",
  "DATA": {
    "CUSTOMER_ID": "123456",
    "START_DATE": "2026-08-01",
    "FREQUENCY": "monthly",
    "OUTPUT_TYPE": "draft",
    "OCCURENCES": 0,
    "ITEMS": [
      { "DESCRIPTION": "Hosting-Paket Pro", "QUANTITY": 1, "UNIT_PRICE": 29.00, "VAT_PERCENT": 19 }
    ]
  }
}
```

Empfehlung: `OUTPUT_TYPE: "draft"` verwenden, solange der Nutzer nicht explizit
den vollautomatischen Abschluss will – abgeschlossene Rechnungen sind nicht
rückholbar.

## recurring.update

**DATA:** `INVOICE_ID` (Pflicht), `DELETE_EXISTING_ITEMS` (0/1), sonst Felder
aus `recurring.create`. **RESPONSE:** STATUS

## recurring.delete

**DATA:** `INVOICE_ID` (Pflicht). **RESPONSE:** STATUS
