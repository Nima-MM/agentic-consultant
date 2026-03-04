# Antigravity Implementation Mapping

Translates abstract multi-agent patterns into concrete Antigravity IDE primitives.
Use this document alongside `pattern-catalog.md` to bridge the gap between
*what pattern to use* and *how to actually build it*.

---

## Antigravity Primitives Glossary

Before mapping patterns, understand the three building blocks:

| Primitive | File Location | Purpose | Analogy |
| --- | --- | --- | --- |
| **Agent** | `.agents/agents/<domain>/<name>.md` | A specialized AI persona with scoped tools and a master routing skill | The "worker" with a job description |
| **Skill** | `.agents/skills/<skill-name>/SKILL.md` | A capability module an agent loads on demand | The "manual" the worker reads |
| **Workflow** | `.agents/workflows/<name>.md` | A multi-step orchestration script chaining agents and skills | The "process playbook" |

---

## Pattern → Primitive Mapping

### Coordinator/Dispatcher

```text
Pattern Role       → Antigravity Primitive
────────────────────────────────────────────
Coordinator        → Agent with Master Router Skill
                     (loads one of N specialist skills based on query type)
Specialist A       → Skill module (e.g., ressources/consult-agentic-patterns/)
Specialist B       → Skill module (e.g., ressources/consult-architecture-review/)
Routing Logic      → Master Router SKILL.md decision rules
```

**This project's live example:**

```text
consultant agent  ←→  skills-consultant (Master Router)
                        ├── consult-agentic-patterns/SKILL.md
                        ├── consult-architecture-review/SKILL.md
                        ├── consult-toolchain-compare/SKILL.md  (pending)
                        └── consult-workflow-optimizer/SKILL.md (pending)
```

**Blueprint for a new Coordinator:**

```text
.agents/
├── agents/<domain>/<coordinator-name>.md     # Agent definition
│     name: <coordinator>
│     tools: [Read, skills-<coordinator>]
└── skills/
    └── skills-<coordinator>/
        ├── SKILL.md                          # Master Router
        └── ressources/
            ├── <specialist-a>/SKILL.md
            ├── <specialist-b>/SKILL.md
            └── <specialist-c>/SKILL.md
```

---

### Sequential Pipeline

```text
Pattern Role       → Antigravity Primitive
────────────────────────────────────────────
Pipeline Stage N   → Workflow step N
Stage Output       → Shared artifact / temp file passed to next step
Stage Agent        → Agent invoked per step (or re-used with new context)
Pipeline Runner    → Workflow .md file
```

**Blueprint:**

```markdown
# Workflow: <Pipeline Name>

## Step 1: <Stage A>
Agent: <agent-name>
Skill: <skill-a>
Output: writes to `.tmp/stage-a-output.md`

## Step 2: <Stage B>
Agent: <agent-name>
Skill: <skill-b>
Input: reads `.tmp/stage-a-output.md`
Output: writes to `.tmp/stage-b-output.md`

## Step 3: <Stage C>
...
```

---

### Parallel Fan-Out / Gather

```text
Pattern Role       → Antigravity Primitive
────────────────────────────────────────────
Fan-Out            → Agent fires multiple tool calls simultaneously
Independent Tasks  → Parallel Glob/Read/search_web calls in one agent turn
Gather             → Agent synthesizes results from all parallel outputs
Coordinator        → Single agent capable of parallel tool execution
```

**Note:** In the Antigravity IDE, a single agent can fire multiple tool calls
in the same turn (parallel execution). No separate "gathering agent" is needed
for simple cases — the same agent collects all results and synthesizes.

**When you DO need a separate gatherer:** When each "branch" requires deep
reasoning that would overflow context in a single agent. Then split into:

```text
.agents/
├── agents/<domain>/fan-out-agent.md    # Dispatches to specialists
├── agents/<domain>/specialist-a.md    # Deep analysis, branch A
├── agents/<domain>/specialist-b.md    # Deep analysis, branch B
└── agents/<domain>/gather-agent.md    # Synthesizes outputs
```

---

### Generator-Critic (Iterative Refinement)

```text
Pattern Role       → Antigravity Primitive
────────────────────────────────────────────
Generator          → Agent with Write tool (creates the artifact)
Critic             → Agent with Read + review skill (evaluates artifact)
Feedback Loop      → Workflow orchestrates: generate → review → revise
Convergence Check  → Workflow condition or manual approval step
```

**Blueprint:**

```text
.agents/
├── agents/<domain>/generator.md           # Creates output
├── agents/<domain>/critic.md              # Reviews output
└── workflows/
    └── refine-<artifact>.md               # The loop workflow

# Workflow: refine-<artifact>.md
## Step 1: Generate
Agent: generator — produces initial draft to `.tmp/draft.md`

## Step 2: Critique
Agent: critic — reads `.tmp/draft.md`, scores quality, writes `.tmp/critique.md`

## Step 3: Revise (conditional)
IF critique score < threshold:
  Agent: generator — reads `.tmp/critique.md`, revises `.tmp/draft.md`
  GOTO Step 2
ELSE:
  Output `.tmp/draft.md` as final artifact
```

**This project's live example:** The `skills-skill-architect` eval flow — the
skill generates output, eval scripts score it, agent revises based on scores.

---

### Hierarchical Decomposition

```text
Pattern Role       → Antigravity Primitive
────────────────────────────────────────────
Goal Agent         → Orchestrator agent (broad tools, high model tier)
Sub-agents         → Specialist agents per sub-domain
Decomposition      → Workflow step where Goal Agent creates task list
Subtask Execution  → Workflow delegates each task to the appropriate specialist
```

**Blueprint:**

```text
.agents/
├── agents/<domain>/orchestrator.md    # Breaks goal into subtasks
├── agents/<domain>/specialist-a.md   # Handles subtask type A
├── agents/<domain>/specialist-b.md   # Handles subtask type B
└── workflows/
    └── hierarchical-<goal>.md        # Top-level orchestration
```

---

### Swarm / Handoff

```text
Pattern Role       → Antigravity Primitive
────────────────────────────────────────────
Active Agent       → Current agent handling the conversation
Handoff Trigger    → Agent identifies topic is outside its scope
Handoff Mechanism  → Agent explicitly tells user: "For X, invoke @agent-Y"
Context Transfer   → Agent summarizes state before handing off
```

**Antigravity-specific note:** The IDE does not support automated agent-to-agent
handoff at runtime. The current pattern is **explicit recommendation handoff**:
the active agent writes a handoff summary and recommends which agent the user
should invoke next, with relevant context included.

---

## Model Tier Mapping

Pattern complexity should drive model tier selection:

| Pattern | Recommended Tier | Rationale |
| --- | --- | --- |
| Sequential Pipeline (simple stages) | Balanced | Each stage is focused and low-complexity |
| Coordinator/Dispatcher (routing) | Turbo/Flash | Routing decisions are fast classification tasks |
| Coordinator/Dispatcher (aggregation) | High | Synthesis requires deeper reasoning |
| Parallel Fan-Out/Gather | Balanced per branch | Each branch is scoped |
| Hierarchical Decomposition | High (top level) | Complex goal analysis requires best judgment |
| Generator-Critic | Balanced (gen) + High (critic) | Critics need to catch subtle quality issues |
| Swarm/Handoff | Balanced | Context transfer is a summarization task |

---

## Anti-Patterns in Antigravity Implementations

| Anti-Pattern | Symptom | Fix |
| --- | --- | --- |
| **Monolithic Agent** | One agent with 10+ tools and no routing skill | Split into Coordinator + Specialists |
| **Skill Flooding** | Master Router loads all specialist docs regardless of query | Strict "load exactly one" routing rules |
| **Missing HitL Gates** | Generator-Critic loop runs indefinitely without user approval | Add explicit convergence condition or max-iteration cap |
| **Context Bleed** | Sequential Pipeline passes entire previous output as next input | Use structured artifact formats with clear field contracts |
| **Phantom Coordinator** | A "coordinator" that always routes to the same specialist | Eliminate coordinator — invoke specialist directly |
| **Orphaned Specialists** | Skills/agents referenced in the router but never implemented | Mark as `(Pending)` in router until fully built |
