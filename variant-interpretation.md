---
title: Variant Interpretation
impact: CRITICAL
impactDescription: Foundational molecular characterization — errors here propagate through all downstream analysis
tags: variant-classification,ACMG,ClinGen,NMD,domain-mapping,gnomAD,POLE,PPAP
---

# Variant Interpretation

Systematic molecular characterization of an ultra-rare variant from DNA sequence
to clinical classification. Steps are sequential — do not skip ahead to ACMG
criteria without completing Step 0 (genotype verification and differential
diagnosis), domain mapping and NMD prediction.

---

## Step 0: Genotype Verification and Differential Diagnosis

Before any "paradox" is invoked, exclude the mundane explanations. Most
apparent germline-truncation + hypermutation cases resolve here.

### 0a. Confirm the germline call

| Check                | Requirement                                                                                                              |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Tissue               | Variant present in blood or non-tumour normal tissue, not tumour-only                                                    |
| VAF                  | ~50% (heterozygous). VAF <35% or >65% in blood -> consider mosaicism, clonal haematopoiesis, or tumour contamination      |
| Mosaicism            | If VAF low, test a second tissue (buccal, skin fibroblasts) and parents                                                  |
| HGVS                 | Validate with VariantValidator: `python3 scripts/hgvs_validate.py "NM_006231.4:c.158_159del"` -> expect p.(Leu53GlnfsTer5) |
| Transcript           | Confirm MANE Select NM_006231.4 / ENST00000320574 (POLE-201, chr12 minus strand); report genomic coordinate (GRCh38 NC_000012.12:g.132681183_132681184del) |
| Orthogonal method    | Sanger or second NGS library confirming the deletion                                                                     |

### 0b. Complete POLE coverage

A single truncation does not establish that the other allele is intact or that
no second POLE event is present.

- All 49 coding exons sequenced at adequate depth (report minimum depth per exon)
- Exon-level CNV analysis (read-depth or MLPA) — a deletion on the other allele
  changes the interpretation entirely
- Promoter and 5′ UTR coverage
- Deep intronic variants: WGS or RNA-seq if exome-only; run SpliceAI on all rare
  intronic calls
- **Phasing**: if a second POLE variant (especially an EDM missense) is present,
  determine cis/trans by long reads, parental testing, or read-backed phasing.
  A trans EDM allele makes the truncation irrelevant to the hypermutator
  phenotype; a cis EDM allele makes it irrelevant for a different reason (the
  EDM allele would be NMD-degraded).

### 0c. Tumour analysis — required before invoking a paradox

| Assay                        | What to look for                                                                                             | Interpretation if positive                                                       |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| Somatic POLE EDM             | Hotspots P286R, V411L, S459F, A456P, F367S, L424V, M444K, P436R (~1–2% CRC, ~7–10% endometrial)             | Hypermutation explained by somatic EDM; germline truncation is a bystander        |
| Somatic POLD1 EDM            | Exo domain aa 304–533 (e.g. D316, S478)                                                                      | Hypermutation explained; signatures SBS10c/SBS10d expected [M9]                  |
| MMR IHC + MSI                | Loss of MLH1/PMS2/MSH2/MSH6; MSI-H                                                                           | dMMR hypermutator (Lynch, sporadic MLH1 methylation, or CMMRD); SBS6/15/26/44     |
| Mutational signatures        | SBS10a/SBS10b/SBS28 (POLE exo) [SIG1–SIG4]; SBS10c/d (POLD1) [M9]; SBS14 (POLE exo + dMMR) [SIG6]; SBS20 (POLD1 + dMMR) | Signature fork decides which pathway is actually defective (see mechanistic-framework.md Pre-checks) |
| TMB and SNV/indel ratio      | POLE-EDM tumours: TMB >100 mut/Mb, SNV-dominant, MSS                                                         | Ultra-hypermutation with MSS strongly implies a proofreading defect somewhere      |
| LOH at POLE locus            | Allele-specific copy number at chr12q24.33                                                                   | Note: POLE is essential, so loss of the WT allele with a null germline allele is inviable (see Step 2) |

### 0d. Germline phenocopies

| Syndrome                        | Genes                                  | Discriminating features                                                                                                   |
| ------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| CMMRD                           | Biallelic MLH1/MSH2/MSH6/PMS2          | Café-au-lait macules, childhood haematologic/brain tumours, consanguinity; tumours often acquire secondary POLE/POLD1 EDM hits and reach the highest TMBs observed [M11] |
| Lynch syndrome                  | Monoallelic MMR genes, EPCAM           | dMMR tumours, MSI-H, family history                                                                                       |
| MUTYH-associated polyposis      | Biallelic MUTYH                        | SBS18/SBS36, G>T transversions, recessive                                                                                 |
| NTHL1-associated polyposis [P8] | Biallelic NTHL1                        | SBS30, multi-tumour phenotype, recessive                                                                                  |
| MBD4 deficiency [P7]            | Biallelic MBD4                         | SBS1-like CpG>TpG excess, polyposis, uveal melanoma, AML                                                                  |
| PPAP (classical)                | Germline POLE/POLD1 EDM missense       | SBS10a/b/28 or SBS10c/d; the established mechanism [P1, C1]                                                               |

Run a germline hereditary-cancer panel covering all of the above before
treating a POLE truncation as causal.

### 0e. Coincidence prior

> **The null hypothesis is coincidence, not paradox.**
> Heterozygous POLE LoF carriers: ~0.20% of controls (~1/500) [P6].
> Somatic POLE EDM: ~1–2% of CRC.
> Expected co-occurrence in CRC: 1/500 × 1/50–1/100 ≈ 1 in 25,000–50,000 CRC
> patients. With >1.9 million CRC diagnoses per year worldwide, dozens of
> patients per year are expected to carry an incidental germline POLE LoF
> allele AND a somatic hypermutator. Observing one such patient is not
> evidence for a novel mechanism.

### Paradox gate

Proceed to [mechanistic-framework.md](mechanistic-framework.md) only if **all**
of the following are negative/confirmed:

- [ ] Germline status confirmed (normal tissue, VAF ~50%, orthogonal method)
- [ ] HGVS validated; transcript confirmed
- [ ] Full POLE coverage: no second POLE SNV/indel/CNV; phasing done if present
- [ ] No somatic POLE EDM in any tumour
- [ ] No somatic POLD1 EDM in any tumour
- [ ] MMR proficient (IHC intact, MSS)
- [ ] Mutational signatures do not identify an alternative driver
- [ ] Germline phenocopy panel negative (MMR genes, MUTYH, NTHL1, MBD4)
- [ ] Phenotype exceeds what coincidence predicts (e.g. ≥2 independent
      hypermutated tumours, or segregation with disease in ≥2 relatives)

If any box is unchecked, the correct conclusion is "hypermutation explained by
X; germline POLE truncation is an incidental finding of uncertain
significance", and Steps 1–5 are completed for the record only.

---

## Step 1: Precise Molecular Consequence

For any frameshift or nonsense variant, establish:

```
Transcript:          NM_006231.4 / ENST00000320574 (POLE-201, MANE Select)
Genomic:             NC_000012.12:g.132681183_132681184del (GRCh38)
cDNA change:         c.158_159del
Protein change:      p.(Leu53GlnfsTer5)  — written p.(Leu53Glnfs*5)
Reading frame:       -2 shift; 4 novel codons then PTC
Stop codon position: codon 57 of 2,286 (2.5% of full-length protein)
Exon location:       exon 2 of 49
Predicted NMD:       YES — PTC >50–55 nt upstream of the last exon-exon junction
```

**NMD prediction rules [M12]:**

- PTC >50–55 nt upstream of the last exon-exon junction -> NMD predicted
- PTC in the final exon or within 50–55 nt of the final junction -> NMD escape
- PTC within ~150 nt of the start codon -> NMD is frequently inefficient
  (start-proximal rule; reinitiation downstream is a major cause)
- Long exons (>400 nt) harbouring the PTC -> reduced NMD efficiency
- Long 3′ UTR -> increased NMD sensitivity
- c.158_159del: PTC at c.169–171, i.e. ~170 nt from the start codon — borderline
  for the start-proximal rule; NMD efficiency should not be assumed

### Reinitiation scan

A start-proximal PTC can be bypassed by leaky scanning or reinitiation at a
downstream in-frame AUG, yielding an N-terminally truncated protein that is
NMD-resistant. In-frame Met codons downstream of the PTC (CDS scan of
ENST00000320574):

| Codon  | Kozak context       | Distance past PTC | Predicted product                                   |
| ------ | ------------------- | ----------------- | --------------------------------------------------- |
| Met66  | adequate (ATTAACATGC) | 9 codons        | ΔN65-POLE: retains exo (268–471), pol, C-terminal CMG-binding half |
| Met221 | adequate            | 164 codons        | ΔN220-POLE: loses most of the catalytic NTD         |
| Met294/295 | adequate      | ~238 codons       | Inside exo domain; unlikely to fold                 |
| Met299 | weak                | 242 codons        | Inside exo domain; unlikely to fold                 |
| Met359 | strong (ACCATCATGG) | 302 codons        | ΔN358-POLE: truncated exo domain                    |

The relevant candidate is **Met66**: only 9 codons past the PTC, adequate
context, and reachable by leaky scanning as well (AUG1 is in a weak context,
GGCTCC**ATG**T, after a 27-nt 5′ UTR). The resulting ΔN65-POLE would lack the
disordered N-terminus (aa 1–30), the first helix (aa 25–47) and the first
β-strand (aa 57–65) of the N-terminal domain [M3, S5] while keeping the
exonuclease, polymerase, all three PCNA contacts (P-domain, thumb, PIP-motif
1180–1187) and the C-terminal replisome-interaction half intact. Whether the
NTD folds without its first strand is unknown (see mechanistic-framework.md H1).

**Precedent [M8]:** BRCA1 c.68_69del (185delAG) places a PTC in exon 3, yet
translation reinitiates at Met297 and produces a RING-less BRCA1 protein that
is stable and partially functional. Reinitiation-mediated NMD escape is a
documented phenomenon in a predisposition gene and must be excluded, not
assumed absent.

**This question is answered experimentally, not computationally:**

1. Allele-specific RNA quantification (RNA-seq or ddPCR across the deletion)
   from patient lymphocytes ± cycloheximide (CHX). Mutant:WT ratio ~1:1 after
   CHX but <1:1 without -> NMD active. Ratio ~1:1 without CHX -> NMD escape.
2. Western blot with a **C-terminal** POLE antibody on patient cells: a band
   ~7 kDa below full-length indicates ΔN65-POLE. An N-terminal antibody will
   not detect the reinitiation product.
3. If a product is detected, mass spectrometry of the N-terminal peptide to
   identify the initiation codon.

**Critical distinction for paradox resolution:** If NMD is efficient, the
allele is null and the only tumour-level consequence is a 50% reduction in POLE
dosage in an essential gene (see Step 2). If a reinitiation product exists, the
question becomes whether ΔN65-POLE has altered fidelity or PCNA/Ctf18
interaction — a testable hypothesis handled in mechanistic-framework.md.

---

## Step 2: Protein Domain Map

```
POLE (Q07864, 2,286 aa) — approximate boundaries:

  1   30    57  65      268       471  ~520   684-729  1085-1117 1180-1187 ~1300            2286
  |----|-----|--|--------|---------|----|------|--------|---------|--------|-----------------|
   dis   NTD (helix 25-47, strand 57-65 ...)  exo      polymerase (P-domain, thumb, PIP     C-terminal non-catalytic
                                              268-471   -> three-point PCNA interface [M3])  half: POLE2/GINS/CMG [M2, M7]
          ^
      PTC codon 57 (this patient)
      Eliminates: everything from aa 57 onward, including exo and pol
      Retains:    aa 1–52 native + 4 frameshifted residues — i.e. nothing
                  functional. Full-length product only if reinitiation (Step 1)
```

**Key N-terminal features (aa 1–~270, the catalytic N-terminal domain) [M3, S5]:**

- aa 1–30: disordered (aa 1–23 invisible in the human Pol ε–PCNA cryo-EM map)
- aa 25–47: first α-helix; aa 57–65: first β-strand of the NTD β-sheet. The
  NTD packs against the exonuclease domain in B-family polymerases.
- **The PCNA interface is NOT in this region.** The three PCNA contacts are the
  P-domain (His684–Lys729), the thumb (Glu1085, Ser1117) and the PIP-motif at
  aa 1180–1187 [M3]; a ΔN65 product retains all of them.
- Exonuclease domain aa 268–471 (Castillejo 2023 boundaries [C1]); all PPAP
  EDM hotspots lie here
- Polymerase domain approx. aa 520–1180
- **aa 1–65 contain NO CMG surface.** CMG/GINS binding is mediated entirely by
  the C-terminal non-catalytic half (~1300–2286): the zinc-finger region binds
  POLE2, which contacts Psf1/MCM5; the inactive pol-like domain's thumb contacts
  MCM2/Cdc45 [M2, M7]. A truncation at codon 57 does not touch any replisome
  interface, and ΔN65-POLE would retain all of them.

**Essentiality constraint.** POLE is a pan-essential gene (DepMap common
essential [M10]; yeast *pol2Δ* is lethal; cells tolerate loss of the catalytic
half only when the C-terminal half remains [M2]). Therefore a tumour cannot be
POLE-null: for a true null germline allele, loss of heterozygosity of the WT
allele is inviable, and the "haploinsufficiency + LOH" route used for the POLD1
L474P precedent [M1] is unavailable (L474P is a hypomorph, not a null).

**For non-POLE variants**, substitute your gene's domain map. Key questions:

- What fraction of the protein is retained?
- Does the retained fragment include any known interaction surfaces?
- Is the truncation point within a disordered linker (less likely to form
  stable fold) or a structured domain (may fold and mis-function)?
- Is the gene cell-essential? (DepMap [M10]) — if yes, a null allele cannot
  undergo two-hit loss in a viable tumour.

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

gnomAD v4.1 comprises ~807,000 individuals (~730,000 exomes + ~76,000 genomes),
i.e. ~1.6 million alleles. Report absence as "0/~1.6 M alleles", and use the
non-cancer subset for PM2 [C1]. `python3 scripts/gnomad_lookup.py` returns
allele counts and the constraint metrics below.

**gnomAD constraint metrics for POLE:**

- pLI ≈ 0 (1.1e-40, gnomAD v4.1, 2026-11-22) -- heterozygous LoF is tolerated.
  This is NOT misleading: heterozygous POLE LoF does not cause PPAP. PPAP
  requires a functional-but-error-prone polymerase (EDM missense), not absence
  of the protein.
- LOEUF 0.76 (o/e LoF 0.67, 188 observed / 279 expected): moderate depletion,
  consistent with recessive developmental constraint (FILS/IMAGe-I are caused
  by biallelic hypomorphic alleles; biallelic null is not observed, as expected
  for an essential gene [M10]) -- not with dominant cancer predisposition.
- Missense z = 2.44 (o/e 0.90): mild missense constraint; EDM hotspots are not
  visible at gene level.
- **ClinVar reality check (2026-11-22):** of 678 POLE frameshift/nonsense
  records, 301 are "Pathogenic" -- almost all single-submitter commercial-lab
  assertions with condition "not provided" (recessive FILS/IMAGe-I carrier
  logic or blanket PVS1), 216 conflicting (typically one lab P vs another VUS),
  145 VUS, 0 B/LB. Under hereditary-cancer / polyposis conditions there is no
  concordant P/LP truncating POLE variant. A report that calls a POLE
  truncation "Pathogenic" is not asserting PPAP risk; check the condition
  field before interpreting it (`scripts/clinvar_lookup.py --gene POLE
  --type truncating`).

**Population-level cancer association data [P6]:**

- POLE LoF: 0.22% in cancer cases vs 0.20% in controls -- no enrichment
- PolED [C2]: "LoF variants cannot cause ultramutated cancers"

> **Critical context: POLE LoF is NOT cancer-predisposing by established
> evidence.** Biallelic hypomorphic POLE alleles cause FILS [O2] and IMAGe-I [O3] --
> recessive congenital disorders, not cancer. If a POLE truncation variant
> is found in a patient with PPAP phenotype, first exhaust Step 0; only then
> is it a paradox -- never a straightforward application of PVS1.

**Key classification resources** (see [references.md](references.md)):

- **PolED** [C2]: 67 POLE + 69 POLD1 variants, 90 publications. Supports PS3/BS3.
- **MAVISp** [C3]: 43,415 POLE + 21,014 POLD1 variants. >300 VUS flagged.
  Missense focus; truncations not assessed as pathogenic.
- **Modern Pathology** [P2]: 360 tumors, 70 families. AlphaMissense 0.87-1.0
  for all P/LP. Aggressive phenotypes linked to specific variants.

---

## Step 4: ACMG/ClinGen Criteria Assembly

Apply ACMG/AMP 2015 [C6] + ClinGen SVI refinements [C7, C8, C12], informed by
gene-specific POLE/POLD1 EDM recommendations [C1] (128 variants, 17 P/LP,
17 B/LB). No ClinGen VCEP rules for POLE/POLD1 exist yet (InSiGHT VCEP queue,
verified 2026-11-22).

### Gene–disease assertion gate [C13]

ACMG codes are only defined relative to a gene–disease pair with established
validity. The validated pair is **POLE – PPAP, mechanism = exonuclease-domain
missense**. A truncating allele does not fit that mechanism. If the clinician
wishes to classify the variant for a *different* entity ("POLE
truncation-associated hypermutation"), that entity must first undergo ClinGen
gene–disease validity curation (Definitive/Strong/Moderate/Limited/No
evidence). With a single proband and no mechanism, the validity level is
"No known disease relationship" and no pathogenicity code can be applied for
that entity. The classification below is therefore made against POLE–PPAP.

### PVS1 decision (ClinGen SVI, Abou Tayoun 2018 [C7])

The SVI decision tree is entered only after confirming that LoF is an
established disease mechanism for the gene–disease pair:

| Decision-tree node                                   | Outcome                                                                 |
| ---------------------------------------------------- | ----------------------------------------------------------------------- |
| Is LoF a known mechanism for POLE–PPAP?              | **No** (mechanism is error-prone proofreading; LoF carriers not enriched [P6]) |
| -> PVS1                                              | **NOT APPLIED** at any strength (there is no "Moderate" fallback for an unestablished mechanism) |
| For reference only, if LoF were established:         | NMD-predicted PTC -> Very Strong; NMD-escape with critical region lost -> Strong; NMD-escape, non-critical region, >10% protein removed -> Moderate; 3′-terminal small truncation -> Supporting/none |

### Tumour-signature criteria from Castillejo 2023 [C1]

| Code       | Specification                                                                                                                     | Use for a non-ED allele                                                                                            |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| PP4_Strong | ≥2 tumours from carrier(s) show SBS10a/SBS10b/SBS28/SBS14 at ≥5% contribution                                                     | Specified for EDM variants; a POLE-exo signature in a carrier of a non-ED allele is evidence that *some* POLE/POLD1 exo defect exists, not that this allele causes it. Apply at most as Supporting, and only after Step 0 excludes somatic EDM |
| BP5        | ≥2 tumours with >1 mut/Mb (or >80 SNVs) lacking those signatures                                                                  | Directly informative: hypermutated tumours without POLE-exo signatures argue against a proofreading mechanism for this allele |

### Pathogenic evidence

| Code | Criterion                                         | Applies?           | Strength / notes                                                                              |
| ---- | ------------------------------------------------- | ------------------ | --------------------------------------------------------------------------------------------- |
| PVS1 | LoF in gene where LoF is disease mechanism        | **NOT APPLIED**    | LoF is not an established mechanism for POLE–PPAP [C7]                                        |
| PM2  | Absent/ultra-rare in population databases         | **YES**            | **Supporting** per [C1] (≤1/200,000 alleles, gnomAD non-cancer) and SVI [C12]; one point only  |
| PM6  | Assumed de novo (unconfirmed)                     | Assess             | Confirm with parental testing; do not stack with PS2                                          |
| PS2  | Confirmed de novo in affected, unaffected parents | Apply if trio done | Strong (4 points) only with maternity/paternity confirmed and phenotype consistent            |
| PP4  | Phenotype highly specific for gene                | Conditional        | Supporting only if Step 0 excludes somatic EDM/dMMR; PP4_Strong [C1] is for EDM variants      |
| PP3  | Computational evidence supports pathogenicity     | Review             | **SpliceAI only** for a frameshift (Δ ≥0.2 -> Supporting [C11]); REVEL/CADD/AlphaMissense thresholds [C10] are calibrated for missense and do not apply |
| PS3  | Functional evidence                               | Pending            | Graded per Brnich 2020 [C9], see below                                                        |

### Functional evidence grading (PS3/BS3) per Brnich 2020 [C9]

1. **Assay validity**: the assay must model the proposed disease mechanism.
   For POLE–PPAP that is replication fidelity (mutation-rate or
   proofreading assay). An NMD assay or expression assay alone does not inform
   PS3/BS3 for PPAP.
2. **Controls**: ≥11 pathogenic and benign controls run in the same assay
   permit calibration; fewer controls cap the strength.
3. **OddsPath -> strength**: OddsPath >18.7 -> Strong; 4.3–18.7 -> Moderate;
   2.1–4.3 -> Supporting; <2.1 -> not applied. BS3 symmetrically for odds
   <0.053 (Strong), 0.053–0.23 (Moderate), 0.23–0.48 (Supporting).
4. **Without calibrating controls**: maximum PS3_Supporting / BS3_Supporting,
   regardless of how clean the result looks.

Patient-derived organoid or isogenic cell mutation-accumulation assays for a
reinitiation product (Step 1) can reach Moderate only if run alongside EDM
positive controls (e.g. P286R, V411L) and WT.

### Bayesian points classification (Tavtigian 2020 [C8])

| Strength     | Pathogenic points | Benign points |
| ------------ | ----------------- | ------------- |
| Supporting   | +1                | −1            |
| Moderate     | +2                | −2            |
| Strong       | +4                | −4            |
| Very Strong  | +8                | −8            |

| Total points | Classification    |
| ------------ | ----------------- |
| ≥10          | Pathogenic        |
| 6–9          | Likely Pathogenic |
| 0–5          | VUS               |
| −1 to −6     | Likely Benign     |
| ≤ −7         | Benign            |

**Worked case (c.158_159del, POLE–PPAP):**

| Scenario                                            | Tally                              | Points | Arithmetic result | Recommended output |
| --------------------------------------------------- | ---------------------------------- | ------ | ----------------- | ------------------ |
| Baseline (Step 0 gate passed)                       | PM2_Supp (1) + PP4_Supp (1)        | 2      | VUS               | **VUS**            |
| + confirmed de novo                                 | + PS2 (4)                          | 6      | Likely Pathogenic | **VUS** (see below) |
| + BP5 (≥2 hypermutated tumours lacking SBS10/28/14) | 2 − 1                              | 1      | VUS               | VUS, trending benign for a proofreading mechanism |
| + PS3_Moderate from calibrated fidelity assay       | 2 + 2 (+4 if de novo)              | 4–8    | VUS / LP          | LP only after the gene–disease entity is curated [C13] |

**Why the de novo row is reported as VUS although the arithmetic says LP.** The
points system [C8] presumes that the variant belongs to a class with an
established relationship to the disease (that prior is built into the
framework); PS2 and PP4 are then weighed against that prior. For a POLE
truncation and PPAP that premise fails: the established mechanism is one this
allele cannot execute unless Step 1 demonstrates a protein product. A ClinGen
curator would therefore hold the variant at VUS pending PS3, exactly as the SVI
PVS1 flowchart declines to apply PVS1 when LoF is not the mechanism [C7]. State
this explicitly in the report, show the arithmetic, and do not present LP as an
available "committee option" without the functional data.

**Bottom line:** for POLE–PPAP the output for this variant is **VUS**. Likely
Pathogenic becomes defensible only with (a) PS3 from a calibrated fidelity assay
of a demonstrated protein product (H1), or (b) a separately curated gene–disease
entity in which truncation is the mechanism [C13].

### Loss-of-Proofreading (LOP) Classification (JITC 2025) [T2]

The MD Anderson LOP POLE stratification framework establishes a critical
distinction:

- In a 69,223-patient pan-cancer cohort, POLE was mutated in 2.8% (1,965/69,223)
  and only **7.5% (148/1,965)** of POLE mutations qualify as
  loss-of-proofreading (LOP)
- In 41 POLE-mutant mCRC patients at MDACC: LOP ORR to ICI 88.9% (8/9);
  non-LOP MSI-H ORR 66.7% (6/9)
- LOP mutations: excellent ICI response, poor chemotherapy response;
  non-LOP mutations: outcomes identical to POLE wild-type
- Endometrial (6.6%) and CRC (1.2%) are the only tumour types with >1% LOP
  POLE incidence
- The authors propose that guidelines (FIGO, NCCN) categorise POLE alleles as
  LOP vs non-LOP

**Relevance to truncation variants:** A truncation variant is definitionally
non-LOP (it eliminates the polymerase rather than corrupting proofreading).
Under this framework, truncation variants predict no ICI benefit — UNLESS a
reinitiation product with a proofreading defect is demonstrated (Step 1), or
the tumour carries a separate somatic LOP event (Step 0c), in which case the
somatic event, not the germline truncation, drives ICI eligibility.

---

## Step 5: Evidence Table Template

```markdown
## Variant Classification Evidence Summary

**Variant:** POLE NM_006231.4:c.158_159del p.(Leu53Glnfs*5); PTC codon 57/2,286; exon 2/49
**Gene/Disease:** POLE / PPAP (OMIM 615083)
**Step 0 gate:** [passed / failed — state which item failed]
**Classification:** VUS (POLE–PPAP)
**Why not LP:** LoF is not the established PPAP mechanism (PVS1 not applied [C7]);
PM2 is Supporting only [C1, C12]; the points framework presumes a variant class with
an established disease relationship, which a POLE truncation lacks for PPAP, so PS2/PP4
points are shown but do not lift the call above VUS without PS3; no validated
gene–disease entity for truncation-associated hypermutation [C13].

| ACMG Code | Evidence                                                         | Strength (points)             |
| --------- | ---------------------------------------------------------------- | ----------------------------- |
| PVS1      | Frameshift, NMD-predicted; LoF is NOT the PPAP mechanism         | Not applied (0)               |
| PM2       | Absent gnomAD v4.1 non-cancer (0/~1.6 M alleles)                 | Supporting (1)                |
| PP4       | Ultra-hypermutated MSS tumour, somatic EDM/dMMR excluded         | Supporting (1)                |
| PP3       | SpliceAI Δ = [value] (threshold ≥0.2)                            | [Supporting (1) / none]       |
| [PS2]     | [Parental testing pending]                                       | [Strong (4), if confirmed]    |
| [PS3/BS3] | [Calibrated fidelity assay, OddsPath = …]                        | [per Brnich 2020]             |

**Points tally:** [sum] -> arithmetic class [VUS 0–5 / LP 6–9 / P ≥10]; reported class: VUS unless PS3 ≥ Moderate or a curated entity exists

**Unresolved:**
- NMD fate and reinitiation product (ΔN65-POLE via Met66) not yet tested
- Somatic POLE/POLD1 EDM status in each tumour: [confirmed negative / pending]
- MMR status: [IHC / MSI result]

**Recommended:** Lymphocyte RNA allele ratio ± CHX; C-terminal-antibody POLE
western; tumour WES/WGS with signature decomposition; parental testing;
patient-derived organoid replication-fidelity assay with EDM controls.
```
