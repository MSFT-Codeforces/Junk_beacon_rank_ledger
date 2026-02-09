
import sys
from io import StringIO

def case_from_edges(n, edges):
    """
    edges: list of (u,v,w)
    returns multiline string for one test case
    """
    out = StringIO()
    out.write(f"{n} {len(edges)}\n")
    for u, v, w in edges:
        out.write(f"{u} {v} {w}\n")
    return out.getvalue()

def large_chain_case(n, extra_edge=True):
    """
    Builds a large chain 1->2->...->n with w=1 (valid permutation 1..n).
    Optionally adds one extra edge 1->n with w=n-1 to make m=n (if desired).
    """
    out = StringIO()
    m = (n - 1) + (1 if extra_edge else 0)
    out.write(f"{n} {m}\n")
    for i in range(1, n):
        out.write(f"{i} {i+1} 1\n")
    if extra_edge:
        out.write(f"1 {n} {n-1}\n")
    return out.getvalue()

cases = []

# 1) Minimum valid: n=2, must have |w|=1
cases.append(case_from_edges(2, [
    (1, 2, 1),
]))

# 2) Minimum invalid: forces equal ranks
cases.append(case_from_edges(2, [
    (1, 2, 0),
]))

# 3) Small valid tree (simple chain), ranks can be 1 2 3
cases.append(case_from_edges(3, [
    (1, 2, 1),
    (2, 3, 1),
]))

# 4) Consistent differences but impossible permutation (range too wide)
cases.append(case_from_edges(3, [
    (1, 2, 2),
    (2, 3, 2),
]))

# 5) Consistent cycle (checks cycle handling)
# Underlying valid permutation example: r = [1,3,4,2]
cases.append(case_from_edges(4, [
    (1, 2, 2),
    (2, 3, 1),
    (3, 4, -2),
    (4, 1, -1),
]))

# 6) Inconsistent cycle (single wrong edge)
cases.append(case_from_edges(4, [
    (1, 2, 2),
    (2, 3, 1),
    (3, 4, -2),
    (4, 1, -2),   # should be -1
]))

# 7) Parallel edges with contradiction
cases.append(case_from_edges(4, [
    (1, 2, 1),
    (2, 3, 1),
    (3, 4, 1),
    (1, 2, 2),    # contradicts first edge
]))

# 8) Direction/sign mistake trap: both (u,v,w) and (v,u,w) present
# Correct consistency requires w_reverse = -w, but here it's +w -> impossible
cases.append(case_from_edges(3, [
    (1, 2, 1),
    (2, 1, 1),    # should have been -1
    (2, 3, 1),
]))

# 9) Self-loop inconsistent (w != 0)
cases.append(case_from_edges(5, [
    (1, 2, 1),
    (2, 3, 1),
    (3, 4, 1),
    (4, 5, 1),
    (3, 3, 1),    # impossible
]))

# 10) Self-loop consistent (w == 0), still must satisfy permutation
# Example valid ranks: [3,1,5,2,4]
cases.append(case_from_edges(5, [
    (1, 2, -2),
    (2, 3, 4),
    (3, 4, -3),
    (4, 5, 2),
    (3, 3, 0),    # harmless
]))

# 11) Large weights along a path (overflow risk if using 32-bit), permutation impossible
cases.append(case_from_edges(10, [
    (1, 2, 10**9),
    (2, 3, 10**9),
    (3, 4, 10**9),
    (4, 5, 10**9),
    (5, 6, 10**9),
    (6, 7, 10**9),
    (7, 8, 10**9),
    (8, 9, 10**9),
    (9, 10, 10**9),
]))

# 12) Equations consistent but force duplicate ranks (permutation violation)
cases.append(case_from_edges(3, [
    (1, 2, 5),
    (2, 3, -5),
    (1, 3, 0),    # implies rank[1] == rank[3]
]))

# 13) Valid but requires shifting (catches solutions that wrongly fix rank[1]=1 and don't shift)
# True valid permutation example: ranks [3,1,4,2]
cases.append(case_from_edges(4, [
    (1, 2, -2),
    (2, 3, 3),
    (3, 4, -2),
]))

# 14) Star graph (high degree), valid permutation example: [4,1,8,3,7,2,6,5]
# Edges: 1 -> i with w = rank[i] - rank[1]
cases.append(case_from_edges(8, [
    (1, 2, -3),
    (1, 3, 4),
    (1, 4, -1),
    (1, 5, 3),
    (1, 6, -2),
    (1, 7, 2),
    (1, 8, 1),
]))

# 15) Max stress: n=200000, m=200000 (chain + one extra edge), valid
cases.append(large_chain_case(200000, extra_edge=True))

# Print in the requested format
sys.stdout.write("Test Cases: \n")
for i, tc in enumerate(cases, 1):
    sys.stdout.write(f"Input {i}:\n")
    sys.stdout.write(tc)
    sys.stdout.write("\n")
