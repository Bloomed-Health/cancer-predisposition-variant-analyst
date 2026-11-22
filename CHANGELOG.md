# Changelog

All notable changes to this skill are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/).

## [2.0.0] - 2026-11-22

### Fixed

- Protein consequence of the canonical variant: p.Leu53Valfs*2 / "~aa 54" corrected to
  NM_006231.4:c.158_159del p.(Leu53Glnfs*5), PTC at codon 57 of 2,286, exon 2 of 49
  (VariantValidator; ENST00000320574).
- POLE UniProt accession: P28340 (which is POLD1, 1,107 aa) corrected to Q07864 (2,286 aa);
  exonuclease domain aa 268–471.
- Structural database entries: 6SKL, 6VVO, 8SGQ, 8SGR removed as wrong; 8TWA retained;
  replaced with verified PDB IDs.
- Clinical trial identifiers: NCT03785834, NCT04230395, NCT03359239 removed as wrong
  (unrelated trials); POLE/POLD1 cohort trial is NCT05103969.
- [M2] DOI/URL corrected to Nat Commun 13:7099 (s41467-022-34911-4).
- SBS28 attribution: Pol δ corrected to Pol ε exonuclease deficiency (co-occurs with SBS10a/b);
  SBS10c/10d are the POLD1 signatures.
- N-terminal CMG-binding premise removed: CMG/GINS binding is via the C-terminal
  non-catalytic half of POLE; nothing in aa 1–65 contacts CMG.
- PM2 strength: Supporting (Castillejo 2023; ClinGen SVI 2020), not Moderate.
- PVS1: no "Moderate" fallback when LoF is not the gene–disease mechanism; PVS1 is not applied.
- NCCN POLE/POLD1 surveillance ages: colonoscopy from 25–30 y, q2–3 y if clear, q1–2 y if polyps.
- Toripalimab EDM response rate carries its denominator: 66.7% (2/3).
- gnomAD v4.1 size: ~807,000 individuals (~1.6 M alleles); "730,000 alleles" removed.
- Reference re-attributions: F2 Church 2013 is Hum Mol Genet (somatic EDM in endometrial
  cancer), F4 is Spier 2015 (germline POLE spectrum; "Weren 2015" is NTHL1 → P8), F8 is
  Roberts 2022 AJMG-A; C7/C8 are Hum Mutat. Every reference row now carries a
  machine-checkable DOI/PMID/NCT/PDB/UniProt ID (101/101 resolve).
- FILS/IMAGe-I described as biallelic *hypomorphic* POLE (not biallelic null), consistent with
  essentiality.
- ClinVar reality: POLE truncating records are mostly single-lab "Pathogenic" with condition
  "not provided" or conflicting; none is concordant P/LP for PPAP. Earlier wording ("usually
  VUS or absent") replaced with the measured distribution and a condition-field warning.

### Added

- Step 0: genotype verification and phenocopy exclusion (somatic POLE/POLD1 EDM hotspot,
  MMR deficiency/CMMRD, MUTYH/NTHL1/MBD4) before any mechanism discussion.
- Essential-gene filter: POLE is pan-essential, so "null + LOH" is inviable and is excluded.
- Mutational signature fork (SBS10a/b/28 POLE; SBS10c/d POLD1; SBS14/20 with MMRd).
- Translation-reinitiation hypothesis (in-frame Met66/Met359 downstream of the PTC) ranked
  first for early-exon PTCs, with BRCA1 c.68_69del RING-less precedent [M8].
- Bayesian points ACMG tally (Tavtigian 2020) [C8].
- Brnich 2020 PS3/BS3 functional-evidence grading [C9].
- Calibrated PP3/BP4 thresholds (Pejaver 2022; Walker 2023 SpliceAI) [C10][C11].
- Second worked example: `examples/brca1-c68_69del.md`.
- Manual evals: `evals/README.md`.
- Stdlib-only helper scripts: `scripts/hgvs_validate.py`, `scripts/gnomad_lookup.py`,
  `scripts/clinvar_lookup.py`, `scripts/check_refs.py`.
- CI workflow checking reference links (`.github/workflows/check-refs.yml`).
- Guardrails section in `SKILL.md`; `last_verified` metadata field.
- New reference IDs C7–C13, M8–M12, P7–P8, T9, SIG6.
- G1 (NCCN colorectal high-risk guideline), S7 (BRCA1 UniProt), CT2/CT4/CT5 verified trials
  (NCT03810339, NCT03639714, NCT03435107).

### Changed

- Workflow expanded from five steps to six (0–5), with deep links to exact section headings.
- "Why this is paradigm-shifting" box rewritten as a neutral "Why this is a paradox" box that
  states the two cheap resolutions (coincidence; reinitiation).
- Trigger clause: adds early-exon truncation/reinitiation questions; drops the blanket BRCA1/2
  exclusion in favour of "routine panel interpretation with no genotype–phenotype conflict".
- Default classification for PPAP from a POLE LoF allele stated explicitly as VUS.
- README: frontmatter removed, file table updated, clone URL moved to bloo-berries, Maintenance section.

### Removed

- PCNA/RFC-based mechanism for the N-terminal fragment.
- CMG-stabiliser hypothesis for the N-terminal fragment.
- Antioxidant chemoprevention recommendation.
- Unsourced ATR-inhibitor agents (ceralasertib Phase III LATIFY negative; elimusertib Phase I only).

## [1.2.0] - 2026-04-16

### Changed

- Split reference tables into `references.md` and `quick-reference.md`.

## [1.0.0] - 2026-04-15

### Added

- Initial release: five-step workflow, POLE frameshift worked example, mechanistic
  framework, ACMG assembly, literature protocol, therapeutic mapping, references.
