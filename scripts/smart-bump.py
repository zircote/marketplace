#!/usr/bin/env python3
"""
Smart version bumper for marketplace plugins.

Detects which plugins have changes since last release and bumps their versions.
Uses bump-my-version for the actual version bumping.

Usage:
    python scripts/smart-bump.py [patch|minor|major]
    python scripts/smart-bump.py --plugin=gh patch
    python scripts/smart-bump.py --dry-run patch
"""

import argparse
import subprocess
import sys
from pathlib import Path

PLUGINS_DIR = Path(__file__).parent.parent / "plugins"
PLUGINS = ["zircote", "gh", "nsip", "datadog", "document-skills"]


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, check=check)


def get_last_tag(plugin: str) -> str | None:
    """Get the last release tag for a plugin."""
    result = run(
        ["git", "tag", "--list", f"{plugin}-v*", "--sort=-v:refname"],
        check=False
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    return result.stdout.strip().split("\n")[0]


def has_changes_since(plugin: str, tag: str | None) -> bool:
    """Check if a plugin has changes since the given tag."""
    plugin_path = f"plugins/{plugin}"

    if tag is None:
        # No previous tag, consider as having changes
        return True

    result = run(
        ["git", "diff", "--name-only", tag, "HEAD", "--", plugin_path],
        check=False
    )
    return bool(result.stdout.strip())


def get_changed_plugins() -> list[str]:
    """Get list of plugins with changes since their last release."""
    changed = []
    for plugin in PLUGINS:
        last_tag = get_last_tag(plugin)
        if has_changes_since(plugin, last_tag):
            changed.append(plugin)
    return changed


def bump_plugin(plugin: str, part: str, dry_run: bool = False) -> bool:
    """Bump version for a specific plugin."""
    plugin_dir = PLUGINS_DIR / plugin

    if not (plugin_dir / ".bumpversion.toml").exists():
        print(f"  ⚠️  No .bumpversion.toml found for {plugin}")
        return False

    cmd = ["bump-my-version", "bump", part]
    if dry_run:
        cmd.append("--dry-run")
        cmd.append("--verbose")

    result = run(cmd, cwd=plugin_dir, check=False)

    if result.returncode != 0:
        print(f"  ❌ Failed to bump {plugin}")
        print(f"     {result.stderr}")
        return False

    if dry_run:
        print(f"  🔍 {plugin}: would bump {part}")
        if result.stdout:
            for line in result.stdout.strip().split("\n")[-5:]:
                print(f"     {line}")
    else:
        print(f"  ✅ {plugin}: bumped {part}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Smart version bumper for marketplace plugins"
    )
    parser.add_argument(
        "part",
        choices=["patch", "minor", "major"],
        help="Version part to bump"
    )
    parser.add_argument(
        "--plugin",
        help="Bump specific plugin only"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Bump all plugins, not just changed ones"
    )

    args = parser.parse_args()

    print(f"🔄 Smart Bump: {args.part}")
    print()

    if args.plugin:
        if args.plugin not in PLUGINS:
            print(f"❌ Unknown plugin: {args.plugin}")
            print(f"   Available: {', '.join(PLUGINS)}")
            sys.exit(1)
        plugins_to_bump = [args.plugin]
        print(f"📦 Bumping specific plugin: {args.plugin}")
    elif args.all:
        plugins_to_bump = PLUGINS
        print(f"📦 Bumping all {len(plugins_to_bump)} plugins")
    else:
        plugins_to_bump = get_changed_plugins()
        if not plugins_to_bump:
            print("✨ No plugins have changes since their last release")
            sys.exit(0)
        print(f"📦 Plugins with changes: {', '.join(plugins_to_bump)}")

    print()

    success = True
    for plugin in plugins_to_bump:
        if not bump_plugin(plugin, args.part, args.dry_run):
            success = False

    print()
    if args.dry_run:
        print("🔍 Dry run complete. No changes made.")
    elif success:
        print("✅ All bumps complete!")
        print()
        print("Next steps:")
        print("  git push --follow-tags")
    else:
        print("⚠️  Some bumps failed. Check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
