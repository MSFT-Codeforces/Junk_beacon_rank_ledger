
import os
from typing import Tuple, List, Optional


def _fail(msg: str) -> Tuple[bool, str]:
    return (False, msg)


def _is_int_token(tok: str) -> bool:
    # Strict integer: optional leading '-', then digits (no '+', no spaces)
    if not tok:
        return False
    if tok[0] == "-":
        return len(tok) > 1 and tok[1:].isdigit()
    return tok.isdigit()


def _parse_int(tok: str, what: str) -> Tuple[bool, int, str]:
    if not _is_int_token(tok):
        return False, 0, f"Invalid integer token for {what}: '{tok}'"
    try:
        return True, int(tok), ""
    except Exception:
        return False, 0, f"Failed to parse integer for {what}: '{tok}'"


def _tokenize_output_strict(output_text: str) -> Tuple[bool, List[str], str]:
    """
    Strict tokenization:
      - Allow at most one trailing '\n' at EOF.
      - Otherwise, no leading/trailing whitespace, no empty lines.
      - Allowed characters: digits, '-', space, newline.
      - Within a line: tokens separated by single spaces (no double spaces),
        and no leading/trailing spaces.
    Returns tokens in order.
    """
    if "\r" in output_text:
        return False, [], "Output contains carriage return characters (\\r); only \\n newlines are allowed"

    core = output_text
    if core.endswith("\n"):
        core = core[:-1]
        if core.endswith("\n"):
            return False, [], "Output has more than one trailing newline (extra empty line at end is not allowed)"

    if core == "":
        return False, [], "Output is empty"

    # Disallow leading/trailing whitespace other than the single allowed trailing '\n' already removed.
    if core[0].isspace() or core[-1].isspace():
        return False, [], "Output has leading/trailing whitespace; only a single trailing newline at EOF is allowed"

    allowed = set("0123456789- \n")
    for ch in core:
        if ch not in allowed:
            return (
                False,
                [],
                f"Output contains invalid character {repr(ch)}; only digits, '-', spaces, and newlines are allowed",
            )

    lines = core.split("\n")
    tokens: List[str] = []
    for i, line in enumerate(lines, start=1):
        if line == "":
            return False, [], f"Output contains an empty line at line {i} (blank lines are not allowed)"
        if line[0] == " " or line[-1] == " ":
            return False, [], f"Line {i} has leading/trailing spaces (not allowed)"
        if "  " in line:
            return False, [], f"Line {i} contains multiple consecutive spaces (not allowed)"
        parts = line.split(" ")
        tokens.extend(parts)

    if not tokens:
        return False, [], "Output contains no tokens"
    return True, tokens, ""


def _parse_single_case_input(in_toks: List[str]) -> Tuple[bool, Optional[List[Tuple[int, int, List[Tuple[int, int, int]]]]], str]:
    if len(in_toks) < 2:
        return False, None, "Input parsing failed: expected at least two integers n and m"

    ok, n, err = _parse_int(in_toks[0], "n")
    if not ok:
        return False, None, f"Input parsing failed: {err}"
    ok, m, err = _parse_int(in_toks[1], "m")
    if not ok:
        return False, None, f"Input parsing failed: {err}"

    if n < 2:
        return False, None, f"Input parsing failed: n must be >= 2, got {n}"
    if m < 0:
        return False, None, f"Input parsing failed: m must be >= 0, got {m}"

    expected = 2 + 3 * m
    if len(in_toks) != expected:
        return False, None, (
            f"Input does not match single-testcase format: expected exactly {expected} tokens (2 + 3*m), got {len(in_toks)}"
        )

    edges: List[Tuple[int, int, int]] = []
    idx = 2
    for ei in range(1, m + 1):
        ok, u, err = _parse_int(in_toks[idx], f"u (edge {ei})")
        if not ok:
            return False, None, f"Input parsing failed: {err}"
        ok, v, err = _parse_int(in_toks[idx + 1], f"v (edge {ei})")
        if not ok:
            return False, None, f"Input parsing failed: {err}"
        ok, w, err = _parse_int(in_toks[idx + 2], f"w (edge {ei})")
        if not ok:
            return False, None, f"Input parsing failed: {err}"
        edges.append((u, v, w))
        idx += 3

    return True, [(n, m, edges)], ""


def _parse_multi_case_input_with_T(in_toks: List[str]) -> Tuple[bool, Optional[List[Tuple[int, int, List[Tuple[int, int, int]]]]], str]:
    if len(in_toks) < 1:
        return False, None, "Input parsing failed: empty input"
    ok, T, err = _parse_int(in_toks[0], "T")
    if not ok:
        return False, None, f"Input parsing failed: {err}"
    if T < 1:
        return False, None, f"Input parsing failed: T must be >= 1, got {T}"

    cases: List[Tuple[int, int, List[Tuple[int, int, int]]]] = []
    idx = 1
    for tc in range(1, T + 1):
        if idx + 1 >= len(in_toks):
            return False, None, f"Input parsing failed: case {tc}: expected n and m but input ended early"
        ok, n, err = _parse_int(in_toks[idx], f"n (case {tc})")
        if not ok:
            return False, None, f"Input parsing failed: {err}"
        ok, m, err = _parse_int(in_toks[idx + 1], f"m (case {tc})")
        if not ok:
            return False, None, f"Input parsing failed: {err}"
        idx += 2

        if n < 2:
            return False, None, f"Input parsing failed: case {tc}: n must be >= 2, got {n}"
        if m < 0:
            return False, None, f"Input parsing failed: case {tc}: m must be >= 0, got {m}"

        need = 3 * m
        if idx + need > len(in_toks):
            return False, None, f"Input parsing failed: case {tc}: expected {need} edge tokens, but input ended early"

        edges: List[Tuple[int, int, int]] = []
        for ei in range(1, m + 1):
            ok, u, err = _parse_int(in_toks[idx], f"u (case {tc}, edge {ei})")
            if not ok:
                return False, None, f"Input parsing failed: {err}"
            ok, v, err = _parse_int(in_toks[idx + 1], f"v (case {tc}, edge {ei})")
            if not ok:
                return False, None, f"Input parsing failed: {err}"
            ok, w, err = _parse_int(in_toks[idx + 2], f"w (case {tc}, edge {ei})")
            if not ok:
                return False, None, f"Input parsing failed: {err}"
            edges.append((u, v, w))
            idx += 3

        cases.append((n, m, edges))

    if idx != len(in_toks):
        return False, None, (
            f"Input parsing failed: expected to consume all tokens for T={T} testcases, "
            f"but {len(in_toks) - idx} extra tokens remain"
        )

    return True, cases, ""


def _parse_input_cases(input_text: str) -> Tuple[bool, Optional[List[Tuple[int, int, List[Tuple[int, int, int]]]]], str]:
    in_toks = input_text.split()
    if not in_toks:
        return False, None, "Input parsing failed: empty input"

    # Prefer single-case exactly matching the statement.
    ok, cases, err = _parse_single_case_input(in_toks)
    if ok:
        return True, cases, ""

    # If it doesn't match single-case, attempt multi-case with leading T (common variant).
    ok2, cases2, err2 = _parse_multi_case_input_with_T(in_toks)
    if ok2:
        return True, cases2, ""

    # Neither format worked.
    return False, None, f"{err}; also failed to parse as multi-testcase with T: {err2}"


def check(input_text: str, output_text: str) -> Tuple[bool, str]:
    ok, cases, err = _parse_input_cases(input_text)
    if not ok or cases is None:
        return _fail(err)

    ok, out_toks, err = _tokenize_output_strict(output_text)
    if not ok:
        return _fail(err)

    ptr = 0
    for tc, (n, m, edges) in enumerate(cases, start=1):
        if ptr >= len(out_toks):
            return _fail(f"Case {tc}: output ended early; expected '-1' or {n} integers")

        if out_toks[ptr] == "-1":
            # Cannot verify unsatisfiability without solving; accept format-correct "-1".
            ptr += 1
            continue

        if ptr + n > len(out_toks):
            return _fail(f"Case {tc}: expected {n} integers, but only {len(out_toks) - ptr} tokens remain")

        ranks = [0] * (n + 1)  # 1-indexed
        seen = [False] * (n + 1)

        for i in range(1, n + 1):
            tok = out_toks[ptr + i - 1]
            ok, val, perr = _parse_int(tok, f"rank[{i}] (case {tc})")
            if not ok:
                return _fail(perr)
            if not (1 <= val <= n):
                return _fail(f"Case {tc}: rank[{i}]={val} is out of range [1..{n}]")
            if seen[val]:
                return _fail(f"Case {tc}: ranks are not distinct: value {val} appears more than once")
            seen[val] = True
            ranks[i] = val

        # Verify each constraint rank[v] - rank[u] == w
        for ei, (u, v, w) in enumerate(edges, start=1):
            if not (1 <= u <= n) or not (1 <= v <= n):
                return _fail(
                    f"Case {tc}: input edge {ei} has vertex out of range: u={u}, v={v}, expected within [1..{n}]"
                )
            lhs = ranks[v] - ranks[u]
            if lhs != w:
                return _fail(
                    f"Case {tc}: constraint violation on edge {ei}: "
                    f"rank[{v}] - rank[{u}] = {ranks[v]} - {ranks[u]} = {lhs}, expected {w}"
                )

        ptr += n

    if ptr != len(out_toks):
        return _fail(f"Extra output tokens: expected end of output after {ptr} tokens, got {len(out_toks) - ptr} extra tokens")

    return True, "OK"


if __name__ == "__main__":
    in_path = os.environ.get("INPUT_PATH")
    out_path = os.environ.get("OUTPUT_PATH")
    if not in_path or not out_path:
        raise SystemExit(2)
    with open(in_path, "r", encoding="utf-8") as f:
        input_text = f.read()
    with open(out_path, "r", encoding="utf-8") as f:
        output_text = f.read()
    ok, _ = check(input_text, output_text)
    print("True" if ok else "False")
