---
title: References
impact: HIGH
impactDescription: Canonical bibliography for all evidence cited across skill files -- ensures traceability and supports case report drafting
tags: references,bibliography,POLE,POLD1,PPAP,literature,evidence
---

# References

Canonical bibliography for the cancer-predisposition-variant-analyst skill.
Organized by topic, with year, journal, and key contribution noted.

Verified: 2026-11-22

Every row carries a machine-checkable `ID` (`doi:`, `pmid:`, `pmcid:`, `omim:`,
`nct:`, `pdb:`, `uniprot:`, `url:`). Re-verify with
`python3 scripts/check_refs.py` (Crossref, NCBI E-utilities, ClinicalTrials.gov
v2, RCSB, UniProt REST). Titles were compared against the stated contribution on
the verification date; preprints that have since been published cite the
journal version.

---

## Foundational PPAP Literature

| Ref | Citation                                      | ID                             | URL                                                                | Key contribution                                                                                                                     |
| --- | --------------------------------------------- | ------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| F1  | Palles et al. 2013, _Nat Genet_               | `doi:10.1038/ng.2503`          | [doi](https://doi.org/10.1038/ng.2503)                             | Original PPAP discovery: germline POLE L424V and POLD1 S478N exonuclease-domain mutations predispose to adenomas and CRC              |
| F2  | Church et al. 2013, _Hum Mol Genet_           | `doi:10.1093/hmg/ddt131`       | [doi](https://doi.org/10.1093/hmg/ddt131)                          | Somatic POLE/POLD1 exonuclease-domain mutations in endometrial cancer define the ultramutated phenotype (same group as F1)           |
| F3  | Bellido et al. 2016, _Genet Med_              | `doi:10.1038/gim.2015.75`      | [doi](https://doi.org/10.1038/gim.2015.75)                         | 529 kindreds: PPAP clinical spectrum, review of reported cases, testing and surveillance recommendations                             |
| F4  | Spier et al. 2015, _Int J Cancer_             | `doi:10.1002/ijc.29396`        | [doi](https://doi.org/10.1002/ijc.29396)                           | Frequency and phenotypic spectrum of germline POLE (and seven other polymerase genes) variants in 266 adenoma/CRC patients           |
| F5  | Haradhvala et al. 2016, _Cell_                | `doi:10.1016/j.cell.2015.12.050` | [doi](https://doi.org/10.1016/j.cell.2015.12.050)                | Replicative strand asymmetry of POLE exonuclease-deficiency mutations (SBS10 context)                                                |
| F6  | Pachlopnik Schmid et al. 2012, _J Exp Med_    | `doi:10.1084/jem.20121303`     | [doi](https://doi.org/10.1084/jem.20121303)                        | FILS syndrome: homozygous hypomorphic POLE splice variant (intron 34) -- recessive, not LoF-null                                      |
| F7  | Logan et al. 2018, _Am J Hum Genet_           | `doi:10.1016/j.ajhg.2018.10.024` | [doi](https://doi.org/10.1016/j.ajhg.2018.10.024)                | IMAGe-I syndrome: biallelic hypomorphic POLE variants (deep-intronic + LoF in trans) with variable immunodeficiency                   |
| F8  | Roberts et al. 2022, _Am J Med Genet A_       | `doi:10.1002/ajmg.a.62908`     | [doi](https://doi.org/10.1002/ajmg.a.62908)                        | Phenotypic continuum between POLE-related recessive disorders (FILS / IMAGe-I): case report and literature review                    |

F4 previously read "Weren et al. 2015" -- that paper is NTHL1-associated polyposis and is now [P8].
F8 previously credited to "Vande Perre et al. 2022"; the AJMG-A continuum paper is Roberts et al.

---

## Variant Classification and Guidelines

| Ref | Citation                                             | ID                                 | URL                                                                                                                | Key contribution                                                                                                                                       |
| --- | ---------------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| C1  | Mur et al. 2023, _Genome Med_                        | `doi:10.1186/s13073-023-01234-y`   | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10580551/)                                                          | Gene-specific ACMG/AMP for POLE/POLD1 exonuclease-domain variants (128 variants; 17 P/LP, 17 B/LB). PM2 at Supporting. Truncating LoF is NOT the PPAP mechanism |
| C2  | PolED database 2025, _Database (Oxford)_             | `doi:10.1093/database/baaf076`     | [doi](https://doi.org/10.1093/database/baaf076) / [poled-db.org](https://poled-db.org)                             | 67 POLE + 69 POLD1 variants, 90 publications (1991-2025). Explicitly: "LoF variants cannot cause ultramutated cancers"                                 |
| C3  | MAVISp DNA-polymerase variants 2025, _bioRxiv_       | `doi:10.1101/2025.08.04.653638`    | [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.08.04.653638v2)                                             | Structure-level in-silico saturation mutagenesis of POLE/POLD1 (MAVISp + MD); >300 VUS flagged                                                         |
| C4  | ClinGen InSiGHT Hereditary CRC/Polyposis VCEP        | `url:https://clinicalgenome.org/affiliation/50099/` | [ClinGen](https://clinicalgenome.org/affiliation/50099/)                                                 | POLE/POLD1-specific rules still queued (after MUTYH, STK11) as of 2026-11-22                                                                           |
| C5  | Bergquist et al. 2025, _Genet Med_                   | `pmid:40084623`                    | [PubMed](https://pubmed.ncbi.nlm.nih.gov/40084623/)                                                                | Calibration of additional computational tools; expands ClinGen PP3/BP4 options                                                                         |
| C6  | Richards et al. 2015, _Genet Med_ (ACMG/AMP)         | `pmid:25741868`                    | [PubMed](https://pubmed.ncbi.nlm.nih.gov/25741868/)                                                                | Joint ACMG/AMP consensus for sequence variant interpretation                                                                                           |
| C7  | Abou Tayoun et al. 2018, _Hum Mutat_                 | `pmid:30192042`                    | [PubMed](https://pubmed.ncbi.nlm.nih.gov/30192042/)                                                                | ClinGen SVI PVS1 decision tree: PVS1 is not applied when LoF is not an established disease mechanism                                                   |
| C8  | Tavtigian et al. 2020, _Hum Mutat_                   | `pmid:32720330`                    | [PubMed](https://pubmed.ncbi.nlm.nih.gov/32720330/)                                                                | Bayesian point system: Supporting 1 / Moderate 2 / Strong 4 / Very Strong 8; P >=10, LP 6-9, VUS 0-5, LB -1 to -6, B <= -7                            |
| C9  | Brnich et al. 2020, _Genome Med_                     | `pmid:31892348`                    | [PubMed](https://pubmed.ncbi.nlm.nih.gov/31892348/)                                                                | PS3/BS3 functional evidence; OddsPath thresholds (pathogenic >2.1 supp / >4.3 mod / >18.7 strong; benign <0.48 / <0.23 / <0.053)                      |
| C10 | Pejaver et al. 2022, _Am J Hum Genet_                | `pmid:36413997`                    | [PubMed](https://pubmed.ncbi.nlm.nih.gov/36413997/)                                                                | Calibrated PP3/BP4: REVEL >=0.644 supp / >=0.773 mod / >=0.932 strong; CADD >=25.3 supp / >=28.1 mod; BP4 REVEL <=0.290                               |
| C11 | Walker et al. 2023, _Am J Hum Genet_                 | `pmid:37352859`                    | [PubMed](https://pubmed.ncbi.nlm.nih.gov/37352859/)                                                                | ClinGen SVI splicing subgroup: SpliceAI >=0.2 supports PP3; framework for predicted and observed splice impact                                         |
| C12 | ClinGen SVI PM2_Supporting recommendation (2020)     | `url:https://clinicalgenome.org/site/assets/files/5182/pm2_-_svi_recommendation_-_approved_sept2020.pdf` | [ClinGen SVI](https://clinicalgenome.org/working-groups/sequence-variant-interpretation/) | PM2 downgraded to Supporting strength by default                                                                       |
| C13 | Strande et al. 2017, _Am J Hum Genet_                | `pmid:28552198`                    | [PubMed](https://pubmed.ncbi.nlm.nih.gov/28552198/)                                                                | ClinGen gene-disease clinical validity framework (Definitive ... Limited; mechanism-specific curation)                                                 |

C7 note: the ClinGen SVI PVS1 flowchart was published in Hum Mutat (not Genet Med).
C8 note: Tavtigian 2020 was published in Hum Mutat (the 2018 Bayesian framework paper is Genet Med).

---

## Guidelines

| Ref | Citation                                                                                     | ID                                                                        | URL                                                                              | Key contribution                                                                                                     |
| --- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| G1  | NCCN Guidelines, Genetic/Familial High-Risk Assessment: Colorectal, Endometrial, and Gastric, v.2025 | `url:https://www.nccn.org/guidelines/guidelines-detail?category=2&id=1436` | [NCCN](https://www.nccn.org/guidelines/guidelines-detail?category=2&id=1436) (login) | POLE/POLD1 carriers: colonoscopy from 25-30 y (or 2-5 y before earliest family CRC if <25), q2-3 y if clear, q1-2 y if polyps |

---

## Mechanistic Studies

| Ref | Citation                                   | ID                                   | URL                                                                | Key contribution                                                                                                                  |
| --- | ------------------------------------------ | ------------------------------------ | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| M1  | Andrianova et al. 2024, _Eur J Hum Genet_  | `doi:10.1038/s41431-024-01598-8`     | [Nature](https://www.nature.com/articles/s41431-024-01598-8)       | POLD1 proofreading is recessive: heterozygous L474P only subtly raises mutation burden in normal cells; tumours reach >100 mut/Mb (SBS10d) after somatic inactivation of the WT allele. L474P is a hypomorph, so LOH is viable |
| M2  | Vipat et al. 2022, _Nat Commun_ 13:7099    | `doi:10.1038/s41467-022-34911-4`     | [Nature](https://www.nature.com/articles/s41467-022-34911-4)       | POLE1 catalytic N-terminal half dispensable for CMG assembly in human cells; cells survive only with the C-terminal half present |
| M3  | He et al. 2024, _Nat Commun_               | `doi:10.1038/s41467-024-52257-x`     | [Nature](https://www.nature.com/articles/s41467-024-52257-x)       | Human Pol-epsilon-PCNA holoenzyme: three-point interface = P-domain (His684-Lys729), thumb (Glu1085, Ser1117), PIP-motif aa 1180-1187; POLE1 N-terminal 23 residues disordered |
| M4  | Roske & Yeeles 2024, _Nat Struct Mol Biol_ | `doi:10.1038/s41594-024-01370-y`     | [Nature](https://www.nature.com/articles/s41594-024-01370-y)       | Cryo-EM of human Pol-epsilon processive synthesis and proofreading: intramolecular pol-to-exo switching                          |
| M5  | Wang et al. 2025, _Proc Natl Acad Sci USA_ | `doi:10.1073/pnas.2507232122`        | [doi](https://doi.org/10.1073/pnas.2507232122)                     | Proofreading intermediates of the human Pol-epsilon holoenzyme (mismatch-editing, backtracking states; PDB 9NE6/9NE7)           |
| M6  | Front Immunol 2025 (review)                | `doi:10.3389/fimmu.2025.1600233`     | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12256436/)          | POLD1 beyond proofreading: BIR-induced LOH, immune evasion orchestration                                                          |
| M7  | Yuan et al. 2020, _Nat Commun_             | `doi:10.1038/s41467-020-16910-5`     | [Nature](https://www.nature.com/articles/s41467-020-16910-5)       | Yeast Pol-epsilon holoenzyme architecture; CMG contacts via C-terminal non-catalytic half (PDB 6WJV)                              |
| M8  | Drost et al. 2016, _J Clin Invest_         | `pmid:27454287`                      | [PubMed](https://pubmed.ncbi.nlm.nih.gov/27454287/)                | BRCA1 185delAG (c.68_69del): translation reinitiation at Met297 yields RING-less BRCA1 -- precedent for reinitiation-mediated NMD escape |
| M9  | Robinson et al. 2021, _Nat Genet_          | `pmid:34594041`                      | [PubMed](https://pubmed.ncbi.nlm.nih.gov/34594041/)                | Normal cells of POLE/POLD1 carriers: SBS10c/SBS10d in POLD1 EDM carriers; replication-strand bias                                |
| M10 | DepMap portal, POLE                        | `url:https://depmap.org/portal/gene/POLE` | [DepMap](https://depmap.org/portal/gene/POLE)                 | POLE is common-essential across cell lines: a tumour cannot be POLE-null                                                          |
| M11 | Shlien et al. 2015, _Nat Genet_            | `pmid:25642631`                      | [PubMed](https://pubmed.ncbi.nlm.nih.gov/25642631/)                | CMMRD tumours acquire secondary somatic POLE/POLD1 EDM hits producing ultra-hypermutation                                         |
| M12 | Lindeboom et al. 2019, _Nat Genet_         | `pmid:31659324`                      | [PubMed](https://pubmed.ncbi.nlm.nih.gov/31659324/)                | NMDetective: genome-wide NMD efficacy rules (last-exon, 50-nt, start-proximal escape)                                             |

---

## Clinical Spectrum and Phenotype

| Ref | Citation                                        | ID                                  | URL                                                                                      | Key contribution                                                                                                                                                |
| --- | ----------------------------------------------- | ----------------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| P1  | Folletet et al. 2025, _Front Oncol_             | `doi:10.3389/fonc.2025.1727289`     | [doi](https://doi.org/10.3389/fonc.2025.1727289)                                         | First duodenal adenocarcinomas in germline POLD1 carriers; two likely pathogenic variants characterised                                                         |
| P2  | Viana-Errasti et al. 2025, _Mod Pathol_         | `doi:10.1016/j.modpat.2025.100843`  | [doi](https://doi.org/10.1016/j.modpat.2025.100843)                                      | Comparative somatic vs germline proofreading deficiency (360 tumours, 70 families, 249 individuals). AlphaMissense 0.87-1.0 for all P/LP                          |
| P3  | Palles et al. 2021, _Fam Cancer_                | `doi:10.1007/s10689-021-00256-y`    | [doi](https://doi.org/10.1007/s10689-021-00256-y)                                        | PPAP clinical features and management recommendations                                                                                                            |
| P4  | Clin J Gastroenterol 2024 (case report)         | `doi:10.1007/s12328-024-01922-1`    | [doi](https://doi.org/10.1007/s12328-024-01922-1)                                        | Multiple duodenal epithelial tumours in a POLE PPAP carrier                                                                                                       |
| P5  | Clin Genet 2022 (di-genic POLE + PMS2)          | `pmid:34967012`                     | [PubMed](https://pubmed.ncbi.nlm.nih.gov/34967012/)                                      | Paediatric cancer from combined germline POLE + PMS2 pathogenic variants                                                                                          |
| P6  | Mur et al. 2020, _Genet Med_                    | `doi:10.1038/s41436-020-0922-2`     | [Nature](https://www.nature.com/articles/s41436-020-0922-2)                              | Role of POLE and POLD1 in familial cancer: heterozygous LoF 0.22% in cases vs 0.20% controls (~1/500) -- no enrichment                                           |
| P7  | Palles et al. 2022, _Am J Hum Genet_            | `pmid:35460607`                     | [PubMed](https://pubmed.ncbi.nlm.nih.gov/35460607/)                                      | Germline biallelic MBD4 deficiency: polyposis / multi-tumour syndrome (phenocopy to exclude)                                                                      |
| P8  | Weren et al. 2015, _Nat Genet_                  | `pmid:25938944`                     | [PubMed](https://pubmed.ncbi.nlm.nih.gov/25938944/)                                      | NTHL1-associated polyposis (homozygous NTHL1 LoF) -- recessive polyposis phenocopy                                                                               |
| P9  | Bray et al. 2024, _CA Cancer J Clin_ (GLOBOCAN 2022) | `pmid:38572751`                  | [PubMed](https://pubmed.ncbi.nlm.nih.gov/38572751/)                                      | ~20 million new cancers in 2022; colorectal 9.6% (~1.9 million) -- denominator for the coincidence prior                                                       |

---

## Immunotherapy and Therapeutics

| Ref | Citation                                             | ID                                       | URL                                                                                                              | Key contribution                                                                                                     |
| --- | ---------------------------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| T1  | Jin et al. 2024, _Signal Transduct Target Ther_ (toripalimab Phase II)  | `doi:10.1038/s41392-024-01939-5` | [Nature](https://www.nature.com/articles/s41392-024-01939-5)                                                     | 15 enrolled / 14 evaluable: ORR 21.4% (3/14); EDM 66.7% (2/3) vs non-EDM 9.1% (1/11); trial NCT03810339 [CT2]        |
| T2  | LOP POLE stratification 2025, _J Immunother Cancer_  | `doi:10.1136/jitc-2025-012190`           | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12636876/)                                                        | 69,223 pan-cancer: POLE mutated 2.8% (1,965), LOP 7.5% (148). LOP ORR 88.9% (8/9); non-LOP MSI-H 66.7% (6/9)         |
| T3  | Ambrosini et al. 2024, _Ann Oncol_                   | `pmid:38777726`                          | [PubMed](https://pubmed.ncbi.nlm.nih.gov/38777726/)                                                              | 27 POLE/POLD1 proofreading-deficient mCRC on ICI vs 610 dMMR: ORR 89% vs 54%; PFS HR 0.24; response tracks signature intensity |
| T4  | MSS/POLE mCRC case report, _AME Med J_ (online 2025; vol. 2026) | `doi:10.21037/amj-24-13`      | [doi](https://doi.org/10.21037/amj-24-13)                                                                        | MSS, TMB-H, POLE-mutated mCRC: complete pathologic response to pembrolizumab, 37 months disease-free                 |
| T5  | Garmezy et al. 2022, _JCO Precis Oncol_              | `pmid:35108036`                          | [PubMed](https://pubmed.ncbi.nlm.nih.gov/35108036/)                                                              | 82 POLE-mutant tumours on ICI: pathogenic vs benign POLE CBR 82.4% vs 30.0%; PFS 15.1 vs 2.2 mo; OS 29.5 vs 6.8 mo   |
| T6  | Li et al. 2025, _Clin Colorectal Cancer_ (neoadjuvant ICI, MSI-H/POLE bulky LACRC) | `pmid:39095269`             | [PubMed](https://pubmed.ncbi.nlm.nih.gov/39095269/)                                                              | Retrospective, 22 patients, only 2 POLE-mutated: R0 20/20, pCR 14/20; both POLE patients responded (pCR, cCR). Not POLE-specific evidence |
| T7  | Non-EDM POLE/POLD1 and TMB 2025, _J Clin Oncol_ (ASCO abstract e14558) | `doi:10.1200/JCO.2025.43.16_suppl.e14558` | [ASCO](https://ascopubs.org/doi/10.1200/JCO.2025.43.16_suppl.e14558)                                 | Some non-exonuclease mutations contribute to high/ultrahigh TMB                                                      |
| T8  | ctDNA response in POLE CRC 2025, _Curr Oncol_        | `doi:10.3390/curroncol32070370`          | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12293316/)                                                        | ctDNA dynamics as ICI response biomarker in POLE-mutated early-onset colon cancer                                    |
| T9  | AstraZeneca press release, 22 Dec 2025               | `url:https://www.astrazeneca.com/media-centre/press-releases/2025/update-on-latify-phase-iii-trial.html` | [AstraZeneca](https://www.astrazeneca.com/media-centre/press-releases/2025/update-on-latify-phase-iii-trial.html) / [SEC 6-K](https://www.sec.gov/Archives/edgar/data/901832/000165495425014164/a3786m.htm) | LATIFY Phase III (ceralasertib + durvalumab vs docetaxel, NSCLC, n=594) did not meet the OS primary endpoint |

---

## Neoantigen Biology

| Ref | Citation                                   | ID                                | URL                                                            | Key contribution                                                                    |
| --- | ------------------------------------------ | --------------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| N1  | Neoantigen evolution in CRC 2026, _Nat Commun_ | `doi:10.1038/s41467-026-71135-2` | [Nature](https://www.nature.com/articles/s41467-026-71135-2) | Stochastic model: clonal neoantigen burden drives ICI response in CRC               |
| N2  | NeoPrecis 2026, _Nat Commun_               | `doi:10.1038/s41467-026-68651-6`  | [Nature](https://www.nature.com/articles/s41467-026-68651-6)   | Clonality-aware neoantigen prediction: +11% (melanoma), +20% (NSCLC) AUROC over TMB |
| N3  | Personalized neoantigen therapies review, _J Exp Med_ 223(2) | `doi:10.1084/jem.20241234` | [JEM](https://rupress.org/jem/article/223/2/e20241234/278560/) | TCR affinity, cross-reactivity, clonotype diversity correlate with vaccine response |

---

## Replication Stress and Targeted Therapy

| Ref | Citation                                             | ID                                 | URL                                                                                                | Key contribution                                                                               |
| --- | ---------------------------------------------------- | ---------------------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| R1  | Hustedt et al. 2019, _Open Biol_                     | `doi:10.1098/rsob.190156`          | [Royal Society](https://royalsocietypublishing.org/doi/10.1098/rsob.190156)                        | Consensus CRISPR screens: POLE3/POLE4 loss causes ATR inhibitor hypersensitivity               |
| R2  | Hocke et al. 2016, _Oncotarget_                      | `pmid:26755646`                    | [PubMed](https://pubmed.ncbi.nlm.nih.gov/26755646/)                                                | 288 DNA-repair gene screen: POLD1 deficiency synthetic lethal with ATR inhibition              |
| R3  | CTNA sensitivity 2025, _DNA Repair_                  | `doi:10.1016/j.dnarep.2025.103885` | [doi](https://doi.org/10.1016/j.dnarep.2025.103885)                                                | POLE exo-deficient cells: 3-4x Ara-C IC50 reduction. Pol-delta/Pol-epsilon independently contribute |
| R4  | CTNAs and genome maintenance, _Cancer Sci_ (online 2025; print 2026) | `doi:10.1111/cas.70285` | [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/cas.70285)                                     | 12 nucleoside analogs x 24 mutant lines. POLE1exo-/- + CTF18-/- synthetic lethality with Ara-C |
| R5  | ATR inhibitor meta-analysis 2025, _Front Oncol_      | `doi:10.3389/fonc.2025.1706837`    | [Frontiers](https://www.frontiersin.org/journals/oncology/articles/10.3389/fonc.2025.1706837/full) | 10 trials, 810 patients: no overall benefit unselected; subgroup benefit in NSCLC              |
| R6  | POLA1-ATR synthetic lethality 2024, _Neoplasia_      | `doi:10.1016/j.neo.2024.101038`    | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11369380/)                                          | B-family polymerase / ATR paradigm extends to Pol-alpha                                        |
| R7  | POLD1 R689W ATR/CHK1 sensitivity 2020, _Sci Rep_     | `doi:10.1038/s41598-020-76033-1`   | [Nature](https://www.nature.com/articles/s41598-020-76033-1)                                       | Specific POLD1 variant increases ATRi/CHK1i sensitivity                                        |
| R8  | Bellelli et al. 2020, _Cell Rep_                     | `pmid:32460026`                    | [PubMed](https://pubmed.ncbi.nlm.nih.gov/32460026/)                                                | RTEL1 deficiency synthetic lethal with Pol-epsilon loss in metazoan replication                |

---

## OMIM Entries

| Ref | ID            | Disease/Gene                                                             | URL                                        |
| --- | ------------- | ------------------------------------------------------------------------ | ------------------------------------------ |
| O1  | `omim:615083` | CRCS12 = PPAP, POLE-related (Polymerase Proofreading-Associated Polyposis) | [OMIM](https://omim.org/entry/615083)    |
| O2  | `omim:615139` | FILS syndrome (biallelic hypomorphic POLE)                               | [OMIM](https://omim.org/entry/615139)      |
| O3  | `omim:618336` | IMAGe-I syndrome (biallelic hypomorphic POLE)                            | [OMIM](https://omim.org/entry/618336)      |

OMIM blocks scripted HTML access (HTTP 403); `check_refs.py` resolves `omim:` via NCBI E-utilities (db=omim).

---

## Structural Database Entries

| Ref | Database     | ID                | Description                                                                                            | URL                                                        |
| --- | ------------ | ----------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------- |
| S1  | PDB          | `pdb:9B8S`        | Human Pol-epsilon (D275A/E277A) -PCNA-DNA holoenzyme, nucleotide-exchange state (He 2024 [M3]; companion 9B8T). Chain A models POLE aa 27-1198 (gap 185-211); helix Arg37-Phe50 contacts exo residues 352-403 | [RCSB](https://www.rcsb.org/structure/9B8S)     |
| S2  | PDB          | `pdb:7PFO`        | Core human replisome: CMG-Pol-epsilon-TIMELESS-TIPIN-CLASPIN-AND-1 (Jones et al. 2021, EMBO J)        | [RCSB](https://www.rcsb.org/structure/7PFO)                |
| S3  | PDB          | `pdb:6WJV`        | S. cerevisiae Pol-epsilon holoenzyme; basis for leading-strand replisome model (Yuan 2020 [M7])        | [RCSB](https://www.rcsb.org/structure/6WJV)                |
| S4  | PDB          | `pdb:8TWA`        | S. cerevisiae Ctf18-RFC-PCNA-Pol-epsilon-DNA (2024)                                                    | [RCSB](https://www.rcsb.org/structure/8TWA)                |
| S5  | UniProt      | `uniprot:Q07864`  | Human POLE (DNA polymerase epsilon catalytic subunit A, 2,286 aa): domains, PTMs, interaction partners | [UniProt](https://www.uniprot.org/uniprotkb/Q07864/entry)  |
| S6  | AlphaFold DB | `url:https://alphafold.ebi.ac.uk/entry/Q07864` | POLE structure prediction; pLDDT for aa 1-65 (disordered aa 1-30, helix 25-47, strand 57-65) and NTD contacts lost in the ΔN65 reinitiation product | [AlphaFold](https://alphafold.ebi.ac.uk/entry/Q07864) |
| S7  | UniProt      | `uniprot:P38398`  | Human BRCA1 (1,863 aa): RING domain aa 1-109; Met297 reinitiation site ([M8], examples/brca1-c68_69del.md) | [UniProt](https://www.uniprot.org/uniprotkb/P38398/entry) |

Superseded (wrong) accessions removed: 6SKL (CMG-fork protection complex, no Pol-epsilon), 6VVO (RFC-PCNA), 8SGQ (CCT), 8SGR (IVD). P28340 is POLD1, not POLE.

---

## Clinical Trial Registrations

| Ref | ID                | Title / Scope                                                                                                     | Status (CT.gov, 2026-11-22) |
| --- | ----------------- | ----------------------------------------------------------------------------------------------------------------- | --------------------------- |
| CT1 | `nct:NCT05103969` | Multicenter prospective cohort of tumours with POLE/POLD1 mutation                                                | UNKNOWN                     |
| CT2 | `nct:NCT03810339` | Toripalimab monotherapy in POLE/POLD1-mutated, non-MSI-H advanced solid tumours (Phase II; source of [T1])        | RECRUITING                  |
| CT3 | `nct:NCT02628067` | KEYNOTE-158: pembrolizumab, predictive biomarkers incl. TMB-H in advanced solid tumours                           | ACTIVE_NOT_RECRUITING       |
| CT4 | `nct:NCT03639714` | GRT-C901/GRT-R902 personalised neoantigen vaccine + checkpoint blockade (nivolumab/ipilimumab), Phase 1/2         | COMPLETED                   |
| CT5 | `nct:NCT03435107` | Durvalumab in dMMR or POLE-mutated metastatic colorectal cancer (Phase II)                                        | COMPLETED                   |

Removed as wrong: NCT03785834 (cellulitis), NCT04230395 (alcohol/TB), NCT03359239 (urothelial vaccine + atezolizumab).

---

## Mutational Signature References

| Ref  | Signature       | ID                                                    | Polymerase            | Description                                                                        |
| ---- | --------------- | ----------------------------------------------------- | --------------------- | ---------------------------------------------------------------------------------- |
| SIG1 | COSMIC SBS10a   | `url:https://cancer.sanger.ac.uk/signatures/sbs/sbs10a/` | Pol-epsilon          | TCT>TAT (C>A); POLE exonuclease-domain deficiency                                  |
| SIG2 | COSMIC SBS10b   | `url:https://cancer.sanger.ac.uk/signatures/sbs/sbs10b/` | Pol-epsilon          | TCG>TTG (C>T); POLE exonuclease-domain deficiency                                  |
| SIG3 | COSMIC SBS10c/d | `url:https://cancer.sanger.ac.uk/signatures/sbs/sbs10c/` | Pol-delta            | POLD1 proofreading deficiency [M9]                                                 |
| SIG4 | COSMIC SBS28    | `url:https://cancer.sanger.ac.uk/signatures/sbs/sbs28/`  | Pol-epsilon          | T>G in TTT context; co-occurs with SBS10a/b in POLE exonuclease-deficient tumours  |
| SIG5 | COSMIC SBS20    | `url:https://cancer.sanger.ac.uk/signatures/sbs/sbs20/`  | MMR + Pol-delta      | Combined MMR + POLD1 deficiency                                                    |
| SIG6 | COSMIC SBS14    | `url:https://cancer.sanger.ac.uk/signatures/sbs/sbs14/`  | MMR + Pol-epsilon    | Combined MMR + POLE exonuclease deficiency (ultra-hypermutation, [M11])            |

---

## Cohort and Population Databases

| Ref | Resource                      | ID                                            | Use case                                                                  |
| --- | ----------------------------- | --------------------------------------------- | ------------------------------------------------------------------------- |
| D1  | gnomAD v4.1 (exomes + genomes) | `url:https://gnomad.broadinstitute.org/`     | Population frequency (~807,000 individuals, ~1.6 M alleles), pLI, LOEUF, o/e LoF |
| D2  | ClinVar                       | `url:https://www.ncbi.nlm.nih.gov/clinvar/`   | Existing classifications, submitter evidence, functional data in comments |
| D3  | LOVD (gene-specific)          | `url:https://www.lovd.nl/`                    | International submissions, curator annotations                            |
| D4  | DECIPHER                      | `url:https://www.deciphergenomics.org/`       | Overlapping patients, CNV context                                         |
| D5  | HGMD (licensed)               | `url:https://www.hgmd.cf.ac.uk/`              | Published mutations, literature links                                     |
| D6  | VarSome / Franklin            | `url:https://varsome.com/`                    | Aggregated pre-classification                                             |
| D7  | Matchmaker Exchange           | `url:https://www.matchmakerexchange.org/`     | Patient matching for ultra-rare variants                                  |
| D8  | TCGA (GDC portal)             | `url:https://portal.gdc.cancer.gov/`          | POLE somatic hypermutator cohort; germline LoF co-occurrence              |
| D9  | UK Biobank                    | `url:https://biobank.ndph.ox.ac.uk/`          | Exome cohort PheWAS for POLE LoF carriers                                 |
| D10 | Genomics England 100K Genomes | `url:https://www.genomicsengland.co.uk/`      | Colorectal panel data                                                     |

---

## Computational Tools

| Ref   | Tool                      | ID                                                                   | Purpose                                                      |
| ----- | ------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------ |
| TOOL1 | SpliceAI                  | `url:https://spliceailookup.broadinstitute.org/`                     | Splice variant prediction (PP3 per [C11])                    |
| TOOL2 | CADD                      | `url:https://cadd.gs.washington.edu/`                                | Combined annotation-dependent depletion score (missense/splice; not for frameshift PP3) |
| TOOL3 | REVEL                     | `url:https://sites.google.com/site/revelgenomics/`                   | Missense ensemble score (thresholds per [C10]); not applicable to frameshifts |
| TOOL4 | AlphaMissense             | `url:https://alphamissense.hegelab.org/`                             | Missense pathogenicity (0.87-1.0 for all P/LP POLE/POLD1 [P2]); not applicable to frameshifts |
| TOOL5 | IUPred3                   | `url:https://iupred3.elte.hu/`                                       | Intrinsic disorder prediction (truncated fragment stability) |
| TOOL6 | NMDetective               | `url:https://figshare.com/articles/dataset/NMDetective/7803398`      | NMD efficacy prediction for every possible PTC [M12]         |
| TOOL7 | NetMHCpan                 | `url:https://services.healthtech.dtu.dk/services/NetMHCpan-4.1/`     | HLA-peptide binding prediction (neoantigen presentation)     |
| TOOL8 | HRDetect / CHORD          | `url:https://github.com/Nik-Zainal-Group/signature.tools.lib`        | Homologous recombination deficiency signature detection (CHORD: github.com/UMCUGenetics/CHORD) |

---

## How to cite in case reports

When drafting a case report or classification submission using this skill,
cite primary sources by their Ref ID above. Minimum citation set for a POLE
truncation paradox case:

- **Paradox framing:** F1, C1, C2, P6 (establishes that LoF is not PPAP)
- **Essential-gene constraint:** M2, M10 (POLE cannot be null; LOH of a null allele is inviable)
- **Mechanistic hypotheses:** M1, M3, M4, M5, M8, M11 (hypomorph-LOH precedent, structural basis, reinitiation precedent, secondary-hit ultra-hypermutation)
- **Classification:** C1, C2, C4, C6, C7, C8, C9 (ACMG framework, PVS1 gating, points, functional evidence)
- **Surveillance:** G1
- **Therapeutic implications:** T1, T2, T5 (ICI stratification by variant class)
- **Neoantigen biology:** N1, N2 (clonality matters, not just TMB)
