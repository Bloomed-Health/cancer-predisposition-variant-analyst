#!/usr/bin/env python3
"""Query the gnomAD GraphQL API for variant allele counts or gene constraint.

Variant mode:
  python3 scripts/gnomad_lookup.py --variant 12-132681182-TCA-T
      prints exome / genome / joint AC, AN, AF, homozygotes, filters, popmax FAF; if the
      variant is absent, prints coverage at the position so "absent" can be interpreted.
      Add --variant-grch37 12-133257768-TCA-T to also query the v2.1.1 non-cancer subset
      (gnomAD v4 does not expose a non-cancer subset through the API).
Gene mode:
  python3 scripts/gnomad_lookup.py --gene POLE
      prints constraint: pLI, o/e LoF with 90% CI (upper bound = LOEUF), o/e missense, z-scores.

Variant IDs are gnomAD style chrom-pos-ref-alt (VCF-normalized, left-anchored base included);
take them from VariantValidator's `vcf` block or `hgvs_validate.py`.
Exit status: 0 success (including "variant absent"), 1 not found/invalid, 2 network error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request

USER_AGENT = "cancer-predisposition-variant-analyst/2.0 (gnomad_lookup.py; +https://github.com)"
TIMEOUT_S = 30
API = "https://gnomad.broadinstitute.org/api"
VARIANT_RE = re.compile(r"^(chr)?([0-9]{1,2}|X|Y|M|MT)-(\d+)-([ACGTN]+)-([ACGTN]+)$", re.I)

VARIANT_QUERY = """
query ($variantId: String!, $dataset: DatasetId!) {
  variant(variantId: $variantId, dataset: $dataset) {
    variant_id reference_genome rsids flags
    exome  { ac an af homozygote_count hemizygote_count filters faf95 { popmax popmax_population } }
    genome { ac an af homozygote_count hemizygote_count filters faf95 { popmax popmax_population } }
    joint  { ac an homozygote_count hemizygote_count filters }
  }
}"""
COVERAGE_QUERY = """
query ($chrom: String!, $start: Int!, $stop: Int!, $ref: ReferenceGenomeId!, $dataset: DatasetId!) {
  region(chrom: $chrom, start: $start, stop: $stop, reference_genome: $ref) {
    coverage(dataset: $dataset) { exome { pos mean median over_20 } genome { pos mean median over_20 } }
  }
}"""
GENE_QUERY = """
query ($symbol: String!, $ref: ReferenceGenomeId!) {
  gene(gene_symbol: $symbol, reference_genome: $ref) {
    gene_id symbol canonical_transcript_id
    mane_select_transcript { ensembl_id refseq_id }
    gnomad_constraint {
      pli oe_lof oe_lof_lower oe_lof_upper oe_mis oe_mis_lower oe_mis_upper oe_syn
      lof_z mis_z syn_z exp_lof obs_lof exp_mis obs_mis exp_syn obs_syn flags
    }
  }
}"""
# dataset -> reference genome; subsets that carry a non-cancer flavour
DATASET_GENOME = {
    "gnomad_r4": "GRCh38", "gnomad_r4_non_ukb": "GRCh38", "gnomad_r3": "GRCh38", "gnomad_r3_non_cancer": "GRCh38",
    "gnomad_r2_1": "GRCh37", "gnomad_r2_1_non_cancer": "GRCh37", "exac": "GRCh37",
}


class ApiError(Exception):
    pass


def graphql(query: str, variables: dict) -> dict:
    payload = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(API, data=payload, method="POST",
                                 headers={"User-Agent": USER_AGENT, "Content-Type": "application/json", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise ApiError(f"HTTP {e.code} from gnomAD API: {e.read().decode('utf-8', 'replace')[:300]}")
    except (urllib.error.URLError, TimeoutError) as e:
        raise ApiError(f"network error contacting gnomAD API: {e}")


def normalize_variant_id(v: str) -> str:
    m = VARIANT_RE.match(v.strip())
    if not m:
        raise ValueError(f"'{v}' is not chrom-pos-ref-alt (e.g. 12-132681182-TCA-T)")
    chrom = m.group(2).upper()
    return f"{chrom}-{m.group(3)}-{m.group(4).upper()}-{m.group(5).upper()}"


def fetch_variant(variant_id: str, dataset: str) -> dict | None:
    data = graphql(VARIANT_QUERY, {"variantId": variant_id, "dataset": dataset})
    errors = data.get("errors") or []
    if any("not found" in (e.get("message") or "").lower() for e in errors):
        return None
    if errors:
        raise ApiError("; ".join(e.get("message", "") for e in errors))
    return (data.get("data") or {}).get("variant")


def fetch_coverage(variant_id: str, dataset: str) -> dict:
    chrom, pos = variant_id.split("-")[0], int(variant_id.split("-")[1])
    ref = DATASET_GENOME.get(dataset, "GRCh38")
    data = graphql(COVERAGE_QUERY, {"chrom": chrom, "start": pos, "stop": pos + 1, "ref": ref, "dataset": dataset})
    cov = (((data.get("data") or {}).get("region") or {}).get("coverage")) or {}
    out = {}
    for kind in ("exome", "genome"):
        rows = [r for r in (cov.get(kind) or []) if r.get("pos") == pos]
        out[kind] = rows[0] if rows else None
    return out


def fetch_gene(symbol: str, ref: str) -> dict | None:
    data = graphql(GENE_QUERY, {"symbol": symbol, "ref": ref})
    errors = data.get("errors") or []
    gene = (data.get("data") or {}).get("gene")
    if gene is None:
        if any("not found" in (e.get("message") or "").lower() for e in errors):
            return None
        if errors:
            raise ApiError("; ".join(e.get("message", "") for e in errors))
        return None
    return gene


def print_freq(label: str, block: dict | None) -> None:
    if not block:
        print(f"  {label:<8} no data")
        return
    af = block.get("af") if block.get("af") is not None else (block["ac"] / block["an"] if block.get("an") else None)
    faf = block.get("faf95") or {}
    extra = f"  popmax FAF95={faf.get('popmax'):.3g} ({faf.get('popmax_population')})" if faf.get("popmax") else ""
    print(f"  {label:<8} AC={block.get('ac')} AN={block.get('an')} AF={af if af is None else f'{af:.3g}'} "
          f"hom={block.get('homozygote_count')} filters={block.get('filters') or 'PASS'}{extra}")


def run_variant(args) -> tuple[int, dict]:
    vid = normalize_variant_id(args.variant)
    result = {"mode": "variant", "variant_id": vid, "dataset": args.dataset, "found": False, "variant": None,
              "coverage": None, "non_cancer": None}
    var = fetch_variant(vid, args.dataset)
    if var:
        result["found"] = True
        result["variant"] = var
    else:
        result["coverage"] = fetch_coverage(vid, args.dataset)
    if args.variant_grch37:
        vid37 = normalize_variant_id(args.variant_grch37)
        nc = fetch_variant(vid37, "gnomad_r2_1_non_cancer")
        result["non_cancer"] = {"dataset": "gnomad_r2_1_non_cancer", "variant_id": vid37, "found": nc is not None, "variant": nc}
    if args.json:
        return 0, result
    print(f"gnomAD {args.dataset}  variant {vid}")
    if var:
        if var.get("rsids"):
            print(f"  rsIDs: {', '.join(var['rsids'])}")
        print_freq("exome", var.get("exome"))
        print_freq("genome", var.get("genome"))
        print_freq("joint", var.get("joint"))
        if var.get("flags"):
            print(f"  flags: {var['flags']}")
    else:
        print("  ABSENT (not in this dataset)")
        for kind in ("exome", "genome"):
            c = (result["coverage"] or {}).get(kind)
            if c:
                print(f"  {kind} coverage at pos: mean depth {c['mean']:.1f}, median {c['median']}, fraction >20x {c['over_20']:.2f}")
            else:
                print(f"  {kind} coverage at pos: no data")
    if result["non_cancer"]:
        nc = result["non_cancer"]
        print(f"gnomAD v2.1.1 non-cancer subset  variant {nc['variant_id']} (GRCh37)")
        if nc["found"]:
            print_freq("exome", nc["variant"].get("exome"))
            print_freq("genome", nc["variant"].get("genome"))
        else:
            print("  ABSENT")
    return 0, result


def run_gene(args) -> tuple[int, dict]:
    ref = DATASET_GENOME.get(args.dataset, "GRCh38")
    gene = fetch_gene(args.gene, ref)
    if gene is None:
        print(f"error: gene '{args.gene}' not found in gnomAD ({ref})", file=sys.stderr)
        return 1, {}
    result = {"mode": "gene", "reference_genome": ref, "gene": gene}
    if args.json:
        return 0, result
    c = gene.get("gnomad_constraint") or {}
    mane = gene.get("mane_select_transcript") or {}
    print(f"gnomAD constraint  {gene['symbol']} ({gene['gene_id']}; canonical {gene.get('canonical_transcript_id')}; "
          f"MANE {mane.get('ensembl_id')}/{mane.get('refseq_id')}; {ref})")
    if not c:
        print("  no constraint record")
        return 0, result

    def f(x, nd=3):
        return "n/a" if x is None else f"{x:.{nd}f}"

    print(f"  pLI            {c.get('pli'):.3g}" if c.get("pli") is not None else "  pLI            n/a")
    print(f"  LoF   o/e      {f(c.get('oe_lof'), 2)}  (90% CI {f(c.get('oe_lof_lower'), 2)}-{f(c.get('oe_lof_upper'), 2)}; LOEUF = {f(c.get('oe_lof_upper'), 2)})  obs/exp {c.get('obs_lof')}/{f(c.get('exp_lof'), 1)}  z={f(c.get('lof_z'), 2)}")
    print(f"  Missense o/e   {f(c.get('oe_mis'), 2)}  (90% CI {f(c.get('oe_mis_lower'), 2)}-{f(c.get('oe_mis_upper'), 2)})  obs/exp {c.get('obs_mis')}/{f(c.get('exp_mis'), 1)}  z={f(c.get('mis_z'), 2)}")
    print(f"  Synonymous o/e {f(c.get('oe_syn'), 2)}  obs/exp {c.get('obs_syn')}/{f(c.get('exp_syn'), 1)}  z={f(c.get('syn_z'), 2)}")
    if c.get("flags"):
        print(f"  flags: {c['flags']}")
    print("  Interpretation: LOEUF < 0.6 (or pLI > 0.9) = LoF-intolerant; LOEUF around 1 = LoF tolerated at haploid dose.")
    return 0, result


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--variant", help="chrom-pos-ref-alt (assembly of --dataset; GRCh38 for gnomad_r4)")
    g.add_argument("--gene", help="HGNC symbol, e.g. POLE")
    ap.add_argument("--dataset", default="gnomad_r4", choices=sorted(DATASET_GENOME), help="default gnomad_r4")
    ap.add_argument("--variant-grch37", help="GRCh37 chrom-pos-ref-alt to also query gnomad_r2_1_non_cancer")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        code, result = run_variant(args) if args.variant else run_gene(args)
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
