#!/usr/bin/env python3
"""
Script to run tests and code quality checks.
Alternative to Makefile for systems without make.
"""
import sys
import subprocess
import argparse


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}\n")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"\n❌ {description} failed!")
        sys.exit(1)
    print(f"\n✅ {description} passed!")
    return result


def main():
    parser = argparse.ArgumentParser(description="Run tests and code quality checks")
    parser.add_argument(
        "command",
        choices=["test", "test-cov", "format", "lint", "lint-fix", "check", "all"],
        help="Command to run",
    )

    args = parser.parse_args()

    if args.command == "test":
        run_command("pytest tests/ -v", "Tests")

    elif args.command == "test-cov":
        run_command(
            "pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html",
            "Tests with coverage",
        )

    elif args.command == "format":
        run_command("black src/ tests/", "Code formatting")

    elif args.command == "lint":
        run_command("ruff check src/ tests/", "Linting")

    elif args.command == "lint-fix":
        run_command("ruff check --fix src/ tests/", "Linting with auto-fix")

    elif args.command == "check":
        run_command("black --check src/ tests/", "Format check")
        run_command("ruff check src/ tests/", "Linting")
        run_command("pytest tests/ -v", "Tests")

    elif args.command == "all":
        run_command("black src/ tests/", "Code formatting")
        run_command("ruff check --fix src/ tests/", "Linting with auto-fix")
        run_command(
            "pytest tests/ -v --cov=src --cov-report=term-missing",
            "Tests with coverage",
        )

    print("\n" + "="*60)
    print("✅ All operations completed successfully!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
