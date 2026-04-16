---
impact: LOW
impactDescription: "Standalone repo README with setup instructions and overview -- not loaded by Claude Code"
tags: "readme,setup,overview"
---

# Cancer Predisposition Variant Analyst

A Claude Code skill for interpreting ultra-rare variants in cancer predisposition genes -- specifically the cases where the genotype shouldn't produce the phenotype you're looking at, but it does anyway.

The worked example throughout is a POLE frameshift at ~residue 54 that eliminates every functional domain yet produces classical ultra-hypermutated PPAP. Current consensus says this shouldn't happen. The PolED database (2025) is explicit: "Loss-of-function variants cannot cause ultramutated cancers." And yet.

That paradox -- and the reasoning framework for resolving it -- is what this skill encodes.

## What's in here

| File | What it does |
|------|-------------|
| `SKILL.md` | Entry point. Trigger clauses, workflow, quick reference table, literature changelog |
| `variant-interpretation.md` | Molecular characterization, NMD prediction, ACMG/ClinGen criteria, LOP classification |
| `mechanistic-framework.md` | Five ranked hypotheses for the paradox, discriminating experiments, decision tree |
| `literature-protocol.md` | Structured search strategy, evidence grading, gap analysis template |
| `therapeutic-mapping.md` | ICI, ATR inhibitors, nucleoside analogs, neoantigen vaccines, biomarker strategy |
| `references.md` | 72 references with stable IDs (F1, M1, T2, etc.) used across all files |

## What it's for

You have a variant that doesn't fit. Maybe it's a truncation in a gene where only missense variants are supposed to be pathogenic. Maybe the patient's phenotype is too severe for the genotype. Maybe your ACMG criteria give you a VUS but the clinical picture screams pathogenic.

This skill walks Claude through the reasoning: characterize the variant precisely, generate ranked mechanistic hypotheses, assemble the evidence table, search the literature systematically, and map mechanism to therapeutic strategy. It won't replace a classification committee, but it'll get you to one with a tighter case.

## Setup

You need [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed. If you already have that, there are three ways to load this skill.

### npx (quickest)

```bash
npx skills@latest add Bloomed-Health/cancer-predisposition-variant-analyst
```

Done. Claude Code picks it up on your next session.

### Manual clone

```bash
git clone git@github.com:Bloomed-Health/cancer-predisposition-variant-analyst.git ~/.claude/skills/cancer-predisposition-variant-analyst
```

Claude Code auto-discovers skills in `~/.claude/skills/`.

### As part of agent-skills

This skill is also available as a submodule in [DROOdotFOO/agent-skills](https://github.com/DROOdotFOO/agent-skills), which bundles 53 skills. If you want the full set:

```bash
npx skills@latest add DROOdotFOO/agent-skills
```

## How it loads

Skills are lazy. Claude Code reads the short trigger clause from `SKILL.md` (a few lines) at session start. The heavy content -- the 1,300+ lines of mechanistic frameworks, reference tables, and therapeutic mapping -- only loads when your conversation matches the trigger.

The trigger fires when you present a genotype-phenotype paradox, ask about POLE/POLD1 truncation variants in cancer predisposition, or need to resolve mechanistic contradictions in multi-domain disease genes. It stays quiet for routine panel interpretation, pharmacogenomics, or common variants.

## Using it

Once installed, just start talking to Claude about your variant. If the trigger matches, the skill loads automatically. You can also invoke it directly:

```
I have a POLE frameshift variant at position X in a patient with ultra-hypermutated
colorectal polyposis. Help me work through the mechanistic paradox and assemble
the ACMG evidence.
```

Claude will follow the skill's five-step workflow: characterize, hypothesize, classify, search, and map to therapeutics.

The reference IDs (like [M1], [T2], [C2]) that appear in Claude's responses trace back to `references.md` -- 72 curated sources with URLs, all verified as of April 2026.

## Scope and limits

This is a research tool, not clinical guidance. It won't replace your lab's variant classification pipeline, and it shouldn't.

What it's good at: generating mechanistic hypotheses for paradoxical variants, structuring ACMG evidence for novel findings, identifying the minimum experiment set to collapse a hypothesis space, mapping mechanism to therapeutic strategy, and drafting case report outlines.

What it's not: a diagnostic tool, a substitute for functional studies, or a replacement for expert review. The skill is explicit about uncertainty -- it'll tell you what's unknown and what experiments would resolve it.

## Contributing

Open an issue or PR. The literature moves fast in this space -- if you find a 2026 paper that changes the mechanistic ranking or adds a therapeutic avenue, that's exactly the kind of update we want.

## License

MIT
