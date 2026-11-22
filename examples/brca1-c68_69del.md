---
title: "Worked example 2: BRCA1 c.68_69del (185delAG)"
impact: MEDIUM
impactDescription: "Second worked example showing the six-step workflow generalises beyond POLE; the transferable lesson is the translation-reinitiation question"
tags: "example,BRCA1,reinitiation,PARPi-resistance,HBOC"
---

# Worked Example 2: BRCA1 NM_007294.4:c.68_69del p.(Glu23Valfs*17)

Purpose: run the same six-step workflow used for the POLE exon-2 frameshift
([SKILL.md](../SKILL.md#workflow)) on a well-characterised variant, to show
(a) that Step 0 correctly declines to call a paradox where there is none at the
classification level, and (b) that the reinitiation question raised in Step 1
is the transferable lesson: here it is experimentally proven [M8] and has
therapeutic consequences.

Last verified: 2026-11-22. Coordinates computed from Ensembl REST
(`/sequence/id/ENST00000357654?type=cds`, `/lookup/id/ENST00000357654?expand=1`),
transcript BRCA1-203 = MANE Select NM_007294.4, 1,863 aa, 23 exons (22 coding).

---

## Step 0: Genotype Verification and Differential Diagnosis

| Check                         | Result                                                                                                  | Consequence                                      |
| ----------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| Call quality / HGVS           | Legacy name 185delAG; HGVS c.68_69del (no 3' shift: c.70_71 = TG, not AG)                               | Verified                                         |
| Germline vs. clonal           | Ashkenazi Jewish founder allele; constitutional, present in non-haematopoietic tissue                    | Germline confirmed                               |
| Phenotype                     | Hereditary breast/ovarian cancer (HBOC)                                                                 | Expected phenotype for BRCA1 LoF                 |
| Phenocopy differential        | Other HBOC genes (BRCA2, PALB2) not needed to explain phenotype                                         | No competing explanation required                |
| Tumour phenotype              | HRD signature (SBS3), BRCA1 second hit (LOH) typical                                                    | Consistent with LoF mechanism                    |
| **Paradox at classification?** | **No.** Genotype (LoF) and phenotype (HBOC) agree with the established gene–disease mechanism [C13].   | Skip to standard classification                  |
| **Paradox elsewhere?**        | **Yes, therapeutic.** Some c.68_69del tumours resist PARP inhibitors and platinum despite a "null" allele [M8]. | Carry the mechanism question into Steps 1–2 and 5 |

Step 0 verdict: not a genotype–phenotype paradox. The classification pathway is
routine; the mechanism pathway is opened only to explain treatment resistance.

---

## Step 1: Precise Molecular Consequence

Computed 2026-11-22 from the ENST00000357654 CDS (5,592 nt incl. stop = 1,863 codons + stop):

| Item                               | Value                                                                                               |
| ---------------------------------- | --------------------------------------------------------------------------------------------------- |
| Variant                            | NM_007294.4:c.68_69del (deletes AG at c.68–69, exon 2 of 23; exon 2 spans c.1–c.80)                  |
| Frame                              | −2, frameshift                                                                                      |
| Protein                            | p.(Glu23Valfs*17): codon 23 Glu→Val, 16 aberrant codons, PTC at codon 39                            |
| PTC position                       | Codon 39 of 1,863 (2.1%); c.115–117, **exon 3** (c.81–c.134)                                        |
| NMD prediction                     | PTC >50–55 nt upstream of the exon 22/23 junction → NMD predicted [M12]; empirically incomplete [M8] |
| In-frame Met codons after PTC      | Met48 (Kozak −3 T/+4 C, weak), Met128 (−3 A/+4 G, strong), **Met297** (−3 A/+4 A, adequate), Met531, Met546… |
| Experimentally used start          | **Met297** (c.889–891, exon 10): RING-less BRCA1 of ~1,567 aa detected by mass spectrometry and antibody mapping [M8] |

Note on the scan: a pure sequence scan ranks Met128 (strong Kozak) above Met297.
Drost et al. mapped the actual product to Met297 [M8]; the scan therefore
generates candidates, it does not choose among them. The same caveat applies to
the POLE Met66/Met359 candidates in the primary example.

---

## Step 2: Protein Domain Map

UniProt P38398 (BRCA1_HUMAN, 1,863 aa):

| Region                       | Residues    | Function                                                | Status in Met297 product |
| ---------------------------- | ----------- | ------------------------------------------------------- | ------------------------ |
| RING finger                  | 24–65 (domain ~1–109) | E3 ubiquitin ligase; BARD1 heterodimerisation            | **Lost**                 |
| Nuclear localisation signals | ~503–508, ~606–615 | Nuclear import                                      | Retained                 |
| Coiled-coil (PALB2 binding)  | ~1393–1424  | Recruits PALB2–BRCA2–RAD51 for homologous recombination | Retained                 |
| BRCT tandem repeats          | 1642–1736, 1756–1855 | Phospho-peptide binding (Abraxas, BACH1, CtIP)      | Retained                 |

The Met297 product lacks RING/BARD1 binding but keeps every element required for
PALB2/BRCA2 recruitment and HR. Contrast with POLE ΔN65 (reinitiation at Met66),
which would keep the exonuclease (aa 268–471), polymerase and C-terminal
CMG-binding regions; in both cases the retained part is the functionally
decisive part.

---

## Mechanism: Hypothesis Ranking

Essential-gene note: BRCA1 is embryonic-lethal when knocked out in mouse and is
selectively essential in many human cell lines, but it is not DepMap
common-essential in the way POLE is [M10]; tumours routinely become BRCA1-null
by LOH. The "null + LOH" route is therefore **viable** for BRCA1 and is in fact
the standard HBOC second hit. This is exactly the pre-check that excludes the
same route for POLE ([mechanistic-framework.md](../mechanistic-framework.md#pre-checks-essential-gene-filter-and-signature-fork)).

| Rank | Hypothesis                                                   | Prediction                                              | Status                                     |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------- | ------------------------------------------ |
| H1   | Translation reinitiation at Met297 → RING-less BRCA1         | Residual HR; PARPi/platinum resistance in tumours that retain the allele and lose WT | **Confirmed** [M8]      |
| H2   | Complete null (NMD + no reinitiation)                        | Full HRD, PARPi sensitivity                             | True in most tumours; does not explain resistant subset |
| H3   | Secondary resistance (reversion, 53BP1 loss, drug efflux)    | Acquired, not allele-intrinsic                          | Real but separate mechanism                |

Discriminating experiments (as applied in [M8]): N-terminal vs C-terminal
anti-BRCA1 immunoblot; mass spectrometry of the truncated species; CRISPR
knock-in of the allele with and without Met297→Ala; PARPi/cisplatin dose–response.
The same four experiments are the minimum set proposed for POLE Met66
([mechanistic-framework.md](../mechanistic-framework.md#minimum-discriminating-experiment-set)).

---

## Evidence Assembly

| Criterion | Applied? | Strength    | Points [C8] | Justification                                                                                   |
| --------- | -------- | ----------- | ----------- | ----------------------------------------------------------------------------------------------- |
| PVS1      | Yes      | Very Strong | 8           | LoF **is** the established HBOC mechanism for BRCA1 [C7]; PTC at codon 39, NMD predicted. **Contrast POLE**: PVS1 not applied because LoF is not the PPAP mechanism. |
| PS4       | Yes      | Strong      | 4           | Founder allele, strongly enriched in HBOC families vs. population                              |
| PP1       | Yes      | Strong      | 4           | Extensive co-segregation across many families                                                   |
| PM2       | No       | —           | 0           | Founder allele is not absent from controls (AJ carrier frequency ~1%); PM2_Supporting [C12] not met |
| PS3       | Yes      | Strong      | 4           | HR/functional assays consistent with LoF across multiple validated assays [C9]                 |
| **Total** |          |             | **≥10**     | **Pathogenic** (threshold ≥10 [C8]); ClinVar expert-panel Pathogenic [D2]                       |

The RING-less product does not change the germline classification: the allele
still confers HBOC risk. It changes the tumour-level prediction of drug response.

---

## Therapeutics

| Question                                   | Answer                                                                                                                            |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| Does the germline label predict PARPi response? | Not reliably. Tumours expressing RING-less BRCA1 from the c.68_69del allele showed PARPi and cisplatin resistance in mouse and human models [M8]. |
| Predicted resistance marker                | Detection of RING-less BRCA1 (C-terminal antibody positive, N-terminal negative) in tumour; retained c.68_69del allele with WT loss [M8] |
| Clinical use today                         | Research-grade; not a validated companion diagnostic. Report as hypothesis-generating.                                           |
| Surveillance / cascade                     | Standard BRCA1 pathogenic-variant management applies; classification is Pathogenic, so cascade testing is appropriate.           |

---

## What transfers to the POLE case

| Lesson                                                           | BRCA1 c.68_69del                      | POLE c.158_159del                                        |
| ---------------------------------------------------------------- | ------------------------------------- | -------------------------------------------------------- |
| Early-exon PTC + downstream in-frame Met ⇒ ask about reinitiation | PTC codon 39; product from Met297 [M8] | PTC codon 57; candidates Met66 (9 codons downstream), Met359 |
| "NMD predicted" ≠ "no protein"                                   | Proven                                | Untested; first experiment                               |
| Essential-gene filter decides whether null+LOH is allowed        | Allowed                               | Not allowed [M10]                                        |
| PVS1 depends on gene–disease mechanism, not on PTC position      | Applied                               | Not applied [C7]                                         |
| Reinitiated product changes therapy, not necessarily classification | PARPi resistance                   | If Met66 product is exo-competent: therapy follows the tumour's actual mutator |
