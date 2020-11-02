def gcd(a, b):
    assert isinstance(a, int) and isinstance(b, int) and a > 0 and b > 0
    while b != 0:
        r = a % b
        b = a
        a = r
    return a


gcd("int", 5)
