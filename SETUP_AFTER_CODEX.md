# Setup After Codex Creates the PR

After reviewing and merging the bootstrap PR:

1. In GitHub repository settings, create an Actions secret:
   - Name: `OPENAI_API_KEY`
   - Value: your OpenAI API key

2. Optional repository variable:
   - Name: `OPENAI_MODEL`
   - Value: `gpt-5.6-sol`

3. Run the workflow manually first:
   - Actions
   - Autonomous engineering review
   - Run workflow

4. Inspect the generated pull request.

5. Only after the first manual cycle behaves correctly should the scheduled
   six-hour cadence be left enabled.

## Important
The workflow never auto-merges. Each autonomous cycle produces a reviewable PR.
This is deliberate: the project concerns high-energy rotating machinery, and
the agent must not promote assumptions or prototype instructions without human
review.
