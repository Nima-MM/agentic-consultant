---
name: agent-creator
agent: agent-architect
user-invocable: true
description: >
  Scaffolds a new customized AI Agent for the Antigravity IDE framework, including
  iterative testing, benchmarking, and description optimization. This skill helps users
  define the agent's role, constraints, available tools, and recommended model tier,
  and generates the necessary Markdown definition file in .agents/agents/. Use this
  whenever a user asks to "build an agent", "create a worker", "design an AI subagent",
  "improve an existing agent", "benchmark an agent", or "optimize agent triggering".
  Even if the user doesn't explicitly say "agent", trigger this skill when they want to
  create a specialized AI persona, a scoped assistant, or a domain-specific sub-worker.
---

# Agent Creator

A skill for designing, scaffolding, and iteratively improving AI Agents for the Antigravity IDE ecosystem.

At a high level, the process of creating an agent goes like this:

- Decide what you want the agent to do, its core responsibilities, and its level of autonomy
- Write a draft of the agent definition (`.md` file)
- Create a few test prompts and run evaluations comparing the agent's behavior against a baseline
- Help the user evaluate the results both qualitatively and quantitatively
  - While the runs happen in the background, draft some quantitative evals if there aren't any (if there are some, you can either use as is or modify if you feel something needs to change about them). Then explain them to the user (or if they already existed, explain the ones that already exist)
  - Use the `eval-viewer/generate_review.py` script to show the user the results for them to look at, and also let them look at the quantitative metrics
- Rewrite the agent definition based on feedback from the user's evaluation of the results (and also if there are any glaring flaws that become apparent from the quantitative benchmarks)
- Repeat until you're satisfied
- Expand the test set and try again at larger scale

Your job when using this skill is to figure out where the user is in this process and then jump in and help them progress through these stages. So for instance, maybe they're like "I want to build an agent for X". You can help narrow down what they mean, write a draft, write the test cases, figure out how they want to evaluate, run all the prompts, and repeat.

On the other hand, maybe they already have a draft of the agent. In this case you can go straight to the eval/iterate part of the loop.

Of course, you should always be flexible and if the user is like "I don't need to run a bunch of evaluations, just vibe with me", you can do that instead.

Then after the agent is done (but again, the order is flexible), you can also run the description improver to optimize the triggering of the agent.

## Communicating with the user

When creating agents, users might have grand visions. Ground them gently in the reality of the framework. The best agents are:

- **Focused**: Designed for one main domain
- **Constrained**: Given only the tools they absolutely need
- **Stateless by default**: Relying on conversation history and explicit files

Please pay attention to context cues to understand how to phrase your communication. In the default case:

- "evaluation" and "benchmark" are borderline, but OK
- for "JSON" and "assertion" you want to see cues from the user that they know what those are before using them without explaining them

It's OK to briefly explain terms if you're in doubt.

---

## Creating an Agent

### Capture Intent

Start by understanding the user's intent. The current conversation might already contain a workflow the user wants to capture into an agent (e.g., they say "make an agent that does this"). If so, extract answers from the conversation history first — the tools used, the sequence of steps, corrections the user made. The user may need to fill gaps, and should confirm before proceeding.

1. **What is the Agent's primary goal?** (e.g., "Analyze python code", "Schedule meetings", "Refactor CSS")
2. **What level of permission does it need?**
   - *Read-Only* (Can read files, search codebase, but not write)
   - *Write/Execution* (Can edit code, run bash commands, spawn other agents)
3. **What specific tools are required?** (e.g., `Bash`, `Write`, `Read`, `Glob`, `Grep`, `search_web`, `Agent`, or community skills like `doc-coauthoring`)
4. **Who triggers this agent?** Will the user talk to it directly, or is it a sub-agent spawned by another agent's workflow?
5. **Should we set up test cases to verify the agent works?** Agents with objectively verifiable outputs (code generation, file transforms, structured workflows) benefit from test cases. Agents with subjective outputs (brainstorming, creative coaching) often don't. Suggest the appropriate default based on the agent type, but let the user decide.

### Interview and Research

Proactively ask questions about edge cases, input/output formats, example files, success criteria, and dependencies. Wait to write test prompts until you've got this part ironed out.

Check available MCPs — if useful for research (searching docs, finding similar agents, looking up best practices), research in parallel via subagents if available, otherwise inline. Come prepared with context to reduce burden on the user.

### Model Tier Selection

The framework uses explicit model tier definitions to optimize cost and capability. Based on the interview, recommend one of the following:

- **High-Reasoning (e.g., gemini 3.1 pro (High))**: Complex architecture decisions, coding, multi-step orchestration, evaluating subjective outputs
- **Code-Optimized**: Heavy refactoring, AST manipulation, deep debugging
- **Balanced**: Drafting natural language texts, reports, summarization
- **Turbo/Flash**: Quick routing, exact text extraction, simple standardized formatting

### Tool Allowlist Design

Enforce the **Single Responsibility Principle**. If an agent is meant to research, don't give it `Bash` or `Write`. If it needs to invoke specific skills, list them explicitly in the context/instructions.

### Write the Agent Definition

Based on the gathered details, generate the `.agents/agents/<agent-name>.md` file in the user's workspace.

#### Anatomy of an Agent File

```markdown
---
name: [agent-id-name]
description: [Concise description of the agent's purpose, used for routing]
model: [Selected Model Tier]
tools:
  - [Tool 1]
  - [Tool 2]
---

# Agent: [Human Readable Name]

## Role: [agent-id-name]
You are the **[Human Readable Name]**. Your primary responsibility is to [briefly state the main goal]. Your objective is to [what it should achieve].

## Context
You operate within a framework where [describe the operational constraint, e.g., you only read code, or you use standardized templates]. You deeply understand [domain knowledge].

## Tool Allowlist
- `Tool 1`: [Reason it has this tool]
- `Skill X`: Invoke `@[path/to/skill]` for [reason].

## Core Directives
1. **[Directive 1]:** [Instruction on how to behave/what to do]
2. **[Directive 2]:** [Instruction on how to behave/what to do]
3. **[Directive 3]:** [Instruction on how to behave/what to do]

---
Read `.agents/rules/*.md` for constraints, rules and conventions.
```

### Agent Writing Guide

#### Progressive Disclosure

Agent definitions use a similar loading system to skills:
1. **Metadata** (name + description) — Always in context (~100 words)
2. **Agent definition body** — Loaded when agent is invoked
3. **Referenced skills and rules** — Loaded as needed by the agent

**Key patterns:**
- Keep agent definitions focused — a sprawling prompt leads to unfocused behavior
- Reference skills and rules files clearly, with guidance on when to consult them
- Explain *why* a directive matters rather than using heavy-handed MUSTs

#### Writing Style

Try to explain to the model why things are important in lieu of heavy-handed constraints. Use theory of mind and make the agent definition general rather than super-narrow to specific examples. Start by writing a draft and then look at it with fresh eyes and improve it.

### Test Cases

After writing the agent draft, come up with 2-3 realistic test prompts — the kind of thing a real user would actually ask this agent to do. Share them with the user: "Here are a few test cases I'd like to try. Do these look right, or do you want to add more?" Then run them.

Save test cases to `<agent-name>-workspace/evals/evals.json`. Don't write assertions yet — just the prompts. You'll draft assertions in the next step while the runs are in progress.

```json
{
  "agent_name": "example-agent",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

See `references/schemas.md` for the full schema (including the `assertions` field, which you'll add later).

## Running and evaluating test cases

This section is one continuous sequence — don't stop partway through.

Put results in `<agent-name>-workspace/` as a sibling to the agent directory. Within the workspace, organize results by iteration (`iteration-1/`, `iteration-2/`, etc.) and within that, each test case gets a directory (`eval-0/`, `eval-1/`, etc.). Don't create all of this upfront — just create directories as you go.

### Step 1: Spawn all runs (with-agent AND baseline) in the same turn

For each test case, spawn two subagents in the same turn — one with the custom agent, one without. This is important: don't spawn the with-agent runs first and then come back for baselines later. Launch everything at once so it all finishes around the same time.

**With-agent run:**

```
Execute this task:
- Agent path: <path-to-agent.md>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_agent/outputs/
- Outputs to save: <what the user cares about>
```

**Baseline run** (same prompt, but the baseline depends on context):
- **Creating a new agent**: no custom agent at all. Same prompt, standard assistant, save to `without_agent/outputs/`.
- **Improving an existing agent**: the old version. Before editing, snapshot the agent definition (`cp <agent.md> <workspace>/agent-snapshot.md`), then point the baseline subagent at the snapshot. Save to `old_agent/outputs/`.

Write an `eval_metadata.json` for each test case (assertions can be empty for now). Give each eval a descriptive name based on what it's testing — not just "eval-0". Use this name for the directory too. If this iteration uses new or modified eval prompts, create these files for each new eval directory — don't assume they carry over from previous iterations.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Step 2: While runs are in progress, draft assertions

Don't just wait for the runs to finish — use this time productively. Draft quantitative assertions for each test case and explain them to the user. If assertions already exist in `evals/evals.json`, review them and explain what they check.

Good assertions are objectively verifiable and have descriptive names — they should read clearly in the benchmark viewer so someone glancing at the results immediately understands what each one checks. Subjective agents (writing style, design quality) are better evaluated qualitatively — don't force assertions onto things that need human judgment.

Update the `eval_metadata.json` files and `evals/evals.json` with the assertions once drafted. Also explain to the user what they'll see in the viewer — both the qualitative outputs and the quantitative benchmark.

### Step 3: As runs complete, capture timing data

When each subagent task completes, you receive a notification containing `total_tokens` and `duration_ms`. Save this data immediately to `timing.json` in the run directory:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

This is the only opportunity to capture this data — it comes through the task notification and isn't persisted elsewhere. Process each notification as it arrives rather than trying to batch them.

### Step 4: Grade, aggregate, and launch the viewer

Once all runs are done:

1. **Grade each run** — spawn a grader subagent (or grade inline) that reads `agents/grader.md` and evaluates each assertion against the outputs. Save results to `grading.json` in each run directory. The grading.json expectations array must use the fields `text`, `passed`, and `evidence` (not `name`/`met`/`details` or other variants) — the viewer depends on these exact field names. For assertions that can be checked programmatically, write and run a script rather than eyeballing it — scripts are faster, more reliable, and can be reused across iterations.

2. **Aggregate into benchmark** — run the aggregation script:
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <agent-name>
   ```
   This produces `benchmark.json` and `benchmark.md` with pass_rate, time, and tokens for each configuration, with mean ± stddev and the delta. If generating benchmark.json manually, see `references/schemas.md` for the exact schema the viewer expects.
Put each with_agent version before its baseline counterpart.

3. **Do an analyst pass** — read the benchmark data and surface patterns the aggregate stats might hide. See `agents/analyzer.md` (the "Analyzing Benchmark Results" section) for what to look for — things like assertions that always pass regardless of agent (non-discriminating), high-variance evals (possibly flaky), and time/token tradeoffs.

4. **Launch the viewer** with both qualitative outputs and quantitative data:
   ```bash
   nohup python eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "<agent-name>" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   For iteration 2+, also pass `--previous-workspace <workspace>/iteration-<N-1>`.

   **Cowork / headless environments:** If `webbrowser.open()` is not available or the environment has no display, use `--static <output_path>` to write a standalone HTML file instead of starting a server. Feedback will be downloaded as a `feedback.json` file when the user clicks "Submit All Reviews". After download, copy `feedback.json` into the workspace directory for the next iteration to pick up.

Note: please use generate_review.py to create the viewer; there's no need to write custom HTML.

5. **Tell the user** something like: "I've opened the results in your browser. There are two tabs — 'Outputs' lets you click through each test case and leave feedback, 'Benchmark' shows the quantitative comparison. When you're done, come back here and let me know."

### What the user sees in the viewer

The "Outputs" tab shows one test case at a time:
- **Prompt**: the task that was given
- **Output**: the files the agent produced, rendered inline where possible
- **Previous Output** (iteration 2+): collapsed section showing last iteration's output
- **Formal Grades** (if grading was run): collapsed section showing assertion pass/fail
- **Feedback**: a textbox that auto-saves as they type
- **Previous Feedback** (iteration 2+): their comments from last time, shown below the textbox

The "Benchmark" tab shows the stats summary: pass rates, timing, and token usage for each configuration, with per-eval breakdowns and analyst observations.

Navigation is via prev/next buttons or arrow keys. When done, they click "Submit All Reviews" which saves all feedback to `feedback.json`.

### Step 5: Read the feedback

When the user tells you they're done, read `feedback.json`:

```json
{
  "reviews": [
    {"run_id": "eval-0-with_agent", "feedback": "the agent missed the edge case", "timestamp": "..."},
    {"run_id": "eval-1-with_agent", "feedback": "", "timestamp": "..."},
    {"run_id": "eval-2-with_agent", "feedback": "perfect, love this", "timestamp": "..."}
  ],
  "status": "complete"
}
```

Empty feedback means the user thought it was fine. Focus your improvements on the test cases where the user had specific complaints.

Kill the viewer server when you're done with it:

```bash
kill $VIEWER_PID 2>/dev/null
```

---

## Improving the agent

This is the heart of the loop. You've run the test cases, the user has reviewed the results, and now you need to make the agent better based on their feedback.

### How to think about improvements

1. **Generalize from the feedback.** The big picture is that we're trying to create agents that will be invoked many times across many different prompts. Here you and the user are iterating on only a few examples because it helps move faster. But if the agent you and the user are codeveloping works only for those examples, it's useless. Rather than put in fiddly overfitty changes, or oppressively constrictive MUSTs, if there's some stubborn issue, try branching out with different metaphors or recommending different patterns of working. It's relatively cheap to try.

2. **Keep the prompt lean.** Remove things that aren't pulling their weight. Make sure to read the transcripts, not just the final outputs — if the agent definition is making the model waste time doing unproductive things, try getting rid of those parts and seeing what happens.

3. **Explain the why.** Try hard to explain the **why** behind everything you're asking the model to do. Today's LLMs are *smart*. They have good theory of mind and when given a good harness can go beyond rote instructions. Even if the feedback from the user is terse, try to actually understand the task and why the user is writing what they wrote, then transmit this understanding into the agent definition. If you find yourself writing ALWAYS or NEVER in all caps, that's a yellow flag — reframe and explain the reasoning so the model understands why the thing is important.

4. **Look for repeated work across test cases.** Read the transcripts and notice if the subagents all independently wrote similar helper scripts or took the same multi-step approach. If all test cases resulted in the agent writing a `validate_output.py` or a `parse_input.py`, that's a strong signal the agent should have a bundled script or reference a specific skill. Write it once, put it in the right place, and tell the agent to use it.

### The iteration loop

After improving the agent:

1. Apply your improvements to the agent definition
2. Rerun all test cases into a new `iteration-<N+1>/` directory, including baseline runs. If you're creating a new agent, the baseline is always `without_agent` (no custom agent) — that stays the same across iterations. If you're improving an existing agent, use your judgment on what makes sense as the baseline: the original version the user came in with, or the previous iteration.
3. Launch the reviewer with `--previous-workspace` pointing at the previous iteration
4. Wait for the user to review and tell you they're done
5. Read the new feedback, improve again, repeat

Keep going until:
- The user says they're happy
- The feedback is all empty (everything looks good)
- You're not making meaningful progress

---

## Advanced: Blind comparison

For situations where you want a more rigorous comparison between two versions of an agent (e.g., the user asks "is the new version actually better?"), there's a blind comparison system. Read `agents/comparator.md` and `agents/analyzer.md` for the details. The basic idea is: give two outputs to an independent agent without telling it which is which, and let it judge quality. Then analyze why the winner won.

This is optional, requires subagents, and most users won't need it. The human review loop is usually sufficient.

---

## Description Optimization

The `description` field in the agent's frontmatter orchestrates when the main routing framework chooses to invoke this agent over others. After creating or improving an agent, offer to optimize the description for better triggering accuracy.

### Step 1: Generate trigger eval queries

Create 20 eval queries — a mix of should-trigger and should-not-trigger. Save as JSON:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

The queries must be realistic and something an Antigravity IDE user would actually type. Not abstract requests, but requests that are concrete and specific with a good amount of detail. For instance, file paths, personal context about the user's job, column names and values, company names, URLs. A little bit of backstory. Some might be in lowercase or contain abbreviations or typos or casual speech. Use a mix of different lengths, and focus on edge cases rather than making them clear-cut.

Bad: `"Analyze code"`, `"Review this file"`, `"Create a report"`

Good: `"i have this huge python codebase (around 400 files) and need someone to go through the auth module in src/auth/ and find any security holes, especially around JWT validation and session handling. can you set up a specialist for this?"`

For the **should-trigger** queries (8-10), think about coverage. Different phrasings of the same intent — some formal, some casual. Include cases where the user doesn't explicitly say "agent" but clearly needs one. Throw in uncommon use cases and cases where this agent competes with another but should win.

For the **should-not-trigger** queries (8-10), the most valuable ones are near-misses — queries that share keywords or concepts but actually need something different. Think adjacent domains, ambiguous phrasing where a naive keyword match would trigger but shouldn't, and cases where the query touches on something the agent does but in a context where another tool is more appropriate.

The key thing to avoid: don't make should-not-trigger queries obviously irrelevant. "Write a fibonacci function" as a negative test for a code-review agent is too easy — it doesn't test anything. The negative cases should be genuinely tricky.

### Step 2: Review with user

Present the eval set to the user for review using the HTML template:

1. Read the template from `assets/eval_review.html`
2. Replace the placeholders:
   - `__EVAL_DATA_PLACEHOLDER__` → the JSON array of eval items (no quotes around it — it's a JS variable assignment)
   - `__SKILL_NAME_PLACEHOLDER__` → the agent's name
   - `__SKILL_DESCRIPTION_PLACEHOLDER__` → the agent's current description
3. Write to a temp file (e.g., `/tmp/eval_review_<agent-name>.html`) and open it
4. The user can edit queries, toggle should-trigger, add/remove entries, then click "Export Eval Set"
5. The file downloads to `~/Downloads/eval_set.json` — check the Downloads folder for the most recent version

This step matters — bad eval queries lead to bad descriptions.

### Step 3: Run the optimization loop

Tell the user: "This will take some time — I'll run the optimization loop in the background and check on it periodically."

Save the eval set to the workspace, then run in the background:

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-agent.md> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Use the model ID from your system prompt (the one powering the current session) so the triggering test matches what the user actually experiences.

While it runs, periodically tail the output to give the user updates on which iteration it's on and what the scores look like.

This handles the full optimization loop automatically. It splits the eval set into 60% train and 40% held-out test, evaluates the current description (running each query 3 times to get a reliable trigger rate), then calls the Gemini API with extended thinking to propose improvements based on what failed. It re-evaluates each new description on both train and test, iterating up to 5 times. When it's done, it opens an HTML report in the browser showing the results per iteration and returns JSON with `best_description` — selected by test score rather than train score to avoid overfitting.

### Step 4: Apply the result

Take `best_description` from the JSON output and update the agent's `.md` frontmatter. Show the user before/after and report the scores.

---

## General IDE-specific instructions

If the core workflow is somewhat restricted (e.g. no subagents), some mechanics change. Here's what to adapt:

**Running test cases**: No subagents means no parallel execution. For each test case, invoke the agent by path (e.g. `@.agents/agents/<agent-name>.md`), then follow through on the test prompt yourself. Do them one at a time. This is less rigorous than independent subagents (you wrote the agent definition and you're also testing it), but it's a useful sanity check — and the human review step compensates. Skip the baseline runs — just use the agent to complete the task as requested.

**Reviewing results**: If you can't open a browser (e.g., you're on a remote server), skip the browser reviewer entirely. Instead, present results directly in the conversation. For each test case, show the prompt and the output. If the output is a file the user needs to see, save it to the filesystem and tell them where it is so they can download and inspect it. Ask for feedback inline: "How does this look? Anything you'd change?"

**Benchmarking**: Skip the quantitative benchmarking — it relies on baseline comparisons which aren't meaningful without subagents. Focus on qualitative feedback from the user.

**The iteration loop**: Same as before — improve the agent, rerun the test cases, ask for feedback — just without the browser reviewer in the middle. You can still organize results into iteration directories on the filesystem.

**Description optimization**: This step triggers Gemini function calling simulation via the google-genai SDK.

**Blind comparison**: Requires subagents. Skip it.

---

## Working in Headless Environments

If you're in a headless remote environment, the main things to know are:

- You have subagents, so the main workflow (spawn test cases in parallel, run baselines, grade, etc.) all works. (However, if you run into severe problems with timeouts, it's OK to run the test prompts in series rather than parallel.)
- You don't have a browser or display, so when generating the eval viewer, use `--static <output_path>` to write a standalone HTML file instead of starting a server. Then proffer a link that the user can click to open the HTML in their browser.
- Whether you're local or remote, after running tests, you should always generate the eval viewer for the human to look at examples before revising the agent yourself and trying to make corrections, using `generate_review.py` (not writing your own boutique html code). GENERATE THE EVAL VIEWER *BEFORE* evaluating inputs yourself. You want to get them in front of the human ASAP!
- Feedback works differently: since there's no running server, the viewer's "Submit All Reviews" button will download `feedback.json` as a file. You can then read it from there.
- Description optimization (`run_loop.py` / `run_eval.py`) uses the Gemini API, so it works anywhere.

---

## Reference files

The agents/ directory contains instructions for specialized subagents. Read them when you need to spawn the relevant subagent.

- `agents/grader.md` — How to evaluate assertions against outputs
- `agents/comparator.md` — How to do blind A/B comparison between two outputs
- `agents/analyzer.md` — How to analyze why one version beat another, and how to analyze benchmark results

The references/ directory has additional documentation:
- `references/schemas.md` — JSON structures for evals.json, grading.json, benchmark.json, etc.

---

Repeating one more time the core loop here for emphasis:

- Figure out what the agent should do
- Draft or edit the agent definition
- Run the agent on test prompts (with baseline comparisons where possible)
- With the user, evaluate the outputs:
  - Create benchmark.json and run `eval-viewer/generate_review.py` to help the user review them
  - Run quantitative evals
- Repeat until you and the user are satisfied
- Optimize the agent's description for triggering accuracy

Please add steps to your TodoList, if you have such a thing, to make sure you don't forget. If you're remote, please specifically put "Create evals JSON and run `eval-viewer/generate_review.py` so human can review test cases" in your TodoList to make sure it happens.

Good luck!
