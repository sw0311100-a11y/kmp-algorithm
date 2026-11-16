# kmp.py

def read_dna(txt_path):
    "txt 파일을 읽어 DNA 문자열로 반환 (줄바꿈·공백 제거)"
    with open(txt_path, encoding="utf-8") as f:
        return "".join(f.read().split())


def build_lps(pattern):
    "LPS 배열과 전처리 단계의 문자 비교 횟수를 반환"
    m = len(pattern)
    lps = [0] * m
    comparisons = 0
    length = 0
    i = 1
    while i < m:
        comparisons += 1                       # pattern[i] == pattern[length]
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:
            length = lps[length - 1]
        else:
            i += 1
    return lps, comparisons


def kmp_search(pattern, text):
    """핵심 알고리즘. 입력: (찾는 문자열, DNA 문자열)
    반환: (일치 시작 위치 리스트, 전처리 비교 횟수, 검색 비교 횟수)"""
    n, m = len(text), len(pattern)
    if m == 0 or n < m:
        return [], 0, 0

    lps, pre_cmp = build_lps(pattern)
    result = []
    search_cmp = 0
    i = j = 0
    while i < n:
        search_cmp += 1                        # text[i] == pattern[j]
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                result.append(i - m)           # 0부터 시작하는 인덱스
                j = lps[j - 1]                 # 겹치는 일치 처리
        elif j > 0:
            j = lps[j - 1]
        else:
            i += 1
    return result, pre_cmp, search_cmp


def kmp_search_file(pattern, txt_path):
    "팀 규칙용 입력: (찾는 문자열, txt 파일 경로)"
    text = read_dna(txt_path)
    return kmp_search(pattern, text)


if __name__ == "__main__":
    from test_common import run_common_tests, random_test
    run_common_tests(kmp_search, "KMP")
    random_test(kmp_search)