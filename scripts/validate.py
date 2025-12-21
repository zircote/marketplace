#!/usr/bin/env python3
"""
Plugin validation script for CI/local parity.

Performs the same validations as .github/workflows/ci.yml:
- JSON syntax validation
- Required fields check
- Semantic version validation
- README existence check

Usage:
    python scripts/validate.py [--check=CHECK] [--verbose]

Checks:
    all         Run all checks (default)
    json        Validate JSON syntax only
    fields      Check required fields only
    version     Validate semantic versions only
    readme      Check README files exist only
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Configuration
PLUGINS = ['zircote', 'gh', 'nsip', 'datadog', 'document-skills']
REQUIRED_FIELDS = ['name', 'version', 'description', 'author', 'license']
AUTHOR_FIELDS = ['name', 'email', 'url']
SEMVER_PATTERN = r'^\d+\.\d+\.\d+$'


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

    @classmethod
    def disable(cls):
        cls.GREEN = cls.RED = cls.YELLOW = cls.BLUE = cls.RESET = cls.BOLD = ''


def ok(msg: str) -> None:
    print(f"  {Colors.GREEN}✅{Colors.RESET} {msg}")


def fail(msg: str) -> None:
    print(f"  {Colors.RED}❌{Colors.RESET} {msg}")


def warn(msg: str) -> None:
    print(f"  {Colors.YELLOW}⚠️{Colors.RESET} {msg}")


def header(msg: str) -> None:
    print(f"\n{Colors.BOLD}{Colors.BLUE}{msg}{Colors.RESET}")


def validate_json(verbose: bool = False) -> list[str]:
    """Validate JSON syntax for all plugin.json files."""
    header("Validating JSON syntax...")
    errors = []

    for plugin in PLUGINS:
        path = Path(f'plugins/{plugin}/.claude-plugin/plugin.json')
        try:
            with open(path) as f:
                json.load(f)
            ok(f"{plugin}/plugin.json")
        except FileNotFoundError:
            fail(f"{plugin}/plugin.json not found")
            errors.append(f"{plugin}: plugin.json not found")
        except json.JSONDecodeError as e:
            fail(f"{plugin}/plugin.json - invalid JSON: {e}")
            errors.append(f"{plugin}: invalid JSON - {e}")

    # Marketplace manifest
    marketplace_path = Path('.claude-plugin/marketplace.json')
    try:
        with open(marketplace_path) as f:
            json.load(f)
        ok("marketplace.json")
    except FileNotFoundError:
        fail("marketplace.json not found")
        errors.append("marketplace.json not found")
    except json.JSONDecodeError as e:
        fail(f"marketplace.json - invalid JSON: {e}")
        errors.append(f"marketplace.json: invalid JSON - {e}")

    return errors


def validate_fields(verbose: bool = False) -> list[str]:
    """Check required fields in plugin.json files."""
    header("Checking required fields...")
    errors = []

    for plugin in PLUGINS:
        path = Path(f'plugins/{plugin}/.claude-plugin/plugin.json')
        plugin_errors = []

        try:
            with open(path) as f:
                data = json.load(f)

            # Check top-level required fields
            for field in REQUIRED_FIELDS:
                if field not in data:
                    plugin_errors.append(f"missing '{field}'")

            # Check author sub-fields
            if 'author' in data and isinstance(data['author'], dict):
                for field in AUTHOR_FIELDS:
                    if field not in data['author']:
                        plugin_errors.append(f"author missing '{field}'")

            if plugin_errors:
                fail(f"{plugin}: {', '.join(plugin_errors)}")
                errors.extend([f"{plugin}: {e}" for e in plugin_errors])
            else:
                ok(f"{plugin} - all required fields present")

        except FileNotFoundError:
            fail(f"{plugin}: plugin.json not found")
            errors.append(f"{plugin}: plugin.json not found")
        except json.JSONDecodeError:
            # Already caught in JSON validation
            pass

    return errors


def validate_versions(verbose: bool = False) -> list[str]:
    """Validate semantic version format."""
    header("Validating semantic versions...")
    errors = []

    for plugin in PLUGINS:
        path = Path(f'plugins/{plugin}/.claude-plugin/plugin.json')

        try:
            with open(path) as f:
                data = json.load(f)

            version = data.get('version', '')
            if not re.match(SEMVER_PATTERN, version):
                fail(f"{plugin}: invalid version '{version}' (expected X.Y.Z)")
                errors.append(f"{plugin}: invalid version '{version}'")
            else:
                ok(f"{plugin} v{version}")

        except (FileNotFoundError, json.JSONDecodeError):
            # Already caught in other validations
            pass

    return errors


def validate_readme(verbose: bool = False) -> list[str]:
    """Check README.md files exist for all plugins."""
    header("Checking README files...")
    errors = []

    for plugin in PLUGINS:
        path = Path(f'plugins/{plugin}/README.md')
        if path.exists():
            ok(f"{plugin}/README.md exists")
        else:
            fail(f"{plugin}/README.md missing")
            errors.append(f"{plugin}: README.md not found")

    return errors


def validate_commands_exist(verbose: bool = False) -> list[str]:
    """Validate that all referenced command files exist."""
    header("Validating command file references...")
    errors = []

    for plugin in PLUGINS:
        manifest_path = Path(f'plugins/{plugin}/.claude-plugin/plugin.json')

        try:
            with open(manifest_path) as f:
                data = json.load(f)

            commands = data.get('commands', [])
            plugin_dir = Path(f'plugins/{plugin}')

            for cmd_path in commands:
                # Resolve relative path
                full_path = plugin_dir / cmd_path.lstrip('./')
                if not full_path.exists():
                    fail(f"{plugin}: command file not found: {cmd_path}")
                    errors.append(f"{plugin}: missing command {cmd_path}")
                elif verbose:
                    ok(f"{plugin}: {cmd_path}")

            if not errors and commands:
                ok(f"{plugin}: {len(commands)} command(s) verified")
            elif not commands:
                ok(f"{plugin}: no commands defined")

        except (FileNotFoundError, json.JSONDecodeError):
            pass

    return errors


def validate_agents_exist(verbose: bool = False) -> list[str]:
    """Validate that all referenced agent files exist."""
    header("Validating agent file references...")
    errors = []

    for plugin in PLUGINS:
        manifest_path = Path(f'plugins/{plugin}/.claude-plugin/plugin.json')

        try:
            with open(manifest_path) as f:
                data = json.load(f)

            agents = data.get('agents', [])
            plugin_dir = Path(f'plugins/{plugin}')

            for agent_path in agents:
                full_path = plugin_dir / agent_path.lstrip('./')
                if not full_path.exists():
                    fail(f"{plugin}: agent file not found: {agent_path}")
                    errors.append(f"{plugin}: missing agent {agent_path}")
                elif verbose:
                    ok(f"{plugin}: {agent_path}")

            if not errors and agents:
                ok(f"{plugin}: {len(agents)} agent(s) verified")
            elif not agents:
                ok(f"{plugin}: no agents defined")

        except (FileNotFoundError, json.JSONDecodeError):
            pass

    return errors


def validate_skills_exist(verbose: bool = False) -> list[str]:
    """Validate that all referenced skill files exist."""
    header("Validating skill file references...")
    errors = []

    for plugin in PLUGINS:
        manifest_path = Path(f'plugins/{plugin}/.claude-plugin/plugin.json')

        try:
            with open(manifest_path) as f:
                data = json.load(f)

            skills = data.get('skills', [])
            plugin_dir = Path(f'plugins/{plugin}')

            for skill_path in skills:
                full_path = plugin_dir / skill_path.lstrip('./')
                if not full_path.exists():
                    fail(f"{plugin}: skill file not found: {skill_path}")
                    errors.append(f"{plugin}: missing skill {skill_path}")
                elif verbose:
                    ok(f"{plugin}: {skill_path}")

            if not errors and skills:
                ok(f"{plugin}: {len(skills)} skill(s) verified")
            elif not skills:
                ok(f"{plugin}: no skills defined")

        except (FileNotFoundError, json.JSONDecodeError):
            pass

    return errors


CHECK_MAP = {
    'json': validate_json,
    'fields': validate_fields,
    'version': validate_versions,
    'readme': validate_readme,
    'commands': validate_commands_exist,
    'agents': validate_agents_exist,
    'skills': validate_skills_exist,
}


def main():
    parser = argparse.ArgumentParser(
        description='Validate Claude Code marketplace plugins',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Checks available:
  all       Run all checks (default)
  json      Validate JSON syntax only
  fields    Check required fields only
  version   Validate semantic versions only
  readme    Check README files exist only
  commands  Validate command file references
  agents    Validate agent file references
  skills    Validate skill file references
"""
    )
    parser.add_argument(
        '--check', '-c',
        choices=['all'] + list(CHECK_MAP.keys()),
        default='all',
        help='Which check to run (default: all)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )

    args = parser.parse_args()

    if args.no_color:
        Colors.disable()

    all_errors = []

    if args.check == 'all':
        for check_fn in CHECK_MAP.values():
            errors = check_fn(args.verbose)
            all_errors.extend(errors)
    else:
        all_errors = CHECK_MAP[args.check](args.verbose)

    # Summary
    print()
    if all_errors:
        print(f"{Colors.RED}{Colors.BOLD}Validation failed with {len(all_errors)} error(s){Colors.RESET}")
        sys.exit(1)
    else:
        print(f"{Colors.GREEN}{Colors.BOLD}All validations passed ✅{Colors.RESET}")
        sys.exit(0)


if __name__ == '__main__':
    main()
