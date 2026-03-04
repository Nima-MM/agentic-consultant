# Architecture Review Framework

A structured framework for reviewing system designs, project structures, and technical decisions. Use this as a flexible toolkit — apply the dimensions most relevant to the user's context rather than forcing a full review every time.

## Table of Contents

1. [Review Workflow](#review-workflow)
2. [Review Dimensions](#review-dimensions)
   - Structural Integrity
   - Dependency Health
   - Scalability & Performance Posture
   - Maintainability & Evolvability
   - Security Posture
   - Operational Readiness
3. [Severity System](#severity-system)
4. [Anti-Pattern Catalog](#anti-pattern-catalog)
5. [Output Template](#output-template)
6. [Tool Usage Heuristics](#tool-usage-heuristics)

---

## Review Workflow

### 1. Scope the Review

Before diving into code, establish boundaries:

- **What to review:** Specific modules, the full project, a particular design decision?
- **What triggered this:** Performance concern? Scaling worry? Onboarding friction? Security audit?
- **Constraints:** Time, access to infrastructure, availability of documentation?

The trigger determines which dimensions to prioritize. A user worried about scaling doesn't need a deep security review first — start where it hurts.

### 2. Gather Context

Use `Read`, `Glob`, and `Grep` to understand the project before making judgments:

- Read the project's README, configuration files, and entry points
- Map the directory structure and identify organizational patterns
- Check for dependency manifests (package.json, requirements.txt, go.mod, Cargo.toml, etc.)
- Look for existing documentation, ADRs (Architecture Decision Records), and CI/CD configs

### 3. Analyze Systematically

Apply the relevant review dimensions (see below). For each finding:

- Identify the specific location (files, modules, patterns)
- Assess severity using the severity system
- Formulate a concrete, actionable recommendation — not just "this is bad"

### 4. Synthesize and Prioritize

Aggregate findings into the output template. Prioritize recommendations by impact vs. effort — quick wins first, then strategic improvements. The user needs a clear path forward, not an overwhelming list of everything that could theoretically be better.

---

## Review Dimensions

### 1. Structural Integrity

Evaluates how well the codebase is organized and whether boundaries between components are clean.

**What to examine:**

- **Directory layout:** Does the structure communicate intent? Can a new developer find things intuitively?
- **Module boundaries:** Is there clear separation between presentation, business logic, and data access?
- **Cohesion:** Do files within a module belong together? Or is it a grab-bag of loosely related utilities?
- **Coupling:** How much do modules depend on each other's internals? Can you change one without breaking another?
- **Naming conventions:** Are naming patterns consistent across the codebase? Do names communicate purpose?
- **Organization pattern:** By feature? By layer? Hybrid? Is the chosen pattern applied consistently?

**Signals of health:**

- Clear, self-documenting directory names
- Modules that can be understood in isolation
- Consistent file naming conventions
- Logical grouping that matches domain concepts

**Red flags:**

- `utils/`, `helpers/`, `misc/` directories that grow unbounded
- Circular imports or dependencies between sibling modules
- God modules that touch everything
- Inconsistent patterns across different parts of the codebase

**How to investigate:**

```text
Glob: Map directory tree and identify organizational patterns
Grep: Search for cross-module imports to detect coupling
Read: Examine key files at module boundaries (index files, barrel exports)
```

---

### 2. Dependency Health

Evaluates the project's relationship with external and internal dependencies.

**What to examine:**

- **Dependency graph:** Are there circular dependencies? How deep are dependency chains?
- **External dependencies:** Are they actively maintained? Are versions current? Any known vulnerabilities?
- **Dependency direction:** Do stable abstractions depend on volatile implementations, or vice versa? (The Dependency Inversion Principle says stable things should not depend on unstable things.)
- **Dependency injection:** Are dependencies injected or hard-coded? Can components be tested in isolation?
- **License compatibility:** Do dependency licenses conflict with the project's license?

**Signals of health:**

- Acyclic dependency graph
- Dependencies pinned to specific versions with a lockfile
- Most dependencies are actively maintained (commits within last 6 months)
- Clear dependency boundaries between layers

**Red flags:**

- Circular dependency chains
- Dependencies with no updates in 12+ months
- Transitive dependencies pulling in massive sub-trees for minimal functionality
- Vendor lock-in through deep framework coupling
- Missing lockfile

**How to investigate:**

```text
Read: Examine package manifests (package.json, requirements.txt, go.mod, etc.)
Grep: Search for import/require patterns to map internal dependencies
search_web: Check maintenance status of critical external dependencies
```

---

### 3. Scalability & Performance Posture

Evaluates whether the architecture can handle growth in users, data, and complexity.

**What to examine:**

- **Bottleneck candidates:** Synchronous choke points, N+1 query patterns, unbounded list processing
- **Caching strategy:** Is caching used where appropriate? Is cache invalidation well-defined?
- **Horizontal scaling readiness:** Can the system scale by adding instances? Is state externalized?
- **Database/storage design:** Indexing strategy, normalization level, partitioning for large datasets
- **Async processing:** Are long-running tasks properly offloaded? Is there a queue/worker pattern?
- **Resource management:** Connection pooling, file handle management, memory lifecycle

**Signals of health:**

- Stateless application tier with externalized session/state
- Database queries use indexes and avoid N+1 patterns
- Long-running operations are async with proper feedback mechanisms
- Resource limits are configured (connection pools, timeouts, rate limits)

**Red flags:**

- In-memory state that prevents horizontal scaling
- Unbounded queries without pagination
- Synchronous processing of naturally async workloads
- No caching strategy despite repeated expensive computations
- Missing connection pooling for database or external service connections

**How to investigate:**

```text
Grep: Search for ORM patterns (eager vs. lazy loading), raw queries, cache usage
Read: Examine database schemas, migration files, configuration files
Glob: Find queue/worker configurations, caching layers
```

---

### 4. Maintainability & Evolvability

Evaluates how easy it is to understand, modify, and extend the codebase over time.

**What to examine:**

- **Code readability:** Is the code self-documenting? Are complex sections explained?
- **Test coverage and strategy:** Unit tests? Integration tests? E2E tests? Is the test strategy appropriate for the project's risk profile?
- **Configuration management:** Are settings environment-based or hardcoded? Is there a clear config hierarchy?
- **Error handling:** Is error handling consistent? Are errors recoverable where appropriate? Are they logged meaningfully?
- **API contracts:** Are internal and external APIs versioned? Are contracts documented?
- **Technical debt indicators:** TODO/FIXME density, dead code, deprecated API usage, duplicated logic

**Signals of health:**

- Tests exist for critical paths and edge cases
- Configuration is environment-driven with sensible defaults
- Error handling follows consistent patterns with structured information
- API changes are versioned or backwards-compatible
- Low density of TODO/FIXME/HACK comments

**Red flags:**

- No tests, or tests that only test happy paths
- Hardcoded configuration values (URLs, credentials, feature flags)
- Catch-all error handling that swallows exceptions silently
- Copy-pasted logic across multiple files
- Large functions (100+ lines) doing multiple unrelated things

**How to investigate:**

```text
Glob: Find test files, configuration files, migration files
Grep: Count TODO/FIXME/HACK occurrences, search for hardcoded values
Read: Examine error handling patterns, test structure, config management
```

---

### 5. Security Posture

Evaluates the architecture's resilience against common security threats. This is a high-level architectural review, not a penetration test.

**What to examine:**

- **Authentication & Authorization:** Are auth patterns centralized? Is there role-based or attribute-based access control? Are auth checks consistently applied?
- **Input validation:** Is user input validated and sanitized at the boundary? Are there parameterized queries?
- **Secrets management:** Are API keys, passwords, and tokens stored securely? Is there a secrets manager or are they in environment variables?
- **Attack surface:** How many endpoints are publicly exposed? Are unused endpoints disabled? Are CORS policies appropriately restrictive?
- **Data handling:** Is sensitive data encrypted at rest and in transit? Is PII handled according to relevant regulations?
- **Dependency vulnerabilities:** Are there known CVEs in the dependency tree?

**Signals of health:**

- Centralized auth middleware applied consistently
- Input validation at API boundaries using schemas/validators
- Secrets stored in environment variables or a secrets manager, never in code
- HTTPS enforced everywhere, CORS properly configured
- Regular dependency audits

**Red flags:**

- Auth logic duplicated across routes instead of centralized
- Raw SQL queries with string interpolation (SQL injection risk)
- API keys or credentials committed to version control (check `.env` files, config files, git history)
- Overly permissive CORS (`*`)
- No rate limiting on authentication endpoints

**How to investigate:**

```text
Grep: Search for hardcoded secrets patterns, SQL string interpolation, CORS config
Read: Examine auth middleware, API route definitions, .gitignore
Glob: Find .env files, credential stores, security configurations
search_web: Check for CVEs in critical dependencies
```

---

### 6. Operational Readiness

Evaluates whether the system is prepared for production operation — monitoring, deployment, and incident response.

**What to examine:**

- **Logging & Observability:** Is logging structured (JSON)? Are log levels used consistently? Are there tracing or metrics hooks?
- **CI/CD pipeline:** Is there automated testing on PR? Automated deployment? Are environments clearly separated?
- **Deployment strategy:** Can releases be rolled back? Is there blue/green or canary deployment? Are database migrations reversible?
- **Error recovery & Resilience:** Are there circuit breakers for external services? Retry logic with backoff? Graceful degradation?
- **Health checks:** Does the system expose health/readiness endpoints? Are they meaningful (not just returning 200)?
- **Documentation:** Is there a runbook for common incidents? Are deployment procedures documented?

**Signals of health:**

- Structured logging with correlation IDs
- CI pipeline runs tests and linters on every PR
- Automated deployment with rollback capability
- Health endpoints that check downstream dependencies
- Documented incident response procedures

**Red flags:**

- `console.log` / `print()` as the primary logging mechanism
- Manual deployment processes
- No health checks or liveness probes
- Missing environment separation (dev/staging/prod)
- No documented recovery procedures

**How to investigate:**

```text
Glob: Find CI/CD configs (.github/workflows, Jenkinsfile, .gitlab-ci.yml, Dockerfile)
Read: Examine logging setup, health endpoints, deployment configs
Grep: Search for console.log/print patterns, error handling in HTTP clients
```

---

## Severity System

Use these severity levels to classify findings. The goal is to give the user a clear sense of urgency:

| Severity | Symbol | Criteria | Action Timeline |
| --- | --- | --- | --- |
| **Critical** | 🔴 | Security vulnerabilities, data loss risk, architectural dead-ends that block progress | Immediate — before next release |
| **High** | 🟠 | Significant maintainability issues, performance risks under realistic load, patterns that worsen over time | Plan within current sprint/cycle |
| **Medium** | 🟡 | Best-practice deviations, improvement opportunities, patterns that work now but won't scale | Address in next refactoring phase |
| **Low** | 🔵 | Stylistic improvements, minor optimizations, nice-to-have enhancements | Address opportunistically |

**Calibration guidance:**

- If you're unsure between two levels, consider: "What happens if this is ignored for 6 months?" If the answer involves data loss, security breach, or complete architectural rewrite → it's probably Critical or High.
- A finding that only affects developer experience (not end users or system reliability) is typically Medium or Low.
- Don't inflate severity to get attention. The user trusts your calibration — use it honestly.

---

## Anti-Pattern Catalog

Quick-reference list of common architectural anti-patterns, organized by the dimension where they're most relevant.

### Structural Anti-Patterns

- **God Object/Module:** One class or module that does everything
- **Spaghetti Architecture:** No clear boundaries, everything depends on everything
- **Lava Flow:** Dead code paths that nobody dares remove because "it might be needed"
- **Golden Hammer:** Using the same pattern/tool for everything regardless of fit

### Dependency Anti-Patterns

- **Dependency Hell:** Incompatible version requirements across the dependency tree
- **Vendor Lock-In:** Deep coupling to a specific framework or service provider
- **Phantom Dependencies:** Using transitive dependencies directly without declaring them

### Scalability Anti-Patterns

- **Premature Optimization:** Complex caching/sharding before confirming actual bottlenecks
- **Monolith-in-Disguise:** Microservices that must be deployed together and share databases
- **Chatty Interfaces:** Excessive network calls between components for single operations

### Maintainability Anti-Patterns

- **Shotgun Surgery:** A single change requires touching many unrelated files
- **Feature Envy:** Code that uses another module's data more than its own
- **Copy-Paste Programming:** Logic duplicated instead of abstracted

### Security Anti-Patterns

- **Security Through Obscurity:** Relying on hidden URLs or undocumented APIs instead of proper auth
- **Trust Boundary Violations:** Treating internal inputs as inherently safe
- **Credential Sprawl:** Secrets scattered across config files, environment variables, and code

### Operational Anti-Patterns

- **Log and Forget:** Logging errors without alerting or acting on them
- **Snowflake Deployments:** Manual, unreproducible deployment processes
- **Missing Circuit Breakers:** Letting cascading failures propagate unchecked

---

## Output Template

When delivering an architecture review, follow this structure for consistency. Adapt the depth and detail to the scope of the review — a focused module review doesn't need the same structure as a full-system audit.

```markdown
# Architecture Review: [Project Name / Scope]

## Executive Summary
[2-3 sentences: overall impression, most critical findings, high-level recommendation.
Frame this as: "The architecture is [assessment] with [key strength], but [primary concern]."]

## Review Scope
- **Reviewed:** [What was examined — modules, directories, configs, etc.]
- **Not reviewed:** [What was explicitly out of scope]
- **Constraints:** [Limited access, time-boxed, missing documentation, etc.]

## Findings

### 🔴 [Finding Title]
- **Dimension:** [e.g., Security Posture]
- **Location:** [File(s) / module(s) / pattern(s)]
- **Issue:** [What the problem is — be specific]
- **Impact:** [Why this matters — what could go wrong]
- **Recommendation:** [Concrete fix with code example or architectural sketch]

### 🟠 [Finding Title]
[Same structure]

### 🟡 [Finding Title]
[Same structure]

### 🔵 [Finding Title]
[Same structure]

## Architecture Scorecard

| Dimension | Score (1-5) | Note |
|---|---|---|
| Structural Integrity | | |
| Dependency Health | | |
| Scalability & Performance | | |
| Maintainability & Evolvability | | |
| Security Posture | | |
| Operational Readiness | | |

**Scoring guide:** 1 = Critical issues, needs immediate attention. 2 = Significant gaps. 3 = Adequate, with room for improvement. 4 = Good, follows best practices. 5 = Excellent, could serve as reference implementation.

## Recommended Next Steps
[Prioritized list of 3-5 actions, ordered by impact × feasibility.
Each item: what to do, why it matters, rough effort estimate.]

1. **[Action]** — [Rationale] *(Effort: [Low/Medium/High])*
2. ...
```

---

## Tool Usage Heuristics

Guidance on which tools to use for different review activities:

| Activity | Primary Tool | When to Use |
|---|---|---|
| Map project structure | `Glob` | Always — first step of every review |
| Read configs and entry points | `Read` | Always — understand the project's foundations |
| Find cross-cutting patterns | `Grep` | When checking for consistency (error handling, logging, auth patterns) |
| Count occurrences | `Grep` | TODO/FIXME density, hardcoded values, import patterns |
| Check dependency freshness | `search_web` | When external deps look stale or when checking for CVEs |
| Verify best practices | `search_web` | When uncertain about current recommendations for a specific tech stack |
| Create diagrams or docs | `Write` | When the review benefits from a visual dependency graph or written ADR |
| Run analysis scripts | `Bash` | When programmatic analysis is more reliable than manual inspection (line counts, complexity metrics) |

**Important:** Ground your findings in actual code and configuration, not assumptions. If you suspect an issue but can't confirm it from the files, say so explicitly — "Based on the absence of X, I suspect Y, but this should be verified."
