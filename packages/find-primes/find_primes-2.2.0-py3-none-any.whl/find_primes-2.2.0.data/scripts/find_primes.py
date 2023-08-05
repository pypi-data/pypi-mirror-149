#!python3

'''
The CLI Tool.
'''

from math import log, sqrt, log2, ceil, floor, gcd
from random import randint, randrange
from functools import reduce
from operator import mul
from argparse import ArgumentParser

NUMPY_ENABLED = True
try:
    from numpy import ones, nonzero, __version__
    print('Detected numpy version {__version__}'.format(**locals()))

except ImportError:
    print('Numpy is not found! Finding primes will be slower!')
    NUMPY_ENABLED = False

print()

def _check_num(n):
    '''
    Internel function to check the input.
    '''
    if not isinstance(n, int):
        raise TypeError('Type of argument n should be int, got {type(n).__name__}'.format(**locals()))

    if n <= 0:
        raise ValueError('The number of argument n should be greater than 0, got {n}'.format(**locals()))

def _check_factors(ans, n, retry = 1, max_retries = 3):
    '''
    Internel function to check the output.
    '''
    if reduce(mul, ans) == n:
        return 0
    
    if retry == max_retries + 1:
        print('Factor Error. The multiplication of {ans} is not {n}.'.format(**locals()))
        raise FactorError('Factor Error. The multiplication of {ans} is not {n}.'.format(**locals()))
    
    print('Factor Error. The multiplication of {ans} is not {n}. Retry {retry}.'.format(**locals()))

    return retry + 1

def is_prime(n):
    '''
    If n is prime, return True.
    '''
    _check_num(n)
    if n in [2, 3, 5, 7]:
        return True

    if not (n % 10 % 2) or n % 10 not in [1, 3, 7, 9] or n == 1 or not isinstance(n, int):
        return False

    for i in range(2, int(n ** 0.5 + 1)):
        if n % i == 0:
            return False

    return True

def all_primes(n, output = 'array'):
    '''
    Return a prime list below n.

    Arguments:
    output ----- 'array' or 'list' ----- The output type of the function.
    '''
    _check_num(n)
    if NUMPY_ENABLED:
        sieve = ones(n + 1, dtype = bool)

    else:
        sieve = [True] * (n + 1)

    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            for j in range(i ** 2, n + 1, i):
                sieve[j] = False

    if NUMPY_ENABLED:
        s = nonzero(sieve)[0]
        if output == 'list':
            return s.tolist()[2:]

        return s[2:]

    else:
        return [x for x in range(2, n + 1) if sieve[x]]

class FactorError(Exception):
    pass

def factor_siqs(n):
    '''
    Return a list that has all factors of n.
    '''
    MAX_DIGITS_POLLARD = 30
    POLLARD_QUICK_ITERATIONS = 20
    MIN_DIGITS_POLLARD_QUICK2 = 45
    POLLARD_QUICK2_ITERATIONS = 25
    SIQS_TRIAL_DIVISION_EPS = 25
    SIQS_MIN_PRIME_POLYNOMIAL = 400
    SIQS_MAX_PRIME_POLYNOMIAL = 4000

    class Polynomial:
        def __init__(self, coeff = [], a = None, b = None):
            self.coeff = coeff
            self.a = a
            self.b = b

        def eval(self, x):
            res = 0
            for a in self.coeff[::-1]:
                res *= x
                res += a
            return res

    class FactorBasePrime:
        def __init__(self, p, tmem, lp):
            self.p = p
            self.soln1 = None
            self.soln2 = None
            self.tmem = tmem
            self.lp = lp
            self.ainv = None

    def lowest_set_bit(a):
        b = (a & -a)
        low_bit = -1
        while (b):
            b >>= 1
            low_bit += 1

        return low_bit

    def to_bits(k):
        k_binary = bin(k)[2:]
        return (bit == '1' for bit in k_binary[::-1])

    def pow_mod(a, k, m):
        r = 1
        b = a
        for bit in to_bits(k):
            if bit:
                r = (r * b) % m

            b = (b * b) % m

        return r

    def is_quadratic_residue(a, p):
        return legendre(a, (p - 1) // 2, 1, p) == 1

    def legendre(a, q, l, n):
        x = q ** l
        if x == 0:
            return 1

        z = 1
        a %= n
        while x != 0:
            if x % 2 == 0:
                a = (a ** 2) % n
                x //= 2

            else:
                x -= 1
                z = (z * a) % n

        return z

    def sqrt_mod_prime(a, p):
        if a == 0:
            return 0

        if p == 2:
            return a

        if p % 2 == 0:
            return None

        p_mod_8 = p % 8
        if p_mod_8 == 1:
            q = p // 8
            e = 3
            while q % 2 == 0:
                q //= 2
                e += 1

            while True:
                x = randint(2, p - 1)
                z = pow_mod(x, q, p)
                if pow_mod(z, 2 ** (e - 1), p) != 1:
                    break

            y = z
            r = e
            x = pow_mod(a, (q - 1) // 2, p)
            v = (a * x) % p
            w = (v * x) % p
            while True:
                if w == 1:
                    return v

                k = 1
                while pow_mod(w, 2 ** k, p) != 1:
                    k += 1

                d = pow_mod(y, 2 ** (r - k - 1), p)
                y = (d ** 2) % p
                r = k
                v = (d * v) % p
                w = (w * y) % p

        elif p_mod_8 == 5:
            v = pow_mod(2 * a, (p - 5) // 8, p)
            i = (2 * a * v * v) % p
            return (a * v * (i - 1)) % p

        else:
            return pow_mod(a, (p + 1) // 4, p)

    def inv_mod(a, m):
        return eea(a, m)[0] % m

    def eea(a, b):
        if a == 0:
            return (0, 1, b)
        x = eea(b % a, a)
        return (x[1] - b // a * x[0], x[0], x[2])

    def is_prime(n):
        if n in [2, 3, 5, 7]:
            return True

        if not (n % 10 % 2) or n % 10 not in [1, 3, 7, 9] or n == 1 or not isinstance(n, int):
            return False

        for i in range(2, int(n ** 0.5 + 1)):
            if n % i == 0:
                return False

        return True

    def siqs_factor_base_primes(n, nf):
        global small_primes
        factor_base = []
        for p in small_primes:
            if is_quadratic_residue(n, p):
                t = sqrt_mod_prime(n % p, p)
                lp = round(log2(p))
                factor_base.append(FactorBasePrime(p, t, lp))
                if len(factor_base) >= nf:
                    break

        return factor_base


    def siqs_find_first_poly(n, m, factor_base):
        p_min_i = None
        p_max_i = None
        for i, fb in enumerate(factor_base):
            if p_min_i is None and fb.p >= SIQS_MIN_PRIME_POLYNOMIAL:
                p_min_i = i
            if p_max_i is None and fb.p > SIQS_MAX_PRIME_POLYNOMIAL:
                p_max_i = i - 1
                break

        if p_max_i is None:
            p_max_i = len(factor_base) - 1

        if p_min_i is None or p_max_i - p_min_i < 20:
            p_min_i = min(p_min_i, 5)

        target = sqrt(2 * float(n)) / m
        target1 = target / ((factor_base[p_min_i].p + factor_base[p_max_i].p) / 2) ** 0.5
        best_q, best_a, best_ratio = None, None, None
        for _ in range(30): 
            a = 1
            q = []
            while a < target1:
                p_i = 0
                while p_i == 0 or p_i in q:
                    p_i = randint(p_min_i, p_max_i)

                p = factor_base[p_i].p
                a *= p
                q.append(p_i)

            ratio = a / target
            if (best_ratio is None or (ratio >= 0.9 and ratio < best_ratio) or best_ratio < 0.9 and ratio > best_ratio):
                best_q = q
                best_a = a
                best_ratio = ratio

        a = best_a
        q = best_q
        s = len(q)
        B = []
        for l in range(s):
            fb_l = factor_base[q[l]]
            q_l = fb_l.p
            gamma = (fb_l.tmem * inv_mod(a // q_l, q_l)) % q_l
            if gamma > q_l // 2:
                gamma = q_l - gamma

            B.append(a // q_l * gamma)

        b = sum(B) % a
        b_orig = b
        if (2 * b > a):
            b = a - b

        g = Polynomial([b * b - n, 2 * a * b, a * a], a, b_orig)
        h = Polynomial([b, a])
        for fb in factor_base:
            if a % fb.p != 0:
                fb.ainv = inv_mod(a, fb.p)
                fb.soln1 = (fb.ainv * (fb.tmem - b)) % fb.p
                fb.soln2 = (fb.ainv * (-fb.tmem - b)) % fb.p

        return g, h, B

    def siqs_find_next_poly(n, factor_base, i, g, B):
        v = lowest_set_bit(i) + 1
        z = -1 if ceil(i / (2 ** v)) % 2 == 1 else 1
        b = (g.b + 2 * z * B[v - 1]) % g.a
        a = g.a
        b_orig = b
        if (2 * b > a):
            b = a - b

        g = Polynomial([b * b - n, 2 * a * b, a * a], a, b_orig)
        h = Polynomial([b, a])
        for fb in factor_base:
            if a % fb.p != 0:
                fb.soln1 = (fb.ainv * (fb.tmem - b)) % fb.p
                fb.soln2 = (fb.ainv * (-fb.tmem - b)) % fb.p

        return g, h

    def siqs_sieve(factor_base, m):
        sieve_array = [0] * (2 * m + 1)
        for fb in factor_base:
            if fb.soln1 is None:
                continue

            p = fb.p
            i_start_1 = -((m + fb.soln1) // p)
            a_start_1 = fb.soln1 + i_start_1 * p
            lp = fb.lp
            if p > 20:
                for a in range(a_start_1 + m, 2 * m + 1, p):
                    sieve_array[a] += lp

                i_start_2 = -((m + fb.soln2) // p)
                a_start_2 = fb.soln2 + i_start_2 * p
                for a in range(a_start_2 + m, 2 * m + 1, p):
                    sieve_array[a] += lp

        return sieve_array

    def siqs_trial_divide(a, factor_base):
        divisors_idx = []
        for i, fb in enumerate(factor_base):
            if a % fb.p == 0:
                exp = 0
                while a % fb.p == 0:
                    a //= fb.p
                    exp += 1


                divisors_idx.append((i, exp))
            if a == 1:
                return divisors_idx

        return None

    def siqs_trial_division(n, sieve_array, factor_base, smooth_relations, g, h, m, req_relations):
        sqrt_n = sqrt(float(n))
        limit = log2(m * sqrt_n) - SIQS_TRIAL_DIVISION_EPS
        for (i, sa) in enumerate(sieve_array):
            if sa >= limit:
                x = i - m
                gx = g.eval(x)
                divisors_idx = siqs_trial_divide(gx, factor_base)
                if divisors_idx is not None:
                    u = h.eval(x)
                    v = gx
                    smooth_relations.append((u, v, divisors_idx))
                    if (len(smooth_relations) >= req_relations):
                        return True

        return False

    def siqs_build_matrix(factor_base, smooth_relations):
        fb = len(factor_base)
        M = []
        for sr in smooth_relations:
            mi = [0] * fb
            for j, exp in sr[2]:
                mi[j] = exp % 2

            M.append(mi)

        return M

    def siqs_build_matrix_opt(M):
        m = len(M[0])
        cols_binary = [''] * m
        for mi in M:
            for j, mij in enumerate(mi):
                cols_binary[j] += '1' if mij else '0'

        return [int(cols_bin[::-1], 2) for cols_bin in cols_binary], len(M), m

    def add_column_opt(M_opt, tgt, src):
        M_opt[tgt] ^= M_opt[src]

    def find_pivot_column_opt(M_opt, j):
        if M_opt[j] == 0:
            return None

        return lowest_set_bit(M_opt[j])

    def siqs_solve_matrix_opt(M_opt, n, m):
        row_is_marked = [False] * n
        pivots = [-1] * m
        for j in range(m):
            i = find_pivot_column_opt(M_opt, j)
            if i is not None:
                pivots[j] = i
                row_is_marked[i] = True
                for k in range(m):
                    if k != j and (M_opt[k] >> i) & 1:
                        add_column_opt(M_opt, k, j)

        perf_squares = []
        for i in range(n):
            if not row_is_marked[i]:
                perfect_sq_indices = [i]
                for j in range(m):
                    if (M_opt[j] >> i) & 1:
                        perfect_sq_indices.append(pivots[j])

                perf_squares.append(perfect_sq_indices)

        return perf_squares

    def siqs_calc_sqrts(square_indices, smooth_relations):
        res = [1, 1]
        for idx in square_indices:
            res[0] *= smooth_relations[idx][0]
            res[1] *= smooth_relations[idx][1]

        res[1] = sqrt_int(res[1])
        return res

    def sqrt_int(n):
        a = n
        s = 0
        o = 1 << (floor(log2(n)) & ~1)
        while o != 0:
            t = s + o
            if a >= t:
                a -= t
                s = (s >> 1) + o

            else:
                s >>= 1

            o >>= 2

        return s

    def kth_root_int(n, k):
        u = n
        s = n + 1
        while u < s:
            s = u
            t = (k - 1) * s + n // pow(s, k - 1)
            u = t // k
        return s

    def siqs_factor_from_square(n, square_indices, smooth_relations):
        sqrt1, sqrt2 = siqs_calc_sqrts(square_indices, smooth_relations)
        return gcd(abs(sqrt1 - sqrt2), n)


    def siqs_find_factors(n, perfect_squares, smooth_relations):
        factors = []
        rem = n
        non_prime_factors = set()
        prime_factors = set()
        for square_indices in perfect_squares:
            fact = siqs_factor_from_square(n, square_indices, smooth_relations)
            if fact != 1 and fact != rem:
                if is_prime(fact):
                    if fact not in prime_factors:
                        prime_factors.add(fact)

                    while rem % fact == 0:
                        factors.append(fact)
                        rem //= fact

                    if rem == 1:

                        break
                    if is_prime(rem):
                        factors.append(rem)
                        rem = 1
                        break

                else:
                    if fact not in non_prime_factors:
                        non_prime_factors.add(fact)

        if rem != 1 and non_prime_factors:
            non_prime_factors.add(rem)
            for fact in sorted(siqs_find_more_factors_gcd(non_prime_factors)):
                while fact != 1 and rem % fact == 0:
                    factors.append(fact)
                    rem //= fact

                if rem == 1 or is_prime(rem):
                    break

        if rem != 1:
            factors.append(rem)

        return factors

    def siqs_find_more_factors_gcd(numbers):
        res = set()
        for n in numbers:
            res.add(n)
            for m in numbers:
                if n != m:
                    fact = gcd(n, m)
                    if fact != 1 and fact != n and fact != m:
                        if fact not in res:
                            res.add(fact)

                        res.add(n // fact)
                        res.add(m // fact)
        return res

    def siqs_choose_nf_m(d):
        if d <= 34:
            return 200, 65536

        if d <= 36:
            return 300, 65536

        if d <= 38:
            return 400, 65536

        if d <= 40:
            return 500, 65536

        if d <= 42:
            return 600, 65536

        if d <= 44:
            return 700, 65536

        if d <= 48:
            return 1000, 65536

        if d <= 52:
            return 1200, 65536

        if d <= 56:
            return 2000, 65536 * 3

        if d <= 60:
            return 4000, 65536 * 3

        if d <= 66:
            return 6000, 65536 * 3

        if d <= 74:
            return 10000, 65536 * 3

        if d <= 80:
            return 30000, 65536 * 3

        if d <= 88:
            return 50000, 65536 * 3

        if d <= 94:
            return 60000, 65536 * 9

        return 100000, 65536 * 9

    def siqs_factorise(n):
        dig = len(str(n))
        nf, m = siqs_choose_nf_m(dig)
        factor_base = siqs_factor_base_primes(n, nf)
        required_relations_ratio = 1.05
        success = False
        smooth_relations = []
        prev_cnt = 0
        i_poly = 0
        while not success:
            required_relations = round(len(factor_base) * required_relations_ratio)
            enough_relations = False
            while not enough_relations:
                if i_poly == 0:
                    g, h, B = siqs_find_first_poly(n, m, factor_base)

                else:
                    g, h = siqs_find_next_poly(n, factor_base, i_poly, g, B)

                i_poly += 1
                if i_poly >= 2 ** (len(B) - 1):
                    i_poly = 0

                sieve_array = siqs_sieve(factor_base, m)
                enough_relations = siqs_trial_division(n, sieve_array, factor_base, smooth_relations, g, h, m, required_relations)

                if (len(smooth_relations) >= required_relations or i_poly % 8 == 0 and len(smooth_relations) > prev_cnt):
                    prev_cnt = len(smooth_relations)

            M = siqs_build_matrix(factor_base, smooth_relations)
            M_opt, M_n, M_m = siqs_build_matrix_opt(M)
            perfect_squares = siqs_solve_matrix_opt(M_opt, M_n, M_m)
            factors = siqs_find_factors(n, perfect_squares, smooth_relations)
            if len(factors) > 1:
                success = True

            else:
                required_relations_ratio += 0.05

        return factors

    def check_factor(n, i, factors):
        while n % i == 0:
            n //= i
            factors.append(i)
            if is_prime(n):
                factors.append(n)
                n = 1

        return n

    def trial_div_init_primes(n, upper_bound):
        global small_primes
        is_prime = [True] * (upper_bound + 1)
        is_prime[0:2] = [False] * 2
        factors = []
        small_primes = []
        max_i = sqrt_int(upper_bound)
        rem = n
        for i in range(2, max_i + 1):
            if is_prime[i]:
                small_primes.append(i)
                rem = check_factor(rem, i, factors)
                if rem == 1:
                    return factors, 1

                for j in (range(i ** 2, upper_bound + 1, i)):
                    is_prime[j] = False

        for i in range(max_i + 1, upper_bound + 1):
            if is_prime[i]:
                small_primes.append(i)
                rem = check_factor(rem, i, factors)
                if rem == 1:
                    return factors, 1

        return factors, rem

    def pollard_brent_f(c, n, x):
        x1 = (x * x) % n + c
        if x1 >= n:
            x1 -= n

        return x1

    def pollard_brent_find_factor(n, max_iter = None):
        y, c, m = (randint(1, n - 1) for _ in range(3))
        r, q, g = 1, 1, 1
        i = 0
        while g == 1:
            x = y
            for _ in range(r):
                y = pollard_brent_f(c, n, y)

            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = pollard_brent_f(c, n, y)
                    q = (q * abs(x - y)) % n

                g = gcd(q, n)
                k += m

            r *= 2
            if max_iter:
                i += 1
                if (i == max_iter):
                    return None

        if g == n:
            while True:
                ys = pollard_brent_f(c, n, ys)
                g = gcd(abs(x - ys), n)
                if g > 1:
                    break

        return g

    def pollard_brent_quick(n, factors):
        rem = n
        while True:
            if is_prime(rem):
                factors.append(rem)
                rem = 1
                break

            digits = len(str(n))
            if digits < MIN_DIGITS_POLLARD_QUICK2:
                max_iter = POLLARD_QUICK_ITERATIONS

            else:
                max_iter = POLLARD_QUICK2_ITERATIONS

            f = pollard_brent_find_factor(rem, max_iter)
            if f and f < rem:
                if is_prime(f):
                    factors.append(f)
                    rem //= f

                else:
                    rem_f = pollard_brent_quick(f, factors)
                    rem = (rem // f) * rem_f

            else:
                break

        return rem

    def check_perfect_power(n):
        largest_checked_prime = small_primes[-1]
        for b in small_primes:
            bth_root = kth_root_int(n, b)
            if bth_root < largest_checked_prime:
                break

            if (bth_root ** b == n):
                return (bth_root, b)

        return None


    def find_prime_factors(n):
        perfect_power = check_perfect_power(n)
        if perfect_power:
            factors = [perfect_power[0]]

        else:
            digits = len(str(n))
            if digits <= MAX_DIGITS_POLLARD:
                factors = [pollard_brent_find_factor(n)]

            else:
                factors = siqs_factorise(n)

        prime_factors = []
        for f in set(factors):
            for pf in find_all_prime_factors(f):
                prime_factors.append(pf)

        return prime_factors

    def find_all_prime_factors(n):
        rem = n
        factors = []
        while rem > 1:
            if is_prime(rem):
                factors.append(rem)
                break

            for f in find_prime_factors(rem):
                while rem % f == 0:
                    rem //= f
                    factors.append(f)

        return factors

    def factor(n):
        if type(n) != int or n < 1:
            return 

        if n == 1:
            return []

        if is_prime(n):
            return [n]

        factors, rem = trial_div_init_primes(n, 1000000)
        if rem != 1:
            digits = len(str(rem))
            if digits > MAX_DIGITS_POLLARD:
                rem = pollard_brent_quick(rem, factors)
                
            if rem > 1:
                for fr in find_all_prime_factors(rem):
                    factors.append(fr)

        factors.sort()
        return factors
    
    return factor(n)

def factor_mpqs(n):
    '''
    Return a list that has all factors of n.
    '''
    PRIMES_31 = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31)
    PRIMONIAL_31 = reduce(mul, PRIMES_31)

    def lcm(a, b):
        return a // gcd(a, b) * b

    class FactoredInteger():
        def __init__(self, integer, factors = None):
            self.integer = int(integer)
            if factors is None:
                self.factors = dict(_factor(self.integer)[0])

            else:
                self.factors = dict(factors)

        @classmethod
        def from_partial_factorization(cls, integer, partial):
            partial_factor = 1
            for p, e in partial.iteritems():
                partial_factor *= p ** e

            return cls(integer // partial_factor) * cls(partial_factor, partial)

        def __iter__(self):
            return self.factors.iteritems()

        def __mul__(self, other):
            if isinstance(other, FactoredInteger):
                integer = self.integer * other.integer
                new_factors = self.factors.copy()
                for p in other.factors:
                    new_factors[p] = new_factors.get(p, 0) + other.factors[p]

                return self.__class__(integer, new_factors)

            else:
                return self * FactoredInteger(other)

        __rmul__ = __mul__

        def __pow__(self, other):
            new_integer = self.integer ** other
            new_factors = {}
            for p in self.factors:
                new_factors[p] = self.factors[p] * other

            return self.__class__(new_integer, new_factors)

        def __mod__(self, other):
            try:
                if other.integer in self.factors:
                    return 0

                return self.integer % other.integer
                
            except AttributeError:
                if int(other) in self.factors:
                    return 0

                return self.integer % int(other)

        def copy(self):
            return self.__class__(self.integer, self.factors.copy())

        def is_divisible_by(self, other):
            if int(other) in self.factors:
                return True

            return not self.integer % int(other)

        def exact_division(self, other):
            divisor = int(other)
            quotient = self.copy()
            if divisor in quotient.factors:
                if quotient.factors[divisor] == 1:
                    del quotient.factors[divisor]

                else:
                    quotient.factors[divisor] -= 1

            elif not isinstance(other, FactoredInteger):
                dividing = divisor
                for p, e in self.factors.iteritems():
                    while not dividing % p:
                        dividing //= p
                        if quotient.factors[p] == 1:
                            del quotient.factors[p]
                            assert dividing % p, dividing

                        else:
                            quotient.factors[p] -= 1

                    if dividing == 1:
                        break

                assert dividing == 1

            else:
                for p, e in other.factors.iteritems():
                    assert p in quotient.factors and quotient.factors[p] >= e
                    if quotient.factors[p] == e:
                        del quotient.factors[p]

                    else:
                        quotient.factors[p] -= e

            quotient.integer //= divisor
            return quotient

        __floordiv__ = exact_division

        def divisors(self):
            divs = [FactoredInteger(1)]
            for p, e in self.factors.iteritems():
                q = FactoredInteger(1)
                pcoprimes = list(divs)
                for j in range(1, e + 1):
                    q *= FactoredInteger(p, {p:1})
                    divs += [k * q for k in pcoprimes]
            return divs

        def proper_divisors(self):
            return self.divisors()[1:-1]

        def prime_divisors(self):
            return self.factors.keys()

    class TestPrime():
        primes = PRIMES_31
        primecache = set(primes)
        def __init__(self, t = 12):
            if isinstance(t, int):
                self.t = FactoredInteger(t)

            else:
                assert isinstance(t, FactoredInteger)
                self.t = t

            powerof2 = self.t.factors[2] + 2
            self.et = FactoredInteger(2 ** powerof2, {2:powerof2})
            for d in self.t.divisors():
                p = d.integer + 1
                if p & 1 and (p in self.primecache or is_prime(p, d.factors)):
                    self.et = self.et * FactoredInteger(p, {p:1})
                    if p in self.t.factors:
                        e = self.t.factors[p]
                        self.et = self.et * FactoredInteger(p ** e, {p:e})

                    self.primecache.add(p)

        def next(self):
            eu = []
            for p in self.primes:
                if p in self.t.factors:
                    eu.append((p - 1) * p ** (self.t.factors[p] - 1))
                else:
                    eu.append(p - 1)
                    break
            p = self.primes[eu.index(min(eu))]
            return self.__class__(self.t * FactoredInteger(p, {p:1}))

    def primitive_root(p):
        pd = FactoredInteger(p - 1).proper_divisors()
        for i in range(2, p):
            for d in pd:
                if pow(i, (p - 1) // d, p) == 1:
                    break

            else:
                return i

    class Zeta():
        def __init__(self, size, pos = None, val = 1):
            self.size = size
            self.z = [0] * self.size
            if pos is not None:
                self.z[pos % self.size] = val

        def __add__(self, other):
            if self.size == other.size:
                m = self.size
                zr_a = Zeta(m)
                for i in range(m):
                    zr_a.z[i] = self.z[i] + other.z[i]

                return zr_a

            else:
                m = lcm(self.size, other.size)
                return self.promote(m) + other.promote(m)

        def __mul__(self, other):
            if not isinstance(other, Zeta):
                zr_m = Zeta(self.size)
                zr_m.z = [x * other for x in self.z]
                return zr_m

            elif self.size == other.size:
                zr_m = Zeta(self.size)
                other = abs(other)
                for k in range(other.size):
                    if not other.z[k]:
                        continue

                    elif other.z[k] == 1:
                        zr_m = zr_m + (self << k)

                    else:
                        zr_m = zr_m + (self << k) * other.z[k]

                return zr_m

            else:
                m = lcm(self.size, other.size)
                return self.promote(m) * other.promote(m)

        __rmul__ = __mul__

        def promote(self, size):
            if size == self.size:
                return abs(self)

            new = Zeta(size)
            r = size // self.size
            for i in range(self.size):
                new.z[i * r] = self.z[i]

            return new

        def weight(self):
            return len(filter(None, self.z))

        def mass(self):
            return sum(self.z)

    def is_prime(n):
        if n in [2, 3, 5, 7]:
            return True

        if not (n % 10 % 2) or n % 10 not in [1, 3, 7, 9] or n <= 1 or not isinstance(n, int):
            return False

        if gcd(n, PRIMONIAL_31) > 1:
            return (n in PRIMES_31)

        if n < 999999999999999:
            for i in range(2, int(n ** 0.5 + 1)):
                if n % i == 0:
                    return False

            return True

        if not smallSpsp(n):
            return False

        if n < 10 ** 12:
            return True
        
        return apr(n)

    class Status():
        def __init__(self):
            self.d = {}

        def yet(self, key):
            self.d[key] = 0

        def done(self, key):
            self.d[key] = 1

        def yet_keys(self):
            return [k for k in self.d if not self.d[k]]

        def isDone(self, key):
            return self.d[key]

        def subodd(self, p, q, n, J):
            s = J.get(1, p, q)
            Jpq = J.get(1, p, q)
            m = s.size
            for x in range(2, m):
                if x % p == 0:
                    continue

                sx = Zeta(m)
                i = x
                j = 1
                while i > 0:
                    sx[j] = Jpq[i]
                    i = (i + x) % m
                    j += 1

                sx[0] = Jpq[0]
                sx = pow(sx, x, n)
                s = s * sx % n

            s = pow(s, n // m, n)
            r = n % m
            t = 1
            for x in range(1, m):
                if x % p == 0:
                    continue

                c = (r * x) // m
                if c:
                    tx = Zeta(m)
                    i = x
                    j = 1
                    while i > 0:
                        tx[j] = Jpq[i]
                        i = (i + x) % m
                        j += 1

                    tx[0] = Jpq[0]
                    tx = pow(tx, c, n)
                    t = t * tx % n

            s = abs(t * s % n)
            if s.weight() == 1 and s.mass() == 1:
                for i in range(1, m):
                    if gcd(m, s.z.index(1)) == 1:
                        self.done(p)
                        
                    return True

            return False

        def sub8(self, q, k, n, J):
            s = J.get(3, q)
            J3 = J.get(3, q)
            m = len(s)
            sx_z = {1:s}
            x = 3
            step = 2
            while m > x:
                z_4b = Zeta(m)
                i = x
                j = 1
                while i != 0:
                    z_4b[j] = J3[i]
                    i = (i + x) % m
                    j += 1

                z_4b[0] = J3[0]
                sx_z[x] = z_4b
                s = pow(sx_z[x], x, n) * s
                step = 8 - step
                x += step

            s = pow(s, n // m, n)
            r = n % m
            step = 2
            x = 3
            while m > x:
                c = r*x
                if c > m:
                    s = pow(sx_z[x], c // m, n) * s

                step = 8 - step
                x += step

            r = r & 7
            if r == 5 or r == 7:
                s = J.get(2, q).promote(m) * s

            s = abs(s % n)

            if s.weight() == 1 and s.mass() == 1:
                if gcd(m, s.z.index(1)) == 1 and pow(q, (n-1) >> 1, n) == n-1:
                    self.done(2)

                return True

            elif s.weight() == 1 and s.mass() == n-1:
                if gcd(m, s.z.index(n-1)) == 1 and pow(q, (n-1) >> 1, n) == n-1:
                    self.done(2)

                return True

            return False

        def sub4(self, q, n, J):
            j2 = J.get(1, 2, q) ** 2
            s = q * j2 % n
            s = pow(s, n >> 2, n)
            if n & 3 == 3:
                s = s * j2 % n
                
            s = abs(s % n)
            if s.weight() == 1 and s.mass() == 1:
                i = s.z.index(1)
                if (i == 1 or i == 3) and pow(q, (n-1) >> 1, n) == n-1:
                    self.done(2)

                return True

            return False

        def sub2(self, q, n):
            s = pow(n - q, (n - 1) >> 1, n)
            if s == n-1:
                if n & 3 == 1:
                    self.done(2)

            elif s != 1:
                return False

            return True

        def subrest(self, p, n, et, J, ub = 200):
            if p == 2:
                q = 5
                while q < 2 * ub + 5:
                    q += 2
                    if not is_prime(q) or et % q == 0:
                        continue

                    if n % q == 0:
                        return False

                    k = vp(q - 1, 2)[0]
                    if k == 1:
                        if n & 3 == 1 and not self.sub2(q, n):
                            return False

                    elif k == 2:
                        if not self.sub4(q, n, J):
                            return False

                    else:
                        if not self.sub8(q, k, n, J):
                            return False

                    if self.isDone(p):
                        return True

                else:
                    return

            else:
                step = p * 2
                q = 1
                while q < step * ub + 1:
                    q += step
                    if not is_prime(q) or et % q == 0:
                        continue

                    if n % q == 0:
                        return False

                    if not self.subodd(p, q, n, J):
                        return False

                    if self.isDone(p):
                        return True

                else:
                    return

    def _factor(n):
        def factor(n):
            if n % 2 == 0:
                return 2

            a = 2
            i = 2
            while True:
                a = pow(a, i, n)
                d = gcd(a - 1, n)
                if d > 1:
                    return d

                i += 1

        num = n
        ans = []
        if is_prime(n):
            ans.append(n)
            return ans

        while True:
            d = factor(num)
            ans.append(d)
            r = num // d
            if is_prime(r):
                ans.append(r)
                break
        
            else:
                num = r
        
        ans.sort()
        result = list(set([(x, ans.count(x)) for x in ans]))
        return result, ans

    class JacobiSum():
        def __init__(self):
            self.shelve = {}

        def get(self, group, p, q = None):
            if q:
                assert group == 1
                if (group, p, q) not in self.shelve:
                    self.make(q)

                return self.shelve[group, p, q]

            else:
                assert group == 2 or group == 3
                if (group, p) not in self.shelve:
                    self.make(p)

                return self.shelve[group, p]

        def make(self, q):
            fx = self.makefx(q)
            qpred = q - 1
            qt = _factor(qpred)[0]
            qt2 = [k for (p, k) in qt if p == 2][0]
            k, pk = qt2, 2 ** qt2
            if k >= 2:
                J2q = Zeta(pk, 1 + fx[1])
                for j in range(2, qpred):
                    J2q[j + fx[j]] = J2q[j + fx[j]] + 1

                self.shelve[1, 2, q] = +J2q
                if k >= 3:
                    J2 = Zeta(8, 3 + fx[1])
                    J3 = Zeta(pk, 2 + fx[1])
                    for j in range(2, qpred):
                        J2[j * 3 + fx[j]] = J2[j * 3 + fx[j]] + 1
                        J3[j * 2 + fx[j]] = J3[j * 2 + fx[j]] + 1

                    self.shelve[3, q] = abs(self.shelve[1, 2, q] * J3)
                    self.shelve[2, q] = abs(J2 ** 2)

            else:
                self.shelve[1, 2, q] = 1

            for (p, k) in qt:
                if p == 2:
                    continue

                pk = p ** k
                Jpq = Zeta(pk, 1 + fx[1])
                for j in range(2, qpred):
                    Jpq[j + fx[j]] = Jpq[j + fx[j]] + 1

                self.shelve[1, p, q] = +Jpq

        @staticmethod
        def makefx(q):
            g = primitive_root(q)
            qpred = q - 1
            qd2 = qpred >> 1
            g_mf = [0, g]
            for _ in range(2, qpred):
                g_mf.append((g_mf[-1] * g) % q)

            fx = {}
            for i in range(1, qd2):
                if i in fx:
                    continue

                j = g_mf.index(q + 1 - g_mf[i])
                fx[i] = j
                fx[j] = i
                fx[qpred - i] = (j - i + qd2) % qpred
                fx[fx[qpred - i]] = qpred - i
                fx[qpred - j] = (i - j + qd2) % qpred
                fx[fx[qpred - j]] = qpred - j

            return fx

    def apr(n):
        L = Status()
        rb = floorsqrt(n) + 1
        el = TestPrime()
        while el.et <= rb:
            el = el.next()

        plist = el.t.factors.keys()
        plist.remove(2)
        L.yet(2)
        for p in plist:
            if pow(n, p - 1, p ** 2) != 1:
                L.done(p)

            else:
                L.yet(p)

        qlist = el.et.factors.keys()
        qlist.remove(2)
        J = JacobiSum()
        for q in qlist:
            for p in plist:
                if (q - 1) % p != 0:
                    continue

                if not L.subodd(p, q, n, J):
                    return False

            k = vp(q - 1, 2)[0]
            if k == 1:
                if not L.sub2(q, n):
                    return False

            elif k == 2:
                if not L.sub4(q, n, J):
                    return False

            else:
                if not L.sub8(q, k, n, J):
                    return False

        for p in L.yet_keys():
            if not L.subrest(p, n, el.et, J):
                return False

        r = int(n)
        for _ in range(1, el.t.integer):
            r = (r * n) % el.et.integer
            if n % r == 0 and r != 1 and r != n:
                return False

        return True

    def spsp(n, base, s = None, t = None):
        if s is None or t is None:
            s, t = vp(n - 1, 2)

        z = pow(base, t, n)
        if z != 1 and z != n-1:
            j = 0
            while j < s:
                j += 1
                z = pow(z, 2, n)
                if z == n - 1:
                    break

            else:
                return False

        return True

    def smallSpsp(n, s = None, t = None):
        if s is None or t is None:
            s, t = vp(n - 1, 2)

        for p in (2, 13, 23, 1662803):
            if not spsp(n, p, s, t):
                return False

        return True

    def extgcd(x, y):
        a, b, g, u, v, w = 1, 0, x, 0, 1, y
        while w:
            q, t = divmod(g, w)
            a, b, g, u, v, w = u, v, w, a - q * u, b - q * v, t

        if g >= 0:
            return (a, b, g)

        else:
            return (-a, -b, -g)

    def legendre(a, m):
        a %= m
        symbol = 1
        while a != 0:
            while a & 1 == 0:
                a >>= 1
                if m & 7 == 3 or m & 7 == 5:
                    symbol = -symbol

            a, m = m, a
            if a & 3 == 3 and m & 3 == 3:
                symbol = -symbol

            a %= m

        if m == 1:
            return symbol

        return 0

    def inverse(x, n):
        x %=  n
        y = extgcd(n, x)
        if y[2] == 1:
            if y[1] < 0:
                r = n + y[1]
                return r

            else:
                return y[1]

    def vp(n, p, k = 0):
        q = p
        while not (n % q):
            k += 1
            q *= p

        return (k, n // (q // p))

    def modsqrt(n, p, e = 1):
        if 1 < e:
            x = modsqrt(n, p)
            if 0 == x:
                return

            ppower = p
            z = inverse(x << 1, p)
            for i in range(e - 1):
                x += (n - x ** 2) // ppower * z % p * ppower
                ppower *= p

            return x
        
        symbol = legendre(n, p)
        if symbol == 1:
            pmod8 = p & 7
            if pmod8 != 1:
                n %= p
                if pmod8 == 3 or pmod8 == 7:
                    x = pow(n, (p >> 2) + 1, p)

                else:
                    x = pow(n, (p >> 3) + 1, p)
                    c = pow(x, 2, p)
                    if c != n:
                        x = (x * pow(2, p >> 2, p)) % p

            else:
                d = 2
                while legendre(d, p) != -1:
                    d = randrange(3, p)

                s, t = vp(p-1, 2)
                A = pow(n, t, p)
                D = pow(d, t, p)
                m = 0
                for i in range(1, s):
                    if pow(A*(D**m), 1 << (s-1-i), p) == (p-1):
                        m += 1 << i

                x = (pow(n, (t+1) >> 1, p) * pow(D, m >> 1, p)) % p

            return x

        elif symbol == 0:
            return 0

        else:
            return

    def floorsqrt(a):
        if a < (1 << 59):
            return int(sqrt(a))

        else:
            x = pow(10, (int(log(a, 10)) >> 1) + 1)
            while True:
                x_new = (x + a // x) >> 1
                if x <= x_new:
                    return x

                x = x_new

    class QS(object):
        def __init__(self, n, sieverange, factorbase):
            self.number = n
            self.sqrt_n = int(sqrt(n))
            for i in PRIMES_31:
                if n % i == 0:
                    return n % 1

            self.digit = log(self.number, 10) + 1
            self.Srange = sieverange
            self.FBN = factorbase
            self.move_range = range(self.sqrt_n - self.Srange, self.sqrt_n + self.Srange + 1)
            i = 0
            k = 0
            factor_base = [-1]
            FB_log = [0]
            while True:
                ii = primes_table[i]
                if legendre(self.number, ii) == 1:
                    factor_base.append(ii)
                    FB_log.append(primes_log_table[i])
                    k += 1
                    i += 1
                    if k == self.FBN:
                        break

                else:
                    i += 1

            self.FB = factor_base
            self.FB_log = FB_log
            self.maxFB = factor_base[-1]
            N_sqrt_list = []
            for i in self.FB:
                if i != 2 and i != -1:
                    e = int(log(2*self.Srange, i))
                    N_sqrt_modp = sqroot_power(self.number, i, e)
                    N_sqrt_list.append(N_sqrt_modp)

            self.solution = N_sqrt_list
            poly_table = []
            log_poly = []
            minus_val = []
            for j in self.move_range:
                jj = (j ** 2) - self.number
                if jj < 0:
                    jj = -jj
                    minus_val.append(j - self.sqrt_n + self.Srange)

                elif jj == 0:
                    jj = 1

                lj = int((log(jj) * 30) * 0.97)
                poly_table.append(jj)
                log_poly.append(lj)
            self.poly_table = poly_table
            self.log_poly = log_poly
            self.minus_check = minus_val

        def run_sieve(self):
            M = self.Srange
            start_location = []
            logp = [0] * (2 * M + 1)
            j = 2
            for i in self.solution:
                k = 0
                start_p = []
                while k < len(i):
                    q = int((self.sqrt_n) / (self.FB[j] ** (k + 1)))
                    s_1 = q * (self.FB[j] ** (k + 1)) + i[k][0]
                    s_2 = q * (self.FB[j] ** (k + 1)) + i[k][1]
                    while True:
                        if s_1 < self.sqrt_n-M:
                            s_1 += (self.FB[j] ** (k + 1))
                            break

                        else:
                            s_1 -= (self.FB[j] ** (k + 1))

                    while True:
                        if s_2 < self.sqrt_n-M:
                            s_2 += (self.FB[j] ** (k + 1))
                            break

                        else:
                            s_2 -= (self.FB[j] ** (k + 1))

                    start_p.append([s_1 - self.sqrt_n + M, s_2 - self.sqrt_n + M])
                    k += 1

                start_location.append(start_p)
                j += 1

            self.start_location = start_location
            if self.poly_table[0] & 1 == 0:
                i = 0
                while i <= 2 * M:
                    j = 1
                    while True:
                        if self.poly_table[i] % (2 ** (j + 1)) == 0:
                            j += 1

                        else:
                            break

                    logp[i] += self.FB_log[1] * j
                    i += 2

            else:
                i = 1
                while i <= 2 * M:
                    j = 1
                    while True:
                        if self.poly_table[i] % (2 ** (j + 1)) == 0:
                            j += 1

                        else:
                            break

                    logp[i] += self.FB_log[1] * j
                    i += 2

            L = 2
            for j in self.start_location:
                k = 0
                while k < len(j):
                    s_1 = j[k][0]
                    s_2 = j[k][1]
                    h_1 = 0
                    h_2 = 0
                    while s_1 + h_1 <= 2 * M:
                        logp[s_1 + h_1] += self.FB_log[L]
                        h_1 += self.FB[L] ** (k + 1)

                    while s_2 + h_2 <= 2 * M:
                        logp[s_2 + h_2] += self.FB_log[L]
                        h_2 += self.FB[L] ** (k + 1)

                    k += 1

                L += 1

            self.logp = logp
            smooth = []
            for t in range(2 * M + 1):
                if logp[t] >= self.log_poly[t]:
                    poly_val = self.poly_table[t]
                    index_vector = []
                    for p in self.FB:
                        if p == -1:
                            if t in self.minus_check:
                                index_vector.append(1)

                            else:
                                index_vector.append(0)

                        else:
                            r = 0
                            while poly_val % (p ** (r + 1)) == 0:
                                r += 1

                            v = r & 1
                            index_vector.append(v)

                    smooth.append([index_vector, (poly_val, t + self.sqrt_n - M)])

            self.smooth = smooth
            return smooth

    class MPQS(object):
        def __init__(self, n, sieverange = 0, factorbase = 0, multiplier = 0):
            self.number = n
            if is_prime(self.number):
                return [n]

            for i in PRIMES_31:
                if n % i == 0:
                    return n % 1

            self.sievingtime = 0
            self.coefficienttime = 0
            self.d_list = []
            self.a_list = []
            self.b_list = []
            self.digit = int(log(self.number, 10) + 1)
            if sieverange != 0:
                self.Srange = sieverange
                if factorbase != 0:
                    self.FBN = factorbase
                elif self.digit < 9:
                    self.FBN = parameters_for_mpqs[0][1]
                else:
                    self.FBN = parameters_for_mpqs[self.digit - 9][1]

            elif factorbase != 0:
                self.FBN = factorbase
                if self.digit < 9:
                    self.Srange = parameters_for_mpqs[0][0]
                else:
                    self.Srange = parameters_for_mpqs[self.digit - 9][0]

            elif self.digit < 9:
                self.Srange = parameters_for_mpqs[0][0]
                self.FBN = parameters_for_mpqs[0][1]

            elif self.digit > 53:
                self.Srange = parameters_for_mpqs[44][0]
                self.FBN = parameters_for_mpqs[44][1]

            else:
                self.Srange = parameters_for_mpqs[self.digit - 9][0]
                self.FBN = parameters_for_mpqs[self.digit - 9][1]

            self.move_range = range(-self.Srange, self.Srange + 1)
            if multiplier == 0:
                self.sqrt_state = []
                for i in [3, 5, 7, 11, 13]:
                    s = legendre(self.number, i)
                    self.sqrt_state.append(s)

                if self.number % 8 == 1 and self.sqrt_state == [1, 1, 1, 1, 1]:
                    k = 1

                else:
                    index8 = (self.number & 7) >> 1
                    j = 0
                    while self.sqrt_state != prime_8[index8][j][1]:
                        j += 1

                    k = prime_8[index8][j][0]
            else:
                if n & 3 == 1:
                    k = 1

                else:
                    if multiplier == 1:
                        return n

                    else:
                        k = multiplier

            self.number = k * self.number
            self.multiplier = k
            i = 0
            k = 0
            factor_base = [-1]
            FB_log = [0]
            while k < self.FBN:
                ii = primes_table[i]
                if legendre(self.number,ii) == 1:
                    factor_base.append(ii)
                    FB_log.append(primes_log_table[i])
                    k += 1

                i += 1

            self.FB = factor_base
            self.FB_log = FB_log
            self.maxFB = factor_base[-1]
            N_sqrt_list = []
            for i in self.FB:
                if i != 2 and i != -1:
                    e = int(log(2 * self.Srange, i))
                    N_sqrt_modp = sqroot_power(self.number, i, e)
                    N_sqrt_list.append(N_sqrt_modp)

            self.Nsqrt = N_sqrt_list

        def make_poly(self):
            if self.d_list == []:
                d = int(sqrt((sqrt(self.number) / (sqrt(2) * self.Srange))))
                if d & 1 == 0:
                    if (d + 1)& 3 == 1:
                        d += 3

                    else:
                        d += 1

                elif d & 3 == 1:
                    d += 2

            else:
                d = self.d_list[-1]

            while d in self.d_list or not is_prime(d) or legendre(self.number, d) != 1 or d in self.FB:
                d += 4

            a = d ** 2
            h_0 = pow(self.number, (d - 3) >> 2, d)
            h_1 = (h_0*self.number) % d
            h_2 = ((inverse(2, d) * h_0 * (self.number - h_1 ** 2)) // d) % d
            b = (h_1 + h_2 * d) % a
            if b & 1 == 0:
                b -= a

            self.d_list.append(d)
            self.a_list.append(a)
            self.b_list.append(b)
            solution = []
            i = 0
            for s in self.Nsqrt:
                k = 0
                p_solution = []
                ppow = 1
                while k < len(s):
                    ppow *= self.FB[i+2]
                    a_inverse = inverse(2 * self.a_list[-1], ppow)
                    x_1 = ((-b + s[k][0]) * a_inverse) % ppow
                    x_2 = ((-b + s[k][1]) * a_inverse) % ppow
                    p_solution.append([x_1, x_2])
                    k += 1

                i += 1
                solution.append(p_solution)

            self.solution = solution

        def run_sieve(self):
            self.make_poly()
            M = self.Srange
            a = self.a_list[-1]
            b = self.b_list[-1]
            c = (b ** 2 - self.number) // (4 * a)
            d = self.d_list[-1]
            self.poly_table = []
            self.log_poly = []
            self.minus_check = []
            for j in self.move_range:
                jj = (a * j + b) * j + c
                if jj < 0:
                    jj = -jj
                    self.minus_check.append(j + M)

                elif jj == 0:
                    jj = 1

                lj = int((log(jj) * 30) * 0.95)
                self.poly_table.append(jj)
                self.log_poly.append(lj)

            y = inverse(2 * d, self.number)
            start_location = []
            logp = [0] * (2 * M + 1)
            j = 2
            for i in self.solution:
                start_p = []
                ppow = 1
                for k in range(len(i)):
                    ppow *= self.FB[j]
                    q = -M // ppow
                    s_1 = (q + 1) * ppow + i[k][0]
                    s_2 = (q + 1) * ppow + i[k][1]
                    while s_1 + M >= ppow:
                        s_1 -=ppow

                    while s_2 + M >= ppow:
                        s_2 -= ppow

                    start_p.append([s_1 + M, s_2 + M])

                start_location.append(start_p)
                j += 1

            self.start_location = start_location
            i = self.poly_table[0] & 1
            while i <= 2 * M:
                j = 1
                while self.poly_table[i] % (2 ** (j + 1)) == 0:
                    j += 1

                logp[i] += self.FB_log[1] * j
                i += 2

            L = 2
            for plocation in self.start_location:
                for k in range(len(plocation)):
                    s_1 = plocation[k][0]
                    s_2 = plocation[k][1]
                    ppow = self.FB[L] ** (k + 1)
                    while s_1 <= 2 * M:
                        logp[s_1] += self.FB_log[L]
                        s_1 += ppow

                    while s_2 <= 2 * M:
                        logp[s_2] += self.FB_log[L]
                        s_2 += ppow

                L += 1

            self.logp = logp
            smooth = []
            for t in range(2 * M + 1):
                if logp[t] >= self.log_poly[t]:
                    poly_val = self.poly_table[t]
                    index_vector = []
                    H = (y * (2 * a * (t-self.Srange) + b)) % self.number
                    for p in self.FB:
                        if p == -1:
                            if t in self.minus_check:
                                index_vector.append(1)

                            else:
                                index_vector.append(0)

                        else:
                            r = 0
                            while poly_val % (p ** (r + 1)) == 0:
                                r += 1

                            v = r & 1
                            index_vector.append(v)

                    smooth.append([index_vector, (poly_val, H)])

            return smooth

        def get_vector(self):
            P = len(self.FB)
            if P < 100:
                V = -5

            else:
                V = 0

            smooth = []
            i = 0
            while P * 1 > V:
                n = self.run_sieve()
                V += len(n)
                smooth += n
                i += 1

            if P < 100:
                V += 5

            self.smooth = smooth
            return smooth

    class Elimination():
        def __init__(self, smooth):
            self.vector = []
            self.history = []
            i = 0
            for vec in smooth:
                self.vector.append(vec[0])
                self.history.append({i:1})
                i += 1
            self.FB_number = len(self.vector[0])
            self.row_size = len(self.vector)
            self.historytime = 0

        def vector_add(self, i, j):
            V_i = self.vector[i]
            V_j = self.vector[j]
            k = 0
            while k < len(V_i):
                if V_i[k] == 1:
                    if V_j[k] == 1:
                        V_j[k] = 0
                    else:
                        V_j[k] = 1
                k += 1

        def transpose(self):
            Transe_vector = []
            i = 0
            while i < self.FB_number:
                j = 0
                vector = []
                while j < self.row_size:
                    vector.append(self.vector[j][i])
                    j += 1

                Transe_vector.append(vector)
                i += 1

            self.Transe = Transe_vector

        def history_add(self, i, j):
            H_i = self.history[i].keys()
            H_j = self.history[j].keys()
            for k in H_i:
                if k in H_j:
                    del self.history[j][k]

                else:
                    self.history[j][k] = 1

        def gaussian(self):
            pivot = []
            FBnum = self.FB_number
            Smooth = len(self.vector)
            for j in range(self.FB_number):
                for k in range(Smooth):
                    if k in pivot or not self.vector[k][j]:
                        continue

                    pivot.append(k)
                    V_k = self.vector[k]
                    for h in range(Smooth):
                        if h in pivot or not self.vector[h][j]:
                            continue

                        self.history_add(k, h)
                        V_h = self.vector[h]
                        for q in range(j, FBnum):
                            if V_k[q]:
                                V_h[q] = not V_h[q]
                                
                    break

            self.pivot = pivot
            zero_vector = []
            for check in range(Smooth):
                if check not in pivot:
                    g = 0
                    while g < FBnum:
                        if self.vector[check][g] == 1:
                            break

                        g += 1

                    if g == FBnum:
                        zero_vector.append(check)

            return zero_vector

    def qs(n, s, f):
        Q = QS(n, s, f)
        Q.run_sieve()
        V = Elimination(Q.smooth)
        A = V.gaussian()
        answerX_Y = []
        N_factors = []
        for i in A:
            B = V.history[i].keys()
            X = 1
            Y = 1
            for j in B:
                X *= Q.smooth[j][1][0]
                Y *= Q.smooth[j][1][1]
                Y = Y % Q.number

            X = sqrt_modn(X, Q.number)
            answerX_Y.append(X - Y)

        for k in answerX_Y:
            if k != 0:
                factor = gcd(k, Q.number)
                if factor not in N_factors and factor != 1 and factor != Q.number and is_prime(factor) == 1:
                    N_factors.append(factor)

        N_factors.sort()

    def mpqs(n, s = 0, f = 0, m = 0):
        M = MPQS(n, s, f, m)
        M.get_vector()
        N = M.number // M.multiplier
        V = Elimination(M.smooth)
        A = V.gaussian()
        answerX_Y = []
        N_prime_factors = []
        N_factors = []
        output = []
        for i in A:
            B = V.history[i].keys()
            X = 1
            Y = 1
            for j in B:
                X *= M.smooth[j][1][0]
                Y *= M.smooth[j][1][1]
                Y %= M.number

            X = sqrt_modn(X, M.number)
            if X != Y:
                answerX_Y.append(X-Y)

        NN = 1
        for k in answerX_Y:
            factor = gcd(k, N)
            if factor not in N_factors and factor != 1 and factor != N and factor not in N_prime_factors:
                if is_prime(factor):
                    NN *= factor
                    N_prime_factors.append(factor)

                else:
                    N_factors.append(factor)

        if NN == N:
            N_prime_factors.sort()
            for p in N_prime_factors:
                N = N // p
                i = vp(N, p, 1)[0]
                output.append((p, i))

            return output

        elif NN != 1:
            f = N // NN
            if is_prime(f):
                N_prime_factors.append(f)
                N_prime_factors.sort()
                for p in N_prime_factors:
                    N = N // p
                    i = vp(N, p, 1)[0]
                    output.append((p, i))

                return output

        for F in N_factors:
            for FF in N_factors:
                if F != FF:
                    Q = gcd(F, FF)
                    if is_prime(Q) and Q not in N_prime_factors:
                        N_prime_factors.append(Q)
                        NN *= Q

        N_prime_factors.sort()
        for P in N_prime_factors:
            i, N = vp(N, P)
            output.append((P, i))

        if  N == 1:
            return output

        for F in N_factors:
            g = gcd(N, F)
            if is_prime(g):
                N_prime_factors.append(g)
                N = N // g
                i = vp(N, g, 1)[0]
                output.append((g, i))

        if N == 1:
            return output

        elif is_prime(N):
            output.append((N, 1))
            return output

        else:
            N_factors.sort()
            return output, N_factors

    def eratosthenes(n):
        sieve = [True] * (n + 1)

        for i in range(2, int(n ** 0.5) + 1):
            if sieve[i]:
                for j in range(i ** 2, n + 1, i):
                    sieve[j] = False

        return [x for x in range(2, n + 1) if sieve[x]]

    def prime_mod8(n):
        primes = eratosthenes(n)
        PrimeList = {1:[], 3:[], 5:[], 7:[]}
        LegendreList = {1:[], 3:[], 5:[], 7:[]}
        sp = [2, 3, 5, 7, 11, 13]
        for p in primes:
            if p not in sp:
                leg = [legendre(p, q) for q in sp[1:]]
                if leg not in PrimeList[p & 7]:
                    LegendreList[p & 7].append(leg)
                    PrimeList[p & 7].append([p, leg])

        return [PrimeList[1], PrimeList[3], PrimeList[5], PrimeList[7]]

    def eratosthenes_log(n):
        primes = eratosthenes(n)
        primes_log = []
        for i in primes:
            l = int(log(i) * 30)
            primes_log.append(l)

        return primes_log

    def sqrt_modn(n, modulo):
        factorOfN = _factor(n)[0]
        prod = 1
        for p, e in factorOfN:
            prod = (prod * pow(p, e >> 1, modulo)) % modulo

        return prod

    def sqroot_power(a, p, n):
        x = modsqrt(a, p)
        answer = [[x, p - x]]
        ppower = p
        i = inverse(x << 1, p)
        for i in range(n - 1):
            x += (a - x ** 2) // ppower * i % p * ppower
            ppower *= p
            answer.append([x, ppower - x])

        return answer

    primes_table = eratosthenes(10 ** 5)
    primes_log_table = eratosthenes_log(10 ** 5)
    prime_8 = prime_mod8(8090)
    mpqs_p_100 = [[100, x] for x in [20, 21, 22, 24, 26, 29, 32]]
    mpqs_p_300 = [[300, x] for x in [40, 60, 80, 100, 120, 140]]
    mpqs_p_2000 = [[2000, x] for x in [240, 260, 280, 325, 355, 375, 400, 425, 550]]
    mpqs_p_15000 = [[15000, x] for x in [1300, 1600, 1900, 2200]]
    parameters_for_mpqs = mpqs_p_100 + [[200, 35]] + mpqs_p_300 + [[600, 160]] + [[900, 180]] + [[1200, 200]] + [[1000,220]] + mpqs_p_2000 + [[3000, 650]] + [[5000, 750]] + [[4000, 850]] + [[4000, 950]] + [[5000, 1000]] + [[14000, 1150]] + mpqs_p_15000 + [[20000,2500]]

    def mpqsfind(n, s = 0, f = 0, m = 0):
        M = MPQS(n, s, f, m)
        M.get_vector()
        N = M.number // M.multiplier
        V = Elimination(M.smooth)
        A = V.gaussian()
        differences = []
        for i in A:
            B = V.history[i].keys()
            X = 1
            Y = 1
            for j in B:
                X *= M.smooth[j][1][0]
                Y *= M.smooth[j][1][1]
                Y %= M.number

            X = floorsqrt(X) % M.number
            if X != Y:
                differences.append(X - Y)

        for diff in differences:
            divisor = gcd(diff, N)
            if 1 < divisor < N:
                return divisor

    def mpqs(n, retry = 1, min_ = 20):
        num = n
        ans = []
        if is_prime(n):
            ans.append(n)
            return ans

        while True:
            r = num
            try:
                if len(str(r)) >= min_:
                    d = mpqsfind(num)
                    ans.append(d)
                    r = num // d
                    if is_prime(r):
                        ans.append(r)
                        break
                
                    else:
                        num = r
                
                else:
                    ans = [x for x in _factor(num)[1]]
                    break
            
            except TypeError:
                ans = [x for x in _factor(num)[1]]
                break

        checked = _check_factors(ans, n, retry)
        if checked == 0:
            ans.sort()
            return ans
        
        return mpqs(n, checked)
    
    return mpqs(n)

def factor_lenstra(n):
    '''
    Return a list that has all factors of n.
    '''
    class Point():
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

    class Curve():
        def __init__(self, a, b, m):
            self.a = a
            self.b = b
            self.m = m

    def double_point(P, curve):
        X = P.x
        Y = P.y
        Z = P.z
        a = curve.a
        m = curve.m
        if Y == 0:
            return Point(0, 1, 0)

        if Z == 0:
            return P

        W = a * pow(Z, 2, m) + 3 * pow(X, 2, m)
        S = Y * Z
        B = X * Y * S
        H = pow(W, 2, m) - 8 * B
        X2 = (2 * H * S) % m
        Y2 = (W * (4 * B - H) - 8 * pow(Y, 2, m) * pow(S, 2, m)) % m
        Z2 = pow(2 * S, 3, m)
        return Point(X2, Y2, Z2)

    def add_points(P1, P2, curve):
        if P1.z == 0:
            return P2

        if P2.z == 0:
            return P1
        
        X1 = P1.x
        Y1 = P1.y
        Z1 = P1.z
        X2 = P2.x
        Y2 = P2.y
        Z2 = P2.z
        m = curve.m
        U1 = Y2 * Z1 % m
        U2 = Y1 * Z2 % m
        V1 = X2 * Z1 % m
        V2 = X1 * Z2 % m
        if V1 == V2:
            if U1 == U2:
                return double_point(P1, curve)

            else:
                return Point(0, 1, 0)

        V = (V1 - V2) % m
        U = (U1 - U2) % m
        W = (Z1 * Z2) % m
        A = pow(U, 2, m) * W - pow(V, 3, m) - 2 * pow(V, 2, m) * V2
        X3 = (V * A) % m
        Y3 = (U * (pow(V, 2, m) * V2 - A) - pow(V, 3, m) * U2) % m
        Z3 = (pow(V, 3, m) * W) % m
        return Point(X3, Y3, Z3)

    def multiply_point(P, k, curve):
        if k == 1:
            return P
        
        P2 = Point(0, 1, 0)
        k2 = 0
        
        bit = 1 << (len(bin(k)) - 3)
        
        while k != k2:
            k2 <<= 1
            if k2: 
                P2 = double_point(P2, curve)
            
            if k & bit:
                k2 += 1
                P2 = add_points(P, P2, curve)

            bit >>= 1
            
        return P2

    def factor(n, mode = 1, tries = 10, retry = 1):
        factors = []
        for i in (2, 3):
            while n % i == 0:
                factors.append(i)
                n //= i

        if n == 1:
            return factors

        if is_prime(n):
            factors.append(n)
            factors.sort()
            return factors
        
        max_points = int(2 * n ** 0.25 + n ** 0.5 + 1)
        
        for current_try in range(1, tries + 1):
            a = 0
            b = 0
            while (4 * pow(a, 3, n) + 27 * pow(b, 2, n)) % n == 0:
                x = 1
                y = current_try
                a = randint(1, n - 1)
                b = (pow(y, 2, n) - a * x - pow(x, 3, n)) % n
            
            P = Point(x, y, 1)
            curve = Curve(a, b, n)
            P2 = P
            i = 1
            while True:
                i += 1
                if mode == 1:
                    P2 = multiply_point(P2, i, curve)

                elif mode == 2:
                    if i == 2:
                        k = 2
                        k_plus = 4

                    elif i <= 5:
                        k = 2 * i - 3

                    else:
                        k += k_plus
                        k_plus = 6 - k_plus
                    
                    k2 = k
                    while k2 <= max_points:
                        P2 = multiply_point(P2, k, curve)
                        k2 *= k
                
                if P2.z == 0:
                    break

                divisor = gcd(n, P2.z)
                if divisor != 1:
                    divisor2 = n // divisor
                    f2 = factor(divisor, mode, tries)
                    for f in f2:
                        factors.append(f)
                    
                    f2 = factor(divisor2, mode, tries)
                    for f in f2:
                        factors.append(f)
                    
                    factors.sort()
                    return factors
                    
                if i >= max_points:
                    factors.append(n)
                    factors.sort()
                    return factors
        
        factors.append(n)
        checked = _check_factors(factors, n, retry)
        if checked == 0:
            factors.sort()
            return factors
            
        return factor(n, retry = checked)
    
    return factor(n)

def factor_pollardpm1(n, retry = 1):
    '''
    Return a list that has all factors of n.
    '''
    def factor(n):
        if n % 2 == 0:
            return 2

        a = 2
        i = 2
        while True:
            a = pow(a, i, n)
            d = gcd(a - 1, n)
            if d > 1:
                return d

            i += 1

    num = n
    ans = []
    if is_prime(n):
        ans.append(n)
        return ans

    while True:
        d = factor(num)
        ans.append(d)
        r = num // d
        if is_prime(r):
            ans.append(r)
            break
    
        else:
            num = r
    
    checked = _check_factors(ans, n, retry)
    if checked == 0:
        ans.sort()
        return ans
        
    return factor_pollardpm1(n, checked)

def factor_williamspp1(n, retry = 1):
    '''
    Return a list that has all factors of n.
    '''
    def v_lucas(P, r, n = 1):
        bstr = bin(r).lstrip('0b')[1:]
        vkm1, vk = 2, P
        if r == 0:
            return vkm1

        if r == 1:
            return vk

        for b in bstr:
            if b == '0':
                vkm1 = (vk * vkm1 - P) % n
                vk = (vk * vk - 2) % n

            else:
                tmp = vkm1
                vkm1 = (vk ** 2 - 2) % n
                vk = (P * (vk ** 2) - vk * tmp - P) % n 

        return vk

    def factor(n, B = 10 ** 6):
        if n % 2 == 0:
            return 2

        v = 3
        for q in all_primes(B, 'list'):
            m = int(log(n, q))
            v = v_lucas(v, pow(q, m), n)
            g = gcd(v - 2, n)
            if 1 < g < n:
                return g
    
    num = n
    ans = []
    if is_prime(n):
        ans.append(n)
        return ans

    while True:
        d = factor(num)
        ans.append(d)
        r = num // d
        if is_prime(r):
            ans.append(r)
            break
    
        else:
            num = r
    
    checked = _check_factors(ans, n, retry)
    if checked == 0:
        ans.sort()
        return ans
        
    return factor_williamspp1(n, checked)

def add_args():
    '''
    Add args.
    '''
    global args
    parser = ArgumentParser(description = 'A module to find all kinds of primes and factors of big numbers.')
    parser.add_argument('-n', metavar = 'num', type = int, help = 'The number')
    parser.add_argument('-method', metavar = 'method', type = str, help = 'The method of the factor function. (siqs, mpqs, lenstra, pollardpm1, williamspp1)')
    parser.add_argument('--is_prime', metavar = 'is_prime', const = is_prime, nargs = '?', help = is_prime.__doc__)
    parser.add_argument('--all_primes', metavar = 'all_primes', const = all_primes, nargs = '?', help = all_primes.__doc__)
    parser.add_argument('--factor', metavar = 'factor', const = factor_mpqs, nargs = '?', help = factor_mpqs.__doc__)
    args = parser.parse_args()
    print_help_is_prime = False
    print_help_all_primes = False
    print_help_factor = False
    if args.is_prime:
        print(is_prime(args.n))
    
    else:
        print_help_is_prime = True
    
    if args.all_primes:
        print(all_primes(args.n))
    
    else:
        print_help_all_primes = True

    if args.factor:
        if args.method == 'siqs':
            print(factor_siqs(args.n))

        elif args.method == 'mpqs':
            print(factor_mpqs(args.n))

        elif args.method == 'lenstra':
            print(factor_lenstra(args.n))
        
        elif args.method == 'pollardpm1':
            print(factor_pollardpm1(args.n))
        
        elif args.method == 'williamspp1':
            print(factor_williamspp1(args.n))
    
    else:
        print_help_factor = True
    
    if print_help_is_prime and print_help_all_primes and print_help_factor:
        print('''usage: find_primes.py [-h] [-n num] [-method method] [--is_prime [is_prime]] [--all_primes [all_primes]]
                      [--factor [factor]]

A module to find all kinds of primes and factors of big numbers.

options:
  -h, --help            show this help message and exit
  -n num                The number
  -method method        The method of the factor function. (siqs, mpqs, lenstra, pollardpm1, williamspp1)
  --is_prime [is_prime]
                        If n is prime, return True.
  --all_primes [all_primes]
                        Return a prime list below n. Arguments: output ----- 'array' or 'list' ----- The output type
                        of the function.
  --factor [factor]     Return a list that has all factors of n.''')

add_args()