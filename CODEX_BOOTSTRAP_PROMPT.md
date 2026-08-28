# Codex Bootstrap Prompt

Paste the following into Codex while the repository
`angeltitts/kinetic-energy-storage-rd` is selected:

---

You are bootstrapping an autonomous engineering R&D repository.

Use the files from the supplied `kinetic-energy-storage-rd-autonomous` package
as the intended repository state.

Tasks:

1. Create a new branch named `phase0-autonomous-engineering`.
2. Add or replace the package files exactly in their corresponding repository
   paths.
3. Preserve the existing root engineering documents unless the package
   explicitly supplies a replacement.
4. Run:
   - `python -m pip install -r requirements.txt`
   - `pytest -q`
   - `python models/system_model.py`
   - `python models/parameter_sweep.py`
5. Verify that `results/baseline.json` and `results/phase0_sweep.csv` are
   generated.
6. Do NOT add an API key to the repository.
7. Do NOT enable auto-merge.
8. Commit the changes with:
   `Bootstrap bounded autonomous engineering R&D loop`
9. Push the branch and open a pull request into `main`.
10. In the PR body, summarize:
    - tests run
    - deterministic baseline result
    - files added
    - GitHub secret still required: `OPENAI_API_KEY`
    - optional repository variable: `OPENAI_MODEL`

Important architectural rules:
- One agent task per scheduled run.
- No direct autonomous writes to `main`.
- No auto-merge.
- Human review required for every autonomous design change.
- Physical high-energy prototype/testing work is outside the autonomous
  workflow and requires human engineering/safety review.
- A result that falsifies DSHC is acceptable and must not be suppressed.

After creating the PR, stop. Do not merge it yourself.

---
