---
name: skills-skill-architect
agent: skill-architect
user-invocable: true
description: >
  CENTRAL ARCHITECT SKILL: Always trigger this skill when you need to
  design, scaffold, evaluate, or optimize an AI agent skill.
---

# Skill-Architect Skills (Master Router)

You are analyzing the user's request regarding skill creation, optimization, or evaluation. Depending on the specific task, load **exactly one** of the following reference documents from the `@[ressources](.agents/skills/skills-skill-architect/ressources/)` directory.

## Available Skill-Modules (References)

The following skills extend this agent's capabilities for specialized domains. They can be invoked when a particular type of action is needed:

1. **Skill-Creator Framework** (@[`.agents/skills/skills-skill-architect/ressources/skill-creator/SKILL.md`])
   Read this file when you need to scaffold, improve, or rigorously evaluate skills within the ecosystem. This contains the comprehensive test loops and evaluator agents.

## Your Workflow

1. Determine the appropriate module from the list above based on the user's request.
2. Use your `Read` tool to open the exact file path provided above.
3. Execute the capability based on this shared expert knowledge.
