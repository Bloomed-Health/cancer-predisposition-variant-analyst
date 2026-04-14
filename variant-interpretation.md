---
title: Variant Interpretation
impact: CRITICAL
impactDescription: Foundational molecular characterization — errors here propagate through all downstream analysis
tags: variant-classification,ACMG,ClinGen,NMD,domain-mapping,gnomAD,POLE,PPAP
---

# Variant Interpretation

Systematic molecular characterization of an ultra-rare variant from DNA sequence
to clinical classification. Steps are sequential — do not skip ahead to ACMG
criteria without completing domain mapping and NMD prediction.

---

## Step 1: Precise Molecular Consequence

For any frameshift or nonsense variant, establish:

```
Transcript:         NM_006231.4 (POLE canonical)
cDNA change:        e.g. c.158_159del
Protein change:     p.Leu53Valfs*2  (truncation at ~aa 54)
Reading frame:      confirmed shifted (+1, +2, or -1)
Stop codon position: aa 54 of 2,286 (2.4% of full-length protein)
Predicted NMD:      YES — stop >55 nt upstream of last exon-exon junction
Exon location:      Exon 2 of 49 (far upstream → strong NMD prediction)
```

**NMD prediction rules of thumb:**

- Stop codon >50–55 nt upstream of the last exon-exon junction → NMD predicted
- Stop codon in final exon or within 50 nt of final junction → NMD escape likely
- Long 3′ UTR (>1 kb) → increased NMD sensitivity
- Early exon stops (exon 1–3) → highly NMD-sensitive; but some escape via
  reinitiation or exon skipping

**Critical distinction for paradox resolution:**
An NMD-predicted variant that escapes NMD produces a truncated protein with
potential gain-of-function or dominant-negative properties. Confirm NMD fate
with allele-specific RNA-seq or nonsense suppression assay before concluding
haploinsufficiency is the sole mechanism.

---

## Step 2: Protein Domain Map (POLE-specific)

```
POLE protein (2,286 aa):

  1    54                268        471         580              1260    2286
  |----[N-term / CMG interaction]----[Exonuclease]----[Polymerase domain]----[C-term]
             ↑
       TRUNCATION POINT (this patient)
       Eliminates: ALL domains including exo (268-471) and pol (580-1260)
       Retains:    First 53 aa of N-terminal region only
```

**Key N-terminal features (aa 1–54):**

- Includes the P-domain / processivity domain initiation region
- aa 1–50 contain surfaces for interaction with GINS (Psf1, Psf2, Psf3) in
  the CMG (Cdc45-MCM-GINS) replisome complex
- PCNA interaction via PIP-box begins ~aa 20–30 in some species homologs
- This region is conserved across eukaryotes — its specific conservation
  pattern is a mechanistic clue, not just background

**For non-POLE variants**, substitute your gene's domain map. Key questions:

- What fraction of the protein is retained?
- Does the retained fragment include any known interaction surfaces?
- Is the truncation point within a disordered linker (less likely to form
  stable fold) or a structured domain (may fold and mis-function)?

---

## Step 3: Population Database Assessment

Check in order:

| Database       | Query              | Key metric                                    |
| -------------- | ------------------ | --------------------------------------------- |
| gnomAD v4 [D1] | Gene + position    | AC=0 -> absent; pLI, LOEUF                    |
| ClinVar [D2]   | Gene + variant     | Existing classifications, submitter evidence  |
| LOVD [D3]      | Gene-specific LOVD | Functional data, international submissions    |
| DECIPHER [D4]  | Phenotype + gene   | Overlapping patients, CNV context             |
| HGMD [D5]      | Gene               | Published mutations, literature links         |
| VarSome [D6]   | Variant            | Aggregated pre-classification                 |
| PolED [C2]     | Gene + variant     | Curated functional data from 90 publications  |
| MAVISp [C3]    | Gene + variant     | Structural VUS prioritization (>64K variants) |

**gnomAD constraint metrics for POLE:**

- pLI: ~0.0 -- consistent with heterozygous LoF being tolerated. This is NOT
  misleading: heterozygous POLE LoF does not cause PPAP. PPAP requires a
  functional-but-error-prone polymerase (EDM missense), not absence of the protein.
- LOEUF: check -- but interpret with caution: low LOEUF reflects developmental
  constraint (biallelic LoF causes FILS/IMAGe-I), not cancer predisposition
- o/e LoF: reflects constraint against biallelic loss, not heterozygous loss

**Population-level cancer association data [P6]:**

- POLE LoF: 0.22% in cancer cases vs 0.20% in controls -- no enrichment
- PolED [C2]: "LoF variants cannot cause ultramutated cancers"

> **Critical context: POLE LoF is NOT cancer-predisposing by established
> evidence.** Biallelic POLE LoF causes FILS [O2] and IMAGe-I [O3] --
> recessive congenital disorders, not cancer. If a POLE truncation variant
> is found in a patient with PPAP phenotype, this is a paradox -- not a
> straightforward application of PVS1.

**Key classification resources** (see [references.md](references.md)):

- **PolED** [C2]: 67 POLE + 69 POLD1 variants, 90 publications. Supports PS3/BS3.
- **MAVISp** [C3]: 43,415 POLE + 21,014 POLD1 variants. >300 VUS flagged.
  Missense focus; truncations not assessed as pathogenic.
- **Modern Pathology** [P2]: 360 tumors, 70 families. AlphaMissense 0.87-1.0
  for all P/LP. Aggressive phenotypes linked to specific variants.

---

## Step 4: ACMG/ClinGen Criteria Assembly

Apply ACMG/AMP 2015 [C6] + ClinGen framework, informed by gene-specific
POLE/POLD1 EDM recommendations [C1] (128 variants, 17 P/LP, 17 B/LB).

> **PVS1 caveat for truncation variants:** The 2023 gene-specific recommendations
> were developed for non-disruptive EDM variants. PVS1 assumes LoF IS the
> disease mechanism. For PPAP, it is NOT -- the disease mechanism is a
> functional-but-error-prone polymerase. Applying PVS1 to a truncation variant
> for PPAP classification is therefore non-standard and requires explicit
> justification. If this patient's phenotype proves to arise from a novel
> mechanism (not classical PPAP), PVS1 may still apply under a different
> gene-disease assertion.

### Pathogenic evidence

| Code | Criterion                                         | Applies?           | Notes                                                              |
| ---- | ------------------------------------------------- | ------------------ | ------------------------------------------------------------------ |
| PVS1 | LoF in gene where LoF is disease mechanism        | **CONTESTED**      | LoF is NOT the established PPAP mechanism -- see PVS1 caveat above |
| PM2  | Absent from population databases                  | **YES**            | gnomAD absent, ultra-rare                                          |
| PM6  | Assumed de novo (unconfirmed)                     | Assess             | Confirm with parental testing                                      |
| PS2  | Confirmed de novo in affected, unaffected parents | Apply if trio done |                                                                    |
| PP4  | Phenotype highly specific for gene                | **YES**            | Ultra-hypermutated PPAP phenotype                                  |
| PP3  | Computational evidence supports pathogenicity     | Review             | SpliceAI, CADD, REVEL where applicable                             |

### Classification thresholds

| Criteria combination        | Classification                            |
| --------------------------- | ----------------------------------------- |
| PM2 + PP4 + PS2             | **Likely Pathogenic** (if PVS1 excluded)  |
| PVS1 + PM2 + PP4            | **Likely Pathogenic** (if PVS1 justified) |
| PVS1 + PM2 + PP4 + PS2      | **Pathogenic** (if PVS1 justified)        |
| Above + functional evidence | **Pathogenic** (strong)                   |

### PVS1 strength modulation for truncation variants (ClinGen LoF SVI):

| Scenario                                                          | PVS1 strength |
| ----------------------------------------------------------------- | ------------- |
| NMD predicted, LoF is established mechanism                       | Very Strong   |
| NMD escape predicted or uncertain, dominant-negative possible     | Strong        |
| Truncation in 3′ terminal exon (<10% of coding sequence affected) | Moderate      |
| LoF mechanism uncertain for this gene                             | Moderate      |

For the POLE p.54fs case: NMD predicted (very early exon). However, PVS1
applicability is contested because LoF is not the established PPAP mechanism.
If PVS1 is applied, it requires a novel gene-disease assertion (e.g., "POLE
truncation-associated hypermutation syndrome") distinct from classical PPAP.
Functional studies are prerequisite before final classification regardless
of PVS1 decision.

### Loss-of-Proofreading (LOP) Classification (JITC 2025)

The MD Anderson LOP POLE stratification framework (J ImmunoTher Cancer, Nov
2025, 41 CRC patients) establishes a critical distinction:

- Only **7.5%** of all POLE mutations (148/1,965 in 69,223-patient pan-cancer
  cohort) qualify as loss-of-proofreading (LOP)
- LOP mutations: excellent ICI response, poor chemotherapy response
- Non-LOP mutations: outcomes identical to POLE wild-type
- Endometrial (6.6%) and CRC (1.2%) are the only tumor types with >1% LOP
  POLE incidence
- National guidelines (FIGO, NCCN) should categorize POLE alleles as LOP
  vs non-LOP

**Relevance to truncation variants:** A truncation variant is definitionally
non-LOP (it eliminates the polymerase rather than corrupting proofreading).
Under this framework, truncation variants would predict no ICI benefit --
UNLESS the paradoxical mechanism produces a hypermutated phenotype through
an alternative path (e.g., LOH + haploinsufficiency).

---

## Step 5: Evidence Table Template

```markdown
## Variant Classification Evidence Summary

**Variant:** POLE c.158_159del (p.Leu53Valfs\*2)
**Gene/Disease:** POLE / PPAP (OMIM 615083)
**Classification:** Likely Pathogenic (pending functional studies)

| ACMG Code | Evidence                                                     | Strength                            |
| --------- | ------------------------------------------------------------ | ----------------------------------- |
| PVS1      | Frameshift, NMD-predicted; but LoF is NOT the PPAP mechanism | Contested -- requires new assertion |
| PM2       | Absent gnomAD v4 (0/~730,000 alleles)                        | Moderate                            |
| PP4       | Ultra-hypermutated colorectal polyposis phenotype            | Supporting                          |
| [PS2]     | [Parental testing pending]                                   | [Strong, if confirmed de novo]      |

**Unresolved:** NMD escape / dominant-negative mechanism not excluded.
**Recommended:** Tumor RNA-seq (allele-specific expression), truncated protein
western blot, patient-derived organoid replication fidelity assay.
```
