import time
import matplotlib.pyplot as plt

# Define the matrix-based solution
class MatrixSolution:
    MOD = 10**9 + 7

    def numTilings(self, n: int) -> int:
        if n == 1:
            return 1
        if n == 2:
            return 2
        if n == 3:
            return 5
        M = [
            [2, 0, 1],
            [1, 0, 0],
            [0, 1, 0]
        ]
        M_power = self.matrix_power(M, n - 3)
        result_vector = self.matrix_multiply(M_power, [[5], [2], [1]])
        return result_vector[0][0]

    def matrix_power(self, matrix, n):
        size = len(matrix)
        result = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
        while n > 0:
            if n % 2 == 1:
                result = self.matrix_multiply(result, matrix)
            matrix = self.matrix_multiply(matrix, matrix)
            n //= 2
        return result

    def matrix_multiply(self, A, B):
        rows_A = len(A)
        cols_A = len(A[0])
        rows_B = len(B)
        cols_B = len(B[0])
        result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % self.MOD
        return result

# Define the DP-based solution
class DPSolution:
    MOD = 10**9 + 7

    def numTilings(self, n: int) -> int:
        if n < 2:
            return 1

        dp = [0] * (n + 1)
        dp[0] = 1
        dp[1] = 1
        dp[2] = 2
        for i in range(3, n + 1):
            dp[i] = (2 * dp[i - 1] + dp[i - 3]) % self.MOD

        return dp[n]

# Test range
test_range = list(range(0, 1000000, 100000))

# Time measurements
times_matrix = []
times_dp = []

matrix_solution = MatrixSolution()
dp_solution = DPSolution()

for n in test_range:
    start_time = time.time()
    matrix_solution.numTilings(n)
    times_matrix.append(time.time() - start_time)

    start_time = time.time()
    dp_solution.numTilings(n)
    times_dp.append(time.time() - start_time)

# Plotting the results
plt.figure(figsize=(10, 8))
plt.plot(test_range, times_matrix, label='Matrix O(log n)', marker='o')
print(times_matrix)
plt.plot(test_range, times_dp, label='DP O(n)', marker='x')
print(times_dp)
plt.xlabel('N-th Number')
plt.ylabel('Time (seconds)')
plt.title('Performance Comparison of Matrix vs DP Solutions')
plt.legend()
plt.grid(True)
plt.show()


