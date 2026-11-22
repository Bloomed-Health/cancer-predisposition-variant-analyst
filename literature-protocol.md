---
title: Literature Protocol
impact: HIGH
impactDescription: Systematic literature synthesis prevents reinventing existing evidence and identifies true knowledge gaps
tags: literature-search,PubMed,ClinVar,gnomAD,evidence-grading,PPAP,POLE,systematic-review,gap-analysis
---

# Literature Protocol

Structured search and evidence synthesis for ultra-rare variant research.
The goal is not comprehensive review -- it is identifying the minimum evidence
that changes classification or mechanism rank, and precisely locating the
knowledge gap this case fills (or showing there is none).

---

## Search Architecture

Run searches in layers. Each layer narrows scope and builds on the previous.
Log every query (template at the end).

### Layer 1: Disease + Gene anchor

Establish the existing clinical and molecular literature for the gene-disease pair.

**PubMed queries** (PubMed has no `[Gene]` field; use `[tiab]` and MeSH):

```
(POLE[tiab] OR "DNA Polymerase II"[MeSH]) AND (polyposis[tiab] OR "colorectal cancer"[tiab] OR PPAP[tiab] OR hypermutation[tiab])
"polymerase proofreading-associated polyposis"[tiab]
POLE[tiab] AND "exonuclease domain"[tiab] AND (cancer[tiab] OR tumor[tiab] OR tumour[tiab])
POLE[tiab] AND (truncating[tiab] OR truncation[tiab] OR frameshift[tiab] OR nonsense[tiab]) AND (pathogenic[tiab] OR cancer[tiab] OR phenotype[tiab])
"replication fidelity"[tiab] AND ("DNA polymerase epsilon"[tiab] OR POLE[tiab]) AND (mutation[tiab] OR variant[tiab])
```

**ClinVar structured query** (or `python3 scripts/clinvar_lookup.py --gene POLE` -- default type is truncating = frameshift + nonsense):

```
Gene: POLE
Variant type: frameshift, nonsense, splice (missense is a separate search)
Clinical significance: all. The distribution itself is evidence, but read it
  carefully: as of 2026-11-22, 678 POLE frameshift/nonsense records = 301
  Pathogenic, 216 Conflicting, 145 VUS, 14 LP or P/LP, 0 B/LB. The
  "Pathogenic" calls are almost all single-submitter commercial-lab SCVs with
  condition "not provided" (recessive FILS/IMAGe-I carrier logic or blanket
  PVS1); under hereditary-cancer / polyposis conditions there is no concordant
  P/LP truncating POLE variant. A lab report saying "Pathogenic" for a POLE
  truncation does NOT assert PPAP risk -- check the asserted condition.
Review status: prefer multi-submitter / expert panel; InSiGHT VCEP POLE/POLD1
  rules are still pending as of 2026-11-22 [C4]
```

**Key papers to retrieve** (see [references.md](references.md)):

- Foundational: F1-F8 (PPAP discovery, clinical spectrum, FILS, IMAGe-I)
- Classification: C1 (gene-specific ACMG/AMP), C2 (PolED), C3 (MAVISp), C6-C13
  (ACMG/AMP, SVI PVS1, points, PS3/BS3, PP3 calibration, gene-disease validity)
- Mechanism: M1 (POLD1 hypomorph + LOH), M2 (CMG interface is C-terminal),
  M3-M5 (holoenzyme structures), M8 (reinitiation precedent), M9 (SBS10c/d),
  M10 (POLE essential), M11 (CMMRD + secondary polymerase hits), M12 (NMD rules)
- Clinical: P1-P4, P6 (LoF population data), P7-P8 (MBD4, NTHL1 phenocopies)
- Therapeutic: T1-T2 (toripalimab, LOP), R3-R4 (CTNA), T9 (LATIFY negative)
- Neoantigen: N1-N2

---

### Layer 2: Variant-level and mechanism-level searches

**Variant-specific:**

```
POLE[tiab] AND ("c.158_159del"[tiab] OR "Leu53Glnfs"[tiab] OR "L53Qfs"[tiab])
POLE[tiab] AND "exon 2"[tiab] AND (frameshift[tiab] OR truncat*[tiab])
```

**Mechanistic equivalents:**

```
("translation reinitiation"[tiab] OR "translational reinitiation"[tiab] OR "downstream initiation"[tiab]) AND (frameshift[tiab] OR "premature termination"[tiab] OR "nonsense-mediated"[tiab])
("translation reinitiation"[tiab] OR "RING-less"[tiab]) AND BRCA1[tiab]
(POLE[tiab] OR "DNA polymerase epsilon"[tiab]) AND ("N-terminal"[tiab] OR "PIP"[tiab] OR PCNA[tiab]) AND (structure[tiab] OR "cryo-EM"[tiab])
POLE[tiab] AND ("loss of heterozygosity"[tiab] OR LOH[tiab]) AND (tumor[tiab] OR tumour[tiab])
POLD1[tiab] AND (recessive[tiab] OR "loss of heterozygosity"[tiab]) AND hypermutation[tiab]
POLE[tiab] AND (FILS[tiab] OR IMAGe[tiab] OR biallelic[tiab]) AND (syndrome[tiab] OR congenital[tiab])
("constitutional mismatch repair deficiency"[tiab] OR CMMRD[tiab]) AND (POLE[tiab] OR POLD1[tiab]) AND (hypermutat*[tiab] OR "ultra-hypermutat*"[tiab])
POLE[tiab] AND germline[tiab] AND somatic[tiab] AND ("exonuclease domain"[tiab] OR P286R[tiab] OR V411L[tiab])
("DNA polymerase epsilon"[tiab] OR POLE1[tiab]) AND "non-catalytic"[tiab] AND ("replication initiation"[tiab] OR CMG[tiab])
```

**Structural databases** (accessions in references.md S1-S7):

- PDB: Pol ε-PCNA holoenzyme and replisome structures (S1-S4). Verify the
  interface location in the primary paper; do not rely on review summaries.
- AlphaFold DB: S6 (POLE; fold confidence of aa 1-100 and of the ΔN65 start).
- UniProt: S5 (Q07864, POLE), S7 (P38398, BRCA1).
- DepMap: M10 (gene essentiality).

---

### Layer 3: Phenotype-first searches

Identify other patients with similar phenotype who may have equivalent variants
unreported in the literature.

**Clinical databases** (references.md D1-D10):

```
DECIPHER [D4]: POLE truncating variants with polyposis / hypermutation terms
Matchmaker Exchange [D7]: POLE truncation + polyposis + (tumour SBS10 if available)
ClinVar [D2]: POLE truncating submissions whose condition is PPAP / CRC; read submitter comments
OMIM [O1]: 615083 (PPAP) allelic variants and cited evidence
PolED [C2]: any functional data on N-terminal or truncating POLE alleles
```

**Cohort studies** (D8-D10):

- TCGA / cBioPortal [D8]: POLE-hypermutated tumours -- check germline LoF
  co-occurrence with somatic EDM (direct evidence for H0 coincidence rates).
- UK Biobank [D9]: exome PheWAS of POLE LoF carriers (expected null).
- Genomics England 100K [D10]: colorectal panel; germline + tumour pairs.

---

### Negative-result sources (read before claiming novelty)

- PolED [C2]: "Loss-of-function variants (deletions, insertions, premature stop
  codons) prevent production of the enzyme and cannot cause ultramutated
  cancers."
- Mur et al. 2020 [P6]: POLE LoF 0.22% in cancer cases vs 0.20% controls.
- ClinVar [D2]: distribution of POLE truncating classifications for PPAP
  (`scripts/clinvar_lookup.py --gene POLE --type truncating`).
- Castillejo 2023 [C1]: scope limited to exonuclease-domain variants; no LoF
  criteria defined because LoF is not the mechanism.

---

## Evidence Grading

Assign a tier before including evidence in the table. Tiers map onto ACMG code
strength and Bayesian points [C8] as shown.

| Tier | Type                           | Examples                                                                                                     | Max ACMG strength / points                      |
| ---- | ------------------------------ | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------- |
| 1    | Functional (validated assay)   | Replication-fidelity reporter with WT/P286R/exo-dead controls; organoid mutation accumulation; yeast complementation. Grade per [C9]: OddsPath ≥18.7 Strong (4), ≥4.3 Moderate (2), ≥2.1 Supporting (1) | PS3 up to Strong (4) |
| 2    | Clinical case (direct)         | Published patient with the same variant, same phenotype, phenocopies excluded                                | PS4/PP4 per gene-specific rules                  |
| 3    | Clinical case (analogous)      | Different variant, same functional class (e.g. another exon-2 PTC), same phenotype                           | Supporting (1)                                   |
| 4    | Computational (calibrated)     | SpliceAI ≥0.2 [C11]; for missense only: REVEL ≥0.644 supp / ≥0.773 mod / ≥0.932 strong, CADD ≥25.3 supp / ≥28.1 mod [C10] | PP3 Supporting-Moderate (1-2)         |
| 5    | Computational (uncalibrated)   | Conservation alone, PolyPhen-2/SIFT alone, AlphaFold confidence                                              | Not usable as an ACMG code                       |
| 6    | Population (negative)          | Absent from gnomAD (PM2_Supporting, 1 point [C12]); LOEUF/pLI (context only)                                 | Supporting (1)                                   |

Missense predictors (REVEL, AlphaMissense, CADD missense calibration) do not
apply to truncating variants. For a frameshift, the only computational code is
PP3 via SpliceAI if a splice effect is predicted.

---

## Literature Gap Analysis Template

Complete after all three layers. The gaps you identify are the scientific
contribution of your case report -- or the reason there is none.

```markdown
## Literature Gap Analysis: POLE p.[variant]

### What is established

- PPAP is caused by POLE/POLD1 exonuclease-domain missense producing a
  replication-competent, proofreading-deficient polymerase [F1, C1]
- SBS10a/SBS10b (± SBS28) are diagnostic of Pol ε proofreading deficiency;
  SBS10c/SBS10d of Pol δ [SIG1-SIG4, M9]
- POLE truncation/LoF does not cause PPAP [C1, C2]; heterozygous LoF carriers
  ~0.2% of the population with no cancer enrichment [P6]
- Biallelic hypomorphic POLE alleles cause FILS/IMAGe-I, not cancer; complete
  biallelic null is not observed, consistent with essentiality [F6, F7, O2, O3, M10]
- POLE is cell-essential; a tumour cannot be POLE-null [M10]
- POLD1 proofreading deficiency is recessive at cellular level; hypermutation
  requires loss of the WT allele in a hypomorph background [M1]
- The CMG interface of POLE is C-terminal; the catalytic domain is dispensable
  for CMG assembly [M2, M7]
- Pol ε engages PCNA via a three-point interface in the N-terminal catalytic
  region; proofreading requires holoenzyme switching [M3-M5]
- Early-exon PTCs can escape NMD via reinitiation (BRCA1 185delAG → Met297) [M8]
- CMMRD and other MMR-deficient tumours acquire secondary POLE/POLD1 EDM hits
  with extreme TMB [M11]
- Only 7.5% (148/1,965) of POLE-mutant tumours are LOP; non-LOP MSS ≈ WT for ICI [T2]

### What is contested

- Whether the POLD1 LOH requirement applies equally to POLE EDM alleles [M1]
- Contribution of non-EDM POLE/POLD1 mutations to TMB [T7]
- Whether "PPAP" should name any truncation-associated entity (no gene-disease
  validity curation exists for such an entity [C13])
- ClinGen InSiGHT VCEP POLE/POLD1 rules pending [C4]

### What is unknown (true gaps)

- Whether POLE exon-2 PTC transcripts reinitiate at Met66 (or Met359) in human
  cells: NO DATA
- Whether a ΔN-POLE lacking aa 1-65 is proofreading-competent: NO DATA
- Rate of germline POLE LoF × somatic EDM coincidence in CRC cohorts: not
  reported, but estimable from cBioPortal germline-tumour pairs [D8]
- NMD efficiency of POLE early-exon PTCs in colon epithelium: UNKNOWN

### Significance of this case (choose one)

A. Step 0 positive (somatic EDM / MMR driver found): this is an incidental
   germline POLE LoF in a somatically driven hypermutator. Contribution: a
   documented coincidence case supporting BP5-type evidence for the allele.
B. Step 0 negative, SBS10a/b present, mutant-allele protein demonstrated:
   first evidence of a reinitiation-derived POLE product with impaired
   proofreading. Contribution: new mechanism class; requires functional data
   (Tier 1) before any classification change.
C. Step 0 negative, mechanism unresolved: report as VUS with the experiment
   plan; contribution is the phenotype-genotype observation and the
   matchmaking call, not a mechanism.
```

---

## Preprint and Grey Literature

For ultra-rare variants, the defining evidence is often in preprints or
conference abstracts before journal publication.

- **bioRxiv / medRxiv**: gene + "truncation" / "frameshift" / "reinitiation"
- **ASHG / ESHG / AACR abstracts**: rare variant cases first appear here
- **ClinVar submitter comments**: sometimes unpublished functional data
- **LOVD curator notes** [D3]
- **Matchmaker Exchange** [D7]: submit the patient; matches arrive over months

---

## Search Log Template

Keep a dated search log. Required for case reports, classification
submissions, and grant applications.

```
Date: YYYY-MM-DD
Database: PubMed
Tool/API: web UI | E-utilities | scripts/clinvar_lookup.py | scripts/gnomad_lookup.py
Query: POLE[tiab] AND (truncat*[tiab] OR frameshift[tiab]) AND (PPAP[tiab] OR polyposis[tiab])
Filters: none
Results: N
Relevant: M
Notes: [key papers identified; PMIDs]

Date: YYYY-MM-DD
Database: ClinVar
Tool/API: scripts/clinvar_lookup.py --gene POLE --type truncating
Query: Gene=POLE, Type=frameshift/nonsense
Results: N (B/LB: a, VUS: b, LP/P: c, conflicting: d)
Relevant: M
Notes: [any analogous exon-2 submissions; conditions cited]

Date: YYYY-MM-DD
Database: gnomAD v4.1
Tool/API: scripts/gnomad_lookup.py --variant 12-132681182-TCA-T
Results: AC/AN (exomes, genomes), non-cancer subset
Notes: [PM2_Supporting applies if ≤1/200,000 alleles per [C1]]
```
