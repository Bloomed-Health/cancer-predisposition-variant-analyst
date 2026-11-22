# Scripts

Stdlib-only Python 3.10+ helpers that pull the live numbers the skill asks for (Step 1 molecular consequence, Step 3 population data, Step 4 ClinVar context) plus a reference-integrity check. No third-party packages. Every script supports `--help` and `--json`, uses a 30 s socket timeout and the shared `_http.py` (retry with back-off on 429/5xx and network errors, `Retry-After` honoured, per-host request spacing, one descriptive `User-Agent`).

| Script | Source | What it returns |
|---|---|---|
| `hgvs_validate.py` | VariantValidator REST, Ensembl REST | normalized HGVS (c./p./g.), VCF key, exon of variant, computed consequence (missense / nonsense / frameshift / in-frame indel / stop-loss), PTC codon (parsed and re-derived), NMD call, fraction of protein lost, downstream in-frame AUG scan with Kozak context |
| `gnomad_lookup.py` | gnomAD GraphQL (v4.1 default) | variant AC/AN/AF (exome, genome, joint), filters, coverage when absent; gene constraint pLI / o-e LoF (LOEUF) / o-e missense |
| `clinvar_lookup.py` | NCBI E-utilities (esearch, esummary, efetch) | variant records with classification, review status, conditions, submitters; gene-level counts by classification, by condition, by submitter |
| `check_refs.py` | Crossref, NCBI E-utilities, ClinicalTrials.gov v2, RCSB, UniProt, publisher URLs | resolves every `ID` in `references.md`, checks every `[ID]` cited in the skill's markdown is defined, optional `--strict` year/first-author comparison |
| `_http.py` | -- | shared HTTP helper (not a CLI) |

Exit codes (all four CLIs): `0` success (including "variant absent" / "no records"), `1` bad input, rejected variant or any `check_refs.py` FAIL, `2` network or API error. argparse usage errors (unknown flag, missing argument) also exit `2`.

Network notes: all four call public endpoints without credentials. VariantValidator and Ensembl are rate-limited (Ensembl answers 429 with `Retry-After`; `_http.py` sleeps for it, delta-seconds or HTTP-date, capped at 60 s). NCBI E-utilities allow 3 requests/s anonymously; set `NCBI_API_KEY` (or `--api-key`) for 10/s. The gnomAD API has no documented limit but is shared infrastructure; do not loop over whole genes. Outputs below were produced live on 2026-11-22; database releases move, so re-run rather than copy.

## hgvs_validate.py

```
python3 scripts/hgvs_validate.py 'NM_006231.4:c.158_159del' [--assembly GRCh38|GRCh37] [--transcript NM_...] [--max-met 10] [--json]
```

Pipeline: VariantValidator (`/VariantValidator/variantvalidator/<assembly>/<hgvs>/<transcript>`), then Ensembl `xrefs/symbol` (RefSeq -> ENST), `lookup/id/<ENST>?expand=1` (exons, translation bounds) and `sequence/id/<ENST>?type=cdna`. The CDS is rebuilt from the exon model, the edit (sub/del/dup/ins/delins/inv in coding positions) is applied and re-translated, reading into the 3' UTR, so the PTC is derived independently of the protein HGVS; the two are compared and any mismatch is printed as a note. NMD rule: PTC more than 55 nt upstream of the last exon-exon junction -> NMD predicted; last exon, or penultimate exon within 55 nt -> escape. Extra flags for start-proximal PTCs (first 150 nt of CDS) and long exons (>400 nt), both associated with inefficient NMD [M12]. Kozak classes: -3 purine and +4 G = strong; one of the two = adequate; neither = weak.

Intronic / UTR / complex descriptions are validated but not re-translated (noted in output). Exon ordinals are Ensembl transcript order; VariantValidator's ordinal is printed alongside and a note is raised if they differ.

Trimmed live output (Met rows after the first six removed), POLE worked example:

```
Submitted:            NM_006231.4:c.158_159del
Transcript HGVS:      NM_006231.4:c.158_159del  (gene POLE, MANE Select: True)
Protein HGVS (VV):    NP_006222.2:p.(Leu53GlnfsTer5)  [NP_006222.2:p.(L53Qfs*5)]
Genomic HGVS:         NC_000012.12:g.132681183_132681184del
VCF (GRCh38):         12-132681182-TCA-T
Ensembl transcript:   ENST00000320574.10 (POLE-201, strand -, canonical=True)
CDS / protein:        6861 nt / 2286 aa; 49 exons
Variant exon:         2 of 49  (exon spans c.63-c.204); VariantValidator exon 2
Protein HGVS (calc):  p.(Leu53Glnfs*5)  [frameshift]
PTC codon:            parsed=57  computed=57
Truncation:           52 WT residues retained (2.3% of 2286), 97.7% lost; +4 frameshift residues; product 56 aa
NMD:                  NMD predicted -- PTC 6576 nt upstream of the last exon-exon junction (> 55 nt); PTC in exon 2/49, first nt c.169
                      flag: borderline start-proximal PTC (c.169; 150 < c. <= 200 nt): reduced NMD efficiency and downstream reinitiation remain possible
Reinitiation scan:    54 in-frame ATG downstream of PTC; first strong Kozak: Met359
  Met     +codons  context(-6..+4)  -3  +4  Kozak     product_aa  retained
  Met66          9  ATTAACATGC       A   C  adequate        2221  97.2%
  Met221       164  GTGGACATGC       G   C  adequate        2066  90.4%
  Met294       237  CAGATTATGA       A   A  adequate        1993  87.2%
  Met295       238  ATTATGATGA       A   A  adequate        1992  87.1%
  Met299       242  TCCTACATGA       T   A  weak            1988  87.0%
  Met359       302  ACCATCATGG       A   G  strong          1928  84.3%
```

Non-truncating controls (full live output of the relevant lines): `NM_000492.4:c.1521_1523del` -> `Protein HGVS (calc):  p.(Phe508del)  [in-frame indel]`, `PTC codon: parsed=None  computed=None`, `NMD: not applicable (no premature termination codon)`; `NM_000546.6:c.1180T>C` -> `p.(Ter394Argext*9)  [stop-loss (extension)]`, VV `p.(Ter394ArgextTer9)`.

BRCA1 c.68_69del (185delAG) for comparison: `p.(Glu23ValfsTer17)`, variant in exon 2/23, PTC codon 39 in exon 3, "NMD predicted" by the junction rule but flagged start-proximal (c.115); the scan lists Met48 (weak), Met128 (strong), Met297 (adequate, `GACAGAATGA`) -- the latter is the documented reinitiation site that yields RING-less BRCA1 [M8].

## gnomad_lookup.py

```
python3 scripts/gnomad_lookup.py --gene POLE [--dataset gnomad_r4] [--json]
python3 scripts/gnomad_lookup.py --variant 12-132681182-TCA-T [--variant-grch37 12-133257768-TCA-T] [--json]
```

Variant IDs are gnomAD style `chrom-pos-ref-alt` with the VCF anchor base; copy them from the `VCF` line of `hgvs_validate.py`. When a variant is absent the script prints exome and genome coverage at the position so "absent" can be distinguished from "not callable". gnomAD v4 exposes no non-cancer subset through the API; pass the GRCh37 key with `--variant-grch37` to also query `gnomad_r2_1_non_cancer` (the subset Castillejo 2023 [C1] uses for PM2_Supporting). gnomAD "Variant not found" is a normal `ABSENT` result (exit 0); HTTP 429/5xx and network errors are retried three times, then exit 2.

Live output (both commands, verbatim):

```
gnomAD constraint  POLE (ENSG00000177084; canonical ENST00000320574; MANE ENST00000320574/NM_006231; GRCh38)
  pLI            1.11e-40
  LoF   o/e      0.67  (90% CI 0.60-0.76; LOEUF = 0.76)  obs/exp 188/279.2  z=4.63
  Missense o/e   0.90  (90% CI 0.87-0.92)  obs/exp 2703/3016.7  z=2.44
  Synonymous o/e 1.04  obs/exp 1214/1172.5  z=-0.72
  Interpretation: LOEUF < 0.6 (or pLI > 0.9) = LoF-intolerant; LOEUF around 1 = LoF tolerated at haploid dose.
gnomAD gnomad_r4  variant 12-132681182-TCA-T
  ABSENT (not in this dataset)
  exome coverage at pos: mean depth 30.9, median 31, fraction >20x 1.00
  genome coverage at pos: mean depth 31.2, median 32, fraction >20x 0.97
gnomAD v2.1.1 non-cancer subset  variant 12-133257768-TCA-T (GRCh37)
  ABSENT
```

Reading: 188 observed vs 279 expected LoF alleles (o/e 0.67, LOEUF 0.76, pLI ~0) means heterozygous POLE LoF is depleted only mildly and is not haploinsufficient-intolerant; the essential-gene phenotype shows up at the cellular level (DepMap [M10]), not as germline LoF intolerance.

## clinvar_lookup.py

```
python3 scripts/clinvar_lookup.py --gene POLE [--type truncating|frameshift|nonsense|missense|synonymous|splice|all]
                                  [--significance VUS] [--condition polyposis] [--submitters] [--limit 20] [--json]
python3 scripts/clinvar_lookup.py --variant 'NM_006231.4:c.158_159del' [--gene POLE] [--position 12:132681183] [--limit 20] [--json]
```

Gene mode runs one `esearch` (`<gene>[gene] AND <molecular consequence>[mcns]`) and pages `esummary` over every Variation ID, then tabulates the ClinVar aggregate germline classification, a classification x condition cross-tab, and with `--submitters` an SCV-level submitter x classification tally from `efetch rettype=vcv` (about 1 min for 700 records at the anonymous rate). `--significance P/LP`, `VUS`, `B/LB` or `Conflicting` matches the collapsed bucket exactly; any other value is a case-insensitive substring of the ClinVar description, so `--significance pathogenic` also keeps "Likely pathogenic" and "Conflicting classifications of pathogenicity" -- use `P/LP` when you mean P+LP only. Variant mode searches `<c.>[varname] AND <accession>[All Fields]`, falls back to the version-less accession (and, with `--gene`, any transcript of that gene), and with `--position` sweeps `[chr] AND [cpos]` so records at the same base are shown even when the HGVS differs; each search fetches at most `--limit` records and prints `(N more not shown; raise --limit)` when it truncates.

Trimmed live output (`--gene POLE --submitters`; "By condition" rows 8-10 and the 20 listed records removed), 2026-11-22:

```
ClinVar  POLE  type=truncating  query: POLE[gene] AND ("frameshift variant"[mcns] OR nonsense[mcns])
  Variation IDs matched: 678
  Germline classification (aggregate per Variation ID):
      301  ( 44.4%)  Pathogenic
      216  ( 31.9%)  Conflicting classifications of pathogenicity
      145  ( 21.4%)  Uncertain significance
       11  (  1.6%)  Likely pathogenic
        3  (  0.4%)  Pathogenic/Likely pathogenic
        2  (  0.3%)  (no germline classification)
  Collapsed: P/LP 315/678 (46.5%), VUS 145/678 (21.4%), B/LB 0/678 (0.0%), Conflicting 216/678 (31.9%), Other 2/678 (0.3%)
  By condition (top 10; a Variation ID counts once per condition it cites):
        n  P/LP   VUS  B/LB Confl Other  condition
      533   302    16     0   215     0  not provided
      334     0   125     0   209     0  Hereditary cancer-predisposing syndrome
       26     4     7     0    15     0  Colorectal cancer, susceptibility to, 12
       14     5     0     0     9     0  Intrauterine growth retardation, metaphyseal dysplasia, adrenal hypoplasia congenita, genital anomalies, and immunodeficiency
       14     4     0     0    10     0  POLE-related disorder
       12     3     0     0     9     0  Facial dysmorphism-immunodeficiency-livedo-short stature syndrome
  By submitter (germline SCVs across the 678 Variation IDs; top 15):
      514  Pathogenic                               Labcorp Genetics (formerly Invitae), Labcorp
      334  Uncertain significance                   Ambry Genetics
       22  Likely pathogenic                        GeneDx
       20  Uncertain significance                   GeneDx
       20  Uncertain significance                   Counsyl
       15  Uncertain significance                   Labcorp Genetics (formerly Invitae), Labcorp
```

Reading: the headline "46.5% P/LP" is not evidence that POLE LoF causes PPAP. 295/301 Pathogenic aggregates are single-laboratory, 1-star calls with condition "not provided" (514 Pathogenic SCVs from Labcorp Genetics/Invitae), and 214/216 conflicts are that Pathogenic call paired with a VUS from a hereditary-cancer-panel submitter (216/216 contain a VUS; Ambry alone contributes 334 VUS SCVs). Restricted to records filed under "Hereditary cancer-predisposing syndrome", the split is 0 P/LP, 125 VUS, 209 conflicting, 0 B/LB (n = 334). Under the PPAP-specific condition names (`--condition colorectal --condition polyposis`, n = 30): 5 P/LP, 7 VUS, 18 conflicting, 0 B/LB; the 5 P/LP are all single-submitter, 1-star records (EVOGEN x2, KCCC Kuwait x1, Labcorp Genetics x1, NCI Genomic Center x1), none with multi-submitter concordance or expert-panel review. The P/LP calls that carry a syndromic condition name are the recessive FILS / IMAGe-I phenotypes (biallelic POLE), where truncating alleles are a recognised mechanism. Net: no expert-panel or multi-submitter-concordant P/LP exists for a truncating POLE allele in the dominant PPAP context, and 0/678 truncating records are B/LB, which is the expected steady state when LoF is not the disease mechanism and PVS1 is not applied [C7]: the default lands at VUS, not benign.

Variant mode, worked example (`--variant 'NM_006231.4:c.158_159del' --gene POLE --position 12:132681183`, verbatim):

```
ClinVar  variant NM_006231.4:c.158_159del
  search [hgvs+accession] c0x2e1580x5f159del[varname] AND NM_006231.4[All Fields] -> 0 record(s)
  search [hgvs+accession-any-version] c0x2e1580x5f159del[varname] AND NM_006231[All Fields] -> 0 record(s)
  search [hgvs+gene] c0x2e1580x5f159del[varname] AND POLE[gene] -> 0 record(s)
  search [position] 12[chr] AND 000132681183[cpos] -> 2 record(s)
  No exact record for this transcript HGVS; related records at the locus:
  VCV001671161.9  (Variation ID 1671161; matched by position)
    title:          NM_006231.4(POLE):c.159G>T (p.Leu53=)
    germline:       Likely benign  [criteria provided, multiple submitters, no conflicts; **; last evaluated 2026/07/04; 2 submission(s)]
    conditions:     Hereditary cancer-predisposing syndrome; not provided
    consequence:    synonymous variant
    submissions:    Likely benign (Labcorp Genetics (formerly Invitae), Labcorp); Likely benign (Ambry Genetics)
    url:            https://www.ncbi.nlm.nih.gov/clinvar/variation/1671161/
  VCV001083946.9  (Variation ID 1083946; matched by position)
    title:          NM_006231.4(POLE):c.159G>A (p.Leu53=)
    germline:       Likely benign  [criteria provided, single submitter; *; last evaluated 2020/11/18; 1 submission(s)]
    conditions:     not provided
    consequence:    synonymous variant
    submissions:    Likely benign (Labcorp Genetics (formerly Invitae), Labcorp)
    url:            https://www.ncbi.nlm.nih.gov/clinvar/variation/1083946/
```

Without `--gene`/`--position` the same variant gives the first two searches and `ABSENT: no ClinVar record for this HGVS`. So c.158_159del itself is absent from ClinVar (and from gnomAD v4.1 / v2.1.1 non-cancer); the only records at the base are two synonymous Leu53= changes. Positive control: `--variant 'NM_007294.4:c.68_69del'` returns VCV000017662 (BRCA1 185delAG), Pathogenic, reviewed by expert panel, 98 submissions.
