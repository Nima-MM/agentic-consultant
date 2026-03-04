---
name: consult-architecture-review
agent: consultant
user-invocable: true
description: >
  Reviews system designs, project structures, and technical decisions against
  current best practices. Provides structured findings with severity ratings
  and concrete improvement recommendations. Trigger when the user asks for an
  architecture review, structural audit, tech-stack assessment, or design
  evaluation of a codebase or system.
---

# Architecture Review Advisory

## Reference Materials

Load this document before conducting a review:

- **Review Framework** — `.agents/skills/skills-consultant/ressources/consult-architecture-review/references/review-framework.md`
  Six standard review dimensions + Dimension 7 (Agentic Systems), severity system, anti-pattern catalog, and the output template.

---

## Advisory Workflow

### Step 0: Automated Discovery (Run First)

Before any manual analysis, run the discovery script to collect a structured
project snapshot. This replaces the first round of manual Glob/Grep/Read calls:

```bash
bash .agents/skills/skills-consultant/ressources/consult-architecture-review/scripts/architecture-discovery.sh <project-root>
```

Use the snapshot output to:

- Identify which review dimensions are most relevant given the tech stack.
- Pre-populate tech debt counts, CI/CD presence, and test file signals.
- Detect if this is an Antigravity IDE project (`.agents/` exists) →
  Dimension 7 (Agent Architecture Quality) becomes mandatory in that case.

### Step 1: Scope & Dimensions

Based on the discovery snapshot and the user's stated concern, select the
most relevant dimensions from the review framework. Do not force a full
6+1 dimension review when the user has a specific concern — start focused,
expand if needed.

### Step 2: Systematic Review

Apply each selected dimension using the framework's investigation heuristics.
Ground every finding in specific files, patterns, or counts — never assume.
Assign a severity rating (🔴 Critical / 🟠 High / 🟡 Medium / 🔵 Low).

### Step 3: Deliver Findings

Structure the output using the Output Template from the review framework.
For the Architecture Scorecard, use the scorecard generator for a structured
and reproducible output:

```bash
python3 .agents/skills/skills-consultant/ressources/consult-architecture-review/scripts/generate_scorecard.py \
  --project "<Project Name>" \
  --reviewer "Consultant Agent" \
  --summary "<2-3 sentence executive summary>" \
  --scores \
    "Structural Integrity:<1-5>:<brief note>" \
    "Dependency Health:<1-5>:<brief note>" \
    "Scalability & Performance:<1-5>:<brief note>" \
    "Maintainability & Evolvability:<1-5>:<brief note>" \
    "Security Posture:<1-5>:<brief note>" \
    "Operational Readiness:<1-5>:<brief note>" \
    "Agent Architecture Quality:<1-5>:<brief note>" \
  --next-steps \
    "<Prioritized action 1>" \
    "<Prioritized action 2>" \
    "<Prioritized action 3>"
```

Select and prioritize review dimensions based on the user's context — not
every review needs all dimensions. Start with the dimensions most relevant to
the user's concern, then expand if time permits.
