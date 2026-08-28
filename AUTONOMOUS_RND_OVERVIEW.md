# Autonomous R&D Layer

This layer turns the static engineering repository into a bounded, persistent
research loop.

## Every scheduled cycle

1. Run analytical model tests.
2. Recompute baseline and parameter sweep.
3. Read the project source-of-truth documents.
4. Select the highest-impact / lowest-confidence claim.
5. Ask the Chief Engineer model to review one uncertainty only.
6. Write a report to `results/latest_agent_report.md`.
7. Push the report and deterministic outputs to a temporary branch.
8. Open a pull request.
9. Stop.

There is intentionally:
- no automatic merge
- no autonomous hardware fabrication
- no unlimited recursive model loop
- no silent mutation of assumptions
