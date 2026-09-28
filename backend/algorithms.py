import random


def factorial(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def fibonacci(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fibonacci_sequence(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1
    sequence = []
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence


def reverse_number(n):
    sign = -1 if n < 0 else 1
    n = abs(int(n))
    result = 0
    while n:
        result = result * 10 + n % 10
        n //= 10
    return sign * result


def count_digits(n):
    return len(str(abs(int(n))))


def gcd(a, b):
    a, b = abs(int(a)), abs(int(b))
    while b:
        a, b = b, a % b
    return a


def sum_and_average(numbers):
    if not numbers:
        raise ValueError("At least one number is required")
    total = sum(numbers)
    return {"sum": total, "average": total / len(numbers)}


def swap_with_temp(a, b):
    temp = a
    a = b
    b = temp
    return a, b


def swap_without_temp(a, b):
    a, b = b, a
    return a, b


def base_conversion(n, base):
    """Convert a decimal integer to base 2..36 using repeated division."""
    base = int(base)
    n = int(n)
    if not 2 <= base <= 36:
        raise ValueError("Base must be between 2 and 36")
    if n == 0:
        return "0"
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sign = "-" if n < 0 else ""
    n = abs(n)
    result = []
    while n > 0:
        n, remainder = divmod(n, base)
        result.append(digits[remainder])
    return sign + "".join(reversed(result))


def smallest_divisor(n):
    n = abs(int(n))
    if n < 2:
        return n
    if n % 2 == 0:
        return 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return divisor
        divisor += 2
    return n


def is_prime(n):
    n = int(n)
    return n >= 2 and smallest_divisor(n) == n


def generate_primes(limit):
    return [n for n in range(2, int(limit) + 1) if is_prime(n)]


def prime_factors(n):
    n = abs(int(n))
    if n < 2:
        return []
    factors = []
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 1
    if n > 1:
        factors.append(n)
    return factors


def square_root_newton(n, tolerance=1e-10, max_iterations=100):
    """Newton-Raphson square root approximation."""
    n = float(n)
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0.0
    x = n if n >= 1 else 1.0
    for _ in range(max_iterations):
        next_x = 0.5 * (x + n / x)
        if abs(next_x - x) < tolerance:
            return next_x
        x = next_x
    return x


def square_root_repeated_subtraction(n):
    n = int(n)
    if n < 0:
        raise ValueError("n must be non-negative")
    root = 0
    odd = 1
    remainder = n
    while remainder >= odd:
        remainder -= odd
        odd += 2
        root += 1
    return {"integer_root": root, "remainder": remainder}


def square_root_long_division(n):
    """Integer square root using the digit-pair/long-division method."""
    n = int(n)
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0

    # Process the number in pairs of decimal digits, as in the long-division method.
    text = str(n)
    if len(text) % 2:
        text = "0" + text
    pairs = [int(text[i:i + 2]) for i in range(0, len(text), 2)]

    root = 0
    remainder = 0
    for pair in pairs:
        remainder = remainder * 100 + pair
        trial = 0
        for digit in range(9, -1, -1):
            candidate = (20 * root + digit) * digit
            if candidate <= remainder:
                trial = digit
                break
        remainder -= (20 * root + trial) * trial
        root = root * 10 + trial
    return root


def large_power(base, exponent):
    """Exponentiation by squaring (no pow() shortcut)."""
    base = int(base)
    exponent = int(exponent)
    if exponent < 0:
        raise ValueError("Exponent must be non-negative")
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result *= base
        base *= base
        exponent //= 2
    return result


def pseudo_random_number(seed, low, high):
    return random.Random(int(seed)).randint(int(low), int(high))


def random_float(low=0, high=1):
    low, high = float(low), float(high)
    if low > high:
        raise ValueError("Minimum cannot be greater than maximum")
    return random.uniform(low, high)
