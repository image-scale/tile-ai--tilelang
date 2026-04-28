"""Parse pytest output into per-test results."""
import re


def parse_log(log: str) -> dict[str, str]:
    """Parse test runner output into per-test results.

    Args:
        log: Full stdout+stderr output of `bash run_test.sh 2>&1`.

    Returns:
        Dict mapping test_id to status string ("PASSED", "FAILED", "SKIPPED", "ERROR").
    """
    results = {}

    # Strip ANSI escape codes
    log = re.sub(r"\x1b\[[0-9;]*m", "", log)

    # Inline lines: "tests/foo.py::TestClass::test_func[param] PASSED [ 50%]"
    # The percentage indicator anchors the end of each test result line.
    inline_pattern = re.compile(
        r"^(testing/\S+::\S[^\s]*(?:\[[^\]]*\])?)\s+(PASSED|FAILED|SKIPPED|ERROR)\s+\[\s*\d+%\]",
        re.MULTILINE,
    )
    for m in inline_pattern.finditer(log):
        test_id, status = m.group(1), m.group(2)
        results.setdefault(test_id, status)

    # Summary lines at the end: "FAILED tests/foo.py::test_bar - error message"
    # Use these to catch any tests not captured by the inline pattern.
    summary_pattern = re.compile(
        r"^(PASSED|FAILED|ERROR)\s+(testing/\S+::\S+?)(?:\s+-.*)?$",
        re.MULTILINE,
    )
    for m in summary_pattern.finditer(log):
        status, test_id = m.group(1), m.group(2)
        results.setdefault(test_id, status)

    # Collection errors: "ERROR tests/foo.py" (no "::")
    collection_error_pattern = re.compile(
        r"^ERROR\s+(testing/[^\s:]+\.py)\s*$",
        re.MULTILINE,
    )
    for m in collection_error_pattern.finditer(log):
        results.setdefault(m.group(1), "ERROR")

    return results

