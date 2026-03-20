import time
import matplotlib.pyplot as plt

MOD = 10**9 + 7

def matrix_multiply(A, B):
    result = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % MOD
    return result

def matrix_power_recursive(matrix, n):
    if n == 1:
        return matrix
    if n % 2 == 0:
        half_power = matrix_power_recursive(matrix, n // 2)
        return matrix_multiply(half_power, half_power)
    else:
        half_power = matrix_power_recursive(matrix, n // 2)
        return matrix_multiply(matrix_multiply(half_power, half_power), matrix)

def matrix_power_iterative(matrix, n):
    result = [[1, 0], [0, 1]]  # Identity matrix
    while n > 0:
        if n % 2 == 1:
            result = matrix_multiply(result, matrix)
        matrix = matrix_multiply(matrix, matrix)
        n //= 2
    return result

def fib_linear(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, (a + b) % MOD
    return b

def fib_matrix(n, matrix_power_func):
    if n == 0:
        return 0
    M = [[1, 1], [1, 0]]
    M_power = matrix_power_func(M, n - 1)
    return M_power[0][0]

# Example usage:
n = 10000


# Test range
test_range = list(range(0, 10000001, 1000000))  # Every 1 million in 10 million.

# Time measurements
times_recursive = []
times_iterative = []
times_linear = []

for n in test_range:
    # Recursive O(log n)
    start_time = time.time()
    fib_matrix(n, matrix_power_recursive)
    times_recursive.append((time.time() - start_time))

    # Iterative O(log n)
    start_time = time.time()
    fib_matrix(n, matrix_power_iterative)
    times_iterative.append((time.time() - start_time))

    # Linear O(n)
    start_time = time.time()
    fib_linear(n)
    times_linear.append((time.time() - start_time))

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(test_range, times_recursive, label='Recursive O(log n)', marker='o')
print( "Recursive Version:",[i * 1000 for i in times_recursive])
plt.plot(test_range, times_iterative, label='Iterative O(log n)', marker='x')
print( "Iterative version:", [i * 1000 for i in times_iterative])
plt.plot(test_range, times_linear, label='Linear O(n)', marker='*')
print( "Linear version: ", [i * 1000 for i in times_linear])
plt.xlabel('N-th Fibonacci Number')
plt.ylabel('Time (seconds)')
plt.title('Performance Comparison of Fibonacci Implementations up to n=10,000,000')
plt.legend()
plt.grid(True)
plt.show()
