**Beacon Rank Ledger**

Time Limit: **1 seconds**

Memory Limit: **128 MB**

You are given a connected graph with $n$ vertices (beacons) and $m$ edges (paths). You must assign each beacon a distinct activation rank from $1$ to $n$ (i.e., $\text{rank}$ must be a permutation of $1,2,\dots,n$).

Each path is described by three integers $(u, v, w)$ and imposes the exact constraint

$$
\text{rank}[v] - \text{rank}[u] = w.
$$

Note that the physical path is undirected, but the equation direction is fixed as written.

Determine whether such an assignment exists. If it exists, output the ranks for all beacons; otherwise output `-1`.

It can be shown that if a valid assignment exists, it is unique.

**Input Format:-**

The first line contains two integers $n, m$.

The next $m$ lines each contain three integers $u, v, w$ meaning:

$$
\text{rank}[v] - \text{rank}[u] = w.
$$

**Output Format:-**

If no valid assignment exists, print `-1`.

Otherwise, print $n$ integers: $\text{rank}[1]\ \text{rank}[2]\ \dots\ \text{rank}[n]$.

**Constraints:-**

- $2 \le n \le 2 \cdot 10^5$
- $n - 1 \le m \le 2 \cdot 10^5$
- $1 \le u, v \le n$
- $-10^9 \le w \le 10^9$
- The given graph is connected.
**Examples:-**
 - **Input:**
```
6 5
1 2 1000000000
2 3 1000000000
3 4 1000000000
4 5 1000000000
5 6 1000000000
```

 - **Output:**
```
-1
```

 - **Input:**
```
6 8
1 2 -1
2 3 -1
3 4 -1
4 5 -1
5 6 -1
1 3 -2
2 5 -3
6 1 5
```

 - **Output:**
```
6 5 4 3 2 1
```

**Note:-**
In the first example, the constraints form a chain:
$\text{rank}[2]-\text{rank}[1]=10^9,\ \text{rank}[3]-\text{rank}[2]=10^9,\dots,\text{rank}[6]-\text{rank}[5]=10^9$.
Adding them gives
$$
\text{rank}[6]-\text{rank}[1]=5\cdot 10^9.
$$
But in any permutation of $\{1,2,3,4,5,6\}$ we always have $|\text{rank}[6]-\text{rank}[1]|\le 5$, so these equations cannot be satisfied and the answer is "-1".

In the first example, from the first five edges we get
$\text{rank}[2]=\text{rank}[1]-1,\ \text{rank}[3]=\text{rank}[1]-2,\dots,\text{rank}[6]=\text{rank}[1]-5$.
The extra edges are consistent with this (for instance, $\text{rank}[3]-\text{rank}[1]=-2$, $\text{rank}[5]-\text{rank}[2]=-3$, and $\text{rank}[1]-\text{rank}[6]=5$).
Choosing $\text{rank}[1]=6$ makes the ranks exactly a permutation of $\{1,2,3,4,5,6\}$, yielding:
$\text{rank}[1..6]=6,5,4,3,2,1$.