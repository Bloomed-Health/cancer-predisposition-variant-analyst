---
title: Mechanistic Framework
impact: CRITICAL
impactDescription: Generating the right mechanistic hypotheses determines which experiments are run and which therapeutic targets are nominated
tags: mechanistic-hypothesis,POLE,PPAP,reinitiation,NMD,essential-gene,mutational-signature,replication-fidelity,paradox-resolution
---

# Mechanistic Framework

A structured method for resolving genotype-phenotype paradoxes in ultra-rare
variants. The working example is the **POLE exon-2 frameshift
NM_006231.4:c.158_159del p.(Leu53Glnfs\*5)**: a premature termination codon at
codon 57 of 2,286 that, on paper, eliminates every functional domain yet is
reported with an ultra-hypermutated PPAP-like phenotype.

The framework generalizes to any multi-domain disease gene where a truncation
outside the canonical disease-causing region co-occurs with the canonical
phenotype.

**Entry condition:** Step 0 of [variant-interpretation.md](variant-interpretation.md#step-0-genotype-verification-and-differential-diagnosis)
is complete and negative (germline status confirmed, no somatic EDM hotspot, no
MMR deficiency, no second POLE variant). If Step 0 was skipped, stop and do it:
most "paradoxes" dissolve there.

---

## Pre-checks: Essential-Gene Filter and Signature Fork

Run both before enumerating mechanisms. They prune the hypothesis space more
cheaply than any experiment.

### Essential-gene filter

Ask: is the gene cell-essential? Check DepMap common-essential status [M10].

- **Essential (POLE: yes).** A tumour cell cannot survive with zero protein.
  Therefore any two-hit model (germline allele + somatic loss of the wild-type
  allele) is viable **only if the germline allele is hypomorphic** -- it must
  still produce a protein that replicates DNA. A true null allele plus LOH of
  the wild-type allele is a dead cell, not a hypermutated tumour.
- The POLD1 L474P precedent [M1] (heterozygous normal cells: only a subtle
  increase in mutation burden; tumours with somatic inactivation of the WT
  allele: >100 mut/Mb, SBS10d) works precisely because L474P is a proofreading-dead but
  replication-competent hypomorph. It is not a precedent for a null allele.
- Consequence for p.(Leu53Glnfs\*5): "haploinsufficiency + LOH" is inviable
  **unless** the allele produces a protein (see H1). Rank accordingly.

### Signature fork

Decompose tumour SBS signatures (WGS preferred; WES acceptable with ≥80 SNVs).

| Tumour shows                               | Inference                                                                                                                                                                       | Next                              |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| SBS10a/SBS10b ± SBS28 [SIG1, SIG2, SIG4]   | A proofreading-deficient **Pol ε is replicating DNA in this tumour**. A PTC-57 allele cannot supply it. Find the allele that does: somatic EDM on the WT allele (Step 0), a reinitiation product (H1), a second cis variant (Step 0). | H1 pipeline if Step 0 negative    |
| SBS10c/SBS10d [SIG3, M9]                   | Pol δ proofreading deficiency. POLE allele is a bystander.                                                                                                                      | POLD1 germline + somatic workup   |
| SBS14 or SBS20 [SIG6, SIG5]                | Polymerase proofreading + MMR deficiency. Look for CMMRD / Lynch with secondary polymerase hit [M11].                                                                             | MMR IHC, germline MMR genes       |
| SBS6/15/26/44 without SBS10                | MMR deficiency alone.                                                                                                                                                           | Lynch / CMMRD workup              |
| SBS18/SBS36                                | 8-oxoG pathway (MUTYH).                                                                                                                                                         | MUTYH germline                    |
| CpG>T excess (SBS1-like) with polyposis    | Consider MBD4 [P7].                                                                                                                                                             | MBD4 germline                     |
| None of the above; TMB elevated            | Hypermutation is not POLE-driven; the germline LoF allele is incidental.                                                                                                        | Exit framework; classify as VUS   |

The fork is also the basis for the gene-specific ACMG codes in [C1] (PP4_Strong
when ≥2 tumours carry SBS10a/b/28/14 at ≥5%; BP5 when ≥2 tumours with >1 mut/Mb
lack them) -- see variant-interpretation.md Step 4 for how those codes apply to a
non-exonuclease-domain allele.

---

## The Paradox Resolution Protocol

```
Step 0 negative + pre-checks done
    ↓
1. Confirm the phenotype is real and specific (not an incidental finding)
    ↓
2. Enumerate all mechanisms that could produce the phenotype (H0–H5 below)
    ↓
3. For each: does it predict the observed signature? Is it viable in an
   essential gene? Does the retained sequence support it?
    ↓
4. Rank by prior probability × consistency with data in hand
    ↓
5. Identify the minimum experiment set that collapses the space
```

---

## Hypotheses (POLE p.(Leu53Glnfs\*5) as worked example)

### H0: Coincidence / phenocopy (null hypothesis)

**Hypothesis:** The germline frameshift is an incidental finding. The tumour's
hypermutation has a different driver -- a somatic POLE exonuclease-domain
mutation on the wild-type allele, a somatic POLD1 EDM, or MMR deficiency.

**Why it is the prior-favoured explanation:**

- Heterozygous POLE LoF carriers: ~0.2% of controls (0.20% vs 0.22% in cancer
  cases; no enrichment) [P6]. That is ~1 in 500 people.
- Somatic POLE EDM hotspots (P286R, V411L, S459F, A456P, F367S, L424V, M444K,
  P436R): ~1–2% of CRC, ~7–10% of endometrial cancer.
- Expected co-occurrence: 1/500 × 1–2% ≈ 2–4 per 100,000 CRC. With >1 million
  CRC diagnoses per year worldwide, tens of such coincidences occur annually.
  A single such case is not evidence for a new mechanism.
- CMMRD with a secondary somatic POLE/POLD1 EDM hit produces the highest TMBs
  recorded (>250 mut/Mb) and presents with polyposis [M11].

**Discriminators:** Tumour sequencing of the full POLE/POLD1 exonuclease domains;
MMR IHC + MSI; signature decomposition (fork above). All are part of Step 0.

**If positive:** stop. Classify the germline variant as VUS for PPAP (or
B/LB if ClinVar/PolED evidence supports); therapy follows the somatic mechanism.

---

### H1: Translation reinitiation → ΔN-POLE (leading true-paradox mechanism)

**Hypothesis:** The frameshift transcript escapes NMD (partially or fully) and
ribosomes initiate at a downstream in-frame AUG -- by reinitiation after the
56-codon ORF, or by leaky scanning past AUG1 -- producing an N-terminally
truncated but otherwise full-length POLE that retains the exonuclease domain
(aa 268–471), the polymerase domain, the PCNA interface, and the C-terminal
CMG-binding half, but lacks the first ~65 residues of the N-terminal domain.

**Sequence basis (computed on ENST00000320574 CDS):**

| In-frame Met | Codons past PTC-57 | Kozak (−3 / +4)   | Context  |
| ------------ | ------------------ | ----------------- | -------- |
| **Met66**    | 9                  | ATTAAC**ATG**C    | adequate |
| Met221       | 164                | GTGGAC**ATG**C    | adequate |
| Met294/295   | 237                | CAGATT**ATG**A    | adequate |
| Met299       | 242                | TCCTAC**ATG**A    | weak     |
| **Met359**   | 302                | ACCATC**ATG**G    | strong   |

Two routes lead to Met66. (i) Reinitiation after termination at codon 57: most
efficient after short uORFs; a 56-codon ORF is at the long end of what still
permits measurable reinitiation, so efficiency is uncertain. (ii) Leaky
scanning: the annotated 5′ UTR of ENST00000320574 is only 27 nt and AUG1 sits
in a weak Kozak context (GGCTCC**ATG**T: −3 = C, +4 = T), both of which favour
scanning past AUG1 to the next adequate AUG -- Met66 -- on the mutant *and* the
wild-type transcript. If ΔN65-POLE is made physiologically from the WT allele,
its existence is not pathogenic per se; H1 then requires that the mutant allele
shifts the balance so that ΔN65-POLE replicates a meaningful fraction of the
genome. Measure both transcripts' products, not just the mutant's.

**What aa 1–65 actually contain, and why removing them might (or might not)
impair fidelity:**

- The PCNA interface is **not** here. In the human Pol ε–PCNA structure the
  three contacts are the PIP-motif at aa 1180–1187, the P-domain (His684,
  Arg685, Gln689, Tyr726, Lys729) and the thumb (Glu1085, Ser1117) [M3]. All are
  retained in ΔN65-POLE. Earlier drafts of this skill placed the PIP contact at
  the N-terminus; that was wrong.
- aa 1–30 are disordered (aa 1–23 invisible in cryo-EM) [M3, S5]; aa 25–47
  form the first helix and aa 57–65 the first β-strand of the N-terminal
  domain (NTD), which in B-family polymerases packs against the exonuclease
  domain. Removing the first strand could destabilise the NTD fold -- yielding
  either a degraded product (no phenotype) or a partially folded enzyme with
  altered exo/pol coordination (a fidelity defect). Which of these occurs is
  unknown; inspect residues 25–65 in PDB 9B8S [S1] / AlphaFold [S6] for
  contacts with the exo domain before investing in wet-lab work.
- Proofreading requires the primer to switch between the pol and exo sites
  within the holoenzyme [M4, M5]; any perturbation of NTD–exo packing is a
  candidate route to "replicates but proofreads poorly", the functional class
  of classical EDM alleles.
- This is the **only listed mechanism by which the mutant allele itself could
  generate SBS10a/b**. It is also the one whose error-prone step is least
  supported: NMD escape and a ΔN product are plausible; a fidelity defect from
  losing aa 1–65 is a hypothesis with no structural or functional data yet.

**Precedent:** BRCA1 c.68_69del (185delAG) places a PTC in exon 3; translation
reinitiates at Met297 and yields a RING-less BRCA1 that is stable, partially
functional, and clinically consequential (PARP-inhibitor/platinum resistance)
[M8]. See [examples/brca1-c68_69del.md](examples/brca1-c68_69del.md).

**Discriminating experiments:**

1. Allele-specific RT-qPCR / RNA-seq on patient normal tissue or LCLs ± CHX
   (or NMDI-14): mutant/WT transcript ratio. Full NMD (<10% mutant) weakens H1
   but does not exclude it -- reinitiation itself protects transcripts from NMD.
2. Western blot with a **C-terminal** anti-POLE antibody on patient cells: look
   for a band ~7 kDa smaller than full-length (ΔN65 ≈ 254 kDa vs 261 kDa).
   Resolution is marginal; confirm by targeted mass spectrometry showing loss
   of N-terminal tryptic peptides (aa 1–65) in a fraction of POLE.
3. Reporter: express ΔN65-POLE cDNA in POLE-exo-reporter or POLE-conditional
   cells; measure mutation rate (HPRT or fluctuation assay) and PCNA
   co-immunoprecipitation versus WT and versus P286R.
4. Patient-derived organoids: mutation accumulation over passages with
   signature decomposition. Grade all functional results per [C9].

**Weaknesses:** No published demonstration of POLE reinitiation. Reinitiation
efficiency in vivo is typically low (single-digit percent of WT output); whether
that is enough to perturb fidelity is unknown. If the ΔN protein is fully
proofreading-proficient, H1 is excluded.

---

### H2: Hypomorphic allele + somatic loss of the wild-type allele

**Hypothesis:** The two-hit model of [M1], applied correctly. Viable **only if
H1 (or H3) supplies a replication-competent product from the mutant allele**.
Then somatic LOH at 12q24.33, or a second somatic POLE hit, leaves the tumour
with ΔN-POLE as its sole Pol ε, and hypermutation follows.

**Status:** Conditional on H1. Not an independent mechanism for a null allele
(see essential-gene filter).

**Discriminators:** Tumour LOH at 12q24.33 (SNP array / WGS allelic imbalance);
tumour RNA allele ratio. LOH **without** evidence of a mutant-allele protein
product is uninterpretable: either the LOH removed the mutant allele (WT tumour,
no paradox) or the tumour is impossibly POLE-null (re-check the call).

---

### H3: Alternative splicing or alternative transcript bypassing the PTC

**Hypothesis:** The PTC is skipped at the RNA level -- in-frame exon skipping,
an alternative promoter, or a transcript whose start codon lies downstream.

**Sequence check (ENST00000320574):** Exon 1 contributes 62 coding nt; exon 2 is
142 nt (c.63–c.204). 142 mod 3 = 1, so skipping exon 2 shifts the frame; exon
2+3 (223 nt) and 2+3+4 (268 nt) likewise. **No in-frame exon-skip rescue
exists.** Ensembl's only other protein-coding POLE transcript (POLE-207,
ENST00000535270, 2,259 aa) shares exon 2 and merely skips the in-frame 81-nt
exon 3, so it carries the same PTC; the remaining transcripts are
NMD/retained-intron biotypes. No annotated transcript bypasses exon 2.

**Status:** Low. Retained only because RNA-seq is cheap and junction evidence
would be decisive.

**Discriminator:** RNA-seq junction counts across exons 1–4; 5′ RACE if an
alternative TSS is suspected.

---

### H4: Pol δ compensation on the leading strand (additive at most)

**Hypothesis:** Reduced Pol ε output (via any viable mechanism above) shifts
leading-strand synthesis toward Pol δ, adding Pol δ-type errors.

**Signature expectation (corrected):** Pol δ proofreading errors produce
SBS10c/SBS10d with lagging-strand bias [SIG3, M9]. SBS28 is **not** a Pol δ
signature; it co-occurs with SBS10a/b in POLE-exo-deficient tumours [SIG4].
Human cells expressing only the POLE C-terminal half replicate slowly using Pol
δ [M2], but with proofreading-proficient Pol δ this does not generate SBS10c/d
at scale.

**Status:** Additive at most; only meaningful after H1/H2 are established.

---

### H5: Dominant-negative N-terminal fragment -- not supported

The native-sequence portion of the predicted peptide is 52 aa (plus 4 aberrant
residues before the stop). Earlier versions of this skill proposed that it
competes for CMG binding. That premise is wrong: the CMG/GINS interface of POLE
is in the **C-terminal** non-catalytic half (zinc-finger region → POLE2 →
Psf1/MCM5; thumb of the inactive polymerase domain → MCM2/Cdc45) [M2, M7].
Nothing in aa 1–65 contacts CMG, and nothing in aa 1–65 contacts PCNA either
(the three PCNA contacts lie at aa 684–1187 [M3]). The fragment comprises a
disordered tail, one helix and one β-strand of the NTD, with no known binding
partner. A 6-kDa peptide from a transcript that is also NMD-targeted has no
mechanism by which to poison replication, let alone to generate the
POLE-specific SBS10 signature. Discard unless proteomics unexpectedly detects
the peptide at high abundance with an identified interactor.

---

## Hypothesis Ranking Table

| Rank | Hypothesis                                   | Prior             | Produces SBS10a/b from the mutant allele? | Key discriminator                                   | Change from v1.2                                          |
| ---- | -------------------------------------------- | ----------------- | ----------------------------------------- | --------------------------------------------------- | --------------------------------------------------------- |
| 0    | H0 Coincidence / phenocopy                   | **HIGHEST**       | No (another driver does)                  | Tumour EDM hotspots, MMR IHC, signatures            | New; was absent                                           |
| 1    | H1 Reinitiation / leaky scanning → ΔN65-POLE | MEDIUM            | **Yes** (only if loss of aa 1–65 impairs fidelity -- untested) | RNA allele ratio; C-term western/MS; ΔN65 reporter | New; replaces "53-aa neomorphic peptide"             |
| 2    | H3 Alternative splicing / transcript         | LOW               | Only if an in-frame product exists (none found) | RNA-seq junctions                               | New                                                       |
| 3    | H2 Hypomorph + LOH of WT                     | Conditional on H1 | Yes, via H1 product                       | LOH at 12q24.33 **plus** mutant protein evidence    | Was rank 1 as "haploinsufficiency + LOH"; inviable for a null |
| 4    | H4 Pol δ compensation                        | Additive          | No (SBS10c/d)                             | SBS10c/d fraction                                   | Signature attribution corrected (SBS28 ≠ Pol δ)           |
| 5    | H5 Dominant-negative N-terminal fragment     | Not supported     | No                                        | Proteomics (negative expected)                      | Was rank 4 "CMG disruption"; premise false                |
| --   | PCNA/RFC trans-regulatory effect             | Removed           | --                                        | --                                                  | Folded into H5; no structural basis                       |

**What changed and why:** v1.2 ranked "haploinsufficiency + somatic LOH" first by
analogy to POLD1 L474P. That analogy fails for a null allele in an essential
gene [M10]. v1.2 also placed a CMG-binding surface in aa 1–50; the CMG interface
is C-terminal [M2, M7]. The structural data [M3–M5] do not sharpen the paradox;
they bound it: the PCNA interface (aa 684–1187) and the replisome interface
(C-terminal half) are both outside aa 1–65, so the only way this allele can
matter mechanistically is through a ΔN product whose N-terminal-domain fold is
perturbed -- a testable, currently unsupported hypothesis -- or not at all (H0).

---

## Minimum Discriminating Experiment Set

Ordered by information per unit cost. Steps 1–2 use existing tumour tissue;
3–4 need patient-derived cells; 5 is a functional study.

1. **Tumour WGS (or WES + SNP array) with germline comparison.** One assay
   answers four questions: somatic POLE/POLD1 EDM hotspot (H0); signature
   decomposition (fork); LOH / allelic imbalance at 12q24.33 (H2); somatic or
   germline MMR gene status (H0). Require ≥80 SNVs for signature calls; WGS
   preferred.
2. **MMR IHC (MLH1/MSH2/MSH6/PMS2) and MSI.** Cheap, routine, excludes the
   most common hypermutator phenocopy.
3. **RNA-seq of tumour and normal tissue (or LCLs ± CHX).** Mutant/WT allele
   ratio (NMD fate), exon 1–4 junction usage (H3), tumour allelic expression
   (H2).
4. **Western blot with a C-terminal POLE antibody ± targeted MS** on patient
   fibroblasts/LCLs. Direct test of H1. Proceed regardless of step 3 result,
   since reinitiation can stabilise the transcript.
5. **Functional assay of ΔN65-POLE** (reporter mutation rate, PCNA co-IP,
   organoid mutation accumulation). Required before any PS3 claim; grade per
   [C9] with validated controls (WT, P286R, exo-dead D275A/E277A).

> **Decision tree.** Step 1 shows a somatic EDM hotspot or step 2 shows MMR loss
> → H0; stop; classify VUS; therapy follows the somatic mechanism. Step 1 shows
> no SBS10a/b → H0 (non-POLE driver); stop. Step 1 shows SBS10a/b with no
> somatic EDM and no second germline variant → proceed to steps 3–5 (H1/H3).
> LOH at 12q24.33 is interpretable only after step 4.

---

## Generalizable Paradox Template

For any gene X where a truncation outside canonical domain Y co-occurs with the
canonical Y-loss phenotype:

```
0. Coincidence prior: carrier frequency of this allele class × rate of
   somatic/phenocopy explanations for the phenotype. If the product is not
   negligible at population scale, H0 is the default.
1. Genotype verification: germline vs mosaic, full-gene coverage, phasing,
   tumour sequencing for somatic drivers (variant-interpretation.md Step 0).
2. Essential-gene check (DepMap [M10]): if essential, two-hit models need a
   hypomorph; a null + LOH is inviable.
3. Reinitiation scan: in-frame AUGs downstream of the PTC, Kozak context,
   distance from PTC; predicted ΔN product and which domains/motifs it loses
   (scripts/hgvs_validate.py does this). Precedent: BRCA1 185delAG [M8].
4. Isoform / exon-skip check: exon length mod 3; alternative transcripts and
   promoters (Ensembl).
5. NMD probability (rule-based + NMDetective [M12, TOOL6]).
6. Map retained sequence to interaction surfaces (UniProt [S5], PDB, AlphaFold
   [S6], STRING/BioGRID). Verify the interface location against primary
   structural papers, not reviews.
7. Biomarker fork: if the phenotype has a molecular readout (mutational
   signature, metabolite, IHC), ask which allele/protein could produce it.
8. Rank: coincidence vs reinitiation/ΔN product vs isoform bypass vs
   hypomorph+LOH vs dominant-negative via a verified retained surface.
```
