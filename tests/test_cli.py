"""Tests für den CLI-Einstiegspunkt und seine Verdrahtung."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(SRC_DIR) + (os.pathsep + existing if existing else "")
    return subprocess.run(
        [sys.executable, "-m", "csvstat", *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_help_exits_zero_and_lists_all_options() -> None:
    result = run_cli("--help")

    assert result.returncode == 0
    for option in ("--delimiter", "--columns", "--json"):
        assert option in result.stdout, f"{option} fehlt in der Hilfe"


def test_main_returns_int_after_parsing() -> None:
    from csvstat import cli

    with pytest.raises(SystemExit) as excinfo:
        cli.main(["--help"])

    assert excinfo.value.code == 0


def test_cli_module_imports_its_wired_modules() -> None:
    from csvstat import cli, reading, render, render_json, select, stats

    assert cli.reading is reading
    assert cli.select is select
    assert cli.stats is stats
    assert cli.render is render
    assert cli.render_json is render_json


def test_main_is_callable_with_default_argv() -> None:
    from csvstat import cli

    assert callable(cli.main)
