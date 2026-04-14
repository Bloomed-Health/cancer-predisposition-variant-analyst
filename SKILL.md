---
name: cancer-predisposition-variant-analyst
description: |
  Ultra-rare disease variant interpretation: mechanistic paradox resolution, clinical
  classification, literature synthesis, and therapeutic target mapping.
  TRIGGER when: user presents a genotype-phenotype paradox (variant that should not
  cause the observed phenotype by current consensus), asks about POLE/POLD1 truncation
  variants in cancer predisposition, needs to resolve mechanistic contradictions in
  multi-domain disease genes where truncation outside the canonical disease region
  produces the expected phenotype, or is drafting a case report for an ultra-rare
  variant that challenges established classification frameworks.
  DO NOT TRIGGER when: user needs standard germline panel interpretation (BRCA1/2,
  Lynch, cardiac panels), routine ACMG classification without a paradox element,
  pharmacogenomics (PGx) interpretation, common population variant annotation, or
  somatic-only tumor profiling without a germline predisposition question.
metadata:
  author: Bloomed-Health
  version: "1.2.0"
  tags: rare-disease,genomics,PPAP,POLE,variant-classification,mechanistic-hypothesis,cancer-predisposition,therapeutic-targets
---

# Cancer Predisposition Variant Analyst Skill

Interpret ultra-rare variants, resolve genotype-phenotype paradoxes, assemble
clinical-grade evidence, and map mechanism to therapeutic opportunity. Designed
for research teams working on novel findings in cancer predisposition, DNA repair,
and replication-fidelity disorders.

The canonical worked example throughout this skill is a **pathogenic frameshift in
POLE at ~residue 54**, which eliminates all functional domains yet produces a
classical ultra-hypermutated PPAP phenotype -- a paradox that encodes a general
reasoning template applicable to any truncation variant in a multi-domain disease gene.

> **Why this is paradigm-shifting:** Current consensus holds that POLE
> truncation/LoF variants do NOT cause PPAP. PPAP is caused exclusively by
> non-disruptive missense variants in the exonuclease domain that produce a
> functional-but-error-prone polymerase (Genome Medicine 2023). The PolED
> database (Database Oxford, 2025) explicitly states: "Loss-of-function
> variants (deletions, insertions, premature stop codons) prevent production
> of the enzyme and cannot cause ultramutated cancers." Heterozygous POLE LoF
> is considered benign; biallelic POLE LoF causes recessive congenital
> disorders (FILS syndrome, OMIM 615139; IMAGe-I, OMIM 618336) -- not cancer
> predisposition. Population-level data confirms no enrichment of POLE LoF
> variants in cancer cases (0.22%) vs. cancer-free controls (0.20%). A
> truncation variant producing a PPAP phenotype therefore challenges the
> established genotype-phenotype model and demands mechanistic resolution.
> Recent evidence (EJHG 2024) showing that even classic POLD1 EDM variants
> require somatic LOH of the wild-type allele for tumor hypermutation further
> reshapes the mechanistic landscape.

---

## Workflow

1. **Characterize the variant** — Establish precise molecular consequence: reading
   frame, predicted NMD fate, protein domain map, gnomAD/ClinVar/LOVD status.
   → [variant-interpretation.md](variant-interpretation.md)

2. **Resolve the mechanistic paradox** — Generate ranked mechanistic hypotheses
   explaining phenotypic severity despite apparent loss of all canonical
   functional domains. Identify experiments that distinguish between them.
   → [mechanistic-framework.md](mechanistic-framework.md)

3. **Assemble clinical evidence** — Apply ACMG/ClinGen criteria systematically.
   Grade functional evidence. Build the evidence table for reclassification.
   → [variant-interpretation.md](variant-interpretation.md)

4. **Synthesize literature** — Execute structured search protocol across PubMed,
   ClinVar submissions, gnomAD constraint data, and relevant preprint servers.
   → [literature-protocol.md](literature-protocol.md)

5. **Map therapeutic targets** — Translate mechanism into actionable therapeutic
   hypotheses, stratified by evidence tier and regulatory pathway.
   → [therapeutic-mapping.md](therapeutic-mapping.md)

---

## What You Get

- Mechanistic hypothesis ranking with experimental discriminators
- ACMG/ClinGen evidence table ready for classification committee
- Structured literature gap analysis
- Therapeutic target map linked to mechanism
- Case report / manuscript outline for novel findings

---

## Sub-files

| File                                                   | Content                                                                    |
| ------------------------------------------------------ | -------------------------------------------------------------------------- |
| [variant-interpretation.md](variant-interpretation.md) | Domain mapping, NMD prediction, ACMG/ClinGen criteria, gnomAD constraint   |
| [mechanistic-framework.md](mechanistic-framework.md)   | Paradox resolution, ranked hypotheses, experimental discriminators         |
| [literature-protocol.md](literature-protocol.md)       | Search strategy, evidence grading, gap analysis                            |
| [therapeutic-mapping.md](therapeutic-mapping.md)       | Mechanism-to-target pipeline, clinical trial landscape, biomarker strategy |
| [references.md](references.md)                         | Canonical bibliography with URLs, organized by topic, citation guidance    |

---

## Quick Reference: POLE Variant Classes

| Feature                        | Classic PPAP (EDM missense)                   | Early truncation (e.g. p.54fs)                           | Biallelic LoF                            |
| ------------------------------ | --------------------------------------------- | -------------------------------------------------------- | ---------------------------------------- |
| Domains eliminated             | None (point mutation in active site)          | All (exo + pol + C-term)                                 | Varies (splicing, frameshift)            |
| Mutant protein present         | Yes, error-prone but functional               | Unknown -- NMD fate critical                             | Severely reduced or absent               |
| Expected phenotype             | PPAP (polyposis, ultra-hypermutation)         | NOT PPAP by current consensus (PolED 2025)               | FILS / IMAGe-I (recessive developmental) |
| Mechanism                      | Defective proofreading, intact polymerization | See [mechanistic-framework.md](mechanistic-framework.md) | Loss of replication capacity             |
| TMB                            | 100-1000 mut/Mb (requires somatic WT LOH)     | Can be >100 mut/Mb (this patient)                        | Not characterized                        |
| LOP classification (JITC 2025) | LOP (loss-of-proofreading)                    | Non-LOP (eliminates protein, not proofreading)           | Non-LOP                                  |
| ICI response prediction        | Excellent (82.4% CBR, LOP class)              | Unknown (depends on mechanism + TMB)                     | Not applicable                           |
| CTNA sensitivity               | Hypersensitive (Ara-C 3-4x, DNA Repair 2025)  | Unknown (depends on NMD escape)                          | Not characterized                        |
| Current ClinVar classification | Pathogenic/Likely Pathogenic                  | Usually VUS or absent                                    | Pathogenic for FILS/IMAGe-I              |
| gnomAD expected                | Rare                                          | Absent (de novo or ultra-rare dominant)                  | Very rare (AR carrier frequency)         |
| Population cancer enrichment   | Enriched in PPAP families                     | NOT enriched (0.22% cases vs 0.20% controls)             | Not applicable (recessive)               |
| Inheritance                    | Autosomal dominant                            | Unknown                                                  | Autosomal recessive                      |

## Key Literature Updates (2024-2026)

| Year | Finding                                                                                                         | Impact                                          | Source                       |
| ---- | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | ---------------------------- |
| 2023 | Gene-specific ACMG/AMP classification for POLE/POLD1 EDM variants (128 variants, 17 P/LP, 17 B/LB)              | PVS1 does not apply to truncations for PPAP     | Genome Medicine              |
| 2024 | POLD1 proofreading deficiency is recessive at cellular level -- hypermutation requires somatic LOH of WT allele | LOH is primary mechanism, not dominant-negative | EJHG                         |
| 2024 | Toripalimab Phase II: 66.7% ORR for EDM vs 9.1% for non-EDM POLE mutations                                      | ICI efficacy depends on variant class           | Signal Transduct Target Ther |
| 2024 | Human POLE1 catalytic domain dispensable for CMG assembly (needed for replication initiation)                   | CMG disruption hypothesis downgraded            | Nature Comms 2022            |
| 2024 | Cryo-EM: 3-point Pol-epsilon/PCNA interface resolved                                                            | New structural data for PCNA hypothesis         | Nature Comms                 |
| 2025 | First duodenal adenocarcinomas in germline POLD1 carriers                                                       | PPAP spectrum expanding                         | Front Oncol                  |
| 2025 | MSS/POLE CRC complete pathologic response to pembrolizumab (37 months)                                          | ICI works in MSS POLE-mutated tumors            | AME Med J                    |
| 2025 | PolED database: 67 POLE + 69 POLD1 variants with functional data; LoF explicitly excluded from PPAP             | Authoritative functional evidence resource      | Database (Oxford)            |
| 2025 | Comparative somatic vs germline proofreading deficiency (360 tumors, 70 families, 31 PVs)                       | Variant-specific risk profiles established      | Modern Pathology             |
| 2025 | LOP POLE stratification: only 7.5% of POLE mutations are LOP; non-LOP shows no ICI benefit (41 CRC pts)         | Critical for ICI patient selection              | JITC (MD Anderson)           |
| 2025 | POLD1 beyond proofreading: BIR-induced LOH, immune evasion orchestration                                        | LOH mechanism expanded                          | Front Immunol                |
| 2025 | Cryo-EM proofreading intermediates: 6nt unwinding/scrunching in Pol-epsilon-PCNA holoenzyme                     | Structural basis for EDM pathogenicity          | bioRxiv/PNAS                 |
| 2025 | MAVISp structural analysis: 43,415 POLE + 21,014 POLD1 variants computationally classified                      | Large-scale VUS prioritization                  | bioRxiv                      |
| 2025 | POLE/POLD1 exo-deficient cells hypersensitive to Ara-C (3-4x IC50 reduction)                                    | New therapeutic: chain-terminating nucleosides  | DNA Repair                   |
| 2025 | Neoadjuvant ICI for MSI-H/POLE-mutated locally advanced CRC: R0 100%, pCR 70%                                   | Neoadjuvant ICI paradigm                        | ScienceDirect                |
| 2025 | Non-EDM POLE/POLD1 mutations can contribute to high/ultrahigh TMB (ASCO)                                        | Broadens variant-TMB landscape                  | JCO (ASCO abstract)          |
| 2026 | Clonal neoantigen crucial for ICI response; stochastic branching-process model in CRC                           | Neoantigen quality > quantity                   | Nature Comms                 |
| 2026 | NeoPrecis: clonality-aware neoantigen prediction, +11-20% AUROC over TMB alone                                  | Beyond TMB for ICI prediction                   | Nature Comms                 |
| 2026 | CTNAs targeting genome maintenance defects: Ara-C + CTF18-loss synthetic lethality with POLE exo-deficiency     | Precision nucleoside analog therapy             | Cancer Science               |
