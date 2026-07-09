# fastbill-skill

Ein [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) für Claude
(Claude Code / Cowork), der die komplette [FastBill-API](https://apidocs.fastbill.com/)
abdeckt: Rechnungen, Kunden, Angebote, wiederkehrende Rechnungen, Einnahmen,
Ausgaben, Artikel, Projekte, Zeiterfassung, Dokumente und Webhooks.

## Was der Skill kann

- Korrekte Requests für alle FastBill-Services bauen (RPC-Stil: ein Endpunkt,
  `SERVICE`-Feld, GROSSGESCHRIEBENE Feldnamen)
- Vollständige Feldreferenzen pro Modul (Pflichtfelder, erlaubte Werte,
  Beispiel-Requests)
- Sicherheitsregeln für steuerlich relevante Aktionen (Entwurf vs. Abschluss,
  Storno, Versand)
- Paginierung (100er-Limit), Fehlerbehandlung über `RESPONSE.ERRORS`, Rate Limits
- Fertiger CLI-Client ohne Abhängigkeiten (`scripts/fastbill_api.py`)

## Installation

**Claude Code:**

```bash
git clone https://github.com/staude/fastbill-skill ~/.claude/skills/fastbill
```

**Claude.ai / Cowork:** Repo als `.zip` bzw. `.skill` paketieren und in den
Einstellungen unter Skills hochladen.

## Verwendung

Credentials als Umgebungsvariablen setzen:

```bash
export FASTBILL_EMAIL="deine@email.de"
export FASTBILL_API_KEY="…"   # FastBill → Einstellungen → API
```

Dann einfach mit Claude über FastBill sprechen – z. B. „Exportiere alle
Rechnungen aus Q2 als CSV" oder „Lege einen Kunden an und erstelle einen
Rechnungsentwurf". Der Skill triggert automatisch bei FastBill-Themen.

Ad-hoc-Aufrufe gehen auch direkt:

```bash
python scripts/fastbill_api.py customer.get --filter '{"TERM": "Meier"}' --limit 100
python scripts/fastbill_api.py --all invoice.get --filter '{"YEAR": "2026"}'
```

## Struktur

```
fastbill-skill/
├── SKILL.md                     # Einstieg: Grundlagen, Workflows, Sicherheitsregeln
├── references/                  # Feldreferenz pro API-Modul
│   ├── customers.md             # customer.*, contact.*
│   ├── invoices.md              # invoice.*, item.* (inkl. ITEMS-Struktur)
│   ├── estimates.md             # estimate.*
│   ├── recurring.md             # recurring.*
│   ├── revenues-expenses.md     # revenue.*, expense.*
│   ├── articles.md              # article.*
│   ├── projects-times.md        # project.*, time.*
│   └── documents-webhooks.md    # document.*, template.get, webhook.*
└── scripts/
    └── fastbill_api.py          # CLI-Client (nur Python-Stdlib)
```

## Benchmark

Getestet gegen 3 realistische Aufgaben (CSV-Export, Kunde + Rechnungsentwurf,
Webhook-Setup), jeweils mit und ohne Skill: **mit Skill 15/15 Kriterien (100 %),
ohne Skill 12/15 (80 %)**. Ohne Skill nutzte das Modell u. a. den veralteten
`MONTH`-Filter und erfand falsche Webhook-Feldnamen (`SOURCE`/`TARGET` statt
`TYPE`/`ENDPOINT`/`EVENTS`).

## Lizenz

MIT
