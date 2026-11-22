#!/usr/bin/env python3
"""Resolve every machine-checkable ID in references.md and check the [ID] citations that use them.

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

Also:
  * every data row of a table with a `Ref` column must yield exactly one entry (a row with a
    missing/unparseable ID is a FAIL rather than silently skipped);
  * every `[ID]` cited in the skill's markdown files (*.md, examples/, evals/, scripts/README.md)
    must be a Ref defined in references.md; a dangling citation is a FAIL;
  * for doi/pmid/pmcid, the resolved publication year (and first-author surname when the API
    returns one) is compared with the `Citation` cell. A mismatch is a WARN; with --strict it
    is a FAIL. Years may differ by one (online-first vs print).

Prints one `OK|FAIL ref id -> title (year)` line per entry plus `WARN` lines.

Usage:
  python3 scripts/check_refs.py [--file references.md] [--only PREFIX] [--strict] [--json]

`--only` filters by Ref prefix (e.g. `CT`, `M`) or by ID scheme (e.g. `pmid`).
Exit status: 0 all OK, 1 any FAIL (or unreadable --file), 2 usage error (argparse).
Stdlib only; Python 3.10+.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
from pathlib import Path

from _http import request

# Crawler-style UA: several publisher/vendor sites answer 403/500 to anything not starting "Mozilla/5.0".
USER_AGENT = "Mozilla/5.0 (compatible; cancer-predisposition-variant-analyst/2.0; +https://github.com/bloo-berries/cancer-predisposition-variant-analyst)"
NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
ID_RE = re.compile(r"`?((?:doi|pmid|pmcid|omim|nct|pdb|uniprot|url):[^\s`|]+)`?")
# Reference IDs as cited in prose: [F1], [C1, C2]. ACMG codes (PS2, PM2) have no matching prefix.
CITE_PREFIX_RE = re.compile(r"^(F|C|G|M|P|T|N|R|O|S|CT|SIG|D|TOOL)\d+$")
BRACKET_RE = re.compile(r"\[([^\[\]]+)\]")
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")
CITED_GLOBS = ("*.md", "examples/*.md", "evals/*.md", "scripts/README.md")

# Hosts that are login- or bot-walled and legitimately answer 403 to scripts.
# A 403 from these is reported OK with a warning instead of FAIL.
FORBIDDEN_OK_HOSTS = ("nccn.org",)

# Minimum spacing between requests to the same host (seconds).
RATE = {"eutils.ncbi.nlm.nih.gov": 0.34, "api.crossref.org": 0.2}
DEFAULT_RATE = 0.2


def fetch(url: str, method: str = "GET", timeout: int = 30) -> tuple[int, bytes]:
    """Return (status, body). Retries 429/5xx and network errors; raises HTTPError otherwise."""
    host = urllib.parse.urlparse(url).hostname or ""
    resp = request(url, method=method, timeout=timeout, min_interval=RATE.get(host, DEFAULT_RATE),
                   headers={"User-Agent": USER_AGENT})
    return resp.status, resp.body


def get_json(url: str) -> dict:
    _, body = fetch(url)
    return json.loads(body.decode("utf-8"))


# --- resolvers: each returns (title, year, author surnames in order | None) or raises ---------


def resolve_doi(doi: str) -> tuple[str, str, list[str] | None]:
    msg = get_json("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe=""))["message"]
    title = " ".join((msg.get("title") or [""])[0].split())
    title = re.sub(r"<[^>]+>", "", title)
    authors = [a.get("family") or a.get("name") or "" for a in msg.get("author") or []] or None
    for key in ("published-print", "published-online", "issued", "posted", "created"):
        parts = msg.get(key, {}).get("date-parts", [[None]])
        if parts and parts[0] and parts[0][0]:
            return title, str(parts[0][0]), authors
    return title, "n.d.", authors


def _esummary(db: str, uid: str) -> dict:
    data = get_json(f"{NCBI_BASE}?db={db}&retmode=json&id={uid}")
    rec = data["result"].get(uid)
    if not rec or "error" in rec:
        raise ValueError(f"{db} uid {uid} not found")
    return rec


def _surnames(rec: dict) -> list[str] | None:
    # esummary names are "Palles C" / "Pachlopnik Schmid J": drop the trailing initials token
    names = [a.get("name", "") for a in rec.get("authors") or [] if a.get("authtype", "Author") == "Author"]
    out = [" ".join(n.split()[:-1]) or n for n in names if n]
    return out or None


def resolve_pmid(pmid: str) -> tuple[str, str, list[str] | None]:
    rec = _esummary("pubmed", pmid)
    return rec["title"], rec.get("pubdate", "")[:4], _surnames(rec)


def resolve_pmcid(pmcid: str) -> tuple[str, str, list[str] | None]:
    rec = _esummary("pmc", pmcid.upper().removeprefix("PMC"))
    return rec["title"], rec.get("pubdate", "")[:4], _surnames(rec)


def resolve_omim(mim: str) -> tuple[str, str, None]:
    rec = _esummary("omim", mim)
    return rec["title"], "OMIM", None


def resolve_nct(nct: str) -> tuple[str, str, None]:
    study = get_json("https://clinicaltrials.gov/api/v2/studies/" + nct)["protocolSection"]
    ident = study["identificationModule"]
    title = ident.get("officialTitle") or ident.get("briefTitle", "")
    status = study.get("statusModule", {}).get("overallStatus", "UNKNOWN")
    return title, status, None


def resolve_pdb(pdb_id: str) -> tuple[str, str, None]:
    entry = get_json("https://data.rcsb.org/rest/v1/core/entry/" + pdb_id.upper())
    return entry["struct"]["title"], entry["rcsb_accession_info"]["initial_release_date"][:4], None


def resolve_uniprot(acc: str) -> tuple[str, str, None]:
    entry = get_json(
        f"https://rest.uniprot.org/uniprotkb/{acc}.json?fields=accession,protein_name,gene_names,organism_name,length"
    )
    desc = entry["proteinDescription"]
    name = (desc.get("recommendedName") or desc.get("submissionNames", [{}])[0])["fullName"]["value"]
    genes = ",".join(g.get("geneName", {}).get("value", "") for g in entry.get("genes", []))
    org = entry["organism"]["scientificName"]
    return f"{name} [{genes}] {org}", f"{entry['sequence']['length']} aa", None


def resolve_url(url: str) -> tuple[str, str, None]:
    host = urllib.parse.urlparse(url).hostname or ""
    try:
        status, _ = fetch(url, method="HEAD", timeout=20)
    except urllib.error.HTTPError as e:
        if e.code in (403, 405, 501):
            try:
                status, _ = fetch(url, method="GET", timeout=20)
            except urllib.error.HTTPError as e2:
                if e2.code == 403 and host.endswith(FORBIDDEN_OK_HOSTS):
                    return f"{url} (WARNING: HTTP 403, login-walled; existence not confirmed)", "HTTP 403", None
                raise
        else:
            raise
    return url, f"HTTP {status}", None


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
LITERATURE_SCHEMES = ("doi", "pmid", "pmcid")

# --- parsing ---------------------------------------------------------------------


def parse_tables(text: str) -> list[dict[str, str]]:
    """Return one dict per table data row keyed by header cell text (missing cells -> '')."""
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
        cells += [""] * (len(header) - len(cells))
        rows.append(dict(zip(header, cells)))
    return rows


def entries(text: str) -> tuple[list[dict[str, str]], int]:
    """Return ({ref, id, citation} per data row of every table with a Ref column, number of such rows).

    Rows whose ID cell is empty or has no recognised scheme get the raw cell as id and FAIL later.
    """
    out = []
    n_rows = 0
    for row in parse_tables(text):
        if "Ref" not in row:
            continue
        n_rows += 1
        token = row.get("ID", "")
        m = ID_RE.search(token)
        out.append({"ref": row["Ref"], "id": m.group(1) if m else (token or "(missing ID cell)"), "citation": row.get("Citation", "")})
    return out, n_rows


def cited_ids(root: Path) -> dict[str, list[str]]:
    """Reference-shaped [ID] tokens cited in the skill's markdown -> list of 'file:line' locations."""
    cites: dict[str, list[str]] = {}
    seen: set[Path] = set()
    for pattern in CITED_GLOBS:
        for path in sorted(root.glob(pattern)):
            if path in seen:
                continue
            seen.add(path)
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                for group in BRACKET_RE.findall(line):
                    for token in re.split(r"[,;]\s*", group):
                        token = token.strip()
                        if CITE_PREFIX_RE.match(token):
                            cites.setdefault(token, []).append(f"{path.relative_to(root)}:{lineno}")
    return cites


# --- checking --------------------------------------------------------------------


def _fold(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).lower()


# "Palles et al. 2013, _Nat Genet_", "Pachlopnik Schmid et al. 2012", "Smith and Jones 2020", "Lindeboom 2016".
# Descriptive cells ("LOP POLE stratification 2025", "NeoPrecis 2026") carry no surname and are not compared.
AUTHOR_CITATION_RE = re.compile(r"^(?:(?P<name>[A-Z][a-z'’-]+(?:[ -][A-Z][a-z'’-]+)*)\s+(?:et al\.?|and\b|&)|(?P<single>[A-Z][a-z'’-]+)\s+(?:19|20)\d{2}\b)")


def citation_warnings(citation: str, year: str, authors: list[str] | None) -> list[str]:
    """Compare resolver metadata with the Citation cell: publication year (+/-1) and first-author surname."""
    warns = []
    if not citation:
        return warns
    cited_year = YEAR_RE.search(citation)
    if cited_year and year.isdigit() and abs(int(cited_year.group(0)) - int(year)) > 1:
        warns.append(f"year: resolved {year}, citation says {cited_year.group(0)}")
    m = AUTHOR_CITATION_RE.match(citation)
    if authors and m:
        # Crossref sometimes lists a consortium ahead of the people; "Palles et al." is still the first author
        while len(authors) > 1 and re.search(r"consortium|group|collaborat|network|team", authors[0], re.I):
            authors = authors[1:]
        cited = _fold(m.group("name") or m.group("single")).strip()
        folded = [_fold(a).strip() for a in authors]
        same = [i for i, a in enumerate(folded) if a and (a in cited or cited in a)]
        if not same:
            warns.append(f"first author: resolved '{authors[0]}' ({len(authors)} authors), citation says '{m.group(0).strip()}' who is not listed")
        elif same[0] != 0:
            warns.append(f"first author: resolved '{authors[0]}', citation says '{m.group(0).strip()}' (author {same[0] + 1} of {len(authors)})")
    return warns


def check(entry: dict[str, str], strict: bool) -> dict:
    ref, ident, citation = entry["ref"], entry["id"], entry["citation"]
    scheme, _, value = ident.partition(":")
    fn = RESOLVERS.get(scheme)
    base = {"ref": ref, "id": ident, "title": "", "year": "", "authors": None, "warnings": [], "error": ""}
    if fn is None or not value:
        return {**base, "ok": False, "error": "unparseable ID"}
    try:
        title, year, authors = fn(value)
    except Exception as e:  # noqa: BLE001 - report every failure mode uniformly
        return {**base, "ok": False, "error": f"{type(e).__name__}: {e}"}
    warns = citation_warnings(citation, year, authors) if scheme in LITERATURE_SCHEMES else []
    ok = not (strict and warns)
    return {**base, "ok": ok, "title": title, "year": year, "authors": authors, "warnings": warns,
            "error": "" if ok else "metadata mismatch (--strict): " + "; ".join(warns)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog="Exit status: 0 all OK, 1 any FAIL, 2 usage error.")
    ap.add_argument("--file", default=str(Path(__file__).resolve().parent.parent / "references.md"))
    ap.add_argument("--only", metavar="PREFIX", help="Ref prefix (C, CT, M...) or ID scheme (doi, pmid...)")
    ap.add_argument("--strict", action="store_true", help="year/first-author mismatches with the Citation cell FAIL instead of WARN")
    ap.add_argument("--json", action="store_true", help="emit a JSON array instead of text lines")
    args = ap.parse_args(argv)

    path = Path(args.file)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"error: cannot read {path}: {e.strerror or e}", file=sys.stderr)
        return 1

    all_entries, n_rows = entries(text)
    results: list[dict] = []
    emit = (lambda *a, **k: None) if args.json else print

    # structural checks: every table row yields an entry; every cited [ID] is defined
    if len(all_entries) != n_rows:
        results.append({"ref": "table", "id": path.name, "ok": False, "title": "", "year": "", "authors": None, "warnings": [],
                        "error": f"parsed {len(all_entries)} entries from {n_rows} table rows"})
    emit(f"{'OK  ' if len(all_entries) == n_rows else 'FAIL'} table  {path.name} -> {n_rows} data rows, {len(all_entries)} entries")
    defined = {e["ref"] for e in all_entries}
    cites = cited_ids(path.resolve().parent)
    missing = {k: v for k, v in cites.items() if k not in defined}
    for token, where in sorted(missing.items()):
        results.append({"ref": "cite", "id": f"[{token}]", "ok": False, "title": "", "year": "", "authors": None, "warnings": [],
                        "error": f"cited but not defined in {path.name}: {', '.join(where[:5])}"})
        emit(f"FAIL cite   [{token}] -> not defined in {path.name}: {', '.join(where[:5])}")
    emit(f"{'OK  ' if not missing else 'FAIL'} cite   {len(cites)} distinct [ID] tokens cited, {len(missing)} undefined")

    todo = all_entries
    if args.only:
        p = args.only.lower()
        todo = [e for e in todo if e["id"].lower().startswith(p + ":") or (re.match(r"[A-Za-z]+", e["ref"]) or [""])[0].lower() == p]
    if not todo:
        print("no entries matched", file=sys.stderr)
        return 1

    for entry in todo:
        res = check(entry, args.strict)
        results.append(res)
        status = "OK  " if res["ok"] else "FAIL"
        detail = f"{res['title']} ({res['year']})" if res["ok"] else res["error"]
        emit(f"{status} {res['ref']:<6} {res['id']} -> {detail}", flush=True)
        if res["ok"]:
            for w in res["warnings"]:
                emit(f"WARN {res['ref']:<6} {res['id']} -> {w}", flush=True)

    failures = [r for r in results if not r["ok"]]
    warnings = sum(len(r["warnings"]) for r in results if r["ok"])
    if args.json:
        json.dump(results, sys.stdout, indent=2, ensure_ascii=False)
        print()
    else:
        print(f"\n{len(results) - len(failures)}/{len(results)} OK, {len(failures)} FAIL, {warnings} WARN")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
