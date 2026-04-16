# Benchmark Artifacts

Each automated run gets its own folder inside this directory.

Recommended shape:

```text
artifacts/<run-id>/
├── run.json
├── outputs/
│   ├── baseline.json
│   └── grit.json
├── metrics/
│   └── technical.json
├── judge/
│   └── judge-result.json
└── summary/
    ├── summary.json
    └── report.md
```

Keep large screenshots or raw generated code outside git if they become noisy.
