@tool
extends McpTestSuite

const GameLogger := preload("res://addons/godot_ai/runtime/game_logger.gd")


func suite_name() -> String:
	return "game_log_queue"


func test_pending_queue_is_bounded_during_a_burst() -> void:
	var logger = GameLogger.new()
	for i in 9000:
		logger._log_message("probe line %d" % i, false)

	var pending: Array = logger.get("_pending")
	assert_true(pending.size() <= 8192, "pending queue must stay bounded during a log burst")
	assert_true(String(pending[-1][1]).ends_with("probe line 8999"), "newest line survives the trim")
	assert_false(String(pending[0][1]).ends_with("probe line 0"), "oldest lines are dropped first")


func test_clear_releases_pending_lines() -> void:
	var logger = GameLogger.new()
	logger._log_message("probe", false)
	assert_true(logger.has_pending(), "probe must enter the queue")
	logger.clear()
	assert_false(logger.has_pending(), "clear must release queued lines")
