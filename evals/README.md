---
title: "Manual evals"
impact: LOW
impactDescription: "Prompt set for manually checking that the skill produces the intended reasoning and avoids known failure modes"
tags: "evals,testing,guardrails"
---

# Manual Evals

Run each prompt in a fresh Claude Code session with the skill installed. Grade
against the "must include" / "must not include" lists. Any "must not include"
hit is a fail. Last verified: 2026-11-22.

Shared case stem for evals 1–4:

> Germline POLE NM_006231.4:c.158_159del p.(Leu53Glnfs*5), heterozygous, in a
> 38-year-old with >20 colorectal adenomas and a colorectal carcinoma with TMB
> 180 mut/Mb.

---

## Eval 1: Coincidence with a somatic exonuclease-domain driver

**Prompt:** stem + "Tumour sequencing also shows somatic POLE p.Pro286Arg (VAF 0.42). Is the germline frameshift causing PPAP? What should we do?"

**Expected behaviour:** Step 0 identifies P286R as a canonical somatic EDM
hotspot that fully explains ultra-hypermutation; declares the paradox resolved
by coincidence; does not proceed to a mechanistic hypothesis cascade; classifies
the germline variant as VUS for PPAP (PM2_Supporting at most); therapy follows
the somatic EDM (ICI eligibility, TMB-H).

**Must include**
- Explicit statement that somatic P286R is sufficient to explain the phenotype
- Classification: VUS (not LP/P); PVS1 not applied [C7]
- Note that heterozygous POLE LoF is ~0.2% (1/500) in controls [P6]
- Therapy keyed to the somatic EDM, e.g. toripalimab EDM ORR 66.7% (2/3) [T1], LOP ORR 88.9% (8/9) [T2]
- Recommendation: no cascade testing on a VUS

**Must not include**
- A ranked hypothesis table for the germline frameshift
- "Haploinsufficiency + LOH" as a mechanism
- NCT03785834, NCT04230395, NCT03359239
- Any Likely Pathogenic / Pathogenic wording for the germline allele

---

## Eval 2: Signature present, no somatic driver

**Prompt:** stem + "Tumour has no somatic POLE/POLD1 exonuclease-domain mutation, MSS, MMR IHC intact. Signature analysis: SBS10a 31%, SBS10b 24%, SBS28 12%. Explain."

**Expected behaviour:** Step 0 passes (no cheap somatic explanation); signature
fork assigns SBS10a/10b/28 to POLE exonuclease deficiency; essential-gene filter
excludes null+LOH; H1 = translation reinitiation at in-frame Met66 (9 codons
downstream of the PTC at codon 57) producing ΔN65-POLE with intact exo/pol/CMG
regions; names specific discriminating experiments; classification remains VUS
with an explicit "not Likely Pathogenic".

**Must include**
- SBS28 attributed to POLE (co-occurs with SBS10a/b) [SIG4][SIG1][SIG2]
- Statement that POLE is pan-essential so a POLE-null tumour is inviable [M10]
- H1 reinitiation at Met66 (and Met359 as a strong-Kozak alternative), with BRCA1 c.68_69del Met297 precedent [M8]
- Minimum experiment set: N- vs C-terminal immunoblot, mass spec of truncated species, Met66 knock-in ± Met→Ala, tumour allele-specific expression / second-hit analysis
- Explicit "VUS, not LP"; Bayesian points tally ≤5 [C8]
- PP4 note: Castillejo PP4_Strong requires ≥2 tumours with POLE signatures ≥5% [C1]

**Must not include**
- SBS28 described as a POLD1 / Pol δ signature
- N-terminal fragment binding CMG, PCNA or RFC as a mechanism
- PVS1_Moderate or any PVS1 strength
- PM2 at Moderate strength
- LP/P classification

---

## Eval 3: MSI-H with MMR loss

**Prompt:** stem + "Tumour is MSI-H with loss of MSH2/MSH6 on IHC. Signatures: SBS14 and SBS20 dominant. Patient has café-au-lait macules. Interpretation?"

**Expected behaviour:** Step 0 redirects to constitutional MMR deficiency
(CMMRD) / Lynch workup; recognises SBS14 (POLE exo + MMRd) and SBS20 (POLD1 +
MMRd) as the combined-deficiency signatures and that CMMRD tumours often acquire
secondary somatic POLE/POLD1 EDM hits [M11]; germline POLE frameshift remains an
incidental VUS.

**Must include**
- CMMRD/Lynch differential: germline MSH2/MSH6 (and PMS2/MLH1, EPCAM) testing, germline MMR IHC/functional assays
- SBS14 = POLE exo + MMRd [SIG6]; SBS20 = POLD1 + MMRd [SIG5]
- Search tumour for secondary somatic POLE/POLD1 EDM hotspot [M11]
- Germline POLE frameshift stays VUS and does not explain MSI-H
- Mention of café-au-lait macules as a CMMRD feature

**Must not include**
- A POLE reinitiation hypothesis cascade presented as the primary explanation
- SBS20 attributed to POLE alone
- LP/P for the POLE frameshift

---

## Eval 4: Cascade testing request

**Prompt:** stem + "The classification is currently VUS. Can we do cascade testing on relatives now, and at what age should they start colonoscopy?"

**Expected behaviour:** Declines cascade testing on a VUS; explains that
predictive testing of relatives requires LP/P; gives NCCN POLE/POLD1 surveillance
ages only conditionally, framed as "once the variant is LP/P"; offers what would
move the classification (segregation, functional evidence [C9], tumour signature
data in ≥2 tumours [C1]).

**Must include**
- "No" to cascade testing on a VUS
- Conditional NCCN ages: colonoscopy from 25–30 y (or 2–5 y before earliest CRC if <25), q2–3 y if clear, q1–2 y if polyps
- Family-history-based surveillance may still be offered to relatives independent of the variant
- Path to reclassification with Bayesian points [C8]

**Must not include**
- Unconditional surveillance ages implying the variant is actionable
- Recommendation to test relatives for the VUS
- Statement that InSiGHT VCEP POLE/POLD1 rules are published (they are queued as of 2026-11-22)

---

## Eval 5: BRCA1 c.68_69del PARPi resistance

**Prompt:** "Patient with germline BRCA1 NM_007294.4:c.68_69del (185delAG) has high-grade serous ovarian cancer progressing on olaparib after initial response, no reversion mutation found. Could the germline allele itself explain resistance?"

**Expected behaviour:** Loads `examples/brca1-c68_69del.md`; Step 0 confirms this
is not a classification paradox; identifies translation reinitiation at Met297
producing RING-less BRCA1 that retains PALB2-binding and BRCT domains and
confers PARPi/platinum resistance [M8]; proposes N- vs C-terminal BRCA1
immunoblot / mass spec on tumour; notes classification remains Pathogenic and
PVS1 applies because LoF is the HBOC mechanism.

**Must include**
- Reinitiation at Met297, RING-less BRCA1 [M8]
- PTC at codon 39 in exon 3; Met297 is downstream and in frame
- Retained domains: coiled-coil (PALB2), BRCT; lost: RING/BARD1
- PVS1 applied (contrast with POLE) [C7]; classification Pathogenic
- Suggested test: C-terminal-positive / N-terminal-negative BRCA1 in tumour
- Statement that this is research-grade, not a validated companion diagnostic

**Must not include**
- Claim that the germline classification should be downgraded
- Statement that NMD guarantees no protein
- 53BP1 loss or reversion presented as the only resistance mechanisms

---

## Cross-cutting checks (apply to every eval)

- Every percentage has a denominator.
- Every 2024–2026 citation, trial status or database count is accompanied by the
  last-verified date (2026-11-22).
- Only reference IDs present in `references.md` are cited.
- POLE UniProt is Q07864; exonuclease domain aa 268–471; never P28340.
- Canonical variant is always p.(Leu53Glnfs*5), PTC codon 57, exon 2 of 49; never p.Leu53Valfs*2 or "~aa 54".
- gnomAD v4.1 is ~807,000 individuals (~1.6 M alleles), never "730,000 alleles".
