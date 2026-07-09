# Artikel / Produkte (article.*)

Produktkatalog. Artikel können in Rechnungs-/Angebotspositionen über
`ARTICLE_NUMBER` referenziert werden.

## article.get

**FILTER:** `ARTICLE_ID`, `ARTICLE_NUMBER`

**RESPONSE-Felder:** ARTICLE_ID, ARTICLE_NUMBER, TYPE, TITLE, DESCRIPTION,
UNIT, UNIT_PRICE, CURRENCY_CODE, VAT_PERCENT, IS_GROSS (0 = netto, 1 = brutto),
TAGS

**TYPE-Werte:** `product` (physisch), `digital_product`, `service`, `none`

## article.create

**DATA – Pflicht:** `ARTICLE_NUMBER`, `TITLE`, `UNIT_PRICE`

**DATA – optional:** TYPE, DESCRIPTION, UNIT, CURRENCY_CODE, VAT_PERCENT,
IS_GROSS (0/1)

**RESPONSE:** STATUS, ARTICLE_ID

```json
{
  "SERVICE": "article.create",
  "DATA": {
    "ARTICLE_NUMBER": "HOSTING-PRO",
    "TITLE": "Hosting-Paket Pro",
    "TYPE": "service",
    "UNIT_PRICE": 29.00,
    "VAT_PERCENT": 19,
    "IS_GROSS": 0
  }
}
```

## article.update

**DATA:** `ARTICLE_ID` (Pflicht) + Felder aus `article.create`.
**RESPONSE:** STATUS

## article.delete

**DATA:** `ARTICLE_ID` (Pflicht). **RESPONSE:** STATUS
