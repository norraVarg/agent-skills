# Stage 5 — measure and report the size impact

Read this at the end of Stage 5, once the skill files are written. Create and update runs reach it; an
audit never does, because nothing has been written to measure.

## 1. Measure

Measure every file this stage wrote: line count and byte count. "Before" is 0 for a new file, or its
copy under `<workspace>/skill-snapshot/` for an update. The token estimate is bytes / 4, rounded.

Sum lines and estimated tokens across every file touched into one total delta, and label the token
figure as an estimate (`~4 chars/token`) rather than presenting it as exact.

## 2. Judge the cost

Report the cost, then judge it against what the skill does. A large bundled file costs nothing unless a
step reads it, while the entry file loads in full every time and cannot be amortised across modes — so
that is the one to look at.

- Entry file past ~300 lines or ~4,000 estimated tokens → report it, and say whether the body justifies
  the length. A multi-mode skill often does; a single-workflow one usually does not.
- Any single bundled file past the same figure → note it, with less urgency.
- **When the body does not justify its length, name the specific block to extract** — the one serving
  the fewest modes, or firing least often — rather than only reporting the number. A bare count has to
  be re-diagnosed later; a named block is actionable in the next Stage 2U pass.

## 3. Trend markers

Mark each measured line with the direction it moved: 📈 larger, 📉 smaller, ➡️ unchanged. A marker is a
direction, not a verdict — 📈 on a skill that gained a mode is expected.

## 4. Output

```
Skill {created|updated} at <skills-root>/<skill-name>/<entry file>

Size impact:
  Lines: {before} -> {after} {trend} (Δ{+/-N})
  Estimated tokens: {before} -> {after} {trend} (Δ{+/-N}, ~4 chars/token, approximate)
{warning line(s), only if a threshold above was crossed}

{the reload note from <format>'s "Where skills live" section}
```
