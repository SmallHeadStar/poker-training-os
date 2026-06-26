# Tests

Current V0.1 test priority follows the H2N4 Bridge route:

1. Session manifest validation tests.
2. H2N4 export folder contract tests.
3. CSV/YAML/manual fallback ingest tests.
4. Source label propagation tests.
5. Output file rendering tests.
6. Missing-export behavior tests.
7. Dashboard smoke tests, later.

Native parser, tagging, stat, and detector tests remain as fallback/later-route folders.

Run all tests:

```bash
python -m pytest
```
