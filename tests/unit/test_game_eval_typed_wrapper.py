"""Contract tests for the GDScript source emitted by game_eval."""

from pathlib import Path

from tests.unit._gdscript_text import get_func_block

PLUGIN_ROOT = Path(__file__).resolve().parents[2] / "plugin" / "addons" / "godot_ai"
GAME_HELPER = PLUGIN_ROOT / "runtime" / "game_helper.gd"


def test_game_eval_wrapper_declares_variant_return_types() -> None:
    """Strictly typed projects reject the generated wrapper without return types."""
    source = GAME_HELPER.read_text(encoding="utf-8")
    block = get_func_block(source, "func _handle_eval(")

    assert '"func execute() -> Variant:\\n"' in block
    assert '"func %s() -> Variant:\\n"' in block
