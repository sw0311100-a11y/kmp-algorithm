# kmp-algorithmDNA Pattern Search: Naive vs. KMP

긴 DNA 서열에서 짧은 패턴의 모든 위치를 찾는 문제를 Naive 탐색과 KMP 알고리즘으로 구현하고, 어떤 데이터에서 성능 차이가 나타나는지 실험으로 비교한 프로젝트입니다.

1. 문제 정의

길이 n인 DNA 문자열 T와 길이 m인 패턴 P가 주어질 때, P가 T에서 나타나는 모든 시작 위치를 찾습니다.

유전자 모티프, 제한효소 절단 부위 탐색 등 생물정보학의 기본 작업입니다.
게놈은 수백만~수십억 염기이므로 탐색 알고리즘의 효율이 중요합니다.
DNA는 A, C, G, T 네 글자뿐이고 반복 구간이 많아 부분 일치가 자주 발생합니다.
2. KMP 알고리즘

KMP(Knuth-Morris-Pratt)는 패턴을 미리 분석해서, 불일치가 발생해도 텍스트 포인터를 되돌리지 않는 알고리즘입니다.

핵심 아이디어

Naive 탐색은 불일치가 나면 텍스트의 시작 위치를 한 칸 옮기고 패턴을 처음부터 다시 비교합니다. 이미 비교한 글자를 다시 보는 낭비가 생깁니다.

KMP는 이미 일치한 부분의 정보를 재활용합니다. 불일치가 나면 패턴만 적절히 밀고, 텍스트 포인터 i는 절대 뒤로 가지 않습니다.

접두사 테이블 (Failure Function)

fail[i]는 P[0..i]에서 접두사이면서 동시에 접미사인 부분 중 가장 긴 것의 길이(자기 자신 제외)입니다. 불일치가 났을 때 패턴을 어디까지 되돌려서 이어 비교할지 알려줍니다.

예: P = ABABAC

index	0	1	2	3	4	5
P[i]	A	B	A	B	A	C
fail[i]	0	0	1	2	3	0

ABABA는 앞의 ABA와 뒤의 ABA가 같으므로 fail[4] = 3입니다.

동작 방식
패턴 P로 접두사 테이블을 만든다. (O(m))
텍스트를 앞에서부터 한 글자씩 읽으며 현재 일치 길이 k를 유지한다.
불일치가 나면 k = fail[k-1]로 줄여서 다시 비교한다. (텍스트 포인터는 그대로)
k == m이면 일치 위치 i - m + 1을 기록하고 k = fail[k-1]로 이어서 탐색한다. (겹치는 일치도 찾음)
시간·공간 복잡도
	Naive	KMP
시간 (최악)	O(nm)	O(n + m)
추가 메모리	O(1)	O(m) (접두사 테이블)
구현 난이도	쉬움	테이블 생성이 까다로움

Naive의 최악 예: T = AAAA...A, P = AAA...AC

3. 구현 (Python)
python
def naive(T, P):
    n, m = len(T), len(P)
    res, cmp = [], 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            cmp += 1
            if T[i + j] != P[j]:
                break
            j += 1
        if j == m:
            res.append(i)
    return res, cmp


def build_table(P):
    fail = [0] * len(P)
    k = 0
    for i in range(1, len(P)):
        while k > 0 and P[i] != P[k]:
            k = fail[k - 1]
        if P[i] == P[k]:
            k += 1
        fail[i] = k
    return fail


def kmp(T, P):
    n, m = len(T), len(P)
    fail = build_table(P)
    res, cmp, k = [], 0, 0
    for i in range(n):
        while k > 0:
            cmp += 1
            if T[i] == P[k]:
                break
            k = fail[k - 1]
        if k == 0:
            cmp += 1
            if T[i] == P[0]:
                k = 1
        else:
            k += 1
        if k == m:
            res.append(i - m + 1)
            k = fail[k - 1]
    return res, cmp

문자 비교 횟수(cmp)는 컴퓨터 성능과 무관하게 비교할 수 있는 지표입니다. 접두사 테이블 생성 과정의 비교는 전처리 비용이므로 제외했습니다.

4. 실험 설계

두 알고리즘이 같은 일치 위치를 반환하는지 먼저 검증한 뒤 아래 실험을 진행합니다.

실험	변수	데이터
1. 텍스트 길이	n: 10^5 ~ 10^7 (패턴 고정)	랜덤 DNA
2. 패턴 길이	m: 4 ~ 1000 (텍스트 고정)	랜덤 DNA
3. 반복 DNA	반복 문자열 (ACAC..., AAAA...)	인위적 생성
확인	실제 게놈	E. coli (NCBI)

Python에서 최악 케이스는 비교 횟수가 n × m에 가까워지므로, 반복 DNA 실험은 n = 10^5, m ≤ 100 정도로 제한합니다.

평가 기준
실행 시간: 입력마다 여러 번 실행한 평균 (time.perf_counter)
메모리 사용량: 최대 메모리 (tracemalloc), KMP는 O(m) 테이블 추가
문자 비교 횟수: 하드웨어와 무관한 지표
5. 실험 결과

TODO: 실험 후 표와 그래프를 채워 넣으세요.

실험	Naive 시간	KMP 시간	Naive 비교 횟수	KMP 비교 횟수
1. 랜덤 DNA (n=10^6)				
2. 랜덤 DNA (m=100)				
3. 반복 DNA				
E. coli				
6. 분석 및 고찰

TODO: 결과에 맞게 수정하세요. 아래는 예상되는 논점입니다.

랜덤 DNA: 불일치가 빨리 발생하므로 Naive의 평균 비교 횟수가 위치당 약 1.3회 수준이며, 두 알고리즘의 차이가 작을 수 있습니다.
반복 DNA: Naive가 부분 일치를 반복하며 최악에 가까워지고, KMP와의 격차가 크게 벌어질 것으로 예상됩니다.
Python 시간 측정: KMP는 상수 배가 커서, 이론상 유리해도 실제 시간은 Naive보다 느릴 수 있습니다. 이 경우 비교 횟수 지표가 이론적 차이를 더 잘 보여줍니다.
메모리: KMP는 접두사 테이블(O(m))만큼 추가 메모리가 필요합니다.
7. 한계 및 확장
정확 일치만 다루며, 실제 DNA는 돌연변이와 시퀀싱 오류가 있어 근사 일치가 필요합니다.
실제 대규모 유전체 분석(BWA, Bowtie2 등)은 텍스트를 미리 색인하는 FM-index + 시드-확장 방식을 사용합니다. KMP는 질의마다 텍스트 전체를 훑기 때문에 질의가 수억 개인 환경에는 맞지 않습니다.
이 프로젝트에서 비교하지 않은 Boyer-Moore, Rabin-Karp, Z-algorithm, Aho-Corasick 등은 추후 확장 대상입니다.
8. 프로젝트 구조
dna_search/
├── algorithms.py   # naive, kmp (비교 횟수 카운트 포함)
├── data_gen.py     # 랜덤/반복 DNA 생성, FASTA 읽기
├── experiment.py   # 실험 1~3 실행, 시간/메모리/비교 횟수 측정
├── verify.py       # 두 알고리즘 결과 일치 검증
└── plot.py         # 결과 그래프
9. 실행 방법
bash
pip install matplotlib
python verify.py        # 정확성 검증
python experiment.py    # 실험 실행
python plot.py          # 그래프 생성
10. 참고 자료
Knuth, Morris, Pratt, "Fast Pattern Matching in Strings", SIAM Journal on Computing, 1977
NCBI Genome (E. coli 실제 서열 데이터)
