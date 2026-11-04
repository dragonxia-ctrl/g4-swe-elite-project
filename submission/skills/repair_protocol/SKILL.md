---
name: repair_protocol
description: Evidence-based minimal patching, targeted testing, and safe patch submission.
---
# Repair protocol

## Before editing
- State expected behavior and observed behavior separately.
- Identify the smallest function/module responsible.
- Prefer reproducing the issue with an existing test.
- Check whether the proposed fix changes a public contract.

## During editing
- Make one logical change at a time.
- Keep the diff narrow.
- Preserve existing conventions and error semantics.
- Do not change tests to conceal a defect.

## After editing
- Re-read changed lines.
- Run the narrowest relevant test, then adjacent tests if time permits.
- Inspect `git diff --check` and `git diff`.
- Submit only after confirming the patch is non-empty and relevant.
