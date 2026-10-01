"""Compiler-backed coverage for the generated game_eval wrapper (#1119)."""

import shutil
import subprocess
from pathlib import Path

import pytest

from tests.integration._self_update_fixture import PLUGIN_ROOT, godot_bin_or_skip

pytestmark = pytest.mark.editor


def test_generated_game_eval_wrapper_compiles_with_untyped_declaration_as_error(
    tmp_path: Path,
) -> None:
    """The generated wrapper must compile when untyped declarations are errors."""
    godot = godot_bin_or_skip()
    project = tmp_path / "typed-eval-project"
    project.mkdir()
    (project / "project.godot").write_text(
        """\
config_version=5

[application]
config/name="typed-eval-wrapper-check"

[debug]
gdscript/warnings/untyped_declaration=2
""",
        encoding="utf-8",
    )

    addons = project / "addons"
    addons.mkdir()
    shutil.copytree(PLUGIN_ROOT, addons / "godot_ai")

    (project / "check.gd").write_text(
        """\
extends SceneTree

const GameHelper := preload("res://addons/godot_ai/runtime/game_helper.gd")


func _initialize() -> void:
	var source := GameHelper._build_eval_script_source("_mcp_run_test", "return 1")
	var script := GDScript.new()
	script.source_code = source
	var error := script.reload()
	if error != OK:
		push_error("generated game_eval wrapper failed to compile: %d" % error)
		quit(1)
		return
	print("GAME_EVAL_WRAPPER_COMPILES")
	quit(0)
""",
        encoding="utf-8",
    )

    result = subprocess.run(
        [godot, "--headless", "--path", str(project), "--script", "res://check.gd"],
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "GAME_EVAL_WRAPPER_COMPILES" in result.stdout
