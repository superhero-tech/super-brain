# Evals - second-brain-setup

Three test fixtures. Each holds canonical answers (Inputs) and expected assertions (Expected output).

## How to run

1. Open a fresh AI session with access to the vault
2. Clear (or stash) the existing `8-System/about.md`
3. Run the `second-brain-setup` skill
4. Feed it the answers from the fixture's `## Inputs` section
5. Check the output against the assertions in `## Expected output`

## Fixtures

| Fixture | Path | Scenario |
|---|---|---|
| `fixture-assessment-gallup.md` | A (assessment) | Pasted Gallup Top 5 results plus a short follow-up |
| `fixture-interview-solo.md` | B (interview) | Full interview, solo operator pre-PMF |
| `fixture-rerun-scope-change.md` | Re-run | Existing about.md plus a role change, delta expected |
