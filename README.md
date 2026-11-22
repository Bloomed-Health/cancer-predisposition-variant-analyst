# Cancer Predisposition Variant Analyst

A Claude Code skill for interpreting ultra-rare variants in cancer predisposition genes -- specifically the cases where the genotype shouldn't produce the phenotype you're looking at, but it does anyway.

The worked example throughout is a germline POLE frameshift, NM_006231.4:c.158_159del p.(Leu53Glnfs*5) (exon 2 of 49, premature stop at codon 57 of 2,286), reported with an ultra-hypermutated PPAP-like phenotype. Current consensus says a POLE null allele shouldn't do this. The skill's first job is to check whether the paradox is real (somatic exonuclease-domain driver? MMR deficiency? translation reinitiation downstream of the stop?) before it lets Claude reach for a novel mechanism.

That discipline -- and the reasoning framework around it -- is what this skill encodes.

## What's in here

| File | What it does |
|------|-------------|
| `SKILL.md` | Entry point. Trigger clauses, six-step workflow (0–5), guardrails, sub-file index |
| `references/variant-interpretation.md` | Step 0 phenocopy exclusion, molecular characterization, NMD prediction, ACMG/ClinGen criteria with Bayesian points |
| `references/mechanistic-framework.md` | Essential-gene filter, signature fork, ranked hypotheses, discriminating experiments, generalizable template |
| `references/literature-protocol.md` | Structured search strategy, evidence grading, gap analysis template |
| `references/therapeutic-mapping.md` | ICI, ATR inhibitors, nucleoside analogs, neoantigen vaccines, biomarker strategy |
| `references/quick-reference.md` | POLE/POLD1 variant class comparison, mutational signature table, 2013–2026 literature updates |
| `references/references.md` | Stable reference IDs (F1, M1, T2, etc.) used across all files; every row carries a machine-checkable ID |
| `examples/brca1-c68_69del.md` | Second worked example: BRCA1 185delAG, reinitiation to RING-less BRCA1, PARPi resistance |
| `evals/README.md` | Manual eval prompts with expected behaviours and failure modes |
| `scripts/` | Optional stdlib-only Python helpers (HGVS validation, gnomAD, ClinVar, PDB contact census, reference check) |
| `CHANGELOG.md` | Version history |

## What it's for

You have a variant that doesn't fit. Maybe it's a truncation in a gene where only missense variants are supposed to be pathogenic. Maybe the patient's phenotype is too severe for the genotype. Maybe your ACMG criteria give you a VUS but the clinical picture screams pathogenic.

This skill walks Claude through the reasoning: verify the genotype and exclude phenocopies, characterize the variant precisely, generate ranked mechanistic hypotheses, assemble the evidence table, search the literature systematically, and map mechanism to therapeutic strategy. It won't replace a classification committee, but it'll get you to one with a tighter case.

## Setup

You need [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed. If you already have that, there are three ways to load this skill.

### npx (quickest)

```bash
npx skills@latest add bloo-berries/cancer-predisposition-variant-analyst
```

Done. Claude Code picks it up on your next session.

### Manual clone

```bash
git clone git@github.com:bloo-berries/cancer-predisposition-variant-analyst.git ~/.claude/skills/cancer-predisposition-variant-analyst
```

Claude Code auto-discovers skills in `~/.claude/skills/`.

### As part of agent-skills

This skill is also available as a submodule in [DROOdotFOO/agent-skills](https://github.com/DROOdotFOO/agent-skills), which bundles many skills. If you want the full set:

```bash
npx skills@latest add DROOdotFOO/agent-skills
```

## How it loads

Skills are lazy. Claude Code reads the short trigger clause from `SKILL.md` (a ~1 kB trigger clause) at session start. The heavy content -- the mechanistic frameworks, reference tables, and therapeutic mapping -- only loads when your conversation matches the trigger.

The trigger fires when you present a genotype-phenotype paradox, ask about POLE/POLD1 truncation variants in cancer predisposition, need to resolve mechanistic contradictions in multi-domain disease genes, or ask about early-exon truncations where translation reinitiation could yield an N-terminally truncated protein. It stays quiet for routine panel interpretation with no genotype-phenotype conflict, pharmacogenomics, or common variants.

## Using it

Once installed, just start talking to Claude about your variant. If the trigger matches, the skill loads automatically. You can also invoke it directly:

```
I have a germline POLE frameshift at codon 53 in a patient with ultra-hypermutated
colorectal polyposis. Help me work through the mechanistic paradox and assemble
the ACMG evidence.
```

Claude will follow the skill's six-step workflow: verify and exclude phenocopies (Step 0), characterize, hypothesize, classify, search, and map to therapeutics.

The reference IDs (like [M1], [T2], [C2]) that appear in Claude's responses trace back to `references/references.md` -- curated sources with URLs, all verified as of 2026-11-22.

## Maintenance

- Run `python3 scripts/check_refs.py` to check that every reference ID in `references/references.md` still resolves (DOI/PMID/OMIM/NCT/PDB/UniProt/URL), that every table row carries one, and that every `[ID]` cited in the skill files is defined there; add `--strict` to fail on year/first-author mismatches with the Citation column.
- When you re-verify the literature, update `last_verified` in the `SKILL.md` frontmatter and the "verified as of" date above.
- Add a `CHANGELOG.md` entry for every content change (Keep a Changelog format).
- The helper scripts in `scripts/` are optional; the skill works without them. They are stdlib-only Python 3.10+ but need network access (Ensembl, gnomAD, ClinVar, RCSB, publisher URLs). `python3 -m unittest discover -s scripts/tests` runs the offline tests.

## Scope and limits

This is a research tool, not clinical guidance. It won't replace your lab's variant classification pipeline, and it shouldn't.

What it's good at: generating mechanistic hypotheses for paradoxical variants, structuring ACMG evidence for novel findings, identifying the minimum experiment set to collapse a hypothesis space, mapping mechanism to therapeutic strategy, and drafting case report outlines.

What it's not: a diagnostic tool, a substitute for functional studies, or a replacement for expert review. The skill is explicit about uncertainty -- it'll tell you what's unknown and what experiments would resolve it.

## Contributing

Open an issue or PR. The literature moves fast in this space -- if you find a 2026 paper that changes the mechanistic ranking or adds a therapeutic avenue, that's exactly the kind of update we want.

## License

MIT
