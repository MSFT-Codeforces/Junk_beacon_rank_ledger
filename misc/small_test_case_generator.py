
def make_case(n, edges):
    lines = [f"{n} {len(edges)}"]
    lines += [f"{u} {v} {w}" for (u, v, w) in edges]
    return "\n".join(lines)

cases = []

# 1) Minimum size, satisfiable (difference ±1)
cases.append(make_case(2, [
    (1, 2, 1),
]))

# 2) Minimum size, impossible (forces equal ranks)
cases.append(make_case(2, [
    (1, 2, 0),
]))

# 3) Simple chain, satisfiable -> consecutive ranks
cases.append(make_case(3, [
    (1, 2, 1),
    (2, 3, 1),
]))

# 4) Simple chain, consistent as equations but impossible as permutation (range too wide)
cases.append(make_case(3, [
    (1, 2, 2),
    (2, 3, 2),
]))

# 5) Cycle consistent but violates permutation (forces duplicate ranks)
cases.append(make_case(3, [
    (1, 2, 1),
    (2, 3, 0),  # rank[3] = rank[2]
    (1, 3, 1),
]))

# 6) Tree, distinct potentials but not shiftable to {1..n} (range too wide / gaps)
cases.append(make_case(4, [
    (1, 2, 1),
    (2, 3, 2),
    (3, 4, 1),
]))

# 7) Inconsistent cycle (cycle sum != 0), plus extra node to keep connected
cases.append(make_case(4, [
    (1, 2, 1),
    (2, 3, 1),
    (3, 1, -1),  # inconsistent with above
    (3, 4, 1),
]))

# 8) Consistent cycle, satisfiable (extra edge closes cycle correctly)
cases.append(make_case(4, [
    (1, 2, 1),
    (2, 3, 1),
    (3, 4, 1),
    (4, 1, -3),  # rank[1]-rank[4] = -3
]))

# 9) Negative weights; needs shifting; satisfiable (gives reversed permutation)
cases.append(make_case(5, [
    (1, 2, -1),
    (2, 3, -1),
    (3, 4, -1),
    (4, 5, -1),
]))

# 10) Parallel edges consistent (should still be satisfiable)
cases.append(make_case(5, [
    (1, 2, 1),
    (1, 2, 1),   # parallel, consistent
    (2, 3, 1),
    (3, 4, 1),
    (4, 5, 1),
]))

# 11) Parallel edges contradictory (must be impossible)
cases.append(make_case(5, [
    (1, 2, 1),
    (1, 2, 2),   # parallel, contradictory
    (2, 3, 1),
    (3, 4, 1),
    (4, 5, 1),
]))

# 12) Self-loop with non-zero w (must be impossible), still connected overall
cases.append(make_case(4, [
    (1, 1, 1),   # impossible constraint
    (1, 2, 1),
    (2, 3, 1),
    (3, 4, 1),
]))

# 13) Both directions given explicitly; consistent iff w reverse is negated (direction/sign trap)
cases.append(make_case(4, [
    (1, 2, 1),
    (2, 1, -1),  # must match the reverse constraint
    (2, 3, 1),
    (3, 4, 1),
]))

# 14) Huge weights to catch 32-bit overflow; also impossible as permutation (range enormous)
cases.append(make_case(6, [
    (1, 2, 1000000000),
    (2, 3, 1000000000),
    (3, 4, 1000000000),
    (4, 5, 1000000000),
    (5, 6, 1000000000),
]))

# 15) Mixed: long chain with extra consistent back-edges (cycle checks), satisfiable
cases.append(make_case(6, [
    (1, 2, -1),
    (2, 3, -1),
    (3, 4, -1),
    (4, 5, -1),
    (5, 6, -1),
    (1, 3, -2),   # consistent with chain
    (2, 5, -3),   # consistent with chain
    (6, 1, 5),    # consistent with chain: rank[1]-rank[6] = 5
]))

print("Test Cases:")
for i, tc in enumerate(cases, 1):
    print(f"Input {i}:")
    print(tc)
    if i != len(cases):
        print()
