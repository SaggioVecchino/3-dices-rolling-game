from collections import Counter
import pandas as pd

eps = 1e-7
faces = [1, 2, 3, 4, 5, 6]
outcomes = [a + b + c for a in faces for b in faces for c in faces]
total = len(outcomes)
pmf = {k: float(v) for k, v in Counter(outcomes).items()}

for s in range(3, 19):
    pmf[s] = pmf.get(s, 0) / total


def final_pmf_for_thresholds(t1, t2):
    pmf_final = dict()
    for s1, p1 in pmf.items():
        if s1 >= t1:
            pmf_final[s1] = pmf_final.get(s1, 0) + p1
        else:
            for s2, p2 in pmf.items():
                if s2 >= t2:
                    pmf_final[s2] = pmf_final.get(s2, 0) + p1 * p2
                else:
                    for s3, p3 in pmf.items():
                        pmf_final[s3] = pmf_final.get(s3, 0) + p1 * p2 * p3
    return {s: pmf_final[s] for s in range(3, 19)}


def win_prob(pmfA, pmfB):
    pA_gt_B = 0.0
    pA_lt_B = 0.0
    pA_eq_B = 0.0
    cumB_lt = {s: sum(pmfB[t] for t in range(3, s)) for s in range(3, 19)}
    cumB_le = {s: sum(pmfB[t] for t in range(3, s + 1)) for s in range(3, 19)}
    for x in range(3, 19):
        pA_x = pmfA.get(x, 0.0)
        if pA_x == 0:
            continue
        pA_gt_B += pA_x * cumB_lt[x]
        pA_eq_B += pA_x * pmfB.get(x, 0.0)
        pA_lt_B += pA_x * (1 - cumB_le[x])
    return pA_gt_B, pA_lt_B, pA_eq_B


strategies = [(t1, t2) for t1 in range(3, 19) for t2 in range(3, 19)]
print(f"The total number of possible strategies is: {len(strategies)}")
pmf_by_strategy = {}
for t1, t2 in strategies:
    pmf_by_strategy[(t1, t2)] = final_pmf_for_thresholds(t1, t2)

results = []
for t1, t2 in strategies:
    pmf_i = pmf_by_strategy[(t1, t2)]
    win_probs_vs_all = []
    nb_wins = 0
    for u1, u2 in strategies:
        pmf_j = pmf_by_strategy[(u1, u2)]
        p_gt, p_lt, p_eq = win_prob(pmf_i, pmf_j)
        win_probs_vs_all.append(p_gt)
        if p_gt + eps >= p_lt:
            nb_wins += 1
    min_vs = min(win_probs_vs_all)
    avg_vs = sum(win_probs_vs_all) / len(win_probs_vs_all)
    results.append(
        {
            "t1": t1,
            "t2": t2,
            "nb_wins": nb_wins,
            "min_win_prob": min_vs,
            "avg_win_prob": avg_vs,
            "E_score": sum(s * pmf_i.get(s, 0) for s in range(3, 19)),
        }
    )

df = pd.DataFrame(results)
df_sorted = df.sort_values(
    ["nb_wins", "min_win_prob", "avg_win_prob"], ascending=False
).reset_index(drop=True)
df_sorted.head(150).to_csv("top150_strategies_maximin.csv", index=False)
print("Saved top150_strategies_maximin.csv")
