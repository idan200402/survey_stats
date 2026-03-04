import math


def binom_prob(n, k):
    """Probability of exactly k successes under H0: p = 0.5"""
    return math.comb(n, k) * (0.5 ** n)


def p_value(n, k):
    """
    Two-sided binomial p-value for H0: p = 0.5
    n = trials
    k = majority count
    """

    k = max(k, n - k)

    p = 0
    for i in range(k, n + 1):
        p += binom_prob(n, i)

    return min(2 * p, 1)


# --------------------------
# hardcoded experiment data

n = 170

# distribution 1
k1 = 107   # AT

# distribution 2
k2 = 87    # BT

# --------------------------

p1 = p_value(n, k1)
p2 = p_value(n, k2)

print("Distribution 1")
print("majority:", k1, "/", n)
print("p-value:", p1)

print()

print("Distribution 2")
print("majority:", k2, "/", n)
print("p-value:", p2)