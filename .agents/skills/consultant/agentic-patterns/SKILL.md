---
name: agentic-patterns
agent: consultant
user-invocable: true
description: >
  Analyzes multi-agent architectures and recommends orchestration strategies,
  communication patterns, and tool-use designs for agentic AI systems. Provides
  pattern selection guidance backed by current best practices from Google,
  Anthropic, and the broader AI engineering community. Use this skill whenever
  the user asks about designing agent systems, choosing between orchestration
  approaches (sequential, parallel, hierarchical), structuring multi-agent
  communication, implementing tool-use patterns like ReAct or reflection loops,
  or evaluating whether their agentic architecture fits the problem. Also
  trigger when users mention swarm agents, agent coordination, agent
  communication protocols, orchestrator-worker setups, or want to understand
  trade-offs between different multi-agent topologies.
---

# Agentic Patterns

A structured advisory skill for analyzing, selecting, and designing multi-agent architecture patterns. This skill helps the consultant agent provide precise, well-reasoned recommendations when users need guidance on how to structure agentic systems.

## When to Use This Skill

This skill activates when the user's question involves architectural decisions about agentic systems — not just "what is an agent?" conceptual questions, but concrete design choices:

- "How should I structure my agents for this workflow?"
- "Should I use an orchestrator or let agents communicate directly?"
- "What's the best way to coordinate three specialized agents?"
- "My multi-agent system is getting chaotic — how do I redesign it?"
- "Should I use sequential or parallel agent execution here?"

The skill is less useful for single-agent prompt engineering or general LLM usage questions — those are better handled by the consultant's core directives directly.

---

## Analysis Workflow

When analyzing an agentic architecture problem, follow this sequence. The depth of each step should match the complexity of the user's question — a quick "which pattern should I use?" doesn't need a full formal analysis.

### Step 1: Understand the Problem Space

Before recommending patterns, map out the problem:

- **Task decomposition:** Can the work be broken into independent subtasks, or are there sequential dependencies?
- **Agent specialization:** Does the problem benefit from specialized agents, or can a single agent handle it with different tools?
- **Coordination complexity:** How much do agents need to share state, results, or decisions?
- **Failure tolerance:** What happens when one agent fails? Does the whole workflow fail, or can others compensate?
- **Latency requirements:** Does the user need real-time responses, or is batch processing acceptable?
- **Scale:** How many agents are involved? Two agents coordinate differently than twenty.

If the user hasn't provided enough context, ask targeted follow-up questions rather than guessing. A wrong pattern recommendation is worse than taking a moment to clarify.

### Step 2: Pattern Selection

Based on the problem analysis, recommend from the pattern catalog. Read `references/pattern-catalog.md` for the full catalog — it contains detailed descriptions, trade-offs, and selection criteria for each pattern.

The key principle: **start simple, add complexity only when the problem demands it.** Many problems that seem to need complex multi-agent orchestration are actually better served by a single well-designed agent with good tool access.

The patterns fall into three categories:

#### Orchestration Patterns
How agents are organized and who controls the workflow.

| Pattern | Best For |
|---|---|
| Sequential Pipeline | Linear workflows where each step depends on the previous |
| Coordinator/Dispatcher | Central routing of tasks to specialized agents |
| Parallel Fan-Out/Gather | Independent subtasks that can run simultaneously |
| Hierarchical Decomposition | Complex goals that need recursive breakdown |
| Generator-Critic | Iterative refinement through creation and validation loops |

#### Communication Patterns
How agents exchange information and coordinate.

| Pattern | Best For |
|---|---|
| Direct Request-Response | Simple, few agents, stable interfaces |
| Orchestrator-Mediated | Business automation, centralized control |
| Publish-Subscribe | Event-driven, loose coupling, multiple consumers |
| Blackboard | Shared knowledge space, collaborative problem-solving |
| Swarm/Handoff | Dynamic expertise routing, conversation continuity |

#### Tool-Use Patterns
How individual agents interact with tools and validate their work.

| Pattern | Best For |
|---|---|
| ReAct (Reason + Act) | Step-by-step reasoning with tool calls between steps |
| Reflection Loop | Self-review and iterative refinement of output |
| Tool Chaining | Multi-step tool sequences for complex operations |
| Parallel Tool Execution | Independent tool calls that can run simultaneously |
| Fallback Cascade | Graceful degradation through alternative tool strategies |

### Step 3: Architecture Recommendation

Present your recommendation as a concrete architecture, not just an abstract pattern name. Include:

1. **Pattern selection** — which pattern(s) you recommend and why this pattern fits their specific problem
2. **Agent roles** — what each agent does, its scope, and what tools it needs
3. **Communication flow** — how data moves between agents (use Mermaid diagrams for complex flows)
4. **Failure handling** — what happens when things go wrong
5. **Trade-offs acknowledged** — what you sacrifice with this approach and when a different pattern would be better

### Step 4: Implementation Guidance

If the user wants to move from design to implementation, provide concrete guidance specific to their ecosystem:

- **Antigravity IDE:** How to structure the `.agents/` directory, write agent definitions, and configure workflows
- **Code-based frameworks:** How to implement the pattern using tools like LangChain, AutoGen, or Google's Agent Development Kit
- **Hybrid approaches:** Combining IDE-managed agents with programmatic orchestration

---

## Anti-Patterns to Watch For

When analyzing existing architectures, actively look for common anti-patterns:

- **The God Agent:** One agent trying to do everything — loses focus and accuracy. Break it into specialists.
- **Over-Orchestration:** Adding coordination layers where a simpler sequential flow would work. Complexity has costs.
- **Silent Failures:** Agents that fail without reporting back, leaving the system in an inconsistent state.
- **Circular Dependencies:** Agent A needs Agent B's output, which needs Agent A's output. Restructure the dependency graph.
- **Premature Parallelism:** Running agents in parallel when there are hidden dependencies between their outputs.
- **Chatty Agents:** Too much inter-agent communication that wastes tokens and increases latency. Agents should communicate results, not thinking process.

---

## Maturity Classification

When recommending patterns, always classify them by maturity level to set correct expectations:

| Level | Description | Example |
|---|---|---|
| **Established** | Battle-tested, widely documented, predictable behavior | Sequential Pipeline, Request-Response |
| **Emerging** | Gaining adoption, good results reported, some rough edges | Swarm Handoff, Hierarchical Decomposition with LLMs |
| **Experimental** | Promising concept, limited real-world validation | Fully autonomous agent negotiation, self-organizing swarms |

---

## Reference Material

For detailed pattern descriptions, trade-off analysis, and implementation examples, read:

- `references/pattern-catalog.md` — Comprehensive catalog of all patterns with selection criteria, examples, and decision trees

---

## Response Template

When providing pattern recommendations, structure your response to be scannable and actionable:

```
## Recommended Architecture: [Pattern Name]

### Why This Pattern
[1-2 sentences connecting the pattern to the user's specific problem]

### Architecture Overview
[Mermaid diagram or concise description of the agent topology]

### Agent Roles
- **Agent A (role):** [what it does, tools it needs]
- **Agent B (role):** [what it does, tools it needs]

### Trade-Offs
- ✅ [Advantage of this approach]
- ⚠️ [What you sacrifice or need to watch for]

### Alternative Considered
[Brief mention of the runner-up pattern and why you chose the recommended one instead]
```

This structure isn't rigid — adapt it to the complexity of the question. Simple questions get simple answers.
