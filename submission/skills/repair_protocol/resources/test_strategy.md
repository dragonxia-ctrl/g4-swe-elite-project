# Test strategy

1. Prefer a single test node or test file that exercises the reported behavior.
2. If the project uses pytest, inspect `pytest.ini`, `pyproject.toml`, and test naming before choosing flags.
3. If tests require unavailable optional services, distinguish environment failure from code failure.
4. Run regression tests around the changed API when budget allows.
5. Never infer success from a command that timed out, was interrupted, or did not execute the intended test.
