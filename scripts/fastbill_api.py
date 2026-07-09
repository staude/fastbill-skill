#!/usr/bin/env python3
"""Minimaler FastBill-API-Client (nur Stdlib).

Credentials über Umgebungsvariablen:
    FASTBILL_EMAIL    E-Mail-Adresse des FastBill-Kontos
    FASTBILL_API_KEY  API-Key (FastBill → Einstellungen)

CLI:
    python fastbill_api.py SERVICE [--filter JSON] [--data JSON]
                                   [--limit N] [--offset N] [--all]

Beispiele:
    python fastbill_api.py customer.get --filter '{"TERM": "Meier"}'
    python fastbill_api.py invoice.setpaid --data '{"INVOICE_ID": "42"}'
    python fastbill_api.py --all invoice.get --filter '{"YEAR": "2026"}'

Als Bibliothek:
    from fastbill_api import call, fetch_all
    customers = fetch_all("customer.get", {"CITY": "Berlin"})
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request

API_URL = "https://my.fastbill.com/api/1.0/api.php"


class FastBillError(RuntimeError):
    """Fachlicher Fehler aus RESPONSE.ERRORS."""


def _auth_header() -> str:
    email = os.environ.get("FASTBILL_EMAIL")
    api_key = os.environ.get("FASTBILL_API_KEY")
    if not email or not api_key:
        sys.exit("FASTBILL_EMAIL und FASTBILL_API_KEY müssen gesetzt sein.")
    token = base64.b64encode(f"{email}:{api_key}".encode()).decode()
    return f"Basic {token}"


def call(service: str, filter_: dict | None = None, data: dict | None = None,
         limit: int | None = None, offset: int | None = None) -> dict:
    """Einen API-Call ausführen und den RESPONSE-Teil zurückgeben.

    Wirft FastBillError, wenn die API fachliche Fehler meldet.
    """
    body: dict = {"SERVICE": service}
    if filter_:
        body["FILTER"] = filter_
    if data:
        body["DATA"] = data
    if limit is not None:
        body["LIMIT"] = limit
    if offset is not None:
        body["OFFSET"] = offset

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": _auth_header(),
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise FastBillError(f"HTTP {e.code}: {e.read().decode(errors='replace')}") from e

    response = payload.get("RESPONSE", {})
    errors = response.get("ERRORS")
    if errors:
        raise FastBillError("; ".join(map(str, errors)))
    return response


def fetch_all(service: str, filter_: dict | None = None, page_size: int = 100):
    """Alle Elemente einer .get-Liste paginiert einsammeln (max. 100 pro Call)."""
    offset = 0
    items: list = []
    while True:
        response = call(service, filter_=filter_, limit=page_size, offset=offset)
        # Der Listen-Container heißt je nach Service anders (CUSTOMERS, INVOICES, ...)
        page = next((v for v in response.values() if isinstance(v, list)), [])
        items.extend(page)
        if len(page) < page_size:
            return items
        offset += page_size


def main() -> None:
    p = argparse.ArgumentParser(description="FastBill-API-Call ausführen")
    p.add_argument("service", help="z. B. customer.get, invoice.create")
    p.add_argument("--filter", type=json.loads, default=None, help="FILTER als JSON")
    p.add_argument("--data", type=json.loads, default=None, help="DATA als JSON")
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--offset", type=int, default=None)
    p.add_argument("--all", action="store_true",
                   help="alle Seiten einsammeln (nur .get-Services)")
    args = p.parse_args()

    try:
        if args.all:
            result: object = fetch_all(args.service, args.filter)
        else:
            result = call(args.service, args.filter, args.data,
                          args.limit, args.offset)
    except FastBillError as e:
        sys.exit(f"FastBill-Fehler: {e}")

    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
