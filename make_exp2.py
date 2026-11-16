# make_exp2.py  (실험 2: 패턴 길이 변화, 54조건)
import os

DATA_DIR = "data"
PATTERN_DIR = "patterns"
TEXT_FILES = {
    "random": os.path.join(DATA_DIR, "text_random_n1000000.txt"),
    "ecoli":  os.path.join(DATA_DIR, "text_ecoli_n1000000.txt"),
}
LENGTHS = [4, 8, 16, 32, 64, 128, 256, 512, 1000]
REPS = ["p01", "p02", "p03"]


def read_pattern(path):
    """패턴 파일 내용을 그대로 읽되, 끝의 줄바꿈 문자만 제거"""
    with open(path, encoding="utf-8") as f:
        return f.read().strip("\r\n")


def make_conditions_exp2(start_id=1):
    conds = []
    cid = start_id
    for source in ["random", "ecoli"]:
        for m in LENGTHS:
            for p in REPS:
                fname = f"pattern_{source}_{p}_m{m}.txt"
                pattern = read_pattern(os.path.join(PATTERN_DIR, fname))
                assert len(pattern) == m, f"{fname}: 길이 {len(pattern)} != {m}"
                conds.append(dict(
                    id=cid,
                    experiment=2,
                    txt_path=TEXT_FILES[source],
                    pattern=pattern,
                    note=f"{source}/{p}/m{m}",
                ))
                cid += 1
    return conds


if __name__ == "__main__":
    c = make_conditions_exp2()
    print(len(c), "조건")
    print("첫 조건:", c[0]["note"], "패턴:", c[0]["pattern"])
    print("끝 조건:", c[-1]["note"], "패턴 길이:", len(c[-1]["pattern"]))
