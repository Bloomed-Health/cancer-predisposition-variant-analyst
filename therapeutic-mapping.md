---
title: Therapeutic Mapping
impact: HIGH
impactDescription: Correct mechanism-to-target mapping determines which clinical interventions are appropriate and prevents harm from mechanistically mismatched treatments
tags: therapeutics,immunotherapy,checkpoint-inhibitor,TMB,PPAP,POLE,mismatch-repair,biomarker,clinical-trials,precision-oncology
---

# Therapeutic Mapping

Translate variant mechanism into actionable therapeutic hypotheses. Organized
from mechanism outward: established therapies first, then investigational
classes, then hypotheses specific to the resolved mechanism.

This is a research planning tool, not clinical guidance. All therapeutic
hypotheses require validation before patient application.

**Prerequisite:** the mechanism must be resolved first. Therapy follows the
**tumour's** actual mechanism, which Step 0 and the signature fork establish --
not the germline allele's label.

---

## Framework: Mechanism → Target → Therapeutic → Evidence Tier

```
Resolved mechanism (Step 0 / mechanistic-framework.md)
    ↓
Downstream molecular consequence (proofreading-deficient Pol ε? MMR loss? neither?)
    ↓
Therapeutic vulnerability (neoantigen load, replication stress, CTNA excision failure)
    ↓
Drug / intervention class
    ↓
Evidence tier (established → investigational → hypothesis), with n
```

### Routing by resolved mechanism

| Resolved mechanism                                              | Therapeutic logic                                                                                                              |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| H0: somatic POLE/POLD1 EDM on the WT allele                     | Treat as somatic proofreading-deficient tumour (TMB-H / LOP pathway). The germline LoF allele carries no therapeutic implication. |
| H0: MMR deficiency (Lynch, CMMRD, sporadic)                     | dMMR/MSI-H pathway (ICI approvals for dMMR). Germline MMR workup drives surveillance, not the POLE allele.                      |
| H0: other hypermutator (MUTYH, MBD4, NTHL1)                     | Follow that syndrome's management; POLE allele incidental.                                                                      |
| H1 confirmed: ΔN-POLE with impaired proofreading                | Behaves as PPAP: TMB-H ICI logic, LOP-class reasoning [T2], CTNA hypothesis [R3, R4]. Surveillance as POLE/POLD1 carrier.      |
| Unresolved (Step 0 negative, H1 untested)                       | Tumour-level biomarkers (TMB, MSI, signatures) still drive oncologic therapy; germline implications remain VUS-level.           |

---

## Tier 1: Established Therapeutic Relevance

### Immune Checkpoint Inhibition (ICI)

**Mechanism link:** Ultra-hypermutated tumours (TMB >100 mut/Mb) generate high
neoantigen loads; frameshift-derived peptides are strongly immunogenic.
Response tracks **proofreading loss in the tumour**, not POLE gene mutation
per se.

**Evidence (with denominators):**

| Source                              | Population                                    | Result                                                                                                        |
| ----------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| KEYNOTE-158 [CT3]                   | TMB-H (≥10 mut/Mb) solid tumours              | Basis of 2020 FDA tumour-agnostic pembrolizumab approval                                                      |
| Toripalimab Phase II [T1]           | Non-MSI-H solid tumours, any POLE/POLD1 variant | ORR 21.4% overall; **EDM 66.7% (2/3)**; non-EDM 9.1%                                                        |
| LOP stratification [T2]             | 41 POLE-mutant mCRC (MDACC); 69,223 pan-cancer | LOP = 148/1,965 POLE-mutant tumours (7.5%). LOP ORR **88.9% (8/9)**; non-LOP MSI-H 66.7% (6/9); non-LOP MSS ≈ WT. LOP tumours respond poorly to cytotoxic chemotherapy |
| POLE/POLD1pd mCRC [T3]              | Proofreading-deficient mCRC on ICI            | Exceptional response rates; confirms proofreading status as the selector                                      |
| MD Anderson retrospective [T5]      | POLE-mutant tumours on ICI                    | Pathogenic POLE: PFS 15.1 mo, OS 29.5 mo; benign POLE: PFS 2.8 mo, OS 11.6 mo                                 |
| MSS POLE mCRC case [T4]             | n = 1                                         | Complete pathologic response to pembrolizumab, 37 months disease-free                                         |
| Neoadjuvant ICI [T6]                | MSI-H/POLE-mutated locally advanced CRC       | R0 100%, pCR 70% (see [T6] for n)                                                                             |
| Neoantigen quality [N1, N2]         | CRC model; melanoma/NSCLC cohorts             | Clonal neoantigen burden predicts response better than TMB (+11-20% AUROC)                                    |

**Interpretation for a germline truncation carrier:**

- The germline allele is non-LOP by definition (no protein). ICI eligibility
  therefore rests on **tumour** TMB (≥10 mut/Mb pathway), tumour MSI status, and
  whatever proofreading-deficient allele the tumour actually carries.
- If Step 0 found a somatic EDM hotspot: the tumour is LOP; expect EDM-class
  response. If H1 is confirmed: treat the ΔN allele as LOP-class pending data.
- The toripalimab EDM figure is 2 of 3 patients. Do not quote it as a
  response rate without n.

**Biomarker strategy:**

- TMB quantification (panel or WES; report assay and cutoff).
- MSI status by IHC (MLH1/MSH2/MSH6/PMS2) and PCR/NGS. POLE hypermutators are
  typically MSS; MSI-H points to an MMR driver (Step 0).
- Mutational signatures (SBS10a/b/28 vs SBS10c/d vs SBS14/20).
- PD-L1 IHC: not required for TMB-H approval; informs combinations.
- HLA typing and clonal neoantigen scoring [N2] where available.

**Clinical trials:** registry entries change; query at run time:
`https://clinicaltrials.gov/api/v2/studies?query.term=POLE+AND+(immunotherapy+OR+pembrolizumab+OR+nivolumab)`.
Verified entries (CT.gov API, 2026-11-22) are in [references.md](references.md):
CT1 NCT05103969 (POLE/POLD1-mutant tumour cohort; status UNKNOWN), CT2
NCT03810339 (toripalimab, POLE/POLD1-mutant non-MSI-H; the [T1] trial;
RECRUITING), CT3 NCT02628067 (KEYNOTE-158; basis of the TMB-H approval), CT4
NCT03639714 (personalised neoantigen vaccine + nivolumab/ipilimumab;
COMPLETED), CT5 NCT03435107 (durvalumab in dMMR/POLE mCRC; COMPLETED).

**Caveats:**

1. **Germline vs somatic.** Most ICI data derive from somatic hypermutators.
   Constitutional proofreading deficiency (true PPAP) means normal tissues also
   accumulate mutations; implications for immune-related adverse events are
   not characterised.
2. **Clonality.** EDM tumours generate clonal neoantigens from the first
   division; a hypermutator acquired late (somatic hit, or H2-type LOH) yields
   more subclonal neoantigens and plausibly weaker ICI response [N1].

---

### Surveillance, Surgery, and Cascade Testing

**Mechanism link:** PPAP causes multifocal adenomatous polyposis (often
attenuated) with accelerated adenoma-carcinoma progression.

**NCCN Genetic/Familial High-Risk Assessment: Colorectal (2025) [G1], POLE/POLD1
pathogenic/likely pathogenic carriers:**

- High-quality colonoscopy from **age 25-30** (or 2-5 years before the
  earliest CRC in the family if diagnosed <25).
- Repeat every **2-3 years** if clear; every **1-2 years** if polyps found.
- Upper GI endoscopy: duodenal neoplasia is reported in POLE and POLD1
  carriers [P1, P4]; follow NCCN/EHTG duodenal surveillance guidance.
- Colectomy threshold by polyp burden and endoscopic controllability [P3].

**Cascade testing gate.** Offer cascade testing to relatives **only** when the
variant is Likely Pathogenic or Pathogenic under a gene-disease assertion for
which the applied criteria are valid (variant-interpretation.md Step 4). For a
POLE truncation classified VUS for PPAP, cascade testing is a harm: it labels
~1-in-500 carriers of a benign carrier state [P6] as at-risk, triggers
surveillance without benefit, and cannot be undone once reported. Surveillance
decisions for relatives in the interim should follow family history, not the
variant.

---

## Tier 2: Investigational Classes

### Replication Stress Exploitation (ATR/CHK1 Inhibition)

**Mechanism link:** Proofreading-deficient or Pol ε-depleted cells accumulate
ssDNA gaps and fork stalling, increasing dependence on ATR-CHK1 signalling.

**Evidence:**

- POLE3/POLE4 loss sensitises to ATR inhibition (CRISPR screen) [R1].
- POLD1 is synthetic lethal with ATR in a 288-gene DNA-repair screen [R2];
  POLD1 R689W increases ATRi/CHK1i sensitivity in CRC cells [R7].
- POLA1-ATR synthetic lethality extends the B-family paradigm [R6].
- RTEL1 deficiency is synthetic lethal with Pol ε loss [R8].
- Meta-analysis of 10 trials / 810 patients: no overall benefit of ATR
  inhibitors in unselected solid tumours [R5].
- **Ceralasertib:** Phase III LATIFY (with durvalumab, previously treated
  NSCLC, n = 594) did not meet its OS primary endpoint [T9].
- **Elimusertib:** Phase I only (NCI Phase 1/2 active-not-recruiting; Bayer
  Phase 1b with niraparib terminated). **Camonsertib:** Phase I/II.

**Status: hypothesis.** No POLE-selected ATR-inhibitor trial exists. Preclinical
rationale applies to cells with a proofreading-deficient or depleted Pol ε --
i.e. only if the tumour's mechanism is H0 (somatic EDM) or H1, and not to a
tumour replicating with wild-type Pol ε.

**Biomarker:** pRPA32 (S33) in tumour biopsies as a replication-stress readout.

---

### Chain-Terminating Nucleoside Analogs (CTNAs)

**Mechanism link:** Pol ε/Pol δ 3′→5′ exonucleases excise incorporated
chain-terminating analogs. Exonuclease-deficient cells cannot, so they are
selectively sensitive.

**Evidence (preclinical only):**

- POLE1exo-/- cells: Ara-C IC50 reduced 3-4x; Pol δ and Pol ε exonucleases
  contribute independently [R3].
- 12 nucleoside analogs × 24 DT40 mutant lines: POLE1exo-/- + CTF18-/- strongly
  synthetic lethal with Ara-C; Ara-C depends on Pol ε exo alone, whereas
  ddC/AZT/alovudine need combined Pol δ + Pol ε exo loss [R4].

**Limits:**

- Chicken DT40 and human cell-line data; no in-vivo or clinical data.
- Cytarabine has no established activity or pharmacology in solid tumours
  (short half-life, poor tumour penetration, myelotoxicity at effective doses).
- Applies only when a **proofreading-deficient Pol ε is replicating the tumour**
  (SBS10a/b present). A tumour relying on wild-type Pol ε (germline null allele,
  H0 non-POLE driver) gains no selectivity.

**Status: preclinical hypothesis.**

---

### PARP Inhibition (Context-Dependent)

**Mechanism link:** Only if an HR defect co-exists (germline BRCA1/2, or an HRD
signature). PPAP tumours are typically HR-proficient.

**Status:** LOW unless HRDetect/CHORD [TOOL8] shows HRD on tumour WGS.

---

### Neoantigen Vaccine / Adoptive T-Cell Therapy

**Mechanism link:** Ultra-hypermutated tumours and polyps carry dense
frameshift neoantigens; POLE signatures produce recurrent mutation contexts,
so shared neoantigens may exist across PPAP patients.

**Hypotheses:** personalised neoantigen vaccine (adjuvant or prophylactic in
polyps); shared-neoantigen vaccine if recurrent frameshift peptides are
catalogued in POLE-hypermutator TCGA data; TIL/TCR-T against POLE neoantigens.

**Evidence tier:** preclinical / early-phase for hypermutated tumours generally
[N3]; no PPAP-specific trial. Query ClinicalTrials.gov at run time.

---

### Chemoprevention (Polyp Burden Reduction)

- Aspirin / sulindac / celecoxib: evidence in FAP and Lynch (CAPP2); **no
  PPAP-specific evidence**. Mechanism (COX-dependent proliferation) does not
  address mutation rate.
- No agent targets replication-error rate. Do not propose antioxidant /
  8-oxoguanine strategies here: that pathway is MUTYH biology, not proofreading.

---

## Tier 3: Mechanism-Specific Hypotheses (This Variant)

### If H1 (reinitiation → ΔN-POLE) is confirmed

- **Not a neoantigen.** Reinitiation at a native in-frame Met (Met66) yields
  native POLE sequence from that point; there is no novel junction peptide.
  Do not propose a vaccine against the ΔN protein.
- The four aberrant residues encoded before the PTC (Gln53…Ter at codon 57)
  exist only on the terminated 56-aa peptide. They are a neoepitope candidate
  only if NMD escape **without** reinitiation is demonstrated (H5 territory,
  not supported); check MHC-I binding [TOOL7] before any investment.
- Therapeutic logic then follows PPAP: ICI by tumour TMB/LOP status; CTNA and
  ATRi hypotheses apply to the tumour's ΔN-POLE-dependent replication.
- Research target: the ΔN-POLE–PCNA interface. If weakened PCNA engagement is
  the mechanism, it is a structural handle for understanding proofreading
  switching [M3-M5], not a near-term drug target.

### If H0 (coincidence) is confirmed

No variant-specific therapeutic hypothesis. Record the case as an incidental
POLE LoF carrier with a somatically driven hypermutator; contribute the
germline allele to ClinVar with the tumour evidence (BP5-relevant if the tumour
lacks SBS10 [C1]).

---

## Biomarker Strategy Summary

| Biomarker                                       | Purpose                                                              | Tier            |
| ----------------------------------------------- | -------------------------------------------------------------------- | --------------- |
| Somatic POLE/POLD1 EDM hotspot (tumour)         | Identifies the actual proofreading-deficient allele (Step 0)         | Established     |
| MMR IHC / MSI                                   | Distinguishes POLE from MMR mechanism; dMMR ICI pathway              | Established     |
| TMB ≥10 mut/Mb (panel/WES)                      | ICI eligibility (tumour-agnostic pembrolizumab)                      | Established     |
| SBS10a/10b/28 vs SBS10c/d vs SBS14/20 [SIG1-6]  | Assigns hypermutation to Pol ε, Pol δ, or MMR+polymerase             | Established     |
| LOP classification [T2]                         | ICI response stratification (LOP vs non-LOP)                         | Emerging        |
| ctDNA dynamics [T8]                             | ICI response monitoring                                              | Emerging        |
| LOH at 12q24.33 (tumour)                        | Interpretable only with mutant-protein evidence (H2)                 | Investigational |
| Clonal neoantigen score (NeoPrecis) [N2]        | ICI response beyond TMB                                              | Investigational |
| HRD signature (HRDetect/CHORD) [TOOL8]          | PARP inhibitor eligibility                                           | Investigational |
| ΔN-POLE protein (C-terminal WB / targeted MS)   | Confirms H1                                                          | Research        |
| pRPA32 (S33)                                    | Replication-stress burden; ATRi stratification                       | Research        |
| CTNA sensitivity (Ara-C IC50, patient organoid) | Nucleoside analog hypothesis                                         | Research        |
| AlphaMissense / REVEL                           | Missense only; **not applicable** to truncations                     | N/A             |

---

## Case Report / Manuscript Recommendation

**Minimum before submission:** Step 0 complete and negative (germline
confirmation; tumour EDM-hotspot sequencing negative; MMR IHC/MSI negative);
signature decomposition reported with SNV count; RNA allele-ratio result; a
C-terminal-antibody western or MS result. Without these, the report describes
an incidental carrier, not a paradox, and reviewers will say so.

Suitable venues: _npj Genomic Medicine_, _Genetics in Medicine_, _JNCI_,
_Human Mutation_, _Familial Cancer_. Frame as:

1. Clinical description and variant characterisation (HGVS validated).
2. Phenocopy exclusion (Step 0) and signature evidence.
3. Mechanistic hypotheses with the reinitiation scan and essential-gene
   argument; proposed/performed experiments.
4. Classification outcome with points tally and gene-disease assertion
   discussion; explicit statement that relatives were not cascade-tested on a
   VUS.
5. Therapeutic implications by tumour mechanism.
6. Call for matching (Matchmaker Exchange [D7]; ClinVar submission).
