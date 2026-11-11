# Optimal strategy for a 3-dice "reroll" game

## Purpose

`script.py` finds the best threshold strategy for a dice game in which two players
each roll three six-sided dice (score = sum, from 3 to 18) and may re-roll to
improve their score. It answers the question:

> Which re-roll rule gives the highest chance of beating an opponent who may
> play *any* rule?

## Game model assumed

- A turn is a roll of 3 dice; the score is their sum (3–18).
- Each player has up to 3 rolls. A strategy is a pair of thresholds `(t1, t2)`:
  - After roll 1, keep the score if `score >= t1`, otherwise re-roll.
  - After roll 2, keep the score if `score >= t2`, otherwise re-roll.
  - Roll 3 is final and must be kept.
- The higher final score wins; equal scores are a tie.

With thresholds ranging over 3–18, there are 16 × 16 = **256 possible strategies**.

## What the script does

1. **Base distribution**: computes the exact probability mass function (PMF) of a
   single 3-dice roll (216 outcomes).
2. **Strategy PMF** (`final_pmf_for_thresholds`): for each `(t1, t2)`, computes the
   exact distribution of the final kept score, by chaining the re-roll rules.
3. **Head-to-head** (`win_prob`): for two strategies, computes the exact
   probability that A beats B, loses to B, or ties.
4. **Round-robin tournament**: plays every strategy against all 256 (itself
   included) and records, for each one:
   - `nb_wins`: number of opponents it beats or matches (P(win) ≥ P(loss), with a
     tolerance `eps = 1e-7`).
   - `min_win_prob`: its worst-case win probability against any opponent
     (the **maximin** criterion).
   - `avg_win_prob`: its average win probability across all opponents.
   - `E_score`: its expected final score.
5. **Ranking and export**: sorts by `nb_wins`, then `min_win_prob`, then
   `avg_win_prob` (all descending) and writes the top 150 to
   `top150_strategies_maximin.csv`.

All results are computed exactly (no Monte-Carlo simulation), so they are
deterministic and reproducible.

## Usage

```bash
pip install pandas
python script.py
```

Output:

- Console: the total number of strategies (256) and a confirmation message.
- File: `top150_strategies_maximin.csv` with columns
  `t1, t2, nb_wins, min_win_prob, avg_win_prob, E_score`.

## Reading the result

The top row of the current CSV is `(t1, t2) = (13, 12)`:

| nb_wins | min_win_prob | avg_win_prob | E_score |
|---------|--------------|--------------|---------|
| 256     | 0.4414       | 0.5683       | 12.32   |

Meaning: re-roll after the first roll unless it is ≥ 13, and after the second
unless it is ≥ 12. This strategy is never worse than a coin flip against any
opponent strategy (it beats or matches all 256), and its worst-case win
probability is about 44.1% (ties are excluded from the win probability, so it is
below 50%).

## Utility

- Identifies a robust, "unbeatable" strategy rather than one tuned to a
  specific opponent.
- Shows how close the runner-up strategies are, via the ranked top 150.
- Can be adapted to other dice counts, faces, or numbers of re-rolls by changing
  `faces`, the outcome sum, and the nesting in `final_pmf_for_thresholds`.
