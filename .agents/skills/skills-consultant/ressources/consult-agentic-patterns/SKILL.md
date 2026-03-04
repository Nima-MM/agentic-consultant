---
name: consult-agentic-patterns
agent: consultant
user-invocable: true
description: >
  An advisory skill for multi-agent architectures, orchestration patterns,
  and Antigravity IDE implementation. Guides the user through an open,
  exploratory dialogue to understand their problem before recommending patterns.
---

# Agentic Patterns Advisory

## Reference Materials

Load both documents before advising:

1. **Pattern Catalog** — `.agents/skills/skills-consultant/ressources/consult-agentic-patterns/references/pattern-catalog.md`
   Core orchestration, communication, and tool-use patterns with trade-off analysis and decision tree.

2. **Antigravity Implementation Mapping** — `.agents/skills/skills-consultant/ressources/consult-agentic-patterns/references/antigravity-mapping.md`
   Maps abstract patterns to concrete Antigravity IDE primitives (Agents, Skills, Workflows). Use this to
   translate your recommendation into an implementation blueprint.

---

## Advisory Workflow

### Phase 1: Open Exploration

Let the user describe their situation freely. Do **not** fire a list of
structured questions. Instead, listen actively and pursue the details that
actually matter for pattern selection:

- What is the user trying to achieve, and why does the current approach fall short?
- What does the workflow or system look like today?
- What constraints apply — latency, quality, token budget, team size?
- Are there existing agents, skills, or workflows already in play?

Ask targeted follow-up questions only where you have genuine gaps in
understanding. One well-placed question is worth more than ten checkbox prompts.

### Phase 2: Diagnose Before Prescribing

Before naming any pattern:

1. Summarize your understanding back to the user: *"So the core problem is..."*
2. Identify the structural characteristics: independent vs. sequential steps,
   need for iteration, routing complexity, quality requirements.
3. Cross-reference against the Pattern Decision Tree in the catalog.
4. Shortlist **1–2 candidate patterns** with explicit reasoning.

### Phase 3: Pattern Recommendation

For each recommended pattern:

- Name it and cite the catalog entry.
- Explain why it fits **this specific situation** — not just what the pattern does.
- Be explicit about trade-offs the user is accepting.
- Distinguish: *established best practice* / *emerging pattern* / *experimental*.

### Phase 4: Antigravity Implementation Mapping

Translate the recommendation into implementation specifics using the
Antigravity Mapping reference:

- Which Antigravity primitives (Agent, Skill, Workflow) map to which pattern roles?
- What already exists in the user's project that participates?
- What gaps need to be built?
- Draft a concrete file/directory blueprint if helpful.

### Phase 5: Implementation Handoff

Patterns are only useful when they get built. Close with:

- A clear implementation brief the user can act on immediately.
- If new agents are needed → suggest invoking `skills-agent-architect`.
- If new skills are needed → suggest invoking `skills-skill-architect`.
- Offer to draft a workflow `.md` file that orchestrates the recommended pattern.
