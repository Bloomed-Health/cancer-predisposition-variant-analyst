---
name: cancer-predisposition-variant-analyst
description: |
  Ultra-rare disease variant interpretation: mechanistic paradox resolution, clinical
  classification, literature synthesis, and therapeutic target mapping.
  TRIGGER when: user presents a genotype-phenotype paradox (variant that should not
  cause the observed phenotype), asks about POLE/POLD1 truncation
  variants in cancer predisposition, needs to resolve mechanistic contradictions in
  multi-domain disease genes where truncation outside the canonical disease region
  produces the expected phenotype, asks about early-exon truncations where translation
  reinitiation could yield an N-terminally truncated protein, or is drafting a case
  report for an ultra-rare variant that challenges established classification frameworks.
  DO NOT TRIGGER when: user needs routine panel interpretation with no
  genotype-phenotype conflict, routine ACMG classification without a paradox element,
  pharmacogenomics interpretation, common population variant annotation, or
  somatic-only tumor profiling without a germline predisposition question.
metadata:
  author: Bloomed-Health
  version: "2.0.0"
  last_verified: "2026-11-22"
  tags: rare-disease,genomics,PPAP,POLE,variant-classification,mechanistic-hypothesis,cancer-predisposition,therapeutic-targets
---

# Cancer Predisposition Variant Analyst Skill

Interpret ultra-rare variants, resolve genotype-phenotype paradoxes, assemble
clinical-grade evidence, and map mechanism to therapeutic opportunity. Designed
for research teams working on novel findings in cancer predisposition, DNA repair,
and replication-fidelity disorders.

The canonical worked example throughout this skill is a germline **POLE
frameshift, NM_006231.4:c.158_159del p.(Leu53Glnfs*5)** (exon 2 of 49; PTC at
codon 57 of 2,286, 2.5% into the CDS), reported in a patient with an
ultra-hypermutated PPAP-like phenotype. By current consensus a POLE null allele
should not do this. The reasoning template for resolving that conflict applies to
any truncation variant in a multi-domain disease gene; a second worked example
(BRCA1 c.68_69del) is in [examples/brca1-c68_69del.md](examples/brca1-c68_69del.md).

> **Why this is a paradox:** PPAP is caused by missense variants in the POLE/POLD1
> exonuclease domain that yield a functional-but-error-prone polymerase [F1][C1].
> Heterozygous POLE LoF is seen in ~0.2% (1/500) of controls and is not enriched
> in cancer cases [P6]; biallelic hypomorphic POLE alleles cause recessive
> developmental syndromes (FILS [O2], IMAGe-I [O3]), not cancer predisposition. POLE is a
> pan-essential gene [M10]: a tumour cannot be POLE-null, so "haploinsufficiency
> plus LOH of the wild-type allele" is inviable for a true null and is NOT a
> candidate mechanism (the POLD1 L474P LOH precedent [M1] works only because
> L474P is a hypomorph). Before invoking any novel mechanism, two cheap
> resolutions must be excluded: (1) **coincidence**: the germline LoF allele is an
> incidental finding and the hypermutation is driven by a somatic POLE/POLD1
> exonuclease-domain mutation (P286R, V411L, S459F, etc.) or by MMR deficiency
> (CMMRD/Lynch, SBS14/20 [M11][SIG6]); (2) **translation reinitiation**: the
> exon-2 PTC lies 9 codons upstream of in-frame Met66, and reinitiation would
> produce an N-terminally truncated POLE retaining the exonuclease (aa 268–471),
> polymerase and C-terminal CMG-binding regions, i.e. not a null at all
> (precedent: RING-less BRCA1 from c.68_69del [M8]). Only if both fail does a
> genuinely novel mechanism need to be argued.

---

## Workflow

0. **Verify genotype and exclude phenocopies** — Confirm the call (read-level
   evidence, HGVS validation, germline vs. clonal haematopoiesis), then rule out
   the cheap explanations: somatic POLE/POLD1 EDM hotspot in the tumour, MMR
   deficiency (MSI/IHC, CMMRD), other polyposis genes (MUTYH, NTHL1, MBD4 [P7][P8]).
   Fork on mutational signature: SBS10a/10b/28 = POLE exo; SBS10c/10d = POLD1;
   SBS14/20 = combined with MMR deficiency [M9][SIG6].
   → [variant-interpretation.md#step-0-genotype-verification-and-differential-diagnosis](variant-interpretation.md#step-0-genotype-verification-and-differential-diagnosis)

1. **Characterize the variant** — Establish precise molecular consequence: reading
   frame, PTC position, predicted NMD fate [M12], downstream in-frame Met codons and
   Kozak context, protein domain map, gnomAD/ClinVar/LOVD status.
   → [variant-interpretation.md#step-1-precise-molecular-consequence](variant-interpretation.md#step-1-precise-molecular-consequence),
   [#step-2-protein-domain-map](variant-interpretation.md#step-2-protein-domain-map),
   [#step-3-population-database-assessment](variant-interpretation.md#step-3-population-database-assessment)

2. **Resolve the mechanistic paradox** — Run the essential-gene filter and the
   signature fork, then rank hypotheses (reinitiation first for early-exon PTCs)
   and pick the minimum experiment set that discriminates between them.
   → [mechanistic-framework.md#pre-checks-essential-gene-filter-and-signature-fork](mechanistic-framework.md#pre-checks-essential-gene-filter-and-signature-fork),
   [#hypothesis-ranking-table](mechanistic-framework.md#hypothesis-ranking-table),
   [#minimum-discriminating-experiment-set](mechanistic-framework.md#minimum-discriminating-experiment-set)

3. **Assemble clinical evidence** — Apply ACMG/ClinGen criteria with Bayesian
   points [C8]; PVS1 only where LoF is the established mechanism [C7]; PM2 at
   Supporting [C12]; PS3/BS3 graded per Brnich [C9]; calibrated PP3/BP4 [C10][C11].
   → [variant-interpretation.md#step-4-acmgclingen-criteria-assembly](variant-interpretation.md#step-4-acmgclingen-criteria-assembly),
   [#step-5-evidence-table-template](variant-interpretation.md#step-5-evidence-table-template)

4. **Synthesize literature** — Execute structured search protocol across PubMed,
   ClinVar submissions, gnomAD constraint data, and relevant preprint servers.
   → [literature-protocol.md](literature-protocol.md)

5. **Map therapeutic targets** — Translate mechanism into actionable therapeutic
   hypotheses, stratified by evidence tier and regulatory pathway. Therapy follows
   the tumour's actual mutator (somatic EDM, MMRd, or reinitiated germline product),
   not the germline label.
   → [therapeutic-mapping.md](therapeutic-mapping.md)

---

## What You Get

- Step-0 phenocopy exclusion checklist (somatic EDM, MMRd/CMMRD, other polyposis genes, signature fork)
- Mechanistic hypothesis ranking with experimental discriminators
- Bayesian-points ACMG tally (Supporting 1, Moderate 2, Strong 4, Very Strong 8; P ≥10, LP 6–9, VUS 0–5) [C8]
- ACMG/ClinGen evidence table ready for classification committee
- Structured literature gap analysis
- Therapeutic target map linked to mechanism
- Case report / manuscript outline for novel findings

---

## Guardrails

- Never output Likely Pathogenic or Pathogenic for POLE–PPAP from a LoF allele
  without functional evidence (PS3 per [C9]) under a valid gene–disease
  mechanism assertion [C13]. Default for a POLE LoF allele and PPAP is **VUS**;
  PVS1 is not applied because LoF is not the established PPAP mechanism [C7].
- Never recommend cascade testing of relatives on a VUS. NCCN surveillance ages
  (colonoscopy from 25–30 y, q2–3 y [G1]) apply only once a variant is LP/P.
- Never propose "haploinsufficiency + LOH" for a POLE null allele; POLE is
  cell-essential [M10].
- Always give denominators with percentages (e.g. "66.7% (2/3)" [T1]).
- Always state the `last_verified` date (2026-11-22) when citing 2024–2026
  literature, trial status, or database counts; these change.
- Cite only reference IDs present in [references.md](references.md).

---

## Sub-files

| File                                                               | Content                                                                                      |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| [variant-interpretation.md](variant-interpretation.md)             | Step 0 phenocopy exclusion, molecular consequence, domain map, gnomAD, ACMG/ClinGen with Bayesian points |
| [mechanistic-framework.md](mechanistic-framework.md)               | Essential-gene filter, signature fork, ranked hypotheses, discriminating experiments, generalizable template |
| [literature-protocol.md](literature-protocol.md)                   | Search strategy, evidence grading, gap analysis                                              |
| [therapeutic-mapping.md](therapeutic-mapping.md)                   | Mechanism-to-target pipeline, clinical trial landscape, biomarker strategy                   |
| [references.md](references.md)                                     | Canonical bibliography with URLs, organized by topic, citation guidance                      |
| [quick-reference.md](quick-reference.md)                           | POLE/POLD1 variant class comparison, signature table, literature updates (2024–2026)         |
| [examples/brca1-c68_69del.md](examples/brca1-c68_69del.md)         | Second worked example: BRCA1 185delAG, reinitiation to RING-less BRCA1, PARPi resistance      |
| [evals/README.md](evals/README.md)                                 | Manual eval prompts with expected behaviours and failure modes                               |
| [scripts/README.md](scripts/README.md)                             | Optional stdlib-only helpers: HGVS validation, gnomAD, ClinVar, reference link check        |
| [CHANGELOG.md](CHANGELOG.md)                                       | Version history                                                                              |
