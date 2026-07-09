# Dokumente, Vorlagen & Webhooks (document.*, template.get, webhook.*)

## document.get

Dokumente und Ordner der Dokumentenablage abfragen.

**FILTER:** `FOLDER_ID`

**RESPONSE:** `FOLDERS` (Ordnerliste), `DOCUMENTS` (Dokumentliste)

## document.create

Dokument in den Posteingang einliefern.

**DATA – Pflicht:** `TYPE`, `TITLE`, `DATE` (`YYYY-MM-DD`)
**DATA – optional:** `NOTE`

Mit Dateianhang: POST als `multipart/form-data` mit zwei Teilen –
`httpbody` (JSON-/XML-Request) und `document` (Datei).

**RESPONSE:** STATUS, DOCUMENT_ID

## template.get

Druck-/Layoutvorlagen abfragen (keine FILTER-Parameter).

**RESPONSE-Felder:** TEMPLATE_ID, TEMPLATE_NAME, TEMPLATE_HASH

Achtung: `TEMPLATE_ID` ist **nicht stabil** – sie ändert sich bei jeder
Änderung an der Vorlage. Für dauerhafte Referenzen (z. B. in `invoice.create`
oder `recurring.create`) `TEMPLATE_HASH` verwenden.

## Webhooks (nur Pro- und Premium-Tarif)

### Verfügbare Events

`customer.created`, `customer.updated`, `customer.deleted`,
`invoice.created`, `invoice.completed`, `invoice.canceled`,
`estimate.created`, `estimate.updated`,
`contact.created`, `contact.updated`, `contact.deleted`

### webhook.get

Alle registrierten Webhooks. **RESPONSE:** WEBHOOK_ID, ENDPOINT,
TYPE (derzeit nur `url`), EVENTS (kommasepariert)

### webhook.create

**DATA – Pflicht:**

| Feld | Wert |
|---|---|
| `TYPE` | `url` (E-Mail noch nicht implementiert) |
| `ENDPOINT` | öffentlich erreichbare HTTPS-URL |
| `EVENTS` | Events, kommasepariert |

**RESPONSE:** STATUS, WEBHOOK_ID

```json
{
  "SERVICE": "webhook.create",
  "DATA": {
    "TYPE": "url",
    "ENDPOINT": "https://example.com/hooks/fastbill",
    "EVENTS": "invoice.completed,invoice.canceled"
  }
}
```

### webhook.delete

**DATA:** `WEBHOOK_ID` (Pflicht). **RESPONSE:** STATUS

### Benachrichtigungs-Payload

FastBill schickt JSON an den Endpoint:

```json
{
  "id": "…",
  "type": "invoice.completed",
  "created": "…",
  "invoice": { "INVOICE_ID": "…", "INVOICE_NUMBER": "…", "CUSTOMER_ID": "…", "TOTAL": "…", "…": "…" }
}
```

Je nach Event enthält das Objekt `customer`, `invoice` oder `estimate` mit den
vollen Entitätsfeldern. Der Empfänger-Endpoint sollte schnell mit HTTP 200
antworten und die Verarbeitung asynchron machen.
