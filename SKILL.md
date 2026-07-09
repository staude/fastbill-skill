---
name: fastbill
description: >-
  Arbeiten mit der FastBill-API (my.fastbill.com) – Rechnungen, Kunden, Angebote,
  wiederkehrende Rechnungen, Einnahmen, Ausgaben, Artikel, Projekte, Zeiterfassung,
  Dokumente und Webhooks. Verwende diesen Skill immer, wenn der Nutzer FastBill
  erwähnt oder etwas mit Rechnungsstellung/Buchhaltung über FastBill automatisieren
  will – z. B. Rechnungen erstellen, versenden, stornieren oder als bezahlt markieren,
  Kunden anlegen oder suchen, Angebote schreiben, Abo-Rechnungen einrichten,
  Umsätze/Ausgaben auswerten, Zeiten erfassen oder Webhooks registrieren. Auch bei
  Anfragen wie "Skript für FastBill", "FastBill-Integration", "FastBill-Export"
  oder beim Debuggen bestehender FastBill-Anbindungen einsetzen.
---

# FastBill API

FastBill ist ein deutsches Rechnungs- und Buchhaltungstool. Die API ist **kein
REST**: Es gibt genau einen Endpunkt, alle Operationen laufen als POST mit einem
`SERVICE`-Feld im Body (RPC-Stil).

## Grundlagen

- **Endpunkt:** `https://my.fastbill.com/api/1.0/api.php` (immer POST, immer SSL)
- **Auth:** HTTP Basic Auth mit `E-Mail-Adresse:API-Key`. Der API-Key steht in den
  FastBill-Kontoeinstellungen. Für Add-on-/App-Zugriff zusätzlich Header
  `X-Username` und `X-Password`.
- **Format:** JSON oder XML – Content-Type `application/json` bzw. `application/xml`.
  Verwende standardmäßig JSON.
- **Feldnamen sind durchgehend GROSSGESCHRIEBEN** (`CUSTOMER_ID`, `INVOICE_DATE`, …).
- **Datumsformat:** `YYYY-MM-DD`, Zeitstempel `YYYY-MM-DD hh:mm:ss`.

### Request-Struktur

```json
{
  "SERVICE": "invoice.get",
  "FILTER": { "CUSTOMER_ID": "123" },
  "DATA": { },
  "LIMIT": 100,
  "OFFSET": 0
}
```

- `SERVICE` – Methodenname, klein geschrieben: `ressource.aktion`
- `FILTER` – nur bei `.get`-Methoden
- `DATA` – Nutzlast bei `.create`/`.update`/`.delete` und Aktionen
- `LIMIT`/`OFFSET` – Paginierung. **Maximal 100 Elemente pro Abfrage** (Default 10).
  Für vollständige Listen in einer Schleife `OFFSET` erhöhen, bis weniger als
  `LIMIT` Elemente zurückkommen.

### Response-Struktur

Die Antwort spiegelt den Request und enthält bei Erfolg `RESPONSE` (Daten in
Containern wie `CUSTOMERS`, `INVOICES`), bei Fehlern `RESPONSE.ERRORS` als Liste.
Prüfe **immer** auf `ERRORS`, nicht auf den HTTP-Statuscode – die API antwortet
auch bei fachlichen Fehlern oft mit HTTP 200.

### Rate Limits

API-Calls pro Stunde je nach Tarif: Solo 50, Solo-Plus 100, Pro 500, Premium 1000.
Webhooks nur in Pro und Premium. Bei Massenoperationen: Calls zählen und ggf.
drosseln; das 100er-Limit pro Listenabfrage macht Paginierung Pflicht.

## Hilfsskript

`scripts/fastbill_api.py` ist ein fertiger CLI-Client (nur Python-Stdlib, keine
Abhängigkeiten). Credentials kommen aus den Umgebungsvariablen `FASTBILL_EMAIL`
und `FASTBILL_API_KEY`:

```bash
python scripts/fastbill_api.py customer.get --filter '{"TERM": "Meier"}' --limit 100
python scripts/fastbill_api.py invoice.create --data '{"CUSTOMER_ID": "123", "ITEMS": [...]}'
python scripts/fastbill_api.py --all invoice.get --filter '{"YEAR": "2026"}'   # paginiert automatisch
```

Nutze das Skript für Ad-hoc-Abfragen und zum Testen; in Integrationen kannst du
seine `call()`-Funktion importieren oder das Muster übernehmen.

## Sicherheitsregeln (wichtig!)

Rechnungen sind steuerlich relevante Dokumente. Halte dich an diese Regeln:

1. **Entwurf zuerst:** `invoice.create` erzeugt immer einen Entwurf. Erst
   `invoice.complete` macht daraus eine echte Rechnung mit fortlaufender
   Rechnungsnummer – das ist **nicht umkehrbar** (nur noch Storno möglich).
   Schließe Rechnungen nur ab, wenn der Nutzer das ausdrücklich will.
2. **Löschen geht nur bei Entwürfen.** Abgeschlossene Rechnungen können nur
   storniert werden (`invoice.cancel`).
3. **Destruktive Aktionen** (`*.delete`, `invoice.cancel`, `invoice.complete`,
   `*.sendbyemail`, `*.sendbypost`) nie "auf Verdacht" ausführen – vorher beim
   Nutzer rückversichern, außer er hat es explizit beauftragt.
4. **API-Key niemals** in Code, Logs oder Repos schreiben – immer über
   Umgebungsvariablen.

## Module

Lies die passende Referenzdatei, bevor du Requests baust – dort stehen alle
Felder, Pflichtangaben und erlaubten Werte:

| Referenz | Services | Wofür |
|---|---|---|
| `references/customers.md` | customer.\*, contact.\* | Kunden & Ansprechpartner |
| `references/invoices.md` | invoice.\*, item.\* | Rechnungen inkl. Lebenszyklus & ITEMS-Struktur |
| `references/estimates.md` | estimate.\* | Angebote, Angebot→Rechnung |
| `references/recurring.md` | recurring.\* | Wiederkehrende (Abo-)Rechnungen |
| `references/revenues-expenses.md` | revenue.\*, expense.\* | Einnahmen & Ausgaben (inkl. Datei-Upload) |
| `references/articles.md` | article.\* | Produkt-/Artikelkatalog |
| `references/projects-times.md` | project.\*, time.\* | Projekte & Zeiterfassung |
| `references/documents-webhooks.md` | document.\*, template.get, webhook.\* | Dokumente, Vorlagen, Webhooks |

## Typische Workflows

**Rechnung stellen (kompletter Zyklus):**
1. Kunde finden oder anlegen: `customer.get` (FILTER `TERM`) → ggf. `customer.create`
2. Entwurf: `invoice.create` mit `CUSTOMER_ID` + `ITEMS`
3. Prüfen: `invoice.get` mit `FILTER.INVOICE_ID`
4. Abschließen: `invoice.complete` (liefert `INVOICE_NUMBER`)
5. Versenden: `invoice.sendbyemail` mit `RECIPIENT`
6. Später: `invoice.setpaid` mit `PAID_DATE`

**Auswertung/Export:** `invoice.get` bzw. `revenue.get`/`expense.get` mit
Datumsfiltern (`START_DATE`/`END_DATE`), paginiert über `LIMIT`/`OFFSET`,
Summen aus `SUB_TOTAL`/`VAT_TOTAL`/`TOTAL`.

**Angebot → Rechnung:** `estimate.create` → `estimate.sendbyemail` → bei Annahme
`estimate.createinvoice` (liefert `INVOICE_ID` eines neuen Entwurfs).
