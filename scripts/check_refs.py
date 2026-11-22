#!/usr/bin/env python3
"""Resolve every machine-checkable ID in references.md.

Parses the markdown tables in references.md, extracts the `ID` column and
resolves each token against the authoritative public API for its scheme:

  doi:10.xxx      Crossref           https://api.crossref.org/works/<doi>
  pmid:NNN        NCBI E-utilities   esummary db=pubmed
  pmcid:PMCNNN    NCBI E-utilities   esummary db=pmc
  omim:NNNNNN     NCBI E-utilities   esummary db=omim
  nct:NCTNNNNNNNN ClinicalTrials.gov https://clinicaltrials.gov/api/v2/studies/<nct>
  pdb:XXXX        RCSB               https://data.rcsb.org/rest/v1/core/entry/<id>
  uniprot:XXXXXX  UniProt REST       https://rest.uniprot.org/uniprotkb/<acc>.json
  url:https://... HEAD, falling back to GET; 2xx/3xx is OK

Prints one `OK|FAIL id -> title (year)` line per entry, exits 1 if any FAIL.

Usage:
  python3 scripts/check_refs.py [--file references.md] [--only PREFIX] [--json]

`--only` filters by Ref prefix (e.g. `CT`, `M`) or by ID scheme (e.g. `pmid`).
Stdlib only; Python 3.10+.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = (
    "Mozilla/5.0 (compatible; cpva-check-refs/2.0; "
    "+https://github.com/cancer-predisposition-variant-analyst)"
)
NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
ID_RE = re.compile(r"`?((?:doi|pmid|pmcid|omim|nct|pdb|uniprot|url):[^\s`|]+)`?")

# Hosts that are login- or bot-walled and legitimately answer 403 to scripts.
# A 403 from these is reported OK with a warning instead of FAIL.
FORBIDDEN_OK_HOSTS = ("nccn.org",)

# Minimum spacing between requests, per API family (seconds).
RATE = {"ncbi": 0.34, "crossref": 0.2, "other": 0.2}
_last: dict[str, float] = {}


def throttle(family: str) -> None:
    now = time.monotonic()
    wait = _last.get(family, 0.0) + RATE[family] - now
    if wait > 0:
        time.sleep(wait)
    _last[family] = time.monotonic()


def fetch(url: str, method: str = "GET", timeout: int = 30, retries: int = 3) -> tuple[int, bytes]:
    """Return (status, body). Raises urllib.error.HTTPError for 4xx/5xx after retries on 429/5xx."""
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"}, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, (b"" if method == "HEAD" else resp.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(2.0 * (attempt + 1))
                continue
            raise
    raise RuntimeError("unreachable")


def get_json(url: str, family: str) -> dict:
    throttle(family)
    _, body = fetch(url)
    return json.loads(body.decode("utf-8"))


# --- resolvers: each returns (title, year) or raises ----------------------------------


def resolve_doi(doi: str) -> tuple[str, str]:
    msg = get_json("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe=""), "crossref")["message"]
    title = " ".join((msg.get("title") or [""])[0].split())
    title = re.sub(r"<[^>]+>", "", title)
    for key in ("published-print", "published-online", "issued", "posted", "created"):
        parts = msg.get(key, {}).get("date-parts", [[None]])
        if parts and parts[0] and parts[0][0]:
            return title, str(parts[0][0])
    return title, "n.d."


def _esummary(db: str, uid: str) -> dict:
    data = get_json(f"{NCBI_BASE}?db={db}&retmode=json&id={uid}", "ncbi")
    rec = data["result"].get(uid)
    if not rec or "error" in rec:
        raise ValueError(f"{db} uid {uid} not found")
    return rec


def resolve_pmid(pmid: str) -> tuple[str, str]:
    rec = _esummary("pubmed", pmid)
    return rec["title"], rec.get("pubdate", "")[:4]


def resolve_pmcid(pmcid: str) -> tuple[str, str]:
    rec = _esummary("pmc", pmcid.upper().removeprefix("PMC"))
    return rec["title"], rec.get("pubdate", "")[:4]


def resolve_omim(mim: str) -> tuple[str, str]:
    rec = _esummary("omim", mim)
    return rec["title"], "OMIM"


def resolve_nct(nct: str) -> tuple[str, str]:
    study = get_json("https://clinicaltrials.gov/api/v2/studies/" + nct, "other")["protocolSection"]
    ident = study["identificationModule"]
    title = ident.get("officialTitle") or ident.get("briefTitle", "")
    status = study.get("statusModule", {}).get("overallStatus", "UNKNOWN")
    return title, status


def resolve_pdb(pdb_id: str) -> tuple[str, str]:
    entry = get_json("https://data.rcsb.org/rest/v1/core/entry/" + pdb_id.upper(), "other")
    return entry["struct"]["title"], entry["rcsb_accession_info"]["initial_release_date"][:4]


def resolve_uniprot(acc: str) -> tuple[str, str]:
    entry = get_json(
        f"https://rest.uniprot.org/uniprotkb/{acc}.json?fields=accession,protein_name,gene_names,organism_name,length",
        "other",
    )
    desc = entry["proteinDescription"]
    name = (desc.get("recommendedName") or desc.get("submissionNames", [{}])[0])["fullName"]["value"]
    genes = ",".join(g.get("geneName", {}).get("value", "") for g in entry.get("genes", []))
    org = entry["organism"]["scientificName"]
    return f"{name} [{genes}] {org}", f"{entry['sequence']['length']} aa"


def resolve_url(url: str) -> tuple[str, str]:
    throttle("other")
    host = urllib.parse.urlparse(url).hostname or ""
    try:
        status, _ = fetch(url, method="HEAD", timeout=20)
    except urllib.error.HTTPError as e:
        if e.code in (403, 405, 501):
            try:
                status, _ = fetch(url, method="GET", timeout=20)
            except urllib.error.HTTPError as e2:
                if e2.code == 403 and host.endswith(FORBIDDEN_OK_HOSTS):
                    return f"{url} (WARNING: HTTP 403, login-walled; existence not confirmed)", "HTTP 403"
                raise
        else:
            raise
    return url, f"HTTP {status}"


RESOLVERS = {
    "doi": resolve_doi,
    "pmid": resolve_pmid,
    "pmcid": resolve_pmcid,
    "omim": resolve_omim,
    "nct": resolve_nct,
    "pdb": resolve_pdb,
    "uniprot": resolve_uniprot,
    "url": resolve_url,
}

# --- parsing ---------------------------------------------------------------------


def parse_tables(text: str) -> list[dict[str, str]]:
    """Return one dict per table row keyed by header cell text."""
    rows: list[dict[str, str]] = []
    header: list[str] | None = None
    for line in text.splitlines():
        if not line.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def entries(path: Path) -> list[tuple[str, str]]:
    out = []
    for row in parse_tables(path.read_text(encoding="utf-8")):
        ref, token = row.get("Ref"), row.get("ID")
        if not ref or not token:
            continue
        m = ID_RE.search(token)
        if not m:
            out.append((ref, token))  # will FAIL as unparseable
            continue
        out.append((ref, m.group(1)))
    return out


def check(ref: str, ident: str) -> dict:
    scheme, _, value = ident.partition(":")
    fn = RESOLVERS.get(scheme)
    if fn is None or not value:
        return {"ref": ref, "id": ident, "ok": False, "title": "", "year": "", "error": "unparseable ID"}
    try:
        title, year = fn(value)
        return {"ref": ref, "id": ident, "ok": True, "title": title, "year": year, "error": ""}
    except Exception as e:  # noqa: BLE001 - report every failure mode uniformly
        return {"ref": ref, "id": ident, "ok": False, "title": "", "year": "", "error": f"{type(e).__name__}: {e}"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", default=str(Path(__file__).resolve().parent.parent / "references.md"))
    ap.add_argument("--only", metavar="PREFIX", help="Ref prefix (C, CT, M...) or ID scheme (doi, pmid...)")
    ap.add_argument("--json", action="store_true", help="emit a JSON array instead of text lines")
    args = ap.parse_args(argv)

    todo = entries(Path(args.file))
    if args.only:
        p = args.only.lower()
        todo = [
            (r, i)
            for r, i in todo
            if i.lower().startswith(p + ":") or (re.match(r"[A-Za-z]+", r) or [""])[0].lower() == p
        ]
    if not todo:
        print("no entries matched", file=sys.stderr)
        return 1

    results = []
    for ref, ident in todo:
        res = check(ref, ident)
        results.append(res)
        if not args.json:
            status = "OK  " if res["ok"] else "FAIL"
            detail = f"{res['title']} ({res['year']})" if res["ok"] else res["error"]
            print(f"{status} {ref:<6} {ident} -> {detail}", flush=True)

    failures = [r for r in results if not r["ok"]]
    if args.json:
        json.dump(results, sys.stdout, indent=2, ensure_ascii=False)
        print()
    else:
        print(f"\n{len(results) - len(failures)}/{len(results)} OK, {len(failures)} FAIL")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
