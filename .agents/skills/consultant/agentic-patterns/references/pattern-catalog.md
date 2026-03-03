# Agentic Pattern Catalog

A comprehensive reference for multi-agent architecture patterns. Each pattern includes a description, when to use it, trade-offs, and concrete examples.

## Table of Contents

1. [Orchestration Patterns](#orchestration-patterns)
   - Sequential Pipeline
   - Coordinator/Dispatcher
   - Parallel Fan-Out/Gather
   - Hierarchical Decomposition
   - Generator-Critic (Iterative Refinement)
2. [Communication Patterns](#communication-patterns)
   - Direct Request-Response
   - Orchestrator-Mediated
   - Publish-Subscribe
   - Blackboard Architecture
   - Swarm/Handoff
3. [Tool-Use Patterns](#tool-use-patterns)
   - ReAct (Reason + Act)
   - Reflection Loop
   - Tool Chaining
   - Parallel Tool Execution
   - Fallback Cascade
4. [Pattern Decision Tree](#pattern-decision-tree)
5. [Composing Patterns](#composing-patterns)

---

## Orchestration Patterns

### Sequential Pipeline

Agents are arranged in a linear chain — each agent processes its input and passes its output to the next agent. Like an assembly line.

```
Agent A → Agent B → Agent C → Final Output
```

**When to use:**
- The workflow has clear, ordered stages (e.g., extract → transform → validate → format)
- Each stage's output is the next stage's input
- The stages are conceptually different enough to warrant separate agents

**When NOT to use:**
- Stages can run independently (use Parallel Fan-Out instead)
- The number of stages is dynamic or unknown upfront
- You need feedback loops between stages

**Trade-offs:**
- ✅ Simple to understand, debug, and maintain
- ✅ Easy to swap out individual agents without affecting others
- ⚠️ Latency is the sum of all stages — no parallelism
- ⚠️ A failure in any stage blocks the entire pipeline

**Antigravity IDE Example:**
```
Workflow: Code Review Pipeline
1. code-scanner agent → finds files matching criteria
2. security-analyzer agent → checks for vulnerabilities
3. style-checker agent → validates coding conventions
4. report-generator agent → produces final review document
```

---

### Coordinator/Dispatcher

A central coordinator agent receives tasks, decides which specialized agent should handle each one, and routes accordingly. The coordinator may also aggregate results.

```
         ┌→ Specialist A →┐
Input → Coordinator → Specialist B → Coordinator → Output
         └→ Specialist C →┘
```

**When to use:**
- You have multiple specialized agents and need intelligent routing
- The right agent for each task isn't known until runtime
- You want a single entry point for diverse request types

**When NOT to use:**
- Routing logic is trivial (a simple if-else would work)
- All tasks go to the same agent anyway
- The coordinator becomes a bottleneck at scale

**Trade-offs:**
- ✅ Clean separation of concerns — agents are fully independent
- ✅ Easy to add new specialists without changing the workflow
- ⚠️ The coordinator needs to be "smart enough" to route correctly
- ⚠️ Single point of failure if the coordinator agent fails

**Antigravity IDE Example:**
```
Agent: consultant (coordinator)
├── Routes architecture questions → to agentic-patterns skill
├── Routes debugging issues → to debug-strategy skill
├── Routes tool comparisons → to toolchain-compare skill
└── Routes workflow questions → to workflow-optimizer skill
```

---

### Parallel Fan-Out/Gather

Multiple agents work on independent subtasks simultaneously. A gathering step synthesizes their outputs into a unified result.

```
         ┌→ Agent A →┐
Input → Fan-Out → Agent B → Gather → Output
         └→ Agent C →┘
```

**When to use:**
- Subtasks are genuinely independent (no shared state or dependencies)
- Latency matters and parallel execution reduces total time
- Different perspectives or analyses need to be consolidated

**When NOT to use:**
- Subtasks depend on each other's results
- The gathering step is trivially simple (just concatenation — then why separate agents?)
- Running N agents costs N times the tokens and you're budget-constrained

**Trade-offs:**
- ✅ Significant latency reduction
- ✅ Each agent has a focused, simplified task
- ⚠️ Gathering step needs to handle conflicting or overlapping outputs
- ⚠️ Total token/compute cost scales linearly with parallelism

---

### Hierarchical Decomposition

A high-level agent breaks a complex goal into subgoals, delegates each to subordinate agents, and those agents may further decompose if needed. Recursive tree structure.

```
         Goal Agent
        /     |     \
   Sub-A   Sub-B   Sub-C
   / \       |
 S-A1 S-A2  S-B1
```

**When to use:**
- The problem is too complex for a single agent to handle in one pass
- Natural hierarchical structure exists (chapters of a document, modules of a system)
- You need different levels of abstraction (strategic vs. tactical decisions)

**When NOT to use:**
- The decomposition depth is unpredictable (risk of infinite recursion)
- Subtasks have heavy cross-dependencies (the tree becomes a graph)
- You don't have strong enough models to do reliable decomposition

**Trade-offs:**
- ✅ Handles very complex, multi-layered tasks
- ✅ Each agent operates at an appropriate abstraction level
- ⚠️ Coordination overhead grows with depth
- ⚠️ Decomposition quality depends heavily on the top-level agent's judgment
- ⚠️ Hard to debug when failures cascade through the tree

---

### Generator-Critic (Iterative Refinement)

One agent generates output, another evaluates it and provides feedback. The generator revises based on the critique. This cycles until quality thresholds are met.

```
Generator → Output → Critic → Feedback ─┐
    ↑                                     │
    └─────────────────────────────────────┘
```

**When to use:**
- Output quality is critical and hard to get right on the first pass
- You have clear evaluation criteria that a critic agent can assess
- The task benefits from iterative polishing (writing, code, design)

**When NOT to use:**
- You don't have well-defined quality criteria
- The generator rarely makes mistakes (wasted cycles)
- Tight latency constraints — each cycle adds time

**Trade-offs:**
- ✅ Significantly improves output quality through iteration
- ✅ Separates creation from evaluation — reduces bias
- ⚠️ Risk of infinite loops if convergence criteria are weak
- ⚠️ Each iteration doubles the token cost approximately
- ⚠️ The critic needs to be at least as capable as the generator for meaningful feedback

---

## Communication Patterns

### Direct Request-Response

The simplest pattern: Agent A directly asks Agent B a question, Agent B responds. No middleware, no coordinator.

**When to use:** 2-3 agents, stable interfaces, clear responsibility boundaries. Often sufficient for straightforward hand-offs between a planner and an executor.

**Trade-offs:**
- ✅ Minimal overhead, easy to implement
- ⚠️ Doesn't scale — becomes spaghetti with many agents
- ⚠️ Tight coupling between agents

---

### Orchestrator-Mediated

All inter-agent communication flows through a central orchestrator. Agents never talk directly to each other — they report results to the orchestrator, which decides next steps.

**When to use:** Business automation workflows, situations requiring audit trails, when you need centralized error handling and recovery.

**Trade-offs:**
- ✅ Full visibility and control — easy to log, monitor, and debug
- ✅ Agents are fully decoupled from each other
- ⚠️ Orchestrator can become a bottleneck
- ⚠️ Single point of failure

---

### Publish-Subscribe (Pub-Sub)

Agents publish events/results to topics. Other agents subscribe to topics they care about. A message queue handles delivery. No direct coupling between producers and consumers.

**When to use:** Event-driven systems, when multiple agents need to react to the same event, when agents are added/removed dynamically.

**Trade-offs:**
- ✅ Extremely loose coupling — agents don't know about each other
- ✅ Easy to add new consumers without changing producers
- ⚠️ Debugging is harder — message flow is implicit
- ⚠️ Requires message queue infrastructure
- ⚠️ Ordering guarantees can be tricky

---

### Blackboard Architecture

A shared knowledge space (the "blackboard") that all agents can read from and write to. Agents watch the blackboard for relevant changes and contribute when they can.

**When to use:** Collaborative problem-solving where agents contribute different kinds of knowledge, ill-structured problems where the solution path isn't predefined.

**Trade-offs:**
- ✅ Flexible — agents contribute when they have something useful
- ✅ Good for problems where the solution emerges from combining perspectives
- ⚠️ Race conditions if write access isn't managed
- ⚠️ Can become chaotic without clear conventions for what goes on the board

---

### Swarm/Handoff

Specialized agents dynamically pass control to each other based on expertise. The active agent maintains conversation context and transfers it when handing off. No central coordinator — routing emerges from agent capabilities.

**When to use:** Conversational systems where different topics require different expertise, customer support scenarios, situations where the "right" agent depends on evolving context.

**Trade-offs:**
- ✅ Natural, conversation-like flow
- ✅ Each user interaction is handled by the most qualified agent
- ⚠️ Context transfer between agents can be lossy
- ⚠️ "Ping-pong" risk if agents can't decide who should handle a request

---

## Tool-Use Patterns

### ReAct (Reason + Act)

The agent alternates between thinking (reasoning about the problem) and acting (calling a tool). After each tool call, the agent reasons about the result before deciding the next action.

```
Think → Act → Observe → Think → Act → Observe → ...→ Answer
```

**When to use:** Multi-step information gathering, complex research tasks, problems where the next step depends on previous results.

**Key principle:** The reasoning step between actions prevents the agent from blindly chaining tool calls. It forces re-evaluation after each observation.

---

### Reflection Loop

After generating an output, the agent reviews its own work, identifies flaws or improvements, and revises. This can be self-reflection (same agent) or external reflection (different critic agent — see Generator-Critic above).

**When to use:** Tasks where accuracy matters more than speed, code generation that needs validation, content that should be polished before delivery.

---

### Tool Chaining

Multiple tools are called in sequence where each tool's output feeds into the next tool's input. The agent orchestrates the chain but the data flows through tools.

```
Tool A output → Tool B input → Tool C input → Final result
```

**When to use:** Data transformation pipelines, multi-step processing (parse file → extract data → transform → validate).

---

### Parallel Tool Execution

Multiple independent tool calls fired simultaneously to reduce latency. Results are gathered and synthesized by the agent.

**When to use:** When gathering information from multiple independent sources, running multiple analyses that don't depend on each other.

---

### Fallback Cascade

A primary tool is attempted first. If it fails (error, timeout, unsatisfactory result), the agent falls back to alternative tools in a predefined priority order.

```
Try Tool A → Failed → Try Tool B → Failed → Try Tool C → Succeed
```

**When to use:** Unreliable external services, varying input types where different tools work for different cases, situations where graceful degradation beats hard failure.

---

## Pattern Decision Tree

Use this decision tree as a starting point for pattern selection. The questions guide you toward the right pattern based on the problem characteristics.

```
Is the task decomposable into steps?
├── Yes: Are the steps independent?
│   ├── Yes → Parallel Fan-Out/Gather
│   └── No → Sequential Pipeline
└── No: Is it a single complex task?
    ├── Yes: Does it need iterative polishing?
    │   ├── Yes → Generator-Critic
    │   └── No: Does it need multiple perspectives?
    │       ├── Yes → Parallel Fan-Out/Gather
    │       └── No → Single Agent (no multi-agent needed)
    └── No: Is there request routing involved?
        ├── Yes → Coordinator/Dispatcher
        └── No: Is the goal structure hierarchical?
            ├── Yes → Hierarchical Decomposition
            └── No → Evaluate if multi-agent is even necessary
```

**Important:** This tree is a heuristic, not a rule. Real problems often combine patterns. For example, a Hierarchical Decomposition where leaf nodes use Generator-Critic loops, all communicated through an Orchestrator-Mediated pattern.

---

## Composing Patterns

Most production multi-agent systems combine multiple patterns. Here are common compositions:

### Coordinator + Parallel Fan-Out
A coordinator dispatches tasks to specialists, some of which run in parallel. This combines intelligent routing with latency optimization.

### Hierarchical + Generator-Critic
High-level decomposition with iterative refinement at the leaf level. The hierarchy handles complexity; the critic loops handle quality.

### Sequential Pipeline + Fallback Cascade
A linear workflow where each stage has fallback strategies. This combines predictability with resilience.

### ReAct + Reflection
An agent that reasons and acts (ReAct) but also periodically reflects on its overall progress. This catches situations where the agent is going in circles or pursuing a dead-end strategy.

---

## Key Design Principles

1. **Start with one agent.** Add more only when a single agent demonstrably can't handle the task. Multi-agent coordination has real costs — token overhead, latency, debugging complexity.

2. **Define boundaries by capability, not by task.** An agent's scope should match what a single model invocation can handle well. If an agent needs too many tools or too much context, split it.

3. **Make failure visible.** Every agent should report what it tried, what worked, and what failed. Silent failures in multi-agent systems are catastrophic for debugging.

4. **Measure before optimizing.** Don't add parallelism, caching, or complex orchestration until you've measured where the actual bottlenecks are.

5. **Design for replacement.** Every agent should be swappable. If replacing one agent requires rewriting the whole system, the coupling is too tight.
