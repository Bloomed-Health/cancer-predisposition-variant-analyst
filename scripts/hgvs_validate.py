#!/usr/bin/env python3
"""Validate a transcript-level HGVS variant and annotate its transcript consequences.

Pipeline (network, stdlib only):
  1. VariantValidator REST  -> normalized transcript HGVS, protein HGVS, genomic HGVS, VCF.
  2. Ensembl REST           -> ENST id, exon structure, cDNA/CDS sequence.
  3. Local computation      -> exon of variant, PTC codon (parsed from p. and re-derived by
                               re-translating the edited CDS), distance to the last exon-exon
                               junction, NMD call, fraction of protein lost, and a scan of
                               in-frame downstream AUGs with Kozak context (reinitiation).

Usage:
  python3 scripts/hgvs_validate.py 'NM_006231.4:c.158_159del'
  python3 scripts/hgvs_validate.py 'NM_007294.4:c.68_69del' --json
Exit status: 0 success, 1 variant rejected/not found, 2 network or data error
(argparse usage errors also exit 2).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse

from _http import request

TIMEOUT_S = 30
VV_BASE = "https://rest.variantvalidator.org/VariantValidator/variantvalidator"
ENSEMBL_BASE = {"GRCh38": "https://rest.ensembl.org", "GRCh37": "https://grch37.rest.ensembl.org"}
NMD_JUNCTION_NT = 55        # PTC > 50-55 nt upstream of the last junction -> NMD
START_PROXIMAL_NT = 150     # PTC within the first ~150 nt of CDS often escapes NMD (reinitiation)
START_BORDERLINE_NT = 200   # 150 < PTC <= 200 nt: borderline for the start-proximal effect
LONG_EXON_NT = 400          # PTC in a long exon reduces NMD efficiency (Lindeboom 2016/2019)

CODON_TABLE = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M", "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T", "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*", "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K", "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W", "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R", "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}
AA3 = {
    "A": "Ala", "R": "Arg", "N": "Asn", "D": "Asp", "C": "Cys", "Q": "Gln", "E": "Glu", "G": "Gly",
    "H": "His", "I": "Ile", "L": "Leu", "K": "Lys", "M": "Met", "F": "Phe", "P": "Pro", "S": "Ser",
    "T": "Thr", "W": "Trp", "Y": "Tyr", "V": "Val", "*": "Ter",
}


class LookupError_(Exception):
    """Raised for network failures or unusable payloads (exit 2)."""


def http_get(url: str, accept: str = "application/json", retries: int = 3):
    """GET with retry/back-off; None on 404; LookupError_ on any other failure."""
    try:
        resp = request(url, headers={"Accept": accept}, timeout=TIMEOUT_S, retries=retries)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise LookupError_(f"HTTP {e.code} from {url}: {e.read().decode('utf-8', 'replace')[:200]}")
    except (urllib.error.URLError, TimeoutError) as e:
        raise LookupError_(f"network error for {url}: {e}")
    body = resp.text()
    return json.loads(body) if accept == "application/json" else body


# ---------------------------------------------------------------- VariantValidator
def variantvalidator(hgvs: str, transcript: str, assembly: str) -> dict:
    url = f"{VV_BASE}/{assembly}/{urllib.parse.quote(hgvs, safe='')}/{urllib.parse.quote(transcript, safe='')}?content-type=application/json"
    data = http_get(url)
    if not isinstance(data, dict):
        raise LookupError_("VariantValidator returned no JSON")
    records = {k: v for k, v in data.items() if k not in ("flag", "metadata")}
    if data.get("flag") != "gene_variant" or not records:
        warnings = []
        for v in records.values():
            warnings.extend(v.get("validation_warnings") or [])
        raise ValueError(f"VariantValidator rejected '{hgvs}' (flag={data.get('flag')}): {'; '.join(warnings) or 'no detail'}")
    key = next((k for k in records if k.startswith(transcript)), next(iter(records)))
    rec = records[key]
    loci = rec.get("primary_assembly_loci") or {}
    locus = loci.get(assembly.lower()) or {}
    prot = rec.get("hgvs_predicted_protein_consequence") or {}
    nc = (locus.get("hgvs_genomic_description") or "").split(":")[0]
    exon_pos = (rec.get("variant_exonic_positions") or {}).get(nc) or {}
    return {
        "submitted": hgvs,
        "transcript_hgvs": rec.get("hgvs_transcript_variant"),
        "protein_hgvs": prot.get("tlr"),
        "protein_hgvs_short": prot.get("slr"),
        "genomic_hgvs": locus.get("hgvs_genomic_description"),
        "vcf": locus.get("vcf"),
        "gene_symbol": rec.get("gene_symbol"),
        "ensembl_gene_id": (rec.get("gene_ids") or {}).get("ensembl_gene_id"),
        "mane_select": (rec.get("annotations") or {}).get("mane_select"),
        "vv_exon": {"start": exon_pos.get("start_exon"), "end": exon_pos.get("end_exon")} if exon_pos else None,
        "validation_warnings": rec.get("validation_warnings") or [],
        "vv_version": (data.get("metadata") or {}).get("variantvalidator_version"),
    }


# ---------------------------------------------------------------- Ensembl
def ensembl_transcript_id(base: str, refseq: str, gene_symbol: str | None) -> str:
    for acc in (refseq, refseq.split(".")[0]):
        hits = http_get(f"{base}/xrefs/symbol/homo_sapiens/{acc}?object_type=transcript") or []
        ids = [h["id"] for h in hits if h.get("type") == "transcript"]
        if ids:
            return ids[0]
    if gene_symbol:
        gene = http_get(f"{base}/lookup/symbol/homo_sapiens/{gene_symbol}?expand=1") or {}
        for t in gene.get("Transcript", []):
            if t.get("is_canonical"):
                return t["id"]
    raise LookupError_(f"could not map {refseq} to an Ensembl transcript")


def ensembl_transcript_model(base: str, enst: str) -> dict:
    model = http_get(f"{base}/lookup/id/{enst}?expand=1")
    if not model or model.get("object_type") != "Transcript":
        raise LookupError_(f"Ensembl lookup failed for {enst}")
    cdna = http_get(f"{base}/sequence/id/{enst}?type=cdna", accept="text/plain")
    if not cdna:
        raise LookupError_(f"Ensembl sequence failed for {enst}")
    cdna = cdna.strip().upper()
    strand = model["strand"]
    exons = sorted(model["Exon"], key=lambda e: e["start"], reverse=(strand == -1))
    table, tx = [], 0
    for i, e in enumerate(exons, 1):
        length = e["end"] - e["start"] + 1
        table.append({"ordinal": i, "id": e["id"], "g_start": e["start"], "g_end": e["end"],
                      "tx_start": tx + 1, "tx_end": tx + length, "length": length})
        tx += length
    if tx != len(cdna):
        raise LookupError_(f"exon lengths ({tx}) do not match cDNA length ({len(cdna)}) for {enst}")
    tr = model.get("Translation")
    if not tr:
        raise LookupError_(f"{enst} has no translation (non-coding)")
    cds_g_start = tr["end"] if strand == -1 else tr["start"]
    cds_g_end = tr["start"] if strand == -1 else tr["end"]

    def g_to_tx(g: int) -> int:
        for ex in table:
            if ex["g_start"] <= g <= ex["g_end"]:
                return ex["tx_start"] + (ex["g_end"] - g if strand == -1 else g - ex["g_start"])
        raise LookupError_(f"genomic position {g} not exonic in {enst}")

    cds_tx_start, cds_tx_end = g_to_tx(cds_g_start), g_to_tx(cds_g_end)
    cds = cdna[cds_tx_start - 1:cds_tx_end]
    for ex in table:
        ex["c_start"] = ex["tx_start"] - cds_tx_start + 1
        ex["c_end"] = ex["tx_end"] - cds_tx_start + 1
    protein = translate(cds)
    notes = []
    if not cds.startswith("ATG"):
        notes.append("CDS does not start with ATG")
    if len(cds) % 3:
        notes.append("CDS length not a multiple of 3")
    if len(protein.rstrip("*")) != tr["length"]:
        notes.append(f"translated length {len(protein.rstrip('*'))} != Ensembl protein length {tr['length']}")
    return {
        "enst": enst, "display_name": model.get("display_name"), "version": model.get("version"),
        "strand": strand, "is_canonical": bool(model.get("is_canonical")), "chrom": model.get("seq_region_name"),
        "exons": table, "n_exons": len(table), "cdna": cdna, "cds": cds, "cds_tx_start": cds_tx_start,
        "cds_tx_end": cds_tx_end, "protein": protein, "protein_length": tr["length"], "notes": notes,
    }


def translate(seq: str) -> str:
    return "".join(CODON_TABLE.get(seq[i:i + 3], "X") for i in range(0, len(seq) - len(seq) % 3, 3))


# ---------------------------------------------------------------- HGVS c. parsing / editing
C_EDIT = re.compile(
    r"^c\.(?P<s>\d+)(?:_(?P<e>\d+))?"
    r"(?:(?P<kind>delins|del|dup|ins|inv)(?P<seq>[ACGTN]*)|(?P<ref>[ACGTN])>(?P<alt>[ACGTN]))$"
)


def parse_c(hgvs: str) -> dict | None:
    m = C_EDIT.match(hgvs.split(":", 1)[-1])
    if not m:
        return None
    s = int(m.group("s"))
    e = int(m.group("e")) if m.group("e") else s
    kind = m.group("kind") or "sub"
    return {"start": s, "end": e, "kind": kind, "seq": m.group("seq") or "", "ref": m.group("ref"), "alt": m.group("alt")}


def apply_edit(cds: str, ed: dict) -> tuple[str, list[str]]:
    s, e, k = ed["start"], ed["end"], ed["kind"]
    notes = []
    if e > len(cds):
        raise ValueError(f"c.{e} beyond CDS length {len(cds)}")
    ref = cds[s - 1:e]
    if k == "sub":
        if ref != ed["ref"]:
            notes.append(f"reference mismatch at c.{s}: transcript has {ref}, HGVS says {ed['ref']}")
        return cds[:s - 1] + ed["alt"] + cds[s:], notes
    if k in ("del", "dup", "delins") and ed["seq"] and k != "delins" and ref != ed["seq"]:
        notes.append(f"reference mismatch at c.{s}_{e}: transcript has {ref}, HGVS says {ed['seq']}")
    if k == "del":
        return cds[:s - 1] + cds[e:], notes
    if k == "dup":
        return cds[:e] + ref + cds[e:], notes
    if k == "ins":
        if e != s + 1:
            raise ValueError("ins requires adjacent positions c.X_X+1ins")
        return cds[:s] + ed["seq"] + cds[s:], notes
    if k == "delins":
        return cds[:s - 1] + ed["seq"] + cds[e:], notes
    if k == "inv":
        comp = str.maketrans("ACGT", "TGCA")
        return cds[:s - 1] + ref.translate(comp)[::-1] + cds[e:], notes
    raise ValueError(f"unsupported edit {k}")


P_FS = re.compile(r"p\.\(?([A-Z][a-z]{2}|[A-Z*])(\d+)([A-Z][a-z]{2}|[A-Z*])?fs(?:Ter|\*)(\d+|\?)\)?")
P_NONSENSE = re.compile(r"p\.\(?([A-Z][a-z]{2}|[A-Z])(\d+)(?:Ter|\*)\)?")


def ptc_from_protein_hgvs(p: str | None) -> dict | None:
    if not p:
        return None
    desc = p.split(":", 1)[-1]
    m = P_FS.search(desc)
    if m:
        pos = int(m.group(2))
        n = m.group(4)
        return {"type": "frameshift", "first_altered": pos, "ptc_codon": (pos + int(n) - 1) if n != "?" else None}
    m = P_NONSENSE.search(desc)
    if m:
        return {"type": "nonsense", "first_altered": int(m.group(2)), "ptc_codon": int(m.group(2))}
    return None


def _aa3(seq: str) -> str:
    return "".join(AA3.get(a, "Xaa") for a in seq)


def _res(prot: str, i: int) -> str:
    """Residue label, e.g. Phe508 (1-based codon i)."""
    return f"{AA3.get(prot[i - 1], 'Xaa')}{i}"


def protein_consequence(wt_prot: str, mut_prot: str, delta_nt: int) -> dict:
    """Compare the wild-type translation (ending in '*') with the mutant read-through translation.

    ``delta_nt`` is the CDS length change (mutant - wild type). Returns the derived protein HGVS,
    a consequence label, the computed PTC codon (None when the product ends at the native stop
    or is a C-terminal extension) and the first altered codon.
    """
    stop = mut_prot.find("*")
    ptc = stop + 1 if stop >= 0 else None
    inframe = delta_nt % 3 == 0
    native_stop = len(wt_prot) + delta_nt // 3 if inframe else None   # codon of the native stop in the mutant
    fd = next((i for i, (a, b) in enumerate(zip(wt_prot, mut_prot)) if a != b), None)
    out = {"first_altered": None if fd is None else fd + 1, "ptc_codon": ptc}
    if fd is None:
        out.update(protein_hgvs="p.(=)" if ptc == native_stop else "p.?", consequence="synonymous" if ptc == native_stop else "unknown")
        out["ptc_codon"] = None
        return out
    if ptc is None:
        out.update(protein_hgvs=f"p.({_res(wt_prot, fd + 1)}{AA3.get(mut_prot[fd], 'Xaa')}fs*?) [no stop found]", consequence="frameshift")
        return out
    if inframe and delta_nt == 0 and ptc == native_stop and wt_prot[fd + 1:] == mut_prot[fd + 1:ptc]:
        out.update(protein_hgvs=f"p.({_res(wt_prot, fd + 1)}{AA3[mut_prot[fd]]})", consequence="missense", ptc_codon=None)
        return out
    if mut_prot[fd] == "*" and not (inframe and delta_nt != 0 and ptc == native_stop):
        out.update(protein_hgvs=f"p.({_res(wt_prot, fd + 1)}Ter)", consequence="nonsense")
        return out
    if inframe and fd == len(wt_prot) - 1:
        out.update(protein_hgvs=f"p.(Ter{fd + 1}{AA3.get(mut_prot[fd], 'Xaa')}ext*{ptc - fd - 1})",
                   consequence="stop-loss (extension)", ptc_codon=None)
        return out
    if not inframe:
        out.update(protein_hgvs=f"p.({_res(wt_prot, fd + 1)}{AA3.get(mut_prot[fd], 'Xaa')}fs*{ptc - fd})", consequence="frameshift")
        return out
    # in-frame indel: align prefix (fd) and suffix, describe the differing span
    mut_t = mut_prot[:ptc]
    s = 0
    while s < min(len(wt_prot), len(mut_t)) - fd and wt_prot[-1 - s] == mut_t[-1 - s]:
        s += 1
    deleted, inserted = wt_prot[fd:len(wt_prot) - s], mut_t[fd:len(mut_t) - s]
    a, b = fd + 1, fd + len(deleted)
    if deleted and not inserted:
        desc = f"{_res(wt_prot, a)}del" if a == b else f"{_res(wt_prot, a)}_{_res(wt_prot, b)}del"
    elif inserted and not deleted:
        n = len(inserted)
        if fd >= n and wt_prot[fd - n:fd] == inserted:
            desc = f"{_res(wt_prot, fd)}dup" if n == 1 else f"{_res(wt_prot, fd - n + 1)}_{_res(wt_prot, fd)}dup"
        else:
            desc = f"{_res(wt_prot, fd)}_{_res(wt_prot, fd + 1)}ins{_aa3(inserted)}"
    else:
        desc = f"{_res(wt_prot, a)}delins{_aa3(inserted)}" if a == b else f"{_res(wt_prot, a)}_{_res(wt_prot, b)}delins{_aa3(inserted)}"
    truncated = ptc < native_stop
    kind = "in-frame indel" if delta_nt else "in-frame delins"
    out.update(protein_hgvs=f"p.({desc})", consequence=f"{kind} (premature stop)" if truncated else kind,
               ptc_codon=ptc if truncated else None)
    return out


# ---------------------------------------------------------------- annotation
def exon_for_c(exons: list[dict], c: int) -> dict | None:
    return next((ex for ex in exons if ex["c_start"] <= c <= ex["c_end"]), None)


def kozak_class(minus3: str, plus4: str) -> str:
    r3, g4 = minus3 in "AG", plus4 == "G"
    return "strong" if (r3 and g4) else ("adequate" if (r3 or g4) else "weak")


def reinitiation_scan(model: dict, ptc_codon: int, limit: int) -> dict:
    cds, cdna, off = model["cds"], model["cdna"], model["cds_tx_start"] - 1
    total = model["protein_length"]
    hits = []
    for codon in range(ptc_codon + 1, len(cds) // 3 + 1):
        i = (codon - 1) * 3
        if cds[i:i + 3] != "ATG":
            continue
        tx = off + i  # 0-based index of A in cDNA
        minus3 = cdna[tx - 3] if tx >= 3 else "N"
        plus4 = cdna[tx + 3] if tx + 3 < len(cdna) else "N"
        context = cdna[max(0, tx - 6):tx + 4]
        hits.append({
            "met_codon": codon, "codons_past_ptc": codon - ptc_codon, "context": context,
            "minus3": minus3, "plus4": plus4, "kozak": kozak_class(minus3, plus4),
            "product_aa": total - codon + 1, "fraction_retained": round((total - codon + 1) / total, 4),
        })
    first_strong = next((h["met_codon"] for h in hits if h["kozak"] == "strong"), None)
    return {"n_inframe_atg_downstream": len(hits), "first_strong_met": first_strong, "candidates": hits[:limit]}


def annotate(vv: dict, model: dict, max_met: int) -> dict:
    out: dict = {"notes": list(model["notes"])}
    exons, total_aa, n_exons = model["exons"], model["protein_length"], model["n_exons"]
    last_junction_tx = exons[-2]["tx_end"] if n_exons > 1 else None
    out["cds_length_nt"] = len(model["cds"])
    out["protein_length_aa"] = total_aa
    out["total_exons"] = n_exons

    ed = parse_c(vv["transcript_hgvs"] or vv["submitted"])
    out["edit"] = ed
    if ed:
        ex = exon_for_c(exons, ed["start"])
        out["variant_exon"] = ex["ordinal"] if ex else None
        out["variant_exon_c_range"] = [ex["c_start"], ex["c_end"]] if ex else None
    else:
        out["variant_exon"] = None
        out["notes"].append("c. description not in a supported coding form (intronic/UTR/complex); CDS re-translation skipped")
    if vv.get("vv_exon") and vv["vv_exon"].get("start"):
        out["variant_exon_variantvalidator"] = vv["vv_exon"]["start"]
        if out["variant_exon"] is not None and str(out["variant_exon"]) != str(vv["vv_exon"]["start"]):
            out["notes"].append(f"exon numbering differs: Ensembl ordinal {out['variant_exon']} vs VariantValidator {vv['vv_exon']['start']}")

    parsed = ptc_from_protein_hgvs(vv.get("protein_hgvs"))
    out["protein_hgvs_parsed"] = parsed
    ptc_hgvs = parsed["ptc_codon"] if parsed else None

    ptc_calc, derived_p = None, None
    if ed:
        try:
            mut_cds, notes = apply_edit(model["cds"], ed)
            out["notes"].extend(notes)
            # read through into the 3' UTR so frameshifts that pass the native stop still terminate
            mut_read = mut_cds + model["cdna"][model["cds_tx_end"]:]
            pc = protein_consequence(model["protein"], translate(mut_read), len(mut_cds) - len(model["cds"]))
            derived_p, ptc_calc = pc["protein_hgvs"], pc["ptc_codon"]
            out["consequence_computed"] = pc["consequence"]
            out["first_altered_codon_computed"] = pc["first_altered"]
        except ValueError as e:
            out["notes"].append(f"re-translation failed: {e}")
    out["ptc_codon_from_protein_hgvs"] = ptc_hgvs
    out["ptc_codon_computed"] = ptc_calc
    out["protein_hgvs_computed"] = derived_p
    if ptc_hgvs and ptc_calc and ptc_hgvs != ptc_calc:
        out["notes"].append(f"PTC mismatch: protein HGVS implies codon {ptc_hgvs}, re-translation gives {ptc_calc}")

    ptc = ptc_hgvs or ptc_calc
    truncating = ptc is not None and ptc <= total_aa
    out["is_truncating"] = truncating
    if not truncating:
        out["ptc_codon"] = None
        out["nmd"] = {"prediction": "not applicable (no premature termination codon)"}
        out["reinitiation"] = None
        return out

    out["ptc_codon"] = ptc
    ptc_c_first = (ptc - 1) * 3 + 1
    ptc_tx_last = model["cds_tx_start"] - 1 + ptc_c_first + 2  # 1-based tx coordinate of the stop codon's 3' nt
    ptc_ex = exon_for_c(exons, ptc_c_first)
    ptc_exon = ptc_ex["ordinal"] if ptc_ex else None
    dist = (last_junction_tx - ptc_tx_last) if last_junction_tx else None
    if n_exons == 1:
        pred, reason = "NMD escape predicted", "single-exon transcript"
    elif ptc_exon == n_exons:
        pred, reason = "NMD escape predicted", "PTC in the last exon"
    elif dist is not None and dist <= NMD_JUNCTION_NT:
        pred, reason = "NMD escape predicted", f"PTC {dist} nt upstream of the last exon-exon junction (<= {NMD_JUNCTION_NT} nt)"
    else:
        pred, reason = "NMD predicted", f"PTC {dist} nt upstream of the last exon-exon junction (> {NMD_JUNCTION_NT} nt)"
    flags = []
    if ptc_c_first <= START_PROXIMAL_NT:
        flags.append(f"start-proximal PTC (c.{ptc_c_first} <= {START_PROXIMAL_NT} nt): NMD often inefficient; reinitiation downstream possible")
    elif ptc_c_first <= START_BORDERLINE_NT:
        flags.append(f"borderline start-proximal PTC (c.{ptc_c_first}; {START_PROXIMAL_NT} < c. <= {START_BORDERLINE_NT} nt): reduced NMD efficiency and downstream reinitiation remain possible")
    if ptc_ex and ptc_ex["length"] > LONG_EXON_NT:
        flags.append(f"PTC in a long exon ({ptc_ex['length']} nt > {LONG_EXON_NT}): reduced NMD efficiency")
    out["nmd"] = {
        "prediction": pred, "reason": reason, "ptc_exon": ptc_exon, "total_exons": n_exons,
        "ptc_first_nt_c": ptc_c_first, "distance_to_last_junction_nt": dist, "efficiency_flags": flags,
        "rule": f"PTC > {NMD_JUNCTION_NT} nt upstream of the last exon-exon junction triggers NMD; last exon or penultimate exon within {NMD_JUNCTION_NT} nt escapes",
    }
    first_altered = (parsed or {}).get("first_altered") or out.get("first_altered_codon_computed") or ptc
    wt_retained = first_altered - 1
    out["truncation"] = {
        "wild_type_residues_retained": wt_retained,
        "fraction_wild_type_retained": round(wt_retained / total_aa, 4),
        "fraction_protein_lost": round(1 - wt_retained / total_aa, 4),
        "novel_frameshift_residues": (ptc - first_altered) if parsed and parsed["type"] == "frameshift" else 0,
        "truncated_product_length_aa": ptc - 1,
    }
    out["reinitiation"] = reinitiation_scan(model, ptc, max_met)
    return out


# ---------------------------------------------------------------- output
def pct(x: float) -> str:
    return f"{100 * x:.1f}%"


def print_report(res: dict) -> None:
    vv, m, a = res["variantvalidator"], res["ensembl"], res["annotation"]
    print(f"Submitted:            {vv['submitted']}")
    print(f"Transcript HGVS:      {vv['transcript_hgvs']}  (gene {vv['gene_symbol']}, MANE Select: {vv['mane_select']})")
    print(f"Protein HGVS (VV):    {vv['protein_hgvs']}  [{vv['protein_hgvs_short']}]")
    print(f"Genomic HGVS:         {vv['genomic_hgvs']}")
    if vv.get("vcf"):
        v = vv["vcf"]
        print(f"VCF ({res['assembly']}):        {v['chr']}-{v['pos']}-{v['ref']}-{v['alt']}")
    print(f"Ensembl transcript:   {m['enst']}.{m['version']} ({m['display_name']}, strand {'+' if m['strand'] == 1 else '-'}, canonical={m['is_canonical']})")
    print(f"CDS / protein:        {a['cds_length_nt']} nt / {a['protein_length_aa']} aa; {a['total_exons']} exons")
    ve = a.get("variant_exon")
    rng = a.get("variant_exon_c_range")
    print(f"Variant exon:         {ve} of {a['total_exons']}" + (f"  (exon spans c.{rng[0]}-c.{rng[1]})" if rng else "")
          + (f"; VariantValidator exon {a['variant_exon_variantvalidator']}" if a.get("variant_exon_variantvalidator") else ""))
    print(f"Protein HGVS (calc):  {a.get('protein_hgvs_computed')}" + (f"  [{a['consequence_computed']}]" if a.get("consequence_computed") else ""))
    print(f"PTC codon:            parsed={a.get('ptc_codon_from_protein_hgvs')}  computed={a.get('ptc_codon_computed')}")
    if a.get("is_truncating"):
        t, n = a["truncation"], a["nmd"]
        print(f"Truncation:           {t['wild_type_residues_retained']} WT residues retained ({pct(t['fraction_wild_type_retained'])} of {a['protein_length_aa']}), "
              f"{pct(t['fraction_protein_lost'])} lost; +{t['novel_frameshift_residues']} frameshift residues; product {t['truncated_product_length_aa']} aa")
        print(f"NMD:                  {n['prediction']} -- {n['reason']}; PTC in exon {n['ptc_exon']}/{n['total_exons']}, first nt c.{n['ptc_first_nt_c']}")
        for f in n["efficiency_flags"]:
            print(f"                      flag: {f}")
        r = a["reinitiation"]
        first_strong = f"Met{r['first_strong_met']}" if r["first_strong_met"] else "none"
        print(f"Reinitiation scan:    {r['n_inframe_atg_downstream']} in-frame ATG downstream of PTC; first strong Kozak: {first_strong}")
        print("  Met     +codons  context(-6..+4)  -3  +4  Kozak     product_aa  retained")
        for h in r["candidates"]:
            print(f"  Met{h['met_codon']:<5} {h['codons_past_ptc']:>7}  {h['context']:<15} {h['minus3']:>2}  {h['plus4']:>2}  {h['kozak']:<9} {h['product_aa']:>10}  {pct(h['fraction_retained'])}")
    else:
        print(f"NMD:                  {a['nmd']['prediction']}")
    for w in vv.get("validation_warnings") or []:
        print(f"VV warning:           {w}")
    for note in a["notes"]:
        print(f"Note:                 {note}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("hgvs", help="transcript HGVS, e.g. NM_006231.4:c.158_159del")
    ap.add_argument("--assembly", default="GRCh38", choices=["GRCh38", "GRCh37"])
    ap.add_argument("--transcript", help="transcript to report on (default: accession in HGVS)")
    ap.add_argument("--max-met", type=int, default=10, help="downstream AUGs to list (default 10)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = ap.parse_args(argv)

    transcript = args.transcript or args.hgvs.split(":", 1)[0]
    try:
        vv = variantvalidator(args.hgvs, transcript, args.assembly)
        base = ENSEMBL_BASE[args.assembly]
        enst = ensembl_transcript_id(base, transcript, vv["gene_symbol"])
        model = ensembl_transcript_model(base, enst)
        ann = annotate(vv, model, args.max_met)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except LookupError_ as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    result = {
        "assembly": args.assembly, "variantvalidator": vv,
        "ensembl": {k: v for k, v in model.items() if k not in ("cdna", "cds", "protein", "exons")},
        "annotation": ann,
    }
    if args.json:
        json.dump(result, sys.stdout, indent=2)
        print()
    else:
        print_report(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
