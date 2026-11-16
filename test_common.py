# test_common.py
import random

TEST_CASES = [
    # (설명, 텍스트, 패턴, 예상 정답)
    ("기본 일치",        "ACGTACGT",   "ACG",     [0, 4]),
    ("겹치는 일치",      "AAAA",       "AA",      [0, 1, 2]),
    ("일치 없음",        "ACGTACGT",   "TTT",     []),
    ("패턴 = 텍스트",    "ACGT",       "ACGT",    [0]),
    ("패턴이 더 김",     "ACG",        "ACGT",    []),
    ("패턴 길이 1",      "ACGTA",      "A",       [0, 4]),
    ("맨 끝에서 일치",   "TTTTACG",    "ACG",     [4]),
    ("맨 앞에서 일치",   "ACGTTTT",    "ACG",     [0]),
    ("반복 패턴 겹침",   "ACACACAC",   "ACAC",    [0, 2, 4]),
    ("단일 문자 반복",   "AAAAAAA",    "AAAA",    [0, 1, 2, 3]),
    ("빈 텍스트",        "",           "A",       []),
    ("LPS 후퇴 필요",    "ACGACGACGT", "ACGACGT",  [3]),
]


def reference_search(pattern, text):
    """정답 검증용: 가장 단순한 방식 (겹치는 일치 포함)"""
    m = len(pattern)
    return [i for i in range(len(text) - m + 1) if text[i:i + m] == pattern]


def run_common_tests(search_func, name="알고리즘"):
    passed = 0
    for desc, text, pattern, expected in TEST_CASES:
        out = search_func(pattern, text)          # ← (패턴, 텍스트) 순서
        if isinstance(out, tuple):
            out = out[0]
        ok = (out == expected)
        passed += ok
        print(f"[{'PASS' if ok else 'FAIL'}] {desc}: 기대={expected}, 결과={out}")
    print(f"\n{name}: {passed}/{len(TEST_CASES)} 통과")
    return passed == len(TEST_CASES)


def random_test(search_func, trials=1000):
    for _ in range(trials):
        n = random.randint(0, 30)
        m = random.randint(1, 6)
        text = "".join(random.choice("ACGT") for _ in range(n))
        pattern = "".join(random.choice("ACGT") for _ in range(m))
        out = search_func(pattern, text)          # ← (패턴, 텍스트) 순서
        if isinstance(out, tuple):
            out = out[0]
        assert out == reference_search(pattern, text), (pattern, text)
    print(f"랜덤 테스트 {trials}회 통과")