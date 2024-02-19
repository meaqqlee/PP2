def squares_generator(N):
    for i in range(N + 1):
        yield i ** 2

def even_numbers_generator(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i
            
def divisible_by_3_and_4_generator(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
            
def squares_range_generator(a, b):
    for i in range(a, b + 1):
        yield i ** 2

def countdown_generator(n):
    while n >= 0:
        yield n
        n -= 1

if __name__ == "__main__":
    N = 10
    print(f"Squares up to {N}: {list(squares_generator(N))}")
    n = 10
    print(f"Even numbers between 0 and {n}: {list(even_numbers_generator(n))}")
    print(f"Numbers divisible by 3 and 4 up to {n}: {list(divisible_by_3_and_4_generator(n))}")
    a, b = 2, 5
    print(f"Squares from {a} to {b}: {list(squares_range_generator(a, b))}")
    print(f"Countdown from {n} to 0: {list(countdown_generator(n))}")
    
squares_generator(5)
