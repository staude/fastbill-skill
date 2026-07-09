# Projekte & Zeiterfassung (project.*, time.*)

## project.get

**FILTER:** `PROJECT_ID`, `CUSTOMER_ID`

**RESPONSE-Felder:** PROJECT_ID, PROJECT_NAME, CUSTOMER_ID,
CUSTOMER_COSTCENTER_ID, HOUR_PRICE, CURRENCY_CODE, VAT_PERCENT, START_DATE,
END_DATE, TASKS (Liste der Aufgaben)

## project.create

**DATA – Pflicht:** `PROJECT_NAME`, `CUSTOMER_ID`

**DATA – optional:** CUSTOMER_COSTCENTER_ID, HOUR_PRICE, CURRENCY_CODE,
VAT_PERCENT, START_DATE, END_DATE (`YYYY-MM-DD`)

**RESPONSE:** STATUS

## project.update

**DATA:** `PROJECT_ID` (Pflicht) + Felder aus `project.create`. **RESPONSE:** STATUS

## project.delete

**DATA:** `PROJECT_ID` (Pflicht). **RESPONSE:** STATUS

## time.get

**FILTER:** `CUSTOMER_ID`, `PROJECT_ID`, `TASK_ID`, `TIME_ID`,
`START_DATE`/`END_DATE`, `DATE` (alle `YYYY-MM-DD`)

**RESPONSE-Felder:** TIME_ID, CUSTOMER_ID, PROJECT_ID, INVOICE_ID, DATE,
START_TIME, END_TIME, MINUTES, BILLABLE_MINUTES, COMMENT

## time.create

**DATA – Pflicht:** `CUSTOMER_ID`, `PROJECT_ID`, `START_TIME`
(Format `YYYY-MM-DD hh:mm:ss`)

**DATA – optional:** DATE, TASK_ID, END_TIME, MINUTES, BILLABLE_MINUTES, COMMENT

**RESPONSE:** STATUS, TIME_ID

```json
{
  "SERVICE": "time.create",
  "DATA": {
    "CUSTOMER_ID": "123456",
    "PROJECT_ID": "789",
    "START_TIME": "2026-07-09 09:00:00",
    "END_TIME": "2026-07-09 11:30:00",
    "BILLABLE_MINUTES": 150,
    "COMMENT": "Konzeption Landingpage"
  }
}
```

## time.update

**DATA:** `TIME_ID` (Pflicht) + Felder aus `time.create`.
**RESPONSE:** TIME_ID, COMMENT

## time.delete

**DATA:** `TIME_ID` (Pflicht). **RESPONSE:** STATUS
