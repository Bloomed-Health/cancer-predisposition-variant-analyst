#!/usr/bin/env python3
"""Query ClinVar through NCBI E-utilities (esearch + esummary).

Gene mode:
  python3 scripts/clinvar_lookup.py --gene POLE                      # truncating (frameshift+nonsense)
  python3 scripts/clinvar_lookup.py --gene POLE --type missense --significance pathogenic
      Summarizes germline classification counts for the matching variants and lists the
      first N records (title, classification, review status, conditions).
Variant mode:
  python3 scripts/clinvar_lookup.py --variant 'NM_006231.4:c.158_159del'
  python3 scripts/clinvar_lookup.py --variant 'NM_006231.4:c.158_159del' --position 12:132681183
      Finds records by HGVS name; --position (GRCh38 chr:pos) adds a positional search so that
      differently named or overlapping records at that base are also listed.

Counts are ClinVar aggregate germline classifications per Variation ID (not per submission).
Set NCBI_API_KEY (or --api-key) to raise the E-utilities rate limit from 3 to 10 requests/s.
Exit status: 0 success (including "no records"), 1 invalid input, 2 network/API error
(argparse usage errors also exit 2).
--significance values P/LP, VUS, B/LB, Conflicting match the collapsed bucket exactly; any other
value is a case-insensitive substring of the ClinVar description, so `pathogenic` also keeps
"Likely pathogenic" and "Conflicting classifications of pathogenicity" -- use P/LP for P+LP only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
from collections import Counter

from _http import request

TIMEOUT_S = 30
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
TOOL = "cancer-predisposition-variant-analyst"
PAGE = 500

TYPE_TERMS = {
    "frameshift": '"frameshift variant"[mcns]',
    "nonsense": "nonsense[mcns]",
    "truncating": '("frameshift variant"[mcns] OR nonsense[mcns])',
    "missense": '"missense variant"[mcns]',
    "synonymous": '"synonymous variant"[mcns]',
    "splice": '("splice donor variant"[mcns] OR "splice acceptor variant"[mcns])',
    "all": None,
}
REVIEW_STARS = {
    "practice guideline": 4,
    "reviewed by expert panel": 3,
    "criteria provided, multiple submitters, no conflicts": 2,
    "criteria provided, conflicting classifications": 1,
    "criteria provided, single submitter": 1,
    "no assertion criteria provided": 0,
    "no classification provided": 0,
    "no classifications from unflagged records": 0,
}
BUCKETS = [
    ("P/LP", ("pathogenic", "likely pathogenic", "pathogenic/likely pathogenic")),
    ("VUS", ("uncertain significance",)),
    ("B/LB", ("benign", "likely benign", "benign/likely benign")),
    ("Conflicting", ("conflicting classifications of pathogenicity", "conflicting interpretations of pathogenicity")),
]


class ApiError(Exception):
    pass


class Eutils:
    def __init__(self, api_key: str | None):
        self.api_key = api_key
        self.min_interval = 0.11 if api_key else 0.34

    def call(self, endpoint: str, params: dict, post: bool = False, raw: bool = False):
        params = {**params, "db": "clinvar", "tool": TOOL}
        if not raw:
            params["retmode"] = "json"
        if self.api_key:
            params["api_key"] = self.api_key
        body = urllib.parse.urlencode(params).encode()
        url = f"{EUTILS}/{endpoint}.fcgi"
        try:
            resp = request(url if post else f"{url}?{body.decode()}", method="POST" if post else "GET",
                           data=body if post else None, timeout=TIMEOUT_S, min_interval=self.min_interval)
        except urllib.error.HTTPError as e:
            raise ApiError(f"HTTP {e.code} from {endpoint}: {e.read().decode('utf-8', 'replace')[:200]}")
        except (urllib.error.URLError, TimeoutError) as e:
            raise ApiError(f"network error contacting {endpoint}: {e}")
        text = resp.text()
        if raw:
            return text
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise ApiError(f"{endpoint} returned non-JSON: {e}")
        if "error" in data and not data.get("result") and not data.get("esearchresult"):
            raise ApiError(f"{endpoint}: {data['error']}")
        return data

    def search(self, term: str) -> dict:
        r = self.call("esearch", {"term": term, "usehistory": "y", "retmax": 0})["esearchresult"]
        if "ERROR" in r:
            raise ApiError(f"esearch: {r['ERROR']}")
        return {"count": int(r.get("count", 0)), "webenv": r.get("webenv"), "query_key": r.get("querykey"),
                "query_translation": r.get("querytranslation")}

    def summaries(self, search: dict, limit: int | None = None) -> list[dict]:
        total = search["count"] if limit is None else min(search["count"], limit)
        out: list[dict] = []
        start = 0
        while start < total:
            r = self.call("esummary", {"WebEnv": search["webenv"], "query_key": search["query_key"],
                                       "retstart": start, "retmax": min(PAGE, total - start)}, post=True)
            res = r.get("result") or {}
            uids = res.get("uids") or []
            if not uids:
                break
            out.extend(res[u] for u in uids)
            start += len(uids)
        return out

    def submissions(self, variation_ids: list[str]) -> list[dict]:
        """SCV-level rows (submitter, classification, review status) from VCV XML via efetch."""
        out: list[dict] = []
        for i in range(0, len(variation_ids), 100):
            xml_text = self.call("efetch", {"rettype": "vcv", "is_variationid": "", "id": ",".join(variation_ids[i:i + 100])},
                                 post=True, raw=True)
            try:
                root = ET.fromstring(xml_text)
            except ET.ParseError as e:
                raise ApiError(f"efetch returned unparsable XML: {e}")
            for va in root.iter("VariationArchive"):
                for ca in va.iter("ClinicalAssertion"):
                    acc = ca.find("ClinVarAccession")
                    cls = ca.find("Classification")
                    desc = kind = None
                    if cls is not None:
                        for tag in ("GermlineClassification", "SomaticClinicalImpact", "OncogenicityClassification"):
                            e = cls.find(tag)
                            if e is not None and e.text:
                                desc, kind = e.text.strip(), tag
                    rs = cls.find("ReviewStatus") if cls is not None else None
                    out.append({"variation_id": va.get("VariationID"), "scv": acc.get("Accession") if acc is not None else None,
                                "submitter": acc.get("SubmitterName") if acc is not None else "?",
                                "classification": desc or "(none)", "kind": kind, "review_status": rs.text if rs is not None else ""})
        return out


def classification(rec: dict) -> dict:
    g = rec.get("germline_classification") or rec.get("clinical_significance") or {}
    review = g.get("review_status") or ""
    conds = [t.get("trait_name") for t in (g.get("trait_set") or []) if t.get("trait_name")]
    onc = (rec.get("oncogenicity_classification") or {}).get("description") or ""
    som = (rec.get("clinical_impact_classification") or {}).get("description") or ""
    return {
        "variation_id": rec.get("uid"), "accession": rec.get("accession_version") or rec.get("accession"),
        "title": rec.get("title"), "germline": g.get("description") or "(no germline classification)",
        "review_status": review, "stars": REVIEW_STARS.get(review), "last_evaluated": (g.get("last_evaluated") or "")[:10],
        "conditions": conds, "molecular_consequence": rec.get("molecular_consequence_list") or [],
        "protein_change": rec.get("protein_change") or "", "n_scv": len(((rec.get("supporting_submissions") or {}).get("scv")) or []),
        "oncogenicity": onc, "somatic_clinical_impact": som,
        "url": f"https://www.ncbi.nlm.nih.gov/clinvar/variation/{rec.get('uid')}/",
    }


def bucket(desc: str) -> str:
    d = desc.lower()
    for name, keys in BUCKETS:
        if d in keys:
            return name
    return "Other"


BUCKET_NAMES = {name.lower(): name for name, _ in BUCKETS}


def significance_matches(germline: str, wanted: str) -> bool:
    """Bucket names (P/LP, VUS, B/LB, Conflicting) match the collapsed bucket exactly; anything else is a substring."""
    w = wanted.lower()
    if w in BUCKET_NAMES:
        return bucket(germline) == BUCKET_NAMES[w]
    return w in germline.lower()


def significance_filter(rows: list[dict], wanted: list[str]) -> list[dict]:
    if not wanted:
        return rows
    return [r for r in rows if any(significance_matches(r["germline"], x) for x in wanted)]


def condition_filter(rows: list[dict], wanted: list[str]) -> list[dict]:
    if not wanted:
        return rows
    w = [x.lower() for x in wanted]
    return [r for r in rows if any(x in c.lower() for c in r["conditions"] for x in w)]


def condition_crosstab(rows: list[dict], top: int) -> list[dict]:
    """Per condition name: how many Variation IDs cite it and their collapsed classifications."""
    per: dict[str, Counter] = {}
    for r in rows:
        for c in set(r["conditions"]):
            per.setdefault(c, Counter())[bucket(r["germline"])] += 1
    ranked = sorted(per.items(), key=lambda kv: -sum(kv[1].values()))[:top]
    return [{"condition": c, "n": sum(cnt.values()), **{k: cnt.get(k, 0) for k in ("P/LP", "VUS", "B/LB", "Conflicting", "Other")}}
            for c, cnt in ranked]


def fmt_row(r: dict) -> str:
    stars = "*" * r["stars"] if r["stars"] is not None else "?"
    cond = "; ".join(r["conditions"][:3]) + (" ..." if len(r["conditions"]) > 3 else "")
    return f"  VCV{int(r['variation_id']):09d}  {r['germline']:<38} {stars:<4} {r['title']}  [{cond}]"


def run_gene(eu: Eutils, args) -> tuple[int, dict]:
    parts = [f"{args.gene}[gene]"]
    types = [t.strip() for t in args.type.split(",") if t.strip()]
    unknown = [t for t in types if t not in TYPE_TERMS]
    if unknown:
        raise ValueError(f"unknown --type {unknown}; choose from {', '.join(TYPE_TERMS)}")
    type_terms = [TYPE_TERMS[t] for t in types if TYPE_TERMS[t]]
    if type_terms:
        parts.append("(" + " OR ".join(type_terms) + ")")
    term = " AND ".join(parts)
    s = eu.search(term)
    rows = [classification(r) for r in eu.summaries(s)]
    rows = condition_filter(significance_filter(rows, args.significance), args.condition)
    counts = Counter(r["germline"] for r in rows)
    buckets = Counter(bucket(r["germline"]) for r in rows)
    xtab = condition_crosstab(rows, 10)
    scv_tab = scvs = None
    if args.submitters:
        scvs = eu.submissions([r["variation_id"] for r in rows])
        tab = Counter((x["submitter"], x["classification"]) for x in scvs if x["kind"] == "GermlineClassification")
        scv_tab = [{"submitter": k[0], "classification": k[1], "n_scv": v} for k, v in tab.most_common()]
    result = {"mode": "gene", "gene": args.gene, "types": types, "query": term, "query_translation": s["query_translation"],
              "n_variation_ids": s["count"], "n_after_filters": len(rows),
              "counts_by_germline_classification": dict(counts.most_common()), "counts_collapsed": dict(buckets),
              "by_condition": xtab, "by_submitter": scv_tab, "submissions": scvs, "records": rows[:args.limit]}
    if args.json:
        return 0, result
    n = len(rows)
    print(f"ClinVar  {args.gene}  type={','.join(types)}  query: {s['query_translation']}")
    print(f"  Variation IDs matched: {s['count']}" + (f"; after --significance/--condition filters: {n}" if args.significance or args.condition else ""))
    if n:
        print("  Germline classification (aggregate per Variation ID):")
        for k, v in counts.most_common():
            print(f"    {v:>5}  ({100 * v / n:5.1f}%)  {k}")
        print("  Collapsed: " + ", ".join(f"{k} {buckets.get(k, 0)}/{n} ({100 * buckets.get(k, 0) / n:.1f}%)" for k in ("P/LP", "VUS", "B/LB", "Conflicting", "Other")))
        print("  By condition (top 10; a Variation ID counts once per condition it cites):")
        print(f"    {'n':>5} {'P/LP':>5} {'VUS':>5} {'B/LB':>5} {'Confl':>5} {'Other':>5}  condition")
        for x in xtab:
            print(f"    {x['n']:>5} {x['P/LP']:>5} {x['VUS']:>5} {x['B/LB']:>5} {x['Conflicting']:>5} {x['Other']:>5}  {x['condition']}")
        if scv_tab is not None:
            print(f"  By submitter (germline SCVs across the {n} Variation IDs; top 15):")
            for x in scv_tab[:15]:
                print(f"    {x['n_scv']:>5}  {x['classification']:<40} {x['submitter']}")
        print(f"  First {min(args.limit, n)} records (ClinVar default order, most recent first):")
        for r in rows[:args.limit]:
            print(fmt_row(r))
    return 0, result


HGVS_RE = re.compile(r"^(?P<acc>[A-Z]{2}_\d+(?:\.\d+)?)(?:\([^)]+\))?:(?P<desc>[cgnmpr]\..+)$")


def run_variant(eu: Eutils, args) -> tuple[int, dict]:
    m = HGVS_RE.match(args.variant.strip())
    if not m:
        raise ValueError(f"'{args.variant}' is not accession:description HGVS (e.g. NM_006231.4:c.158_159del)")
    acc, desc = m.group("acc"), m.group("desc")
    position_term = None
    if args.position:
        pm = re.match(r"^(chr)?([0-9XYM]{1,2}):(\d+)$", args.position, re.I)
        if not pm:
            raise ValueError("--position must be chr:pos on GRCh38, e.g. 12:132681183")
        position_term = f"{pm.group(2).upper()}[chr] AND {pm.group(3)}[cpos]"
    found: dict[str, dict] = {}
    log = []

    def run(label: str, term: str) -> int:
        s = eu.search(term)
        rows = eu.summaries(s, limit=args.limit) if s["count"] else []
        log.append({"strategy": label, "query": s["query_translation"], "count": s["count"], "fetched": len(rows)})
        for r in rows:
            row = classification(r)
            row["matched_by"] = label
            found.setdefault(row["variation_id"], row)
        return s["count"]

    # exact HGVS on the requested transcript; if none, same c. description on another version of the
    # accession (and, with --gene, any transcript of that gene); then the positional sweep
    if not run("hgvs+accession", f"{desc}[varname] AND {acc}[All Fields]"):
        if not run("hgvs+accession-any-version", f"{desc}[varname] AND {acc.split('.')[0]}[All Fields]") and args.gene:
            run("hgvs+gene", f"{desc}[varname] AND {args.gene}[gene]")
    if position_term:
        run("position", position_term)
    exact = [r for r in found.values() if r["matched_by"] == "hgvs+accession"]
    scvs = eu.submissions(list(found)) if found else []
    result = {"mode": "variant", "variant": args.variant, "searches": log, "exact_match": bool(exact),
              "records": list(found.values()), "submissions": scvs}
    if args.json:
        return 0, result
    print(f"ClinVar  variant {args.variant}")
    for entry in log:
        more = entry["count"] - entry["fetched"]
        print(f"  search [{entry['strategy']}] {entry['query']} -> {entry['count']} record(s)"
              + (f" ({more} more not shown; raise --limit)" if more > 0 else ""))
    if not found:
        print("  ABSENT: no ClinVar record for this HGVS" + (" or position" if args.position else ""))
        return 0, result
    if not exact:
        print("  No exact record for this transcript HGVS; related records at the locus:")
    for r in found.values():
        mc = ",".join(r["molecular_consequence"]) or "-"
        print(f"  {r['accession']}  (Variation ID {r['variation_id']}; matched by {r['matched_by']})")
        print(f"    title:          {r['title']}")
        print(f"    germline:       {r['germline']}  [{r['review_status']}; {'*' * r['stars'] if r['stars'] is not None else '?'}; last evaluated {r['last_evaluated'] or 'n/a'}; {r['n_scv']} submission(s)]")
        print(f"    conditions:     {'; '.join(r['conditions']) or '-'}")
        print(f"    consequence:    {mc}  {r['protein_change']}")
        if r["oncogenicity"] or r["somatic_clinical_impact"]:
            print(f"    somatic:        oncogenicity={r['oncogenicity'] or '-'}; clinical impact={r['somatic_clinical_impact'] or '-'}")
        mine = [x for x in scvs if x["variation_id"] == r["variation_id"]]
        if mine:
            tally = Counter((x["classification"], x["submitter"]) for x in mine)
            shown = "; ".join(f"{c} ({s})" for (c, s), _ in tally.most_common(6))
            print(f"    submissions:    {shown}" + (" ..." if len(tally) > 6 else ""))
        print(f"    url:            {r['url']}")
    return 0, result


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gene", help="HGNC symbol: gene mode, or restricts the fallback search in variant mode")
    ap.add_argument("--variant", help="transcript HGVS, e.g. 'NM_006231.4:c.158_159del' (variant mode)")
    ap.add_argument("--type", default="truncating", help=f"gene mode: comma list of {', '.join(TYPE_TERMS)} (default truncating)")
    ap.add_argument("--significance", action="append", default=[],
                    help="gene mode: keep records whose classification matches; P/LP, VUS, B/LB, Conflicting match the collapsed "
                         "bucket exactly, any other value is a substring (so 'pathogenic' also keeps Likely pathogenic and "
                         "Conflicting ... of pathogenicity); repeatable")
    ap.add_argument("--condition", action="append", default=[],
                    help="gene mode: keep only records whose condition names contain this text (e.g. polyposis); repeatable")
    ap.add_argument("--submitters", action="store_true", help="gene mode: also tally submitter x classification at SCV level (one efetch per 100 records)")
    ap.add_argument("--position", help="variant mode: GRCh38 chr:pos for an additional positional search")
    ap.add_argument("--limit", type=int, default=20, help="records to list (default 20)")
    ap.add_argument("--api-key", default=os.environ.get("NCBI_API_KEY"), help="NCBI API key (or env NCBI_API_KEY)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if not args.gene and not args.variant:
        ap.error("one of --gene or --variant is required")
    eu = Eutils(args.api_key)
    try:
        code, result = run_variant(eu, args) if args.variant else run_gene(eu, args)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except ApiError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if args.json and code == 0:
        json.dump(result, sys.stdout, indent=2)
        print()
    return code


if __name__ == "__main__":
    sys.exit(main())
