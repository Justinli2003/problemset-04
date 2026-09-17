# CMPS 6610 Problem Set 04
## Answers

**Name:**_________________________


Place all written answers from `problemset-04.md` here for easier grading.




- **1d.**

File | Fixed-Length Coding | Huffman Coding | Huffman vs. Fixed-Length
----------------------------------------------------------------------
f1.txt    |    1,340    |    826    |  0.616
alice29.txt    |    1,039,367    |    676,374    |  0.651
asyoulik.txt    |    876,253    |    606,448    |  0.692
grammar.lsp    |    26,047    |    17,356    |  0.666
fields.c    |    78,050    |    56,206    |  0.720

  (All costs in bits. `f1.txt` has an alphabet of 25 distinct characters, so
  fixed-length uses `ceil(lg 25) = 5` bits per character; the other four files
  have 68–90 distinct characters and use 7 bits.)

  **Is there a consistent trend?** Yes. Huffman coding consistently costs about
  **62%–72% of the fixed-length encoding**, i.e. it saves roughly a third of the
  bits, and it never does worse. The savings are remarkably stable across files
  that differ enormously in size (268 characters up to 148,481) and in kind
  (English prose, a play, Lisp source, C source).

  The reason for the consistency is that Huffman's average code length tracks
  the *entropy* of the character distribution almost exactly:

  | File | entropy `H` (bits/char) | Huffman (bits/char) | fixed (bits/char) |
  |------|------------------------|---------------------|-------------------|
  | f1.txt | 3.035 | 3.082 | 5 |
  | alice29.txt | 4.513 | 4.555 | 7 |
  | asyoulik.txt | 4.808 | 4.845 | 7 |
  | grammar.lsp | 4.632 | 4.664 | 7 |
  | fields.c | 5.008 | 5.041 | 7 |

  Huffman lands within 0.05 bits of the entropy in every case (it must, since
  `H <= Huffman < H + 1`), whereas fixed-length always pays `ceil(lg |S|)` bits
  regardless of how the characters are actually distributed. So the ratio is
  essentially `H / ceil(lg |S|)`. Natural text is far from uniform — space and
  `e` are enormously more common than `q` or `z` — and Huffman converts exactly
  that skew into savings.

  The trend also explains the spread within the table: `fields.c` has the
  highest ratio (0.720) because it has the flattest distribution (entropy 5.01
  of a possible 6.49), while `f1.txt` has the lowest (0.616) because its
  distribution is the most skewed relative to its alphabet size.


- **1e.** (the second part also labelled "1d" in `problemset-04.md`)

  Suppose every character in `S` has the same frequency, and the document has
  `n` characters total, so each of the `|S|` characters occurs `n/|S|` times.

  With equal frequencies Huffman's greedy merging always combines nodes of
  (nearly) equal weight, so it builds an **essentially balanced** tree. Two
  cases:

  - **If `|S| = 2^m` is a power of two**, the tree is perfectly balanced: every
    character sits at depth `m = lg |S|`, so every code is exactly `lg |S|` bits
    and the total cost is

    ```
    n * lg |S|  =  n * ceil(lg |S|)  =  the fixed-length cost
    ```

    Huffman gives **no savings whatsoever** — it produces (one of the) optimal
    fixed-length codes.

  - **If `|S|` is not a power of two**, the tree is almost-complete: code lengths
    are `floor(lg |S|)` or `ceil(lg |S|)`, and the expected cost is
    `n * lg |S|` rounded up slightly. This beats the fixed-length cost of
    `n * ceil(lg |S|)` by less than `n` bits, i.e. by under 1 bit per character.

  So the **expected cost is `n * lg |S|` bits**, or `lg |S|` bits per character.

  **Is it consistent across documents?** Yes — completely. Under the uniform
  assumption the cost depends only on the alphabet size `|S|` and the document
  length `n`, and not at all on the content: any two documents with the same
  alphabet size and the same length cost exactly the same. That is the opposite
  of the situation in part 1d, where the cost depended heavily on how skewed
  each file's distribution was.

  This is also the **worst case for Huffman coding**. The uniform distribution
  is the one that maximizes entropy (`H = lg |S|`), so there is no statistical
  redundancy left to exploit. Huffman only wins when frequencies are unequal,
  and the more unequal they are, the more it wins.


- **2a.** Construct a binary min-heap algorithm

  **Setup.** Given an array `A[0..n-1]`, view it as an almost-complete binary
  tree in the usual implicit way: node `i` has children `2i+1` and `2i+2`, and
  parent `floor((i-1)/2)`. The key observation is that the indices
  `floor(n/2), ..., n-1` are exactly the **leaves**, and a leaf is already a
  valid min-heap all by itself. So only the first `floor(n/2)` nodes need any
  work.

  **Algorithm (bottom-up heapify, i.e. Floyd's algorithm).**

  ```
  build-min-heap (A) =
    for i = floor(n/2) - 1 downto 0 :
        sift-down (A, i)

  sift-down (A, i) =
    let c = the index of the smaller child of i (if i has any children)
    in  if i has a child and A[c] < A[i] then
            swap A[i] and A[c]
            sift-down (A, c)
        else
            ()                      (* heap property already holds at i *)
    end
  ```

  **Correctness.** The loop runs in *decreasing* index order, which means we
  process the tree bottom-up: when we call `sift-down(A, i)`, both subtrees of
  `i` are already valid min-heaps. `sift-down` then pushes `A[i]` down along a
  single root-to-leaf path until it is no larger than both of its children,
  which restores the heap property at `i` without breaking it anywhere below.
  By induction, once `i = 0` is processed the whole array is a min-heap.

  **Why this is `O(n)` and not `O(n log n)`.** The naive approach — start with
  an empty heap and `insert` each of the `n` elements — costs `O(log n)` per
  insert and `O(n log n)` total. Bottom-up heapify is cheaper because
  `sift-down` from a node of **height** `h` costs `O(h)`, and in an
  almost-complete tree the overwhelming majority of nodes have tiny height:
  there are at most `ceil(n / 2^(h+1))` nodes at height `h`. Summing:

  ```
  W(n)  =  sum over h = 0 .. lg n  of  ceil(n / 2^(h+1)) * O(h)
        <= O(n) * sum over h >= 0 of h / 2^(h+1)
        =  O(n) * 1                        (since sum_{h>=0} h/2^h = 2)
        =  O(n)
  ```

  In words: half the nodes are leaves and cost `O(0)`, a quarter are at height 1
  and cost `O(1)`, an eighth are at height 2 and cost `O(2)`, and so on. The
  series `sum h/2^h` converges, so the total is linear. The essential difference
  from the insert-based method is the *direction*: sifting **down** from mostly
  short nodes is cheap, whereas sifting **up** from a leaf always risks the full
  `lg n` height.


- **2b.** Span of your algorithm

  The loop as written is sequential, but it does not have to be. All nodes at
  the **same height** are independent — their subtrees are disjoint, so their
  `sift-down` calls touch disjoint sets of array entries and can run in
  parallel. The only real dependency is between heights: a node at height `h`
  can be sifted down only after everything at heights `< h` is already a valid
  heap. So we process the tree level by level:

  ```
  for h = 1 to lg n :
      in parallel, sift-down every node at height h
  ```

  - There are `lg n` levels, which must be done in order.
  - Level `h` has span `O(h)`, because a single `sift-down` from height `h`
    walks a path of length at most `h`, and all the sift-downs at that level
    happen simultaneously.

  ```
  S(n)  =  sum over h = 1 .. lg n  of  O(h)  =  O( (lg n)^2 )
  ```

  So the **span is `O(log^2 n)`** with work `O(n)`, giving parallelism
  `O(n / log^2 n)` — highly parallel.

  (If we instead leave the loop sequential, the span equals the work, `O(n)`.
  The level-by-level version is what buys the parallelism.)


- **3a.** Greedy algorithm for making change

  Denominations are `2^0, 2^1, ..., 2^k`.

  **Greedy rule: repeatedly hand over the largest coin whose value does not
  exceed the amount still owed.**

  ```
  greedy-change (N) =
    let coins = <>
    while N > 0 :
        let m = the largest index with 2^m <= N   (* m = min(k, floor(lg N)) *)
        coins = coins + <2^m>
        N = N - 2^m
    return coins
  ```

  **What this actually computes.** Assuming `2^k >= N` (so the denominations go
  high enough), this is exactly the **binary representation of `N`**: subtracting
  the largest power of two `2^m <= N` clears the highest set bit of `N`, so the
  algorithm hands over one coin of value `2^j` for each bit `j` that is set in
  `N`, and nothing else. The number of coins is therefore `popcount(N)`, the
  number of 1-bits in `N`.

  That is the "very clever reason" for the denominations: making change in
  Geometrica is just writing the amount in binary, and the greedy answer is
  automatically optimal (proved below). If `N > 2^k`, the algorithm first hands
  over `floor(N / 2^k)` coins of the largest denomination and then writes the
  remainder `N mod 2^k` in binary.


- **3b.** Optimality proof

  Let `OPT(N)` denote the minimum number of coins summing to `N`. Assume
  `2^k >= N` (otherwise apply the argument to `N mod 2^k` after the forced
  `floor(N/2^k)` largest coins).

  **Lemma.** In any optimal solution, each denomination `2^j` with `j < k` is
  used at most once.

  *Proof.* Suppose an optimal solution used two coins of value `2^j` with
  `j < k`. Replace that pair with a single coin of value `2^(j+1)`, which exists
  as a denomination since `j + 1 <= k`. The total value is unchanged
  (`2^j + 2^j = 2^(j+1)`), but the coin count drops by one — contradicting
  optimality. `[]`

  **Greedy choice property.** Let `2^m` be the largest denomination with
  `2^m <= N`. Then *every* optimal solution for `N` uses at least one coin of
  value `2^m`.

  *Proof.* Suppose some optimal solution `S` uses only coins of value at most
  `2^(m-1)`. By the Lemma, `S` contains at most one coin of each denomination
  `2^0, ..., 2^(m-1)`, so its total value is at most

  ```
  2^0 + 2^1 + ... + 2^(m-1)  =  2^m - 1  <  2^m  <=  N.
  ```

  So `S` cannot sum to `N` — a contradiction. Hence `S` must contain a coin of
  value `2^m`. `[]`

  This is exactly the greedy choice property: the coin the greedy algorithm
  takes first is contained in an optimal solution, so committing to it costs us
  nothing.

  **Optimal substructure.** For `N > 0`, `OPT(N) = 1 + OPT(N - 2^m)`.

  *Proof.* (`<=`) Take an optimal solution for `N - 2^m` and add one coin `2^m`;
  this is a valid solution for `N`, so `OPT(N) <= 1 + OPT(N - 2^m)`.

  (`>=`) By the greedy choice property, some optimal solution `S` for `N`
  contains a coin `2^m`. Then `S \ {2^m}` sums to `N - 2^m` using
  `OPT(N) - 1` coins, so `OPT(N - 2^m) <= OPT(N) - 1`.

  Moreover `S \ {2^m}` must itself be *optimal* for `N - 2^m`: if some solution
  `S'` for `N - 2^m` used strictly fewer coins, then `S' ∪ {2^m}` would be a
  solution for `N` with fewer than `|S|` coins, contradicting the optimality of
  `S`. This cut-and-paste argument is the optimal substructure property —
  an optimal solution is built from an optimal solution to a smaller instance.
  `[]`

  **Conclusion.** By induction on `N`. Base case: `N = 0` needs 0 coins, and
  greedy returns none. Inductive step: greedy's first coin `2^m` belongs to some
  optimal solution (greedy choice), and greedy then solves `N - 2^m` optimally
  (inductive hypothesis), so by optimal substructure greedy produces
  `1 + OPT(N - 2^m) = OPT(N)` coins. Greedy is optimal. `[]`


- **3c.** Work and span of your algorithm

  The natural measure of input size here is the number of **bits** of `N`, which
  is `b = floor(lg N) + 1`, together with the `k+1` denominations. (Reporting a
  bound in terms of `N` itself would be misleading — `N` is exponential in its
  own encoding length.)

  - **Work: `O(k) = O(log N)`.** The loop removes the highest set bit of `N` on
    each iteration, so it runs `popcount(N) <= b` times, and finding the largest
    `2^m <= N` is `O(1)` with a bit-length operation (or `O(k)` by scanning the
    denominations, which would give `O(k^2)` overall — still polynomial in the
    input size).

  - **Span: `O(log N)`** for the loop as written, since each iteration depends
    on the remainder left by the previous one.

  **But the loop is unnecessary.** As shown in 3a, the answer *is* the binary
  representation of `N`: the coin multiset is
  `{ 2^j : bit j of N is 1 }`. Each bit can be examined independently, so
  producing the set of coins is a `map` over the `b` bits:

  - Work `O(b) = O(log N)`, span `O(1)`.

  and if we also want the *count* of coins, that is a `reduce` (a sum) over the
  bits:

  - Work `O(log N)`, span `O(log b) = O(log log N)`.

  So the algorithm is linear in the size of the input and essentially perfectly
  parallel.


- **4a.** Fortuito counter example proof

  **Counterexample 1 — greedy uses too many coins.**
  Denominations `{1, 3, 4}`, and `N = 6`.

  - Greedy: take `4` (largest `<= 6`), leaving `2`; then `1`, leaving `1`; then
    `1`. Result: `4 + 1 + 1` = **3 coins**.
  - Optimal: `3 + 3` = **2 coins**.

  Greedy is not optimal. The problem is that grabbing the `4` destroys the
  ability to use the `3`s, which tile `6` perfectly.

  **Counterexample 2 — greedy fails to make change at all.**
  Denominations `{3, 4}`, and `N = 6`.

  - Greedy: take `4`, leaving `2`. No denomination is `<= 2`, so greedy gets
    stuck and reports that change cannot be made.
  - But `3 + 3 = 6` works fine.

  This is worse than suboptimal: greedy returns *no* answer for an instance that
  is perfectly solvable, so it is not even correct as a feasibility test.

  (For completeness, change genuinely is impossible sometimes — e.g.
  denominations `{2, 4}` with `N = 5` — so any correct algorithm has to be able
  to report "impossible".)


- **4b.** Optimal substructure property

  Let the denominations be `D_0, ..., D_k` (arbitrary positive integers,
  unlimited supply of each), and define

  ```
  OPT(v) = the minimum number of coins summing to exactly v,
           or infinity if no such multiset exists.
  ```

  **Property.** `OPT(0) = 0`, and for `v > 0`,

  ```
  OPT(v)  =  1 + min { OPT(v - D_i) : 0 <= i <= k and D_i <= v }
  ```

  with the convention that the minimum over an empty set is `infinity`.
  Furthermore, if an optimal solution `S` for `v` contains a coin `D_i`, then
  `S \ {D_i}` is an *optimal* solution for `v - D_i`.

  **Proof.**

  (`<=`) Fix any `i` with `D_i <= v` for which `OPT(v - D_i)` is finite, and let
  `S'` be an optimal solution for `v - D_i`. Then `S' ∪ {D_i}` sums to `v` and
  uses `OPT(v - D_i) + 1` coins, so `OPT(v) <= 1 + OPT(v - D_i)`. Since this
  holds for every admissible `i`, it holds for the minimum.

  (`>=`) Let `S` be an optimal solution for `v`, so `|S| = OPT(v)`. Since
  `v > 0`, `S` is non-empty; pick any coin `D_i ∈ S`. Note `D_i <= v` because
  the coins are positive and sum to `v`. Then `S \ {D_i}` sums to `v - D_i`
  using `|S| - 1` coins, so

  ```
  OPT(v - D_i) <= |S| - 1 = OPT(v) - 1,
  ```

  and therefore `1 + min_j OPT(v - D_j) <= 1 + OPT(v - D_i) <= OPT(v)`.

  Together the two inequalities give equality.

  **Cut-and-paste (the substructure claim itself).** Suppose `S \ {D_i}` were
  *not* optimal for `v - D_i`, i.e. some `T` sums to `v - D_i` with
  `|T| < |S| - 1`. Then `T ∪ {D_i}` sums to `v` with `|T| + 1 < |S|` coins,
  contradicting the optimality of `S`. So an optimal solution to the problem
  necessarily contains an optimal solution to the subproblem — which is exactly
  the optimal substructure property. `[]`

  Note what this does *not* say: it does not tell us *which* `D_i` to remove, so
  we must try all `k+1` of them. That is precisely the difference from Part 3,
  where the greedy choice property identified the right coin (`2^m`) for free.
  Feasibility comes along for free too: change can be made for `N` exactly when
  `OPT(N) < infinity`.


- **4c.** Fortuito dynamic programming algorithm

  The recurrence in 4b has **overlapping subproblems** — `OPT(v)` is needed by
  `OPT(v + D_i)` for every `i`, so a plain recursive evaluation would recompute
  it exponentially many times. Memoizing gives a DP over the `N+1` subproblems
  `OPT(0), ..., OPT(N)`.

  **Bottom-up version.**

  ```
  make-change (N, D) =
    let OPT[0] = 0, choice[0] = none
    for v = 1 to N :
        OPT[v] = infinity
        for i = 0 to k :
            if D_i <= v and 1 + OPT[v - D_i] < OPT[v] :
                OPT[v]    = 1 + OPT[v - D_i]
                choice[v] = i
    in
        if OPT[N] = infinity then "change cannot be made"
        else OPT[N], with the coins recovered by following
             choice[N], choice[N - D_choice[N]], ... back down to 0
    end
  ```

  The `choice` array lets us reconstruct the actual coins in `O(OPT(N))` time
  after the fact, which is why we only need to store counts during the main loop.

  **Work.** There are `N` subproblems and each one takes a minimum over `k+1`
  denominations at `O(1)` per denomination:

  ```
  W  =  O(N k)
  ```

  **Span.** The values must be filled in increasing order of `v`, because
  `OPT[v]` reads `OPT[v - D_i]` for smaller indices — that is a **dependency
  chain of length `N`** and it cannot be parallelized away. Within a single `v`,
  however, the `k+1` candidates are independent, so the minimum is a `reduce`
  with span `O(log k)`:

  ```
  S  =  O(N log k)
  ```

  So the parallelism is only `O(k / log k)`: we can parallelize *across
  denominations* but not *across amounts*. Space is `O(N)`.

  **Top-down memoization** gives the same asymptotics: each of the `N+1` distinct
  subproblems is solved once at `O(k)` work, so `O(Nk)` work, and the recursion
  depth is `N / min_i D_i = O(N)`, giving `O(N log k)` span. Top-down has the
  practical advantage of only touching subproblems that are actually reachable
  from `N`; bottom-up avoids recursion overhead and is easier to parallelize
  across the inner loop.

  **A caveat worth stating.** `O(Nk)` is **pseudo-polynomial**, not polynomial.
  The input `N` is written in `O(log N)` bits, so the running time is
  *exponential in the size of the input encoding*. This is expected — coin change
  is a special case of the knapsack family and is NP-hard in the general
  (binary-encoded) setting.


- **5a.** Weighted task selection: Optimal substructure?

  **Yes, the optimal substructure property holds.**

  **Setup.** Sort the tasks by finish time, so `f_0 <= f_1 <= ... <= f_(n-1)`.
  For each `i` define

  ```
  p(i) = the largest index j < i with f_j <= s_i   (or -1 if there is none),
  ```

  i.e. the last task, in finish-time order, that is compatible with `a_i`
  because it finishes before `a_i` starts. Let

  ```
  OPT(i) = the maximum total value of a set of pairwise non-overlapping tasks
           chosen from { a_0, ..., a_i },     with OPT(-1) = 0.
  ```

  **Property.** For `0 <= i <= n-1`,

  ```
  OPT(i)  =  max( OPT(i-1),  v_i + OPT(p(i)) )
  ```

  and the answer to the whole problem is `OPT(n-1)`.

  **Proof.** Let `S` be an optimal solution for `{a_0, ..., a_i}`, so
  `value(S) = OPT(i)`. Exactly one of two cases holds.

  *Case 1: `a_i ∉ S`.* Then `S` is a feasible set drawn from
  `{a_0, ..., a_(i-1)}`, so `value(S) <= OPT(i-1)`. Conversely any feasible set
  for `{a_0, ..., a_(i-1)}` is feasible for `{a_0, ..., a_i}`, so
  `OPT(i) >= OPT(i-1)`. Hence `OPT(i) = OPT(i-1)` in this case.

  *Case 2: `a_i ∈ S`.* Every other task `a_j ∈ S` must be compatible with
  `a_i`. Since `j < i` implies `f_j <= f_i`, a task overlapping `a_i` could only
  do so by finishing after `s_i`; so compatibility forces `f_j <= s_i`, which by
  the definition of `p(i)` means `j <= p(i)`. Therefore `S \ {a_i}` is a
  feasible set drawn from `{a_0, ..., a_(p(i))}`, and

  ```
  value(S) = v_i + value(S \ {a_i}) <= v_i + OPT(p(i)).
  ```

  **Cut-and-paste.** `S \ {a_i}` is in fact *optimal* for
  `{a_0, ..., a_(p(i))}`. Suppose not: let `T` be feasible for that subproblem
  with `value(T) > value(S \ {a_i})`. Every task in `T` finishes by `s_i`, so
  `T ∪ {a_i}` is feasible for `{a_0, ..., a_i}` and has value
  `v_i + value(T) > value(S)` — contradicting the optimality of `S`. So an
  optimal solution contains an optimal solution to a subproblem, which is the
  optimal substructure property.

  The two cases are exhaustive, and both bounds are attainable (take the
  optimal solution for `i-1`, or the optimal solution for `p(i)` plus `a_i`), so
  `OPT(i) = max(OPT(i-1), v_i + OPT(p(i)))`. `[]`

  Note that sorting by finish time is what makes the subproblems line up as
  simple *prefixes* `{a_0, ..., a_i}` — without it, "the tasks compatible with
  `a_i`" would not be a contiguous range and the subproblem structure would
  not collapse to a single index.


- **5b.** Does the greedy choice property hold?

  **No.** For the unweighted problem, "always take the task with the earliest
  finish time" satisfies the greedy choice property, because all tasks are worth
  the same and finishing earliest leaves the most room for everything else.
  Once tasks carry values, no such local rule works: whether a task is worth
  taking depends on the *value of what it blocks*, which is a global property of
  the rest of the instance. Here are two natural greedy criteria and instances
  where each fails. Tasks are written as `(s, f, v)`.

  **Counterexample 1 — greedy by earliest finish time.**

  ```
  a_0 = (0, 1, 1)
  a_1 = (0, 10, 100)
  ```

  Greedy takes `a_0` because `f_0 = 1` is earliest. That rules out `a_1`, which
  starts at 0 and so overlaps. Greedy's total value is **1**. The optimal
  solution is `{a_1}` with value **100**. Greedy is off by a factor of 100, and
  by scaling `v_1` this ratio can be made arbitrarily bad.

  **Counterexample 2 — greedy by largest value.**

  ```
  a_0 = (0, 10, 10)
  a_1 = (0, 4, 9)
  a_2 = (5, 10, 9)
  ```

  Greedy takes `a_0` because `v_0 = 10` is the largest value. `a_0` occupies the
  whole interval `[0, 10)`, so it overlaps both `a_1` and `a_2`, and greedy
  stops with total value **10**. But `a_1` and `a_2` are compatible with each
  other (`f_1 = 4 <= 5 = s_2`), so the optimal solution is `{a_1, a_2}` with
  value **18**. Greedy is fooled by one fat task that blocks two good ones.

  **Counterexample 3 — greedy by shortest duration** (a third, for good
  measure).

  ```
  a_0 = (3, 6, 1)      duration 3
  a_1 = (0, 4, 50)     duration 4
  a_2 = (5, 9, 50)     duration 4
  ```

  Greedy takes the shortest task `a_0`, which overlaps both `a_1` and `a_2`,
  for a total of **1**; the optimum is `{a_1, a_2}` with value **100**.

  **Why every local criterion fails.** A greedy rule commits to a task using
  only that task's own `(s, f, v)`. But the correct decision requires comparing
  `v_i` against the best total value obtainable from the tasks `a_i` would
  displace — and that quantity is not a function of `a_i` alone. This is exactly
  the tradeoff between a task's value and the room it consumes, and it is why we
  fall back on dynamic programming: the DP considers *both* alternatives at
  every task ("take it" versus "skip it") instead of committing to one.


- **5c.** Dynamic programming algorithm for Weighted Task Selection

  Directly implementing the recurrence from 5a:

  ```
  weighted-task-selection (A) =
    let
      (* 1. sort by finish time *)
      A = sort A by f                          (* f_0 <= f_1 <= ... <= f_(n-1) *)

      (* 2. for each i, find the last task compatible with a_i, by binary
            search over the sorted finish times for the largest j with f_j <= s_i *)
      p = < binary-search (f, s_i) : 0 <= i < n >

      (* 3. fill the table in increasing i *)
      OPT[-1] = 0
      for i = 0 to n-1 :
          skip = OPT[i-1]
          take = v_i + OPT[p(i)]
          OPT[i]    = max(skip, take)
          choice[i] = (take > skip)
    in
      OPT[n-1]      (* recover the actual set by walking choice backwards:
                       if choice[i] then output a_i and jump to p(i),
                       else move to i-1 *)
    end
  ```

  **Work.**

  | Step | Work | Span |
  |------|------|------|
  | 1. sort by finish time | `O(n log n)` | `O(log^2 n)` |
  | 2. all `p(i)` (n independent binary searches) | `O(n log n)` | `O(log n)` |
  | 3. fill `OPT[0..n-1]` | `O(n)` | `O(n)` |
  | 4. reconstruct the chosen set | `O(n)` | `O(n)` |

  - **Work: `O(n log n)`**, dominated by the sort and the `n` binary searches.
    The DP table itself is only `O(n)` — each entry is a single `max` of two
    already-computed values. Space is `O(n)`.

  - **Span: `O(n)`**, dominated by step 3. `OPT[i]` reads `OPT[i-1]`, so the
    table entries form a dependency chain of length `n` that cannot be broken:
    we cannot know whether to take `a_i` until we know the best value achievable
    on the prefix before it.

  So the parallelism is only `O(log n)`. The preprocessing (sorting and the
  binary searches) parallelizes beautifully — those `n` binary searches are
  completely independent — but the recurrence itself is essentially sequential,
  which is typical of one-dimensional dynamic programs.

  Compare this with the unweighted problem, which the greedy algorithm solves in
  `O(n log n)` work (just the sort) and a single sequential pass. The DP pays no
  extra asymptotic work here; what we lose by having weights is the ability to
  commit to a choice immediately, which is what the `choice` array and the
  backward reconstruction pass restore.
