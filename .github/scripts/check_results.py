#!/usr/bin/env python3
"""Enforce the CI pass/skip budget for a pytest JUnit XML report.

Fails the job when:
  * any test failed or errored;
  * every test skipped, which means the RIPL-4 data never resolved and the
    run proved nothing;
  * the skip count rose above the baseline, which usually means the upstream
    RIPL-4 data layout moved and coverage was silently lost.

A skip count *below* the baseline is reported but not fatal: it means the
IAEA release gained data files the suite previously had to skip. Re-baseline
SKIP_BASELINE in tests.yml when that happens.

Usage: check_results.py <report.xml> <skip-baseline>
"""

import sys
import xml.etree.ElementTree as ET


def main(path: str, baseline: int) -> int:
    root = ET.parse(path).getroot()
    suites = root.findall("testsuite") if root.tag == "testsuites" else [root]

    tests = sum(int(s.get("tests", 0)) for s in suites)
    failures = sum(int(s.get("failures", 0)) for s in suites)
    errors = sum(int(s.get("errors", 0)) for s in suites)
    skipped = sum(int(s.get("skipped", 0)) for s in suites)
    ran = tests - skipped

    print(f"tests={tests} ran={ran} failures={failures} "
          f"errors={errors} skipped={skipped} (baseline {baseline})")

    ok = True

    if failures or errors:
        print(f"::error::{failures} failure(s) and {errors} error(s); "
              f"a release requires a clean run")
        ok = False

    if tests == 0:
        print("::error::no tests were collected")
        ok = False
    elif ran == 0:
        print("::error::every test skipped - the RIPL-4 database did not "
              "resolve, so this run proves nothing")
        ok = False

    if skipped > baseline:
        print(f"::error::skips rose to {skipped} from a baseline of "
              f"{baseline}; the upstream RIPL-4 layout may have changed and "
              f"coverage been lost silently")
        ok = False
    elif skipped < baseline:
        print(f"::notice::skips fell to {skipped} from a baseline of "
              f"{baseline}; upstream likely added data files. Lower "
              f"SKIP_BASELINE in tests.yml to lock the gain in.")

    print("RESULT:", "pass" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], int(sys.argv[2])))
