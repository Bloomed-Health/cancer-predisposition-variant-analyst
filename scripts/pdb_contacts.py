#!/usr/bin/env python3
"""Residue-contact census for a segment of a PDB chain (stdlib only).

Downloads the mmCIF for a PDB entry from RCSB, selects one polymer chain by
author chain ID, and lists every residue outside a query segment that has a
heavy atom within --cutoff angstroms of any heavy atom of a segment residue.
Partners are bucketed into user-defined sequence regions so that the output
answers questions like "does the POLE N-terminal helix touch the exonuclease
domain?" without a structure viewer.

Examples:
  python3 scripts/pdb_contacts.py 9B8S --chain A --segment 25-65 \
      --regions NTD:1-270,exo:268-471,pol:472-1180,CTD:1181-2286
  python3 scripts/pdb_contacts.py 9B8S --chain A --segment 25-65 --json

Numbering is the author (auth_seq_id) numbering of the entry; for 9B8S that is
UniProt Q07864 numbering. Residues absent from the model are reported.
Exit status: 0 success, 1 bad input or entry/chain not found, 2 network error
(argparse usage errors exit 2 as well).
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
import urllib.error
from typing import Dict, List, Tuple

from _http import request

RCSB_FILES = "https://files.rcsb.org/download/{pdb}.cif"


def parse_range(text: str) -> Tuple[int, int]:
    lo, _, hi = text.partition("-")
    try:
        a, b = int(lo), int(hi or lo)
    except ValueError:
        raise argparse.ArgumentTypeError(f"bad range {text!r}; expected N-M")
    if a > b:
        a, b = b, a
    return a, b


def parse_regions(text: str) -> List[Tuple[str, int, int]]:
    out = []
    for item in filter(None, (s.strip() for s in text.split(","))):
        name, _, rng = item.partition(":")
        if not rng:
            raise argparse.ArgumentTypeError(f"bad region {item!r}; expected name:N-M")
        a, b = parse_range(rng)
        out.append((name, a, b))
    return out


def load_atoms(cif_text: str, chain: str):
    """Return {resnum: (resname, [(x, y, z), ...])} for heavy ATOM records of one author chain."""
    cols: List[str] = []
    residues: Dict[int, Tuple[str, List[Tuple[float, float, float]]]] = {}
    in_loop = False
    for line in cif_text.splitlines():
        if line.startswith("_atom_site."):
            cols.append(line.strip().split(".", 1)[1])
            in_loop = True
            continue
        if not in_loop:
            continue
        if line.startswith("#"):
            if residues:
                break
            continue
        if not (line.startswith("ATOM") or line.startswith("HETATM")):
            continue
        f = line.split()
        if len(f) < len(cols):
            continue
        rec = dict(zip(cols, f))
        if rec.get("group_PDB") != "ATOM" or rec.get("auth_asym_id") != chain:
            continue
        if rec.get("type_symbol", "").upper() == "H":
            continue
        try:
            num = int(rec["auth_seq_id"])
            xyz = (float(rec["Cartn_x"]), float(rec["Cartn_y"]), float(rec["Cartn_z"]))
        except (KeyError, ValueError):
            continue
        name, atoms = residues.setdefault(num, (rec.get("label_comp_id", "?"), []))
        atoms.append(xyz)
    return residues


def residues_touch(a: List[Tuple[float, float, float]], b: List[Tuple[float, float, float]], cut: float) -> float | None:
    """Minimum heavy-atom distance if below cut, else None."""
    cut2 = cut * cut
    best = None
    for x1, y1, z1 in a:
        for x2, y2, z2 in b:
            dx = x1 - x2
            if dx > cut or dx < -cut:
                continue
            dy = y1 - y2
            if dy > cut or dy < -cut:
                continue
            dz = z1 - z2
            d2 = dx * dx + dy * dy + dz * dz
            if d2 < cut2 and (best is None or d2 < best):
                best = d2
    return None if best is None else best ** 0.5


def region_of(n: int, regions: List[Tuple[str, int, int]]) -> str:
    for name, a, b in regions:
        if a <= n <= b:
            return name
    return "other"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdb", help="4-character PDB ID, e.g. 9B8S")
    ap.add_argument("--chain", default="A", help="author chain ID (default A)")
    ap.add_argument("--segment", type=parse_range, required=True, help="query residue range N-M (author numbering)")
    ap.add_argument("--cutoff", type=float, default=4.0, help="heavy-atom distance cutoff in angstroms (default 4.0)")
    ap.add_argument("--regions", type=parse_regions, default=[], help="comma list name:N-M used to bucket partner residues")
    ap.add_argument("--exclude-neighbours", type=int, default=2, help="ignore partners within this many residues of the segment ends (default 2)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)

    pdb = args.pdb.strip().upper()
    if len(pdb) != 4 or not pdb.isalnum():
        print(f"error: {args.pdb!r} is not a PDB ID", file=sys.stderr)
        return 1
    try:
        body = request(RCSB_FILES.format(pdb=pdb), timeout=60).body
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            print(f"error: PDB entry {pdb} not found", file=sys.stderr)
            return 1
        print(f"error: RCSB download failed: HTTP {exc.code}", file=sys.stderr)
        return 2
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"error: network: {exc}", file=sys.stderr)
        return 2

    residues = load_atoms(body.decode("utf-8", "replace"), args.chain)
    if not residues:
        print(f"error: no ATOM records for chain {args.chain!r} in {pdb}", file=sys.stderr)
        return 1

    lo, hi = args.segment
    modeled = sorted(n for n in residues if lo <= n <= hi)
    missing = [n for n in range(lo, hi + 1) if n not in residues]
    all_nums = sorted(residues)
    pad = args.exclude_neighbours

    contacts = {}
    for n1 in modeled:
        partners = []
        for n2 in all_nums:
            if lo - pad <= n2 <= hi + pad:
                continue
            d = residues_touch(residues[n1][1], residues[n2][1], args.cutoff)
            if d is not None:
                partners.append((n2, residues[n2][0], round(d, 2), region_of(n2, args.regions)))
        if partners:
            contacts[n1] = partners

    by_region: collections.Counter = collections.Counter()
    partner_set: Dict[str, set] = collections.defaultdict(set)
    for n1, plist in contacts.items():
        for n2, _, _, reg in plist:
            by_region[reg] += 1
            partner_set[reg].add(n2)

    result = {
        "pdb": pdb,
        "chain": args.chain,
        "segment": [lo, hi],
        "cutoff": args.cutoff,
        "modeled_range": [all_nums[0], all_nums[-1]],
        "segment_modeled": modeled,
        "segment_missing": missing,
        "contacts": {
            str(n1): [{"res": n2, "name": nm, "min_dist": d, "region": reg} for n2, nm, d, reg in plist]
            for n1, plist in contacts.items()
        },
        "pair_counts_by_region": dict(by_region),
        "partner_residues_by_region": {k: sorted(v) for k, v in partner_set.items()},
    }
    if args.json:
        json.dump(result, sys.stdout, indent=2)
        print()
        return 0

    print(f"{pdb} chain {args.chain}: modeled residues {all_nums[0]}-{all_nums[-1]} ({len(all_nums)} residues)")
    print(f"segment {lo}-{hi}: {len(modeled)} modeled, missing {missing if missing else 'none'}")
    print(f"heavy-atom cutoff {args.cutoff} A; partners within {pad} residues of the segment ends ignored")
    print()
    for n1 in modeled:
        plist = contacts.get(n1)
        if not plist:
            continue
        regs = collections.Counter(reg for *_, reg in plist)
        detail = ", ".join(f"{nm}{n2}({d})" for n2, nm, d, _ in plist)
        print(f"  {residues[n1][0]}{n1:<5} {len(plist):2d} partners  {dict(regs)}  {detail}")
    print()
    print("residue-pair contacts by region:", dict(by_region) or "none")
    for reg, s in sorted(partner_set.items()):
        print(f"  {reg}: partner residues {sorted(s)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
