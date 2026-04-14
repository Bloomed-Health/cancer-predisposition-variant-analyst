---
title: Literature Protocol
impact: HIGH
impactDescription: Systematic literature synthesis prevents reinventing existing evidence and identifies true knowledge gaps
tags: literature-search,PubMed,ClinVar,gnomAD,evidence-grading,PPAP,POLE,systematic-review,gap-analysis
---

# Literature Protocol

Structured search and evidence synthesis for ultra-rare variant research.
The goal is not comprehensive review — it is identifying the minimum evidence
that changes classification or mechanism rank, and precisely locating the
knowledge gap this case fills.

---

## Search Architecture

Run searches in layers. Each layer narrows scope and builds on the previous.

### Layer 1: Disease + Gene anchor

Establish the existing clinical and molecular literature for the gene-disease pair.

**PubMed queries (run all, deduplicate):**

```
POLE[Gene] AND (polyposis OR colorectal cancer OR PPAP OR hypermutation)
"Polymerase Proofreading-Associated Polyposis"
"POLE" AND "exonuclease domain" AND (cancer OR tumor)
"POLE" AND "truncation" AND (pathogenic OR cancer OR phenotype)
"replication fidelity" AND "DNA polymerase epsilon" AND (mutation OR variant)
```

**ClinVar structured query:**

```
Gene: POLE
Clinical significance: Pathogenic, Likely Pathogenic, VUS
Variant type: frameshift, nonsense, deletion (not missense — separate search)
Review status: expert panel preferred (ClinGen PPAP VCEP if active)
```

**Key papers to retrieve** (see [references.md](references.md) for full
citations and URLs):

- Foundational: F1-F8 (Palles, Church, Bellido, Weren, Haradhvala, FILS, IMAGe-I)
- Classification: C1 (gene-specific ACMG/AMP), C2 (PolED), C3 (MAVISp)
- Mechanism: M1 (LOH recessive effect), M2 (CMG dispensability), M3-M5 (cryo-EM structures)
- Clinical: P1 (duodenal adenocarcinoma), P2 (somatic vs germline comparative), P6 (population data)
- Therapeutic: T1-T2 (toripalimab, LOP stratification), R3-R4 (CTNA sensitivity)
- Neoantigen: N1-N2 (clonality models, NeoPrecis)
- Also: TCGA/COSMIC POLE hypermutator studies (SIG1-SIG2), M6 (BIR-induced LOH)

---

### Layer 2: Variant-level searches

Search for evidence specific to this variant or mechanistically equivalent variants.

**Variant-specific:**

```
POLE c.[your_cDNA_change]
POLE p.[your_protein_change]
POLE exon [N] frameshift
```

**Mechanistic equivalents (LOH, dominant-negative, truncation precedent):**

```
"POLE" AND ("dominant negative" OR "truncation" OR "N-terminal")
"DNA polymerase epsilon" AND ("CMG complex" OR "GINS" OR "replisome")
"NMD escape" AND "cancer predisposition"
"frameshift" AND ("ultra-hypermutation" OR "TMB" AND "truncation")
"POLE" AND ("loss of heterozygosity" OR "LOH") AND (tumor OR cancer)
"POLD1" AND ("recessive" OR "LOH" OR "loss of heterozygosity") AND hypermutation
"POLE" AND ("FILS" OR "IMAGe" OR "biallelic") AND (syndrome OR congenital)
"DNA polymerase epsilon" AND "non-catalytic" AND "replication initiation"
```

**Structural databases** (see references.md S1-S6 for accessions):

- PDB: S1-S4 (CMG complexes, Pol-epsilon/PCNA holoenzyme, Ctf18-RFC)
- AlphaFold DB: S6 (POLE N-terminal fragment fold confidence)
- UniProt: S5 (P28340, domain annotations, PTMs, interaction partners)

---

### Layer 3: Phenotype-first searches

Identify other patients with similar phenotype who may have equivalent variants
unreported in the literature.

**Clinical databases** (see references.md D1-D10 for details):

```
DECIPHER [D4]: POLE variants with ultra-hypermutated phenotype
Matchmaker Exchange [D7]: submit query for POLE truncation + polyposis
ClinVar [D2]: review all POLE submissions with TMB/hypermutation in clinical context
OMIM [O1]: 615083 (PPAP) -- review all cited genetic evidence
```

**Cohort studies** (D8-D10):

- TCGA [D8]: POLE somatic hypermutator cases -- check for germline LoF co-occurrence
- UK Biobank [D9]: exome PheWAS for POLE LoF carriers
- Genomics England 100K [D10]: colorectal panel data
- International PPAP registry if accessible

---

## Evidence Grading

For each piece of evidence retrieved, assign a tier before including in the
evidence table.

| Tier | Type                           | Examples                                                                                        |
| ---- | ------------------------------ | ----------------------------------------------------------------------------------------------- |
| 1    | Functional (experimental)      | Cell viability assay, replication fidelity assay, yeast complementation, organoid mutation rate |
| 2    | Clinical case (direct)         | Published patient with same variant + same phenotype                                            |
| 3    | Clinical case (analogous)      | Published patient with different variant in same domain + same phenotype                        |
| 4    | Computational (validated tool) | SpliceAI ≥0.5, CADD ≥25, REVEL ≥0.75 with known calibration                                     |
| 5    | Computational (unvalidated)    | Conservation scores, PolyPhen-2, SIFT alone                                                     |
| 6    | Population (negative)          | Absent from gnomAD, constraint data (LOEUF)                                                     |

ACMG strong/very strong codes require Tier 1–2 evidence. Tier 4–6 supports
only PP3 (supporting) criteria.

---

## Literature Gap Analysis Template

After completing all three search layers, complete this gap analysis. The gaps
you identify are the scientific contribution of your case report.

```markdown
## Literature Gap Analysis: POLE p.[variant]

### What is established

- PPAP caused by POLE EDM missense: well characterized [F1-F5]
- SBS10a/10b diagnostic for POLE hypermutator [SIG1-SIG2]
- POLE truncation/LoF does NOT cause PPAP [C1, C2]
- Population: POLE LoF not enriched in cancer (0.22% vs 0.20%) [P6]
- Biallelic POLE LoF causes FILS/IMAGe-I, not cancer [F6, F7, O2, O3]
- POLD1 proofreading is recessive -- LOH required for hypermutation [M1, M6]
- POLE1 catalytic domain dispensable for CMG assembly [M2]
- Three-point Pol-epsilon/PCNA interface required for holoenzyme [M3]
- Proofreading requires intact holoenzyme (6nt switching) [M4, M5]
- Only 7.5% of POLE mutations are LOP; non-LOP = no ICI benefit [T2]
- All P/LP EDM variants have AlphaMissense 0.87-1.0 [P2]
- [other established facts from Layer 1 search]

### What is contested

- Whether POLD1 LOH requirement applies equally to POLE [M1]
- Classification of non-EDM POLE variants: some contribute to TMB [T7]
- Whether "PPAP" should include truncation-associated hypermutation
- ClinGen InSiGHT VCEP: POLE/POLD1-specific rules pending [C4]

### What is unknown (true gaps)

- Whether POLE truncations at N-terminus can produce PPAP phenotype: NO PUBLISHED CASES
- Mechanism by which pre-domain truncations cause hypermutation: UNCHARACTERIZED
- Fate (NMD vs. escape) of POLE frameshift transcripts in patient tissue: UNKNOWN
- Whether truncated POLE N-terminal fragment interacts with CMG complex: UNKNOWN
- Prevalence of POLE truncation PPAP variants in population databases: NOT ASSESSABLE
  (gnomAD constraint under-represents dominant cancer predisposition variants)

### Significance of this case

This is the [first/second/Nth] reported patient with POLE truncation upstream of
the exonuclease domain producing ultra-hypermutated PPAP phenotype. The case:

1. Expands the PPAP molecular spectrum to include N-terminal truncations
2. Establishes mechanistic questions requiring resolution for classification
3. Has direct implications for [N] gnomAD carriers of analogous POLE truncations
   whose cancer risk is currently unclassified
```

---

## Preprint and Grey Literature

Do not skip these — for ultra-rare variants, the defining evidence is often in
preprints or conference abstracts before journal publication.

- **bioRxiv / medRxiv**: search gene + "truncation" or "frameshift"
- **ASHG / ESHG abstracts**: annual meetings are where rare variant cases first appear
- **ClinVar submitter comments**: sometimes contain unpublished functional data
- **LOVD curator notes**: gene-specific LOVDs often have curator annotations not
  in published literature
- **Personal communication via Matchmaker Exchange**: submit your patient;
  other teams with similar patients will match

---

## Search Log Template

Keep a dated search log. This is required for case reports, classification
submissions, and grant applications.

```
Date: YYYY-MM-DD
Database: PubMed
Query: POLE AND truncation AND (PPAP OR polyposis)
Filters: None
Results: N
Relevant: M
Notes: [key papers identified]

Date: YYYY-MM-DD
Database: ClinVar
Query: Gene=POLE, Type=frameshift, Significance=P/LP/VUS
Results: N
Relevant: M
Notes: [any analogous truncation submissions]
```
