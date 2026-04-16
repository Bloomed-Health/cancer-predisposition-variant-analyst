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
| [quick-reference.md](quick-reference.md)               | POLE variant class comparison table + literature updates (2024-2026)       |
