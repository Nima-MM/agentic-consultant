---
name: skills-consultant
agent: consultant
user-invocable: true
description: >
  CENTRAL ADVISORY SKILL: Always trigger this skill when the user asks for
  architectural advice, system design patterns, debugging strategies, workflow
  optimizations, or toolchain comparisons.
---

# Consultant Skills (Master Router)

You are analyzing the user's technical query. Depending on the specific topic the user requests, load **exactly one** of the following reference documents from the `@[ressources](.agents/skills/skills-consultant/ressources/)` directory.

## Available Skill-Modules (References)
 The following skills extend this agent's advisory capabilities for specialized domains. They can be invoked when a particular type of guidance is needed:

1. **Agentic Patterns** (@[`.agents/skills/skills-consultant/ressources/consult-agentic-patterns/SKILL.md`])
   Read this file when you need to understand core multi-agent patterns and orchestration strategies recommendation, communication patterns, and tool-use designs for agentic systems (like Coordinator, Swarm, Pipeline) to design a new agent layout.

2. **Toolchain Compare** (Pending implementation)
   Compares AI development tools (Antigravity, Gemini CLI, Claude Code, Cursor, etc.) for a specific use case and recommends the optimal choice with trade-off analysis.

3. **Debug Strategy** (Pending implementation)
   Guides systematic debugging of complex issues across AI-assisted workflows, including prompt failures, tool misconfigurations, and integration problems.

4. **Architecture Review** (@[`.agents/skills/skills-consultant/ressources/consult-architecture-review/SKILL.md`])
   Read this file when you need to review system designs, project structures, and technical decisions against current best practices. Provides a structured review framework with severity ratings, an anti-pattern catalog, and concrete improvement recommendations.

5. **Workflow Optimizer** (Pending implementation)
   Analyzes existing development workflows and proposes optimizations based on available AI tooling, automation opportunities, and efficiency gains.

## Your Workflow:

1. Determine the appropriate module from the list above based on the user's request.
2. Use your `Read` tool to open the exact file path provided above.
3. Advise/help the user based on this shared expert knowledge of yours.
