# Project: Agentic-Consultant

> **Status:** 🚧 In Development | Version: 0.1.0-alpha | Date: March 2026

---

## 1. Project Goal

The **Agentic-Consultant** is a highly specialized, agent-based system designed to automate, support, and optimize daily workflows. The objective is to delegate repetitive tasks, enable context-aware operations, and support data-driven decision making through the targeted use of AI agents, skills, and workflows.

**Core Use Cases & Success Criteria:**
* **Automated Daily Planning:** Compiling daily priorities, calendar events, and open tasks into a coherent morning briefing.
* **Contextual Research & Summarization:** Quickly digesting long articles, documentation, or meeting transcripts into actionable insights.
* **Task Automation:** Seamlessly executing multi-step routines like creating scaffolding for new features, formatting standardized reports, or auditing code.
* **Success Metric:** Reduction of manual context-switching time by 30% and consistent, error-free execution of defined daily routines.

---

## 2. General Context

| Property | Value |
| --- | --- |
| Operating System | Ubuntu 24.04 LTS |
| IDE | [Antigravity IDE](https://antigravityide.com) (latest) |
| Primary Language | German (Chat) / English (Technical Terms & Code) / Generated Files (English) |
| Project Start | March 2026 |
| Lifecycle Phase | Alpha / Concept & Baseline Structure |

---

## 3. Architecture Overview

The system follows a modular, composable architecture where lightweight, single-purpose skills are orchestrated by specialized agents through defined workflows.

### 3.1 Core Components

* **Agents:** Highly specialized, purpose-driven entities with specific tool allowlists (e.g., Planner, Researcher, Coder).
* **Skills:** Atomic units of capability. We utilize community skills from `skills.sh` alongside custom-built, project-specific skills.
* **Workflows:** Reusable, orchestrated sequences that chain multiple skills and agents together to complete complex objectives.
* **Documents:** Context documents, templates, and the knowledge base that ground the agents.

### 3.2 Directory Structure

```text
skillsh-pm/
├── .agents/
│   ├── agents/          # Agent definitions (.md)
│   ├── skills/          # Custom project-specific skills
│   └── workflows/       # Workflow definitions (.md)
├── docs/                # Project documentation & Knowledge Base
├── GEMINI.md            # Main configuration and system prompt rules
└── skills-lock.json     # Versioned skill references
```

---

## 4. LLM Model Strategy

Model selection dynamically adapts to the cognitive load, context length, and required speed of the specific task, utilizing the latest models available within the Antigravity IDE.

| Category | Use Case | Target Model Tier |
| --- | --- | --- |
| **Reasoning / Planning** | Complex architecture decisions, multi-step orchestration | `Antigravity High-Reasoning Model (e.g., latest frontier model)` |
| **Coding & Refactoring** | Code generation, complex debugging, AST manipulation | `Antigravity Code-Optimized Model` |
| **Documents & Drafts** | Text generation, reports, summarization in natural language | `Antigravity Balanced Model (optimized for speed/quality)` |
| **Fast / Lightweight** | Quick routing, exact extraction, simple formatting | `Antigravity Turbo/Flash Model` |

---

## 5. Agent Roster

The system relies on a swarm of specialized agents. Each has a tightly scoped role, a restricted toolset, and specific skills.

* **Daily-Planning-Agent:** Analyzes schedules, prior conversation logs, and task trackers to draft a daily agenda.
* **Research-Agent:** Specifically given read-only access to browse the web, read files, and synthesize technical documentation.
* **Execution-Agent:** Given write access to execute code, run commands, and apply concrete file changes based on approved plans (*Requires strict Human-in-the-Loop approval for destructive/system-altering actions*).
* **Review-Agent:** Analyzes diffs, checks against style guides, and ensures Markdown/Code linting rules are followed before finalization.

---

## 6. Skills Strategy

### 6.1 Community Skills (`skills.sh`)

Leveraging vetted community tools to prevent reinventing the wheel.

* `doc-coauthoring`: Structured co-authoring of documentation and proposals.
* `skill-creator`: Creating, optimizing, and evaluating new skills.
* `draft-framework-audit`: Auditing the agent runtime and ecosystem.

### 6.2 Custom Project Skills

Purpose-built skills for the Daily Helper's unique requirements.

* `daily-briefing`: Generates the morning summary based on current system state.
* `commit-summarizer`: Standardizes and structures git commit messages based on diffs.
* `context-prep`: Prepares the workspace with necessary files for a specific context mode.
* `agent-creator`: Scaffolds and guides the design of new AI target-agents for the ecosystem based on an interview process.

### 6.3 Skill Design Principles

* **Single Responsibility:** Each skill does exactly one thing well.
* **Composability:** Expected outputs of one skill should easily pipe into the inputs of another workflow step.
* **Idempotency:** Running a skill multiple times with the same input should yield the same safe result without destructive side-effects.
* **Explicit Model Requirements:** Skills declare if they require a specific class of model.

---

## 7. Workflows

Workflows provide the orchestration layer, combining Agents and Skills.

* **Morning Boot-Up (`morning-routine.md`):** Triggers the `daily-briefing` skill, fetches calendar, and lists stale PRs.
* **Deep Work Prep (`deep-work.md`):** Silences notifications, sets up the IDE context, and pulls relevant tickets.
* **End of Day Wrap-up (`eod-review.md`):** Summarizes accomplished tasks, commits pending changes, and stages the next day's top priority.

---

## 8. Development Principles

* **Antigravity Best Practices:** Strict adherence to Antigravity IDE patterns, utilizing standard tool calls and avoiding brittle bash scripts.
* **Iterative Assembly:** Start by perfecting one agent/skill combination before building the entire swarm. No premature over-engineering.
* **Documentation-First:** Every component is defined in a `.md` specification before code is written.
* **Continuous Evaluation:** Skills and prompts are regularly benchmarked using the `skill-creator` eval functionality.

---

## 9. AI Assistant Rules

* **Language:** Chat interactions and explanations are in **German**. Technical terms and all generated system configurations/files are in **English**.
* **Role:** Act as an Elite Solutions Architect focusing on pragmatic, scalable, and maintainable state-of-the-art architectures (as of March 2026).
* **Proactivity:** Pre-fill templates with highly educated, realistic defaults rather than simple `[`PLACEHOLDER`]` tags.
* **Scope Discipline:** Focus strictly on the defined task boundaries. Step 1 is only generating and finalizing this `GEMINI.md`.

---

## 10. Open Questions & Roadmap

* How will secure credentials (API keys for external services) be passed to the agents safely?
* Which specific external APIs (e.g., Jira, GitHub, Google Calendar) will be prioritized for the MVP?
* Will the agent state and memory be persistently stored via a local vector DB or simple JSON logging?

---

## 11. Changelog

| Date | Version | Changes | Author |
| --- | --- | --- | --- |
| 2026-03-02 | 0.1.0 | Initial template generation | AI Assistant + User |
| 2026-03-03 | 0.1.1 | Translated to English, populated with realistic architectural defaults for an Agentic Helper | AI Assistant |

---
*This document is a living configuration artifact and will be continuously updated.*
