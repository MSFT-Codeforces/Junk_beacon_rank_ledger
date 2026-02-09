
from collections import deque, defaultdict

def solve():
    n, m = map(int, input().split())
    
    # Build adjacency list
    # For each edge (u, v, w), we have rank[v] - rank[u] = w
    adj = defaultdict(list)
    for _ in range(m):
        u, v, w = map(int, input().split())
        adj[u].append((v, w))      # rank[v] = rank[u] + w
        adj[v].append((u, -w))     # rank[u] = rank[v] - w
    
    # Assign relative ranks using BFS starting from vertex 1
    rank = [None] * (n + 1)
    rank[1] = 0
    queue = deque([1])
    
    while queue:
        u = queue.popleft()
        for v, w in adj[u]:
            expected_rank = rank[u] + w
            if rank[v] is None:
                rank[v] = expected_rank
                queue.append(v)
            elif rank[v] != expected_rank:
                # Conflict: trying to assign different rank to same vertex
                print(-1)
                return
    
    # Extract ranks for vertices 1 to n
    ranks = [rank[i] for i in range(1, n + 1)]
    
    # Shift ranks so minimum becomes 1
    min_rank = min(ranks)
    ranks = [r - min_rank + 1 for r in ranks]
    
    # Check if result is a valid permutation of [1, 2, ..., n]
    if sorted(ranks) != list(range(1, n + 1)):
        print(-1)
        return
    
    print(' '.join(map(str, ranks)))

solve()
