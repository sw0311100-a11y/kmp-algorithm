# kmp-algorithmDNA Pattern Search: KMP

KMP (Knuth-Morris-Pratt) 알고리즘

긴 문자열에서 패턴이 나타나는 모든 위치를 O(n + m)에 찾는 문자열 탐색 알고리즘입니다. 이 저장소에서는 KMP를 Python으로 구현하고, DNA 염기서열 패턴 검색에 적용합니다.

1. 문제 정의

길이 n인 텍스트 T와 길이 m인 패턴 P가 주어질 때, P가 T에서 나타나는 모든 시작 위치를 찾습니다.

DNA 서열(A, C, G, T)에서의 활용 예:

유전자 모티프 탐색
제한효소 절단 부위 탐색 (예: GAATTC)
프라이머 위치 확인

DNA는 알파벳이 4개뿐이고 반복 구간이 많아 부분 일치가 자주 발생하므로, 불필요한 재비교를 없애는 KMP가 유용한 데이터입니다.

2. 핵심 아이디어

불일치가 발생했을 때 이미 일치한 부분의 정보를 재활용합니다.

텍스트 포인터 i는 절대 뒤로 돌아가지 않습니다.
대신 패턴 쪽 포인터 k(현재까지 일치한 길이)만 접두사 테이블을 보고 줄입니다.
따라서 텍스트의 각 글자는 최대 한 번씩만 처리되어 전체가 선형 시간입니다.
3. 접두사 테이블 (Failure Function)

fail[i]는 P[0..i]에서 접두사이면서 동시에 접미사인 부분 중 가장 긴 것의 길이(자기 자신 제외)입니다. 불일치가 났을 때 패턴을 어디까지 되돌려 이어서 비교할지 알려줍니다.

예: P = ABABAC

index	0	1	2	3	4	5
P[i]	A	B	A	B	A	C
fail[i]	0	0	1	2	3	0

ABABA는 앞의 ABA와 뒤의 ABA가 같으므로 fail[4] = 3입니다.

4. 탐색 과정
패턴 P로 접두사 테이블을 만든다. (O(m))
텍스트를 앞에서부터 한 글자씩 읽으며 현재 일치 길이 k를 유지한다.
불일치가 나면 k = fail[k-1]로 줄여서 같은 텍스트 글자를 다시 비교한다.
k == m이면 일치 위치 i - m + 1을 기록하고, k = fail[k-1]로 이어서 탐색한다. (겹치는 일치도 찾을 수 있음)
예시: T = ABABABAC, P = ABABAC
i	T[i]	동작	k
0~4	A B A B A	모두 일치	5
5	B	P[5]=C와 불일치 → k = fail[4] = 3 → P[3]=B와 일치	4
6	A	P[4]=A와 일치	5
7	C	P[5]=C와 일치 → k == m	6

일치 위치는 7 - 6 + 1 = 2입니다. i = 5에서 패턴을 처음부터 다시 비교하지 않고, 앞에서 맞춘 ABA를 재활용한 것이 핵심입니다.

5. 복잡도
	복잡도	설명
전처리	O(m)	접두사 테이블 생성
탐색	O(n)	텍스트 포인터가 뒤로 가지 않음
전체 시간	O(n + m)	최악의 경우에도 동일
추가 메모리	O(m)	접두사 테이블

탐색이 O(n)인 이유: 내부 while 루프에서 k가 줄어드는 횟수는 k가 늘어난 횟수를 넘을 수 없고, k는 텍스트 글자 하나당 최대 1씩만 증가하므로 전체 감소 횟수도 n 이하입니다.

6. 구현 (Python)
python
def build_table(P):
    """접두사 테이블(failure function) 생성"""
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
    """T에서 P가 나타나는 모든 시작 위치를 반환"""
    n, m = len(T), len(P)
    if m == 0 or m > n:
        return []
    fail = build_table(P)
    res, k = [], 0
    for i in range(n):
        while k > 0 and T[i] != P[k]:
            k = fail[k - 1]
        if T[i] == P[k]:
            k += 1
        if k == m:
            res.append(i - m + 1)
            k = fail[k - 1]
    return res
사용 예
python
print(build_table("ABABAC"))        # [0, 0, 1, 2, 3, 0]
print(kmp("ABABABAC", "ABABAC"))    # [2]
print(kmp("AAAAA", "AAA"))          # [0, 1, 2]  (겹치는 일치)
print(kmp("GATTACAGATTACA", "GATTACA"))  # [0, 7]
문자 비교 횟수까지 세고 싶다면

하드웨어와 무관한 성능 지표로 비교 횟수를 셀 수 있습니다.

python
def kmp_count(T, P):
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

접두사 테이블 생성 중의 비교는 전처리 비용이므로 제외했습니다.

7. 정확성 검증

구현이 맞는지 Python 내장 re 모듈과 비교해서 확인할 수 있습니다. (검증용으로만 사용)

python
import random, re

def expected(T, P):
    return [m.start() for m in re.finditer(f"(?={re.escape(P)})", T)]

for _ in range(1000):
    T = "".join(random.choices("ACGT", k=random.randint(1, 50)))
    P = "".join(random.choices("ACGT", k=random.randint(1, 5)))
    assert kmp(T, P) == expected(T, P), (T, P)
print("OK")

경계 케이스도 확인하세요: 패턴이 텍스트보다 긴 경우, 겹치는 일치(AAA in AAAAA), 일치가 없는 경우.

8. DNA 서열에 적용
python
def read_fasta(path):
    with open(path) as f:
        return "".join(line.strip() for line in f if not line.startswith(">"))

genome = read_fasta("ecoli.fasta")   # NCBI에서 받은 E. coli 서열
print(kmp(genome, "GAATTC"))         # EcoRI 제한효소 절단 부위 위치
9. 장단점과 한계

장점

최악의 경우에도 O(n + m)이 보장됩니다.
텍스트를 한 번만 앞에서 뒤로 읽으므로 스트리밍 입력에도 적합합니다.
반복이 많은 서열에서도 성능이 떨어지지 않습니다.

단점 및 한계

접두사 테이블 때문에 O(m) 추가 메모리가 필요합니다.
정확 일치만 가능합니다. 실제 DNA는 돌연변이와 시퀀싱 오류가 있어 근사 일치가 필요한 경우가 많습니다.
질의마다 텍스트 전체를 훑으므로 O(n)이 듭니다. 같은 참조 게놈에 질의가 수억 개 들어오는 대규모 분석(BWA, Bowtie2 등)에서는 텍스트를 미리 색인하는 FM-index 기반 방식을 사용합니다.
짧은 서열에서의 일회성 검색(제한효소 부위, 프라이머 위치 등)에는 KMP로 충분합니다.
10. 참고 자료
Knuth, Morris, Pratt, "Fast Pattern Matching in Strings", SIAM Journal on Computing, 1977
NCBI Genome (E. coli 서열 데이터)
