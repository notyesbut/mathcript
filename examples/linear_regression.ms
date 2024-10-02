# Linear Regression Implementation in MathScript

function compute_mse(y_true, y_pred) {
    n = len(y_true)
    error_sum = 0
    for i in range(0, n) {
        error = y_true[i] - y_pred[i]
        error_sum = error_sum + (error ^ 2)
    }
    mse = error_sum / n
    return mse
}

function linear_regression(x, y, learning_rate, epochs) {
    m = 0  # Initial weight
    b = 0  # Initial bias
    n = len(x)

    for epoch in range(1, epochs + 1) {
        y_pred = []  # Initialize empty list
        for i in range(0, n) {
            y_pred.append(m * x[i] + b)
        }

        # Compute gradients
        dm = 0
        db = 0
        for i in range(0, n) {
            dm = dm - (2 / n) * x[i] * (y[i] - y_pred[i])
            db = db - (2 / n) * (y[i] - y_pred[i])
        }

        # Update parameters
        m = m - learning_rate * dm
        b = b - learning_rate * db

        # Optional: Print MSE every 100 epochs
        if epoch % 100 == 0 {
            mse = compute_mse(y, y_pred)
            print("Epoch:", epoch, "MSE:", mse)
        }
    }
    return [m, b]
}

# Data
x = [1, 2, 3, 4, 5]
y = [3, 5, 7, 9, 11]

# Hyperparameters
learning_rate = 0.01
epochs = 1000

# Train the model
params = linear_regression(x, y, learning_rate, epochs)
m = params[0]
b = params[1]

print("Trained parameters:")
print("Slope (m):", m)
print("Intercept (b):", b)

# Make predictions
y_pred = []
n = len(x)
for i in range(0, n) {
    y_pred.append(m * x[i] + b)
}

print("Predicted values:", y_pred)
