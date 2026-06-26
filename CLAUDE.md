# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

**pypeit-and-dragons** — A comparison of reducing Gemini data with
[DRAGONS](https://www.gemini.edu/observing/phase-iii/reducing-data/dragons-data-reduction-software)
and [PypeIt](https://pypeit.readthedocs.io/).

## Working agreements

- **The user performs all git commands** (commit, push, branch, merge, etc.).
  Do not run `git` write operations. You may use read-only git commands
  (e.g. `git status`, `git diff`, `git log`) to inspect state, but leave all
  committing and pushing to the user.

## Logging

Significant work should be logged in `claude_prompts/start_up.md` under the
"Logs" section, using the format documented there:

```
### <Date> (Short summary of the work)

<Detailed description of the work and what you learned>
```
