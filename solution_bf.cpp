#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

struct Edge {
    int u;
    int v;
    long long w;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<Edge> edges(m);
    for (int i = 0; i < m; i++) {
        cin >> edges[i].u >> edges[i].v >> edges[i].w;
    }

    // Brute-force baseline:
    // Enumerate all permutations of ranks 1..n assigned to vertices 1..n,
    // and check whether all constraints rank[v] - rank[u] == w are satisfied.
    //
    // This is correct but factorial-time and intended only for tiny n.
    vector<int> perm(n);
    for (int i = 0; i < n; i++) {
        perm[i] = i + 1;
    }

    do {
        bool ok = true;
        for (const Edge &e : edges) {
            long long diff = (long long)perm[e.v - 1] - (long long)perm[e.u - 1];
            if (diff != e.w) {
                ok = false;
                break;
            }
        }

        if (ok) {
            for (int i = 0; i < n; i++) {
                if (i) cout << ' ';
                cout << perm[i];
            }
            cout << '\n';
            return 0;
        }
    } while (next_permutation(perm.begin(), perm.end()));

    cout << -1 << '\n';
    return 0;
}