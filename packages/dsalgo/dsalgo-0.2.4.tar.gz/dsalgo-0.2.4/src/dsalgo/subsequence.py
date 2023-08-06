from __future__ import annotations

import typing

from dsalgo.type import T


def count_common_subsequences(
    a: typing.Sequence[T],
    b: typing.Sequence[T],
    mod: int | None = None,
) -> int:
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    for i in range(n):
        dp[i + 1][0] = 1
    for j in range(m):
        dp[0][j + 1] = 1
    for i in range(n):
        for j in range(m):
            dp[i + 1][j + 1] = dp[i][j + 1] + dp[i + 1][j] - dp[i][j]
            dp[i + 1][j + 1] += dp[i][j] * (a[i] == b[j])
            if mod:
                dp[i + 1][j + 1] %= mod
    return dp[-1][-1]


def longest_common_subsequence(
    a: typing.Sequence[T],
    b: typing.Sequence[T],
) -> list[T]:
    n, m = len(a), len(b)
    length = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            length[i + 1][j + 1] = max(
                length[i][j + 1],
                length[i + 1][j],
                length[i][j] + (b[j] == a[i]),
            )
    lcs = []
    i, j = n - 1, m - 1
    while i >= 0 and j >= 0:
        x = length[i + 1][j + 1]
        if length[i + 1][j] == x:
            j -= 1
            continue
        if length[i][j + 1] == x:
            i -= 1
            continue
        lcs.append(a[i])
        i -= 1
        j -= 1
    return lcs[::-1]


def count_subsequences(arr: typing.Sequence[int]) -> int:
    ...
