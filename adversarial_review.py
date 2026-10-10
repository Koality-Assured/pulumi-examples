#!/usr/bin/env python3
"""Adversarial Security & Quality Auditor for Koality-Assured/pulumi-examples.

Performs strict adversarial validation across the repository:
1. Leak Scan: Scans every file for prohibited terms, internal company/studio names,
   real AWS account numbers, employee names, proprietary project names, internal URLs,
   and hardcoded absolute filesystem paths.
2. Syntax Validation: Ensures 100% valid syntax across all YAML, Python, and JSON files.
3. Execution Policy Enforcement: Guarantees no live GitHub Actions workflows exist,
   enforcing the directive that this repository provides clean reference examples only.
4. Documentation Coverage: Validates that all example directories maintain clear,
   navigable README files.
"""

import ast
import json
import os
import sys
from pathlib import Path
import yaml

# Sensitive identifiers that MUST NOT appear anywhere in public code or documentation
FORBIDDEN_TERMS = [
    # Real AWS account IDs from source repositories
    "077167033847", "682316754057", "026296209333", "660961353139",
    "057099253745", "648259795211", "688469372830", "412019586027",
    "961469660534", "450779680578", "629495089425", "673222099655",
    "992382745564", "135728714311",

    # Corporate / proprietary entity names
    "take-two", "taketwo", "2k-sec-iac", "2ksecurity", "2k.com",
    "autoris", "pixelgun", "franklin", "symbiote", "dataexile",

    # Internal domains and directory identifiers
    "awsapps.com", "d-90670a9c56",

    # Local filesystem paths
    "c:\\code\\other2k", "c:/code/other2k",
    "c:\\users\\", "c:/users/",

    # Ciphertext secret examples
    "AAABAOC+cMRNeKMjmQUtGK210lN3woKmjyIvZHQwR07z12h/OXMmJ37GVbnO+w8vlYQ3wRwxBLVEZVYAhw+YSRDAbrTRlbmL",
]

REPO_ROOT = Path(__file__).resolve().parent


def audit_leaks() -> list[tuple[str, str]]:
    """Scans all repository files for forbidden sensitive terms."""
    findings = []
    for root, dirs, files in os.walk(REPO_ROOT):
        # Exclude version control and cache artifacts
        for skip in [".git", ".pytest_cache", "__pycache__", "node_modules", "venv", ".venv"]:
            if skip in dirs:
                dirs.remove(skip)

        for f in files:
            # Self-exclusion
            if f == "adversarial_review.py":
                continue

            fp = Path(root) / f
            rel = fp.relative_to(REPO_ROOT)

            try:
                content = fp.read_text(encoding="utf-8", errors="ignore").lower()
                for term in FORBIDDEN_TERMS:
                    if term.lower() in content:
                        findings.append((str(rel), term))
            except Exception as e:
                findings.append((str(rel), f"File read error: {e}"))

    return findings


def audit_syntax() -> list[tuple[str, str]]:
    """Validates syntax across YAML, Python, and JSON files."""
    syntax_errors = []
    for root, dirs, files in os.walk(REPO_ROOT):
        for skip in [".git", ".pytest_cache", "__pycache__", "node_modules", "venv", ".venv"]:
            if skip in dirs:
                dirs.remove(skip)

        for f in files:
            fp = Path(root) / f
            rel = fp.relative_to(REPO_ROOT)

            # YAML validation
            if f.endswith((".yaml", ".yml")):
                try:
                    class SafeLoaderIgnoreUnknown(yaml.SafeLoader):
                        pass

                    def any_constructor(loader, tag_suffix, node):
                        if isinstance(node, yaml.ScalarNode):
                            return loader.construct_scalar(node)
                        elif isinstance(node, yaml.SequenceNode):
                            return loader.construct_sequence(node)
                        elif isinstance(node, yaml.MappingNode):
                            return loader.construct_mapping(node)
                        return None

                    SafeLoaderIgnoreUnknown.add_multi_constructor("!", any_constructor)

                    with open(fp, "r", encoding="utf-8") as yf:
                        yaml.load(yf, Loader=SafeLoaderIgnoreUnknown)
                except Exception as e:
                    syntax_errors.append((str(rel), f"YAML Parse Error: {e}"))

            # Python syntax validation
            elif f.endswith(".py") and f != "adversarial_review.py":
                try:
                    with open(fp, "r", encoding="utf-8") as pf:
                        ast.parse(pf.read(), filename=str(fp))
                except Exception as e:
                    syntax_errors.append((str(rel), f"Python Syntax Error: {e}"))

            # JSON syntax validation
            elif f.endswith(".json") and not f.endswith("package-lock.json"):
                try:
                    with open(fp, "r", encoding="utf-8") as jf:
                        json.load(jf)
                except Exception as e:
                    syntax_errors.append((str(rel), f"JSON Parse Error: {e}"))

    return syntax_errors


def audit_execution_policy() -> list[str]:
    """Ensures no live GitHub Actions workflows exist per user instruction."""
    violations = []
    gh_workflows = REPO_ROOT / ".github" / "workflows"
    if gh_workflows.exists() and any(gh_workflows.iterdir()):
        violations.append(
            f"Found live GitHub Actions workflows in {gh_workflows}. "
            "Policy strictly prohibits real running workflows in this example repository."
        )
    return violations


def audit_documentation_coverage() -> list[str]:
    """Verifies that every example domain and subdirectory includes a README."""
    missing_docs = []
    for root, dirs, files in os.walk(REPO_ROOT):
        for skip in [".git", ".pytest_cache", "__pycache__", "node_modules", "venv", ".venv"]:
            if skip in dirs:
                dirs.remove(skip)

        rel = Path(root).relative_to(REPO_ROOT)
        # Skip root level and leaf files
        if str(rel) == ".":
            continue

        # If a directory contains Pulumi.yaml or template.yaml or __main__.py, require a README.md
        if any(f in files for f in ["Pulumi.yaml", "template.yaml", "__main__.py"]):
            if "README.md" not in files:
                missing_docs.append(str(rel))

    return missing_docs


def main() -> int:
    print("=" * 80)
    print(" ADVERSARIAL SECURITY & QUALITY AUDITOR: Koality-Assured/pulumi-examples")
    print("=" * 80)

    # 1. Leak Scan
    leaks = audit_leaks()
    if leaks:
        print(f"\n[FAIL] Found {len(leaks)} prohibited sensitive strings / identifiers:")
        for rel, term in leaks:
            print(f"  - {rel}: contains '{term}'")
    else:
        print("\n[PASS] Zero internal account numbers, company names, or sensitive terms found.")

    # 2. Syntax Validation
    syntax_issues = audit_syntax()
    if syntax_issues:
        print(f"\n[FAIL] Found {len(syntax_issues)} syntax errors:")
        for rel, err in syntax_issues:
            print(f"  - {rel}: {err}")
    else:
        print("[PASS] 100% of YAML, Python, and JSON files parsed cleanly without syntax errors.")

    # 3. Execution Policy Enforcement
    policy_violations = audit_execution_policy()
    if policy_violations:
        print(f"\n[FAIL] Execution policy violations detected:")
        for viol in policy_violations:
            print(f"  - {viol}")
    else:
        print("[PASS] Zero live GitHub Actions workflows detected (Reference example policy verified).")

    # 4. Documentation Coverage
    missing_docs = audit_documentation_coverage()
    if missing_docs:
        print(f"\n[FAIL] Missing README.md in {len(missing_docs)} example directories:")
        for d in missing_docs:
            print(f"  - {d}")
    else:
        print("[PASS] 100% documentation coverage: Every example directory maintains a README.md.")

    print("\n" + "=" * 80)
    if leaks or syntax_issues or policy_violations or missing_docs:
        print(" ADVERSARIAL AUDIT STATUS: FAILED")
        print("=" * 80)
        return 1

    print(" ADVERSARIAL AUDIT STATUS: ALL CHECKS PASSED (MERGE READY)")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
