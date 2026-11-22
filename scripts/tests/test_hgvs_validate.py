"""Offline unit tests for hgvs_validate.py on a toy 3-exon transcript (no network).

Run: python3 -m unittest discover -s scripts/tests
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import hgvs_validate as hv  # noqa: E402

# Toy transcript: 6 nt 5'UTR, 36-codon CDS (35 aa + stop), 15 nt 3'UTR with stops in every frame.
#   codon  1 ATG c.1-3      2 AAA c.4-6      3 TTT c.7-9     4 GGG c.10-12    5 CCC c.13-15
#   codons 6-9 GCT c.16-27   10 CTA c.28-30 (TAG in the -1 frame)  11-29 GCT c.31-87
#   codon 30 GAG c.88-90   31 GAC c.91-93   32 AAG c.94-96
#   codon 33 ATG c.97-99   34 GCC c.100-102  35 AAG c.103-105  stop TAA c.106-108
UTR5 = "GGGGGG"
CDS = "ATGAAATTTGGGCCC" + "GCT" * 4 + "CTAGCT" + "GCT" * 18 + "GAGGACAAGATGGCCAAGTAA"
UTR3 = "GTTAATTAATTAAGC"
CDNA = UTR5 + CDS + UTR3
EXON_LENGTHS = (16, 86, 27)   # exon1 c.-6..10, exon2 c.11-96, exon3 c.97-123; last junction at tx 102


def toy_model(exon_lengths=EXON_LENGTHS) -> dict:
    assert sum(exon_lengths) == len(CDNA)
    cds_tx_start = len(UTR5) + 1
    exons, tx = [], 0
    for i, length in enumerate(exon_lengths, 1):
        exons.append({"ordinal": i, "tx_start": tx + 1, "tx_end": tx + length, "length": length,
                      "c_start": tx + 1 - cds_tx_start + 1, "c_end": tx + length - cds_tx_start + 1})
        tx += length
    protein = hv.translate(CDS)
    return {"exons": exons, "n_exons": len(exons), "cdna": CDNA, "cds": CDS, "cds_tx_start": cds_tx_start,
            "cds_tx_end": cds_tx_start + len(CDS) - 1, "protein": protein,
            "protein_length": len(protein.rstrip("*")), "notes": []}


def vv(c_hgvs: str, protein_hgvs: str | None = None) -> dict:
    return {"submitted": c_hgvs, "transcript_hgvs": c_hgvs, "protein_hgvs": protein_hgvs, "vv_exon": None}


class TranslateTests(unittest.TestCase):
    def test_translate_toy_cds(self):
        self.assertEqual(hv.translate(CDS), "MKFGP" + "AAAAL" + "A" * 19 + "EDKMAK*")

    def test_translate_ignores_trailing_partial_codon_and_marks_unknown(self):
        self.assertEqual(hv.translate("ATGNNNAA"), "MX")


class ParseCTests(unittest.TestCase):
    def test_forms(self):
        self.assertEqual(hv.parse_c("NM_1.1:c.4A>T"), {"start": 4, "end": 4, "kind": "sub", "seq": "", "ref": "A", "alt": "T"})
        self.assertEqual(hv.parse_c("c.7_9del")["kind"], "del")
        self.assertEqual(hv.parse_c("c.7_9delTTT")["seq"], "TTT")
        self.assertEqual(hv.parse_c("c.4dup"), {"start": 4, "end": 4, "kind": "dup", "seq": "", "ref": None, "alt": None})
        self.assertEqual(hv.parse_c("c.4_5insGGG")["kind"], "ins")
        self.assertEqual(hv.parse_c("c.4_6delinsGGG")["kind"], "delins")
        self.assertEqual(hv.parse_c("c.4_6inv")["kind"], "inv")

    def test_unsupported_forms_return_none(self):
        for h in ("c.10+1G>A", "c.-5A>G", "c.*3del", "c.4_6del;c.9A>T", "p.(Lys2Ter)", "c.4A>T;"):
            self.assertIsNone(hv.parse_c(h), h)


class ApplyEditTests(unittest.TestCase):
    def test_sub_and_reference_mismatch_note(self):
        mut, notes = hv.apply_edit(CDS, hv.parse_c("c.4A>T"))
        self.assertEqual(mut[3], "T")
        self.assertEqual(notes, [])
        _, notes = hv.apply_edit(CDS, hv.parse_c("c.4G>T"))
        self.assertIn("reference mismatch at c.4", notes[0])

    def test_del_dup_ins_delins_inv(self):
        self.assertEqual(hv.apply_edit(CDS, hv.parse_c("c.7_9del"))[0], CDS[:6] + CDS[9:])
        self.assertEqual(hv.apply_edit(CDS, hv.parse_c("c.4dup"))[0], CDS[:4] + "A" + CDS[4:])
        self.assertEqual(hv.apply_edit(CDS, hv.parse_c("c.3_4insCCC"))[0], CDS[:3] + "CCC" + CDS[3:])
        self.assertEqual(hv.apply_edit(CDS, hv.parse_c("c.4_6delinsGGG"))[0], CDS[:3] + "GGG" + CDS[6:])
        self.assertEqual(hv.apply_edit(CDS, hv.parse_c("c.7_9inv"))[0][6:9], "AAA")
        _, notes = hv.apply_edit(CDS, hv.parse_c("c.7_9delAAA"))
        self.assertIn("reference mismatch", notes[0])

    def test_errors(self):
        with self.assertRaises(ValueError):
            hv.apply_edit(CDS, hv.parse_c("c.4_200del"))
        with self.assertRaises(ValueError):
            hv.apply_edit(CDS, hv.parse_c("c.4_6insA"))


class PtcFromProteinHgvsTests(unittest.TestCase):
    def test_frameshift_and_nonsense(self):
        self.assertEqual(hv.ptc_from_protein_hgvs("NP_006222.2:p.(Leu53GlnfsTer5)"),
                         {"type": "frameshift", "first_altered": 53, "ptc_codon": 57})
        self.assertEqual(hv.ptc_from_protein_hgvs("p.(L53Qfs*5)")["ptc_codon"], 57)
        self.assertEqual(hv.ptc_from_protein_hgvs("p.(Arg342Ter)"), {"type": "nonsense", "first_altered": 342, "ptc_codon": 342})
        self.assertEqual(hv.ptc_from_protein_hgvs("p.(R342*)")["ptc_codon"], 342)
        self.assertIsNone(hv.ptc_from_protein_hgvs("p.(Glu23ValfsTer?)")["ptc_codon"])

    def test_non_truncating_forms_return_none(self):
        for p in (None, "", "p.(Phe3Ile)", "p.(Phe508del)", "p.(Ter394ArgextTer9)", "p.(=)", "p.?"):
            self.assertIsNone(hv.ptc_from_protein_hgvs(p), p)


class KozakTests(unittest.TestCase):
    def test_classes(self):
        self.assertEqual(hv.kozak_class("A", "G"), "strong")
        self.assertEqual(hv.kozak_class("G", "G"), "strong")
        self.assertEqual(hv.kozak_class("A", "C"), "adequate")
        self.assertEqual(hv.kozak_class("T", "G"), "adequate")
        self.assertEqual(hv.kozak_class("T", "A"), "weak")
        self.assertEqual(hv.kozak_class("N", "N"), "weak")


class ReinitiationScanTests(unittest.TestCase):
    def test_scan_finds_downstream_inframe_atg_with_context(self):
        r = hv.reinitiation_scan(toy_model(), ptc_codon=2, limit=10)
        self.assertEqual(r["n_inframe_atg_downstream"], 1)
        self.assertEqual(r["first_strong_met"], 33)
        hit = r["candidates"][0]
        self.assertEqual(hit["met_codon"], 33)
        self.assertEqual(hit["codons_past_ptc"], 31)
        self.assertEqual((hit["minus3"], hit["plus4"], hit["kozak"]), ("A", "G", "strong"))
        self.assertEqual(hit["context"], "GACAAGATGG")   # cDNA -6..+4 around the A of ATG
        self.assertEqual(hit["product_aa"], 3)
        self.assertAlmostEqual(hit["fraction_retained"], 3 / 35, places=4)

    def test_scan_respects_limit_and_ptc(self):
        r = hv.reinitiation_scan(toy_model(), ptc_codon=33, limit=10)
        self.assertEqual(r["n_inframe_atg_downstream"], 0)
        self.assertIsNone(r["first_strong_met"])


class ProteinConsequenceTests(unittest.TestCase):
    WT = "MKFGPEDK*"

    def test_missense_synonymous_nonsense(self):
        self.assertEqual(hv.protein_consequence(self.WT, "MKIGPEDK*XX", 0)["protein_hgvs"], "p.(Phe3Ile)")
        self.assertEqual(hv.protein_consequence(self.WT, "MKFGPEDK*XX", 0)["protein_hgvs"], "p.(=)")
        r = hv.protein_consequence(self.WT, "MK*GPEDK*", 0)
        self.assertEqual((r["protein_hgvs"], r["consequence"], r["ptc_codon"]), ("p.(Phe3Ter)", "nonsense", 3))

    def test_frameshift(self):
        r = hv.protein_consequence(self.WT, "MNLG*", -1)
        self.assertEqual((r["protein_hgvs"], r["ptc_codon"], r["first_altered"]), ("p.(Lys2Asnfs*4)", 5, 2))
        self.assertEqual(hv.protein_consequence(self.WT, "MK*", -1)["protein_hgvs"], "p.(Phe3Ter)")
        self.assertIn("fs*?", hv.protein_consequence(self.WT, "MNLGRT", -1)["protein_hgvs"])

    def test_inframe_del_dup_ins_delins(self):
        r = hv.protein_consequence(self.WT, "MKGPEDK*", -3)
        self.assertEqual((r["protein_hgvs"], r["consequence"], r["ptc_codon"]), ("p.(Phe3del)", "in-frame indel", None))
        self.assertEqual(hv.protein_consequence(self.WT, "MKPEDK*", -6)["protein_hgvs"], "p.(Phe3_Gly4del)")
        self.assertEqual(hv.protein_consequence(self.WT, "MKFFGPEDK*", 3)["protein_hgvs"], "p.(Phe3dup)")
        self.assertEqual(hv.protein_consequence(self.WT, "MKFWGPEDK*", 3)["protein_hgvs"], "p.(Phe3_Gly4insTrp)")
        r = hv.protein_consequence(self.WT, "MKWWPEDK*", 0)
        self.assertEqual((r["protein_hgvs"], r["consequence"]), ("p.(Phe3_Gly4delinsTrpTrp)", "in-frame delins"))
        r = hv.protein_consequence(self.WT, "MKW*", -3)
        self.assertEqual((r["consequence"], r["ptc_codon"]), ("in-frame indel (premature stop)", 4))

    def test_stop_loss_extension(self):
        r = hv.protein_consequence(self.WT, "MKFGPEDKQVN*", 0)
        self.assertEqual((r["protein_hgvs"], r["consequence"], r["ptc_codon"]), ("p.(Ter9Glnext*3)", "stop-loss (extension)", None))


class AnnotateTests(unittest.TestCase):
    def setUp(self):
        self.model = toy_model()

    def test_early_nonsense_is_nmd_and_start_proximal(self):
        a = hv.annotate(vv("NM_T.1:c.4A>T", "NP_T.1:p.(Lys2Ter)"), self.model, 10)
        self.assertTrue(a["is_truncating"])
        self.assertEqual((a["ptc_codon_from_protein_hgvs"], a["ptc_codon_computed"], a["ptc_codon"]), (2, 2, 2))
        self.assertEqual(a["protein_hgvs_computed"], "p.(Lys2Ter)")
        self.assertEqual(a["consequence_computed"], "nonsense")
        self.assertEqual(a["variant_exon"], 1)
        self.assertEqual(a["nmd"]["prediction"], "NMD predicted")
        self.assertEqual(a["nmd"]["distance_to_last_junction_nt"], 90)
        self.assertEqual(a["nmd"]["ptc_exon"], 1)
        self.assertTrue(any("start-proximal" in f for f in a["nmd"]["efficiency_flags"]))
        self.assertEqual(a["truncation"]["wild_type_residues_retained"], 1)
        self.assertEqual(a["truncation"]["truncated_product_length_aa"], 1)
        self.assertEqual(a["reinitiation"]["first_strong_met"], 33)

    def test_early_frameshift_without_protein_hgvs(self):
        a = hv.annotate(vv("NM_T.1:c.4del"), self.model, 10)
        self.assertTrue(a["is_truncating"])
        self.assertEqual(a["consequence_computed"], "frameshift")
        self.assertIsNone(a["ptc_codon_from_protein_hgvs"])
        self.assertEqual(a["ptc_codon"], 10)   # -1 frame reads TAG at c.29-31
        self.assertEqual(a["first_altered_codon_computed"], 2)
        self.assertEqual(a["protein_hgvs_computed"], "p.(Lys2Asnfs*9)")
        self.assertEqual(a["nmd"]["prediction"], "NMD predicted")
        self.assertEqual(a["nmd"]["distance_to_last_junction_nt"], 66)
        self.assertEqual(a["truncation"]["novel_frameshift_residues"], 0)   # only counted when VV supplies the fs HGVS

    def test_ptc_mismatch_note(self):
        a = hv.annotate(vv("NM_T.1:c.4A>T", "p.(Lys3Ter)"), self.model, 10)
        self.assertTrue(any("PTC mismatch" in n for n in a["notes"]))

    def test_last_exon_escapes(self):
        a = hv.annotate(vv("NM_T.1:c.103A>T"), self.model, 10)
        self.assertTrue(a["is_truncating"])
        self.assertEqual(a["protein_hgvs_computed"], "p.(Lys35Ter)")
        self.assertEqual(a["nmd"]["ptc_exon"], 3)
        self.assertEqual(a["nmd"]["prediction"], "NMD escape predicted")
        self.assertIn("last exon", a["nmd"]["reason"])

    def test_penultimate_exon_within_55nt_escapes(self):
        a = hv.annotate(vv("NM_T.1:c.88G>T"), self.model, 10)
        self.assertEqual(a["protein_hgvs_computed"], "p.(Glu30Ter)")
        self.assertEqual(a["nmd"]["ptc_exon"], 2)
        self.assertEqual(a["nmd"]["distance_to_last_junction_nt"], 6)
        self.assertEqual(a["nmd"]["prediction"], "NMD escape predicted")

    def test_borderline_start_proximal_flag(self):
        self.assertTrue(hv.START_PROXIMAL_NT < 169 <= hv.START_BORDERLINE_NT)

    def test_missense_not_truncating(self):
        a = hv.annotate(vv("NM_T.1:c.7T>A", "p.(Phe3Ile)"), self.model, 10)
        self.assertFalse(a["is_truncating"])
        self.assertEqual(a["protein_hgvs_computed"], "p.(Phe3Ile)")
        self.assertEqual(a["consequence_computed"], "missense")
        self.assertIsNone(a["ptc_codon_computed"])
        self.assertIsNone(a["reinitiation"])

    def test_inframe_deletion_not_truncating(self):
        a = hv.annotate(vv("NM_T.1:c.7_9del", "p.(Phe3del)"), self.model, 10)
        self.assertFalse(a["is_truncating"])
        self.assertEqual(a["protein_hgvs_computed"], "p.(Phe3del)")
        self.assertEqual(a["consequence_computed"], "in-frame indel")
        self.assertIsNone(a["ptc_codon_computed"])
        self.assertIn("no premature termination codon", a["nmd"]["prediction"])

    def test_stop_loss_extension_not_truncating(self):
        a = hv.annotate(vv("NM_T.1:c.106T>C", "p.(Ter36GlnextTer3)"), self.model, 10)
        self.assertFalse(a["is_truncating"])
        self.assertEqual(a["protein_hgvs_computed"], "p.(Ter36Glnext*3)")
        self.assertEqual(a["consequence_computed"], "stop-loss (extension)")
        self.assertIsNone(a["ptc_codon_computed"])

    def test_intronic_skips_retranslation(self):
        a = hv.annotate(vv("NM_T.1:c.10+1G>A"), self.model, 10)
        self.assertIsNone(a["edit"])
        self.assertFalse(a["is_truncating"])
        self.assertTrue(any("not in a supported coding form" in n for n in a["notes"]))

    def test_exon_numbering_note_when_vv_differs(self):
        v = vv("NM_T.1:c.4A>T")
        v["vv_exon"] = {"start": "2", "end": "2"}
        a = hv.annotate(v, self.model, 10)
        self.assertTrue(any("exon numbering differs" in n for n in a["notes"]))


if __name__ == "__main__":
    unittest.main()
