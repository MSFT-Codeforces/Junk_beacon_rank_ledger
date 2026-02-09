
import sys
import re

INT_LINE_RE = re.compile(r"-?\d+(?: -?\d+)*\Z")

def is_strict_int_line(s: str) -> bool:
    # No leading/trailing whitespace, no tabs, no empty lines; only single spaces between ints.
    if s == "" or s != s.strip():
        return False
    if "\t" in s:
        return False
    return INT_LINE_RE.fullmatch(s) is not None

class DSU:
    __slots__ = ("p", "sz", "cc")
    def __init__(self, n: int):
        self.p = list(range(n))
        self.sz = [1] * n
        self.cc = n

    def find(self, a: int) -> int:
        p = self.p
        while p[a] != a:
            p[a] = p[p[a]]
            a = p[a]
        return a

    def union(self, a: int, b: int) -> None:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return
        if self.sz[ra] < self.sz[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        self.sz[ra] += self.sz[rb]
        self.cc -= 1

def parse_one_case(lines, idx):
    # returns (ok, new_idx)
    if idx >= len(lines):
        return (False, idx)

    parts = lines[idx].split(" ")
    if len(parts) != 2:
        return (False, idx)
    try:
        n = int(parts[0]); m = int(parts[1])
    except:
        return (False, idx)

    # constraints
    if not (2 <= n <= 2 * 10**5):
        return (False, idx)
    if not (n - 1 <= m <= 2 * 10**5):
        return (False, idx)

    # Need lines idx+1 ... idx+m
    if idx + m >= len(lines):
        return (False, idx)

    dsu = DSU(n)

    for j in range(1, m + 1):
        parts = lines[idx + j].split(" ")
        if len(parts) != 3:
            return (False, idx)
        try:
            u = int(parts[0]); v = int(parts[1]); w = int(parts[2])
        except:
            return (False, idx)

        if not (1 <= u <= n and 1 <= v <= n):
            return (False, idx)
        if not (-10**9 <= w <= 10**9):
            return (False, idx)

        # connectedness considers undirected adjacency; self-loops don't help but are allowed.
        if u != v:
            dsu.union(u - 1, v - 1)

    # graph must be connected (undirected)
    if dsu.cc != 1:
        return (False, idx)

    return (True, idx + 1 + m)

def validate_cases_concatenated(lines):
    idx = 0
    while idx < len(lines):
        ok, idx2 = parse_one_case(lines, idx)
        if not ok:
            return False
        idx = idx2
    return True

def validate_cases_with_T(lines):
    if not lines:
        return False
    parts = lines[0].split(" ")
    if len(parts) != 1:
        return False
    try:
        T = int(parts[0])
    except:
        return False
    if T < 1:
        return False

    idx = 1
    for _ in range(T):
        ok, idx2 = parse_one_case(lines, idx)
        if not ok:
            return False
        idx = idx2
    return idx == len(lines)

def main():
    data = sys.stdin.read()
    if data == "":
        print("False")
        return

    lines = data.splitlines()

    # Strictly reject blank lines anywhere and enforce strict spacing.
    for s in lines:
        if not is_strict_int_line(s):
            print("False")
            return

    # Support either:
    # 1) T then T cases
    # 2) One or more cases concatenated, each starting with "n m"
    first_parts = lines[0].split(" ")
    if len(first_parts) == 1:
        print("True" if validate_cases_with_T(lines) else "False")
    elif len(first_parts) == 2:
        print("True" if validate_cases_concatenated(lines) else "False")
    else:
        print("False")

if __name__ == "__main__":
    main()
