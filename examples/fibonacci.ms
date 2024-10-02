# Fibonacci sequence in MathScript

function fibonacci(n) {
    if n <= 1 {
        return n
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2)
    }
}

n = 10
print("Fibonacci sequence up to", n, ":")

for i in range(0, n) {
    print(fibonacci(i))
}
