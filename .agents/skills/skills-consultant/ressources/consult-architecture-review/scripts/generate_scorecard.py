#!/usr/bin/env python3
"""
generate_scorecard.py
Generates a structured Architecture Review Scorecard in Markdown format.

Usage:
    python3 generate_scorecard.py \
        --project "My Project" \
        --reviewer "Consultant Agent" \
        --scores "Structural Integrity:4:Clean modular layout" \
                 "Dependency Health:3:Some stale deps" \
                 "Scalability & Performance:2:N+1 patterns found" \
                 "Maintainability & Evolvability:4:Good test coverage" \
                 "Security Posture:3:Auth centralized, CORS too open" \
                 "Operational Readiness:2:No CI pipeline" \
                 "Agent Architecture Quality:5:Excellent skill modularity"

    Or pipe from stdin for agent-generated input:
        echo '...' | python3 generate_scorecard.py --from-stdin

Output:
    Prints the scorecard Markdown to stdout.
    Pipe to a file:
        python3 generate_scorecard.py ... > .tmp/scorecard.md
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


# ─── Domain Model ──────────────────────────────────────────────────────────────

STANDARD_DIMENSIONS: list[str] = [
    "Structural Integrity",
    "Dependency Health",
    "Scalability & Performance",
    "Maintainability & Evolvability",
    "Security Posture",
    "Operational Readiness",
    "Agent Architecture Quality",  # Agentic-systems-specific dimension
]

SCORE_LABELS: dict[int, str] = {
    1: "Critical — Immediate action needed",
    2: "Significant gaps — High priority",
    3: "Adequate — Room for improvement",
    4: "Good — Follows best practices",
    5: "Excellent — Reference quality",
}

SCORE_EMOJIS: dict[int, str] = {1: "🔴", 2: "🟠", 3: "🟡", 4: "🟢", 5: "⭐"}


@dataclass
class DimensionScore:
    name: str
    score: int
    note: str = ""

    @property
    def label(self) -> str:
        return SCORE_LABELS.get(self.score, "Unknown")

    @property
    def emoji(self) -> str:
        return SCORE_EMOJIS.get(self.score, "❓")

    def validate(self) -> None:
        if not 1 <= self.score <= 5:
            raise ValueError(
                f"Score for '{self.name}' must be between 1 and 5, got {self.score}"
            )


@dataclass
class Scorecard:
    project_name: str
    reviewer: str = "Consultant Agent"
    date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    dimensions: list[DimensionScore] = field(default_factory=list)
    executive_summary: str = ""
    next_steps: list[str] = field(default_factory=list)

    @property
    def average_score(self) -> float:
        if not self.dimensions:
            return 0.0
        return sum(d.score for d in self.dimensions) / len(self.dimensions)

    @property
    def overall_rating(self) -> str:
        avg = self.average_score
        if avg >= 4.5:
            return "⭐ Excellent"
        elif avg >= 3.5:
            return "🟢 Good"
        elif avg >= 2.5:
            return "🟡 Adequate"
        elif avg >= 1.5:
            return "🟠 Needs Improvement"
        else:
            return "🔴 Critical"

    @property
    def critical_dimensions(self) -> list[DimensionScore]:
        return [d for d in self.dimensions if d.score <= 2]

    def to_markdown(self) -> str:
        lines: list[str] = []

        # Header
        lines += [
            f"# Architecture Review Scorecard: {self.project_name}",
            "",
            f"> **Reviewer:** {self.reviewer}  ",
            f"> **Date:** {self.date}  ",
            f"> **Overall Rating:** {self.overall_rating} ({self.average_score:.1f}/5.0)",
            "",
            "---",
            "",
        ]

        # Executive Summary
        if self.executive_summary:
            lines += [
                "## Executive Summary",
                "",
                self.executive_summary,
                "",
                "---",
                "",
            ]

        # Scorecard Table
        lines += [
            "## Scorecard",
            "",
            "| Dimension | Score | Rating | Note |",
            "|---|---|---|---|",
        ]
        for dim in self.dimensions:
            score_display = f"{dim.emoji} {dim.score}/5"
            lines.append(f"| {dim.name} | {score_display} | {dim.label} | {dim.note} |")

        lines += [
            "",
            f"**Average Score:** {self.average_score:.1f}/5.0 — {self.overall_rating}",
            "",
        ]

        # Critical findings callout
        if self.critical_dimensions:
            lines += [
                "---",
                "",
                "## 🔴 Dimensions Requiring Immediate Attention",
                "",
            ]
            for dim in self.critical_dimensions:
                lines.append(f"- **{dim.name}** (Score: {dim.score}/5) — {dim.note}")
            lines.append("")

        # Next Steps
        if self.next_steps:
            lines += [
                "---",
                "",
                "## Recommended Next Steps",
                "",
            ]
            for i, step in enumerate(self.next_steps, 1):
                lines.append(f"{i}. {step}")
            lines.append("")

        # Scoring Guide Footer
        lines += [
            "---",
            "",
            "## Scoring Reference",
            "",
            "| Score | Symbol | Meaning |",
            "|---|---|---|",
        ]
        for score in range(1, 6):
            lines.append(
                f"| {score} | {SCORE_EMOJIS[score]} | {SCORE_LABELS[score]} |"
            )

        return "\n".join(lines)


# ─── Parsing ───────────────────────────────────────────────────────────────────

def parse_score_entry(entry: str) -> DimensionScore:
    """
    Parse a score entry in the format:
        "Dimension Name:score:optional note"
    Examples:
        "Structural Integrity:4:Clean modular layout"
        "Security Posture:2"
    """
    parts = entry.split(":", 2)
    if len(parts) < 2:
        raise ValueError(
            f"Invalid score entry '{entry}'. "
            "Expected format: 'Dimension Name:score[:optional note]'"
        )
    name = parts[0].strip()
    try:
        score = int(parts[1].strip())
    except ValueError:
        raise ValueError(f"Score in '{entry}' must be an integer, got '{parts[1]}'")
    note = parts[2].strip() if len(parts) > 2 else ""
    dim = DimensionScore(name=name, score=score, note=note)
    dim.validate()
    return dim


def parse_from_stdin() -> list[DimensionScore]:
    """
    Parse score entries from stdin, one per line.
    Lines starting with '#' are treated as comments and ignored.
    """
    dimensions: list[DimensionScore] = []
    for line in sys.stdin:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        dimensions.append(parse_score_entry(line))
    return dimensions


def build_default_scorecard(project_name: str, reviewer: str) -> Scorecard:
    """
    Returns an empty scorecard pre-populated with all 7 standard dimensions
    at score 0 (placeholder). Useful for the agent to fill in interactively.
    """
    dimensions = [
        DimensionScore(name=dim, score=3, note="[To be assessed]")
        for dim in STANDARD_DIMENSIONS
    ]
    return Scorecard(
        project_name=project_name,
        reviewer=reviewer,
        dimensions=dimensions,
        executive_summary="[Executive summary to be filled in after review]",
        next_steps=["[Prioritized action item 1]", "[Prioritized action item 2]"],
    )


# ─── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate an Architecture Review Scorecard in Markdown format.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--project", default="Unnamed Project", help="Name of the reviewed project."
    )
    parser.add_argument(
        "--reviewer", default="Consultant Agent", help="Reviewer name or identifier."
    )
    parser.add_argument(
        "--scores",
        nargs="+",
        metavar="DIMENSION:SCORE[:NOTE]",
        help='Score entries in "Dimension Name:score:note" format.',
    )
    parser.add_argument(
        "--summary",
        default="",
        help="Executive summary text.",
    )
    parser.add_argument(
        "--next-steps",
        nargs="+",
        metavar="STEP",
        help="Recommended next steps (one per arg).",
    )
    parser.add_argument(
        "--from-stdin",
        action="store_true",
        help="Read score entries from stdin (one per line, format: Name:score:note).",
    )
    parser.add_argument(
        "--template",
        action="store_true",
        help="Output an empty template scorecard with all standard dimensions.",
    )
    args = parser.parse_args()

    if args.template:
        scorecard = build_default_scorecard(args.project, args.reviewer)
        print(scorecard.to_markdown())
        return

    dimensions: list[DimensionScore] = []

    if args.from_stdin:
        dimensions = parse_from_stdin()
    elif args.scores:
        for entry in args.scores:
            dimensions.append(parse_score_entry(entry))
    else:
        # No scores provided — output template
        print(
            "No scores provided. Outputting template. "
            "Use --scores or --from-stdin to supply actual scores.\n",
            file=sys.stderr,
        )
        scorecard = build_default_scorecard(args.project, args.reviewer)
        print(scorecard.to_markdown())
        return

    scorecard = Scorecard(
        project_name=args.project,
        reviewer=args.reviewer,
        dimensions=dimensions,
        executive_summary=args.summary,
        next_steps=args.next_steps or [],
    )
    print(scorecard.to_markdown())


if __name__ == "__main__":
    main()
