
import sys, random

def flush(buf):
    if buf:
        sys.stdout.write("".join(buf))
        buf.clear()

def print_header():
    # Match required format header line
    sys.stdout.write("Test Cases:\n")

def print_case_label(idx):
    sys.stdout.write(f"Input {idx}:\n")

def print_nm(n, m):
    sys.stdout.write(f"{n} {m}\n")

def case1_valid_long_path():
    # n=2e5, tree path, w=+1 => valid permutation after shift
    n = 200_000
    m = n - 1
    print_nm(n, m)
    buf = []
    for i in range(1, n):
        buf.append(f"{i} {i+1} 1\n")
        if len(buf) >= 20000:
            flush(buf)
    flush(buf)

def case2_overflow_stress_but_invalid_permutation():
    # n=2e5, path, w=n-1 each step => consistent but potential range huge; tests 32-bit overflow
    n = 200_000
    m = n - 1
    w = n - 1
    print_nm(n, m)
    buf = []
    for i in range(1, n):
        buf.append(f"{i} {i+1} {w}\n")
        if len(buf) >= 20000:
            flush(buf)
    flush(buf)

def case3_star_high_degree_valid():
    # Star centered at 1, with rank[i]=i achievable (up to shift)
    n = 200_000
    m = n - 1
    print_nm(n, m)
    buf = []
    for i in range(2, n + 1):
        # rank[i] - rank[1] = (i-1)
        buf.append(f"1 {i} {i-1}\n")
        if len(buf) >= 20000:
            flush(buf)
    flush(buf)

def case4_many_edges_consistent_dense():
    # Smaller n but max m to be "dense-ish": consistent system with rank[i]=i (up to shift)
    n = 50_000
    m = 200_000
    rng = random.Random(12345)
    print_nm(n, m)

    buf = []
    # Spanning path (connected)
    for i in range(1, n):
        buf.append(f"{i} {i+1} 1\n")
        if len(buf) >= 20000:
            flush(buf)
    flush(buf)

    extra = m - (n - 1)
    buf = []
    for _ in range(extra):
        u = rng.randint(1, n)
        v = rng.randint(1, n - 1)
        if v >= u:
            v += 1  # ensure v != u
        w = v - u  # consistent with rank[i]=i+c
        buf.append(f"{u} {v} {w}\n")
        if len(buf) >= 20000:
            flush(buf)
    flush(buf)

def case5_many_edges_one_bad_edge():
    # Same as case4 but inject one inconsistent constraint (cycle contradiction)
    n = 50_000
    m = 200_000
    rng = random.Random(54321)
    print_nm(n, m)

    buf = []
    # Spanning path
    for i in range(1, n):
        buf.append(f"{i} {i+1} 1\n")
        if len(buf) >= 20000:
            flush(buf)
    flush(buf)

    extra = m - (n - 1)
    # Produce extra-1 consistent edges, then one inconsistent edge
    buf = []
    for _ in range(extra - 1):
        u = rng.randint(1, n)
        v = rng.randint(1, n - 1)
        if v >= u:
            v += 1
        w = v - u
        buf.append(f"{u} {v} {w}\n")
        if len(buf) >= 20000:
            flush(buf)
    flush(buf)

    # Inconsistent edge
    u, v = 123, 40_000
    bad_w = (v - u) + 1
    sys.stdout.write(f"{u} {v} {bad_w}\n")

def case6_parallel_edges_contradiction():
    # n=2e5, tree path plus one contradictory parallel edge
    n = 200_000
    m = 200_000
    print_nm(n, m)

    buf = []
    for i in range(1, n):
        buf.append(f"{i} {i+1} 1\n")
        if len(buf) >= 20000:
            flush(buf)
    flush(buf)

    # Contradict the existing edge (100000 -> 100001 should be +1)
    sys.stdout.write("100000 100001 2\n")

def case7_self_loop_inconsistency():
    # n=2e5, tree path plus self-loop w!=0 => impossible
    n = 200_000
    m = 200_000
    print_nm(n, m)

    buf = []
    for i in range(1, n):
        buf.append(f"{i} {i+1} 1\n")
        if len(buf) >= 20000:
            flush(buf)
    flush(buf)

    sys.stdout.write("1 1 1\n")  # self-loop inconsistency

def case8_directionality_trap_many_reverse_edges():
    # Bidirectional constraints explicitly included; catches solvers that store same w in both directions
    n = 100_000
    m = 2 * (n - 1)  # 199998
    print_nm(n, m)

    buf = []
    for i in range(1, n):
        buf.append(f"{i} {i+1} 1\n")
        buf.append(f"{i+1} {i} -1\n")
        if len(buf) >= 20000:
            flush(buf)
    flush(buf)

def case9_extreme_weight_1e9():
    # n=2e5, path plus one edge with huge w (inconsistent with any permutation)
    n = 200_000
    m = 200_000
    print_nm(n, m)

    buf = []
    for i in range(1, n):
        buf.append(f"{i} {i+1} 1\n")
        if len(buf) >= 20000:
            flush(buf)
    flush(buf)

    sys.stdout.write(f"1 {n} 1000000000\n")

def case10_all_zero_weights_duplicates():
    # All w=0 along a spanning tree => consistent equations but forces all ranks equal -> violates permutation
    n = 200_000
    m = n - 1
    print_nm(n, m)

    buf = []
    for i in range(1, n):
        buf.append(f"{i} {i+1} 0\n")
        if len(buf) >= 20000:
            flush(buf)
    flush(buf)

def main():
    print_header()

    generators = [
        case1_valid_long_path,
        case2_overflow_stress_but_invalid_permutation,
        case3_star_high_degree_valid,
        case4_many_edges_consistent_dense,
        case5_many_edges_one_bad_edge,
        case6_parallel_edges_contradiction,
        case7_self_loop_inconsistency,
        case8_directionality_trap_many_reverse_edges,
        case9_extreme_weight_1e9,
        case10_all_zero_weights_duplicates,
    ]

    for idx, gen in enumerate(generators, start=1):
        print_case_label(idx)
        gen()
        if idx != len(generators):
            sys.stdout.write("\n")

if __name__ == "__main__":
    main()
