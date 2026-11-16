# run_kmp_experiment.py
import csv
import time
from kmp import kmp_search, read_dna
from test_common import reference_search

REPEAT = 5


def run_condition(pattern, txt_path):
    text = read_dna(txt_path)                    # 파일은 한 번만 읽음 (측정 제외)
    expected = reference_search(pattern, text)

    times = []
    for _ in range(REPEAT):
        t0 = time.perf_counter()
        positions, pre_cmp, search_cmp = kmp_search(pattern, text)
        times.append(time.perf_counter() - t0)

    correct = (positions == expected)
    if not correct:
        print("위치 목록이 정답과 다릅니다")

    return {
        "text_len": len(text),
        "pattern_len": len(pattern),
        "match_count": len(positions),
        "correct": correct,
        "avg_time_ms": round(sum(times) / REPEAT * 1000, 4),
        "search_comparisons": search_cmp,
        "preprocess_comparisons": pre_cmp,
    }


def main(conditions, out_path="results/kmp_results.csv"):
    """conditions: [{"id":, "experiment":, "pattern":, "txt_path":, "note":}, ...]"""
    fields = ["condition_id", "experiment", "note", "text_len", "pattern_len",
              "match_count", "correct", "avg_time_ms",
              "search_comparisons", "preprocess_comparisons"]

    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for k, c in enumerate(conditions, 1):
            r = run_condition(c["pattern"], c["txt_path"])
            writer.writerow({
                "condition_id": c["id"],
                "experiment": c["experiment"],
                "note": c.get("note", ""),
                **r,
            })
            print(f"[{k}/{len(conditions)}] 조건 {c['id']} 완료 (정답 일치: {r['correct']})")
    print(f"\n저장 완료: {out_path}")


if __name__ == "__main__":
    from make_exp2 import make_conditions_exp2
    main(make_conditions_exp2(), out_path="results/kmp_results_exp2.csv")