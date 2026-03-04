#!/usr/bin/env bash
# =============================================================================
# architecture-discovery.sh
# Automated codebase fact-gathering for architecture reviews.
# Produces a structured snapshot that the Consultant agent uses as the
# foundation for a systematic review — replacing manual Glob/Grep/Read passes.
#
# Usage:
#   bash .agents/skills/skills-consultant/ressources/consult-architecture-review/scripts/architecture-discovery.sh [PROJECT_ROOT]
#
# Arguments:
#   PROJECT_ROOT  Path to the project root to analyze. Defaults to current dir.
#
# Output:
#   Prints a structured markdown report to stdout.
#   Optionally pipe to a file:
#     bash architecture-discovery.sh /path/to/project > .tmp/project-snapshot.md
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${1:-$(pwd)}"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Detect dominant tech stack languages
detect_languages() {
  local root="$1"
  declare -A counts
  while IFS= read -r ext; do
    counts["$ext"]=$(( ${counts["$ext"]:-0} + 1 ))
  done < <(find "$root" -type f \( \
    -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \
    -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.java" \
    -o -name "*.cs" -o -name "*.rb" -o -name "*.php" -o -name "*.md" \
    \) 2>/dev/null | sed 's/.*\.//' | head -500)
  # Print top languages
  for ext in "${!counts[@]}"; do
    echo "${counts[$ext]} $ext"
  done | sort -rn | head -8 | awk '{print "  - " $2 ": " $1 " files"}'
}

# Count test files heuristically
count_test_files() {
  find "$1" -type f \( \
    -name "*.test.*" -o -name "*_test.*" -o -name "*.spec.*" \
    -o -name "*Test.*" -o -name "*Spec.*" \
    \) 2>/dev/null | wc -l | tr -d ' '
}

# Detect CI/CD systems present
detect_cicd() {
  local root="$1"
  local found=()
  [[ -d "$root/.github/workflows" ]] && found+=("GitHub Actions")
  [[ -f "$root/Jenkinsfile" ]] && found+=("Jenkins")
  [[ -f "$root/.gitlab-ci.yml" ]] && found+=("GitLab CI")
  [[ -f "$root/.circleci/config.yml" ]] && found+=("CircleCI")
  [[ -f "$root/azure-pipelines.yml" ]] && found+=("Azure Pipelines")
  [[ -f "$root/bitbucket-pipelines.yml" ]] && found+=("Bitbucket Pipelines")
  [[ -f "$root/Makefile" ]] && found+=("Makefile")
  if [[ ${#found[@]} -eq 0 ]]; then
    echo "  - None found"
  else
    for ci in "${found[@]}"; do echo "  - $ci"; done
  fi
}

# Detect container/infra tooling
detect_infra() {
  local root="$1"
  local found=()
  [[ -f "$root/Dockerfile" ]] || find "$root" -maxdepth 3 -name "Dockerfile" -quit 2>/dev/null && found+=("Docker")
  [[ -f "$root/docker-compose.yml" || -f "$root/docker-compose.yaml" ]] && found+=("Docker Compose")
  find "$root" -maxdepth 3 -name "*.tf" -quit 2>/dev/null && found+=("Terraform")
  find "$root" -maxdepth 3 -name "*.k8s.yml" -o -name "*.k8s.yaml" -quit 2>/dev/null && found+=("Kubernetes")
  [[ -f "$root/serverless.yml" || -f "$root/serverless.yaml" ]] && found+=("Serverless Framework")
  if [[ ${#found[@]} -eq 0 ]]; then
    echo "  - None found"
  else
    for infra in "${found[@]}"; do echo "  - $infra"; done
  fi
}

# ============================================================
# MAIN REPORT
# ============================================================

cat <<EOF
# Architecture Discovery Snapshot

> **Project:** \`$PROJECT_ROOT\`
> **Generated:** $TIMESTAMP

---

## Project Structure (depth 3)

\`\`\`
$(find "$PROJECT_ROOT" -maxdepth 3 -not -path '*/.git/*' -not -path '*/node_modules/*' \
    -not -path '*/__pycache__/*' -not -path '*/.venv/*' 2>/dev/null \
  | sed "s|$PROJECT_ROOT||" | sort | head -80)
\`\`\`

---

## Dependency Manifests

$(find "$PROJECT_ROOT" -maxdepth 4 \
    \( -name "package.json" -not -path "*/node_modules/*" \) \
    -o -name "requirements.txt" -o -name "requirements*.txt" \
    -o -name "go.mod" -o -name "Cargo.toml" -o -name "pom.xml" \
    -o -name "pyproject.toml" -o -name "composer.json" \
    2>/dev/null | sed "s|$PROJECT_ROOT/||" | head -20 \
  | awk '{print "- `" $0 "`"}')

---

## Technology Stack

**Detected languages (approx.):**
$(detect_languages "$PROJECT_ROOT")

---

## Test Coverage Signal

- **Test files found:** $(count_test_files "$PROJECT_ROOT")
- **Test directories:**
$(find "$PROJECT_ROOT" -maxdepth 4 -type d \
    \( -name "tests" -o -name "test" -o -name "__tests__" \
    -o -name "spec" -o -name "e2e" -o -name "integration" \) \
    -not -path "*/node_modules/*" 2>/dev/null \
  | sed "s|$PROJECT_ROOT/||" | head -10 | awk '{print "  - `" $0 "`"}')

---

## CI/CD Systems

$(detect_cicd "$PROJECT_ROOT")

---

## Infrastructure / Container Tooling

$(detect_infra "$PROJECT_ROOT")

---

## Technical Debt Indicators

| Indicator | Count |
|---|---|
| TODO | $(grep -rn "TODO" "$PROJECT_ROOT" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.py" --include="*.go" --include="*.rs" --include="*.md" --exclude-dir=".git" --exclude-dir="node_modules" 2>/dev/null | wc -l | tr -d ' ') |
| FIXME | $(grep -rn "FIXME" "$PROJECT_ROOT" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.py" --include="*.go" --include="*.rs" --include="*.md" --exclude-dir=".git" --exclude-dir="node_modules" 2>/dev/null | wc -l | tr -d ' ') |
| HACK | $(grep -rn "HACK" "$PROJECT_ROOT" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.py" --include="*.go" --include="*.rs" --exclude-dir=".git" --exclude-dir="node_modules" 2>/dev/null | wc -l | tr -d ' ') |
| XXX | $(grep -rn "XXX" "$PROJECT_ROOT" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.py" --include="*.go" --include="*.rs" --exclude-dir=".git" --exclude-dir="node_modules" 2>/dev/null | wc -l | tr -d ' ') |

---

## Security Quick-Scan

**Potential secret exposures in non-.gitignored files** (top 20):
\`\`\`
$(grep -rn \
    -e "password\s*=" -e "secret\s*=" -e "api_key\s*=" -e "apikey\s*=" \
    -e "token\s*=" -e "private_key\s*=" \
    "$PROJECT_ROOT" \
    --include="*.env" --include="*.json" --include="*.yaml" \
    --include="*.yml" --include="*.toml" --include="*.ini" \
    --exclude-dir=".git" --exclude-dir="node_modules" \
    2>/dev/null | grep -v "example\|sample\|test\|mock\|dummy\|placeholder" \
    | head -20 || echo "None found.")
\`\`\`

---

## Agentic System Snapshot (Antigravity IDE Projects)

$(if [[ -d "$PROJECT_ROOT/.agents" ]]; then
  echo "**Agents defined:**"
  find "$PROJECT_ROOT/.agents/agents" -name "*.md" 2>/dev/null \
    | sed "s|$PROJECT_ROOT/||" | head -20 | awk '{print "- `" $0 "`"}'

  echo ""
  echo "**Skills defined:**"
  find "$PROJECT_ROOT/.agents/skills" -name "SKILL.md" 2>/dev/null \
    | sed "s|$PROJECT_ROOT/||" | head -30 | awk '{print "- `" $0 "`"}'

  echo ""
  echo "**Workflows defined:**"
  find "$PROJECT_ROOT/.agents/workflows" -name "*.md" 2>/dev/null \
    | sed "s|$PROJECT_ROOT/||" | head -20 | awk '{print "- `" $0 "`"}'

  PENDING=$(grep -rn "Pending" "$PROJECT_ROOT/.agents/skills" --include="SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
  echo ""
  echo "**Pending skill modules:** $PENDING"
else
  echo "_No \`.agents/\` directory found — not an Antigravity IDE project or not in scope._"
fi)

---

## Summary (for Reviewer)

> Use this snapshot to pre-populate your architecture review findings.
> Do not treat automated counts as ground truth — verify critical findings manually.
> The security scan is a heuristic only, not a penetration test.
EOF
