# MA629 LAB EXAM - LINEAR REGRESSION FROM SCRATCH
# Dataset: data_lin.csv in the same folder; last column is target.
# Rename this file with your roll number before submission.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

np.random.seed(42)

# 1. Load and explore data
data = pd.read_csv("data_lin.csv", header=None)
X = data.iloc[:, :-1].values.astype(float)
y = data.iloc[:, -1].values.astype(float)

print("Dataset shape:", data.shape)
print(data.head())
print(data.describe())
print("Samples:", X.shape[0], "| Features:", X.shape[1])

# 2. Train-test split
X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print("Training shape:", X_train_raw.shape)
print("Testing shape:", X_test_raw.shape)

# 3. Model implemented from scratch
def hypothesis(X, W):
    return X @ W

def cost_function(X, y, W):
    m = len(y)
    return np.sum((hypothesis(X, W) - y) ** 2) / (2 * m)

def gradient_descent(X, y, learning_rate, epochs):
    m, n = X.shape
    W = np.zeros(n)
    loss_history = []

    for epoch in range(epochs):
        y_pred = hypothesis(X, W)
        gradient = (X.T @ (y_pred - y)) / m
        W = W - learning_rate * gradient
        loss_history.append(cost_function(X, y, W))

    return W, loss_history

# 4. 5-fold CV to select learning rate
learning_rates = [0.001, 0.01, 0.05, 0.1]
kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = []
epochs_cv = 2000

print("\\n5-FOLD CROSS-VALIDATION")
for lr in learning_rates:
    fold_errors = []

    for train_idx, val_idx in kf.split(X_train_raw):
        X_tr_raw, X_val_raw = X_train_raw[train_idx], X_train_raw[val_idx]
        y_tr, y_val = y_train[train_idx], y_train[val_idx]

        # Fit scaler only on this fold's training data
        fold_scaler = MinMaxScaler()
        X_tr = fold_scaler.fit_transform(X_tr_raw)
        X_val = fold_scaler.transform(X_val_raw)

        # Add bias column
        X_tr = np.c_[np.ones(len(X_tr)), X_tr]
        X_val = np.c_[np.ones(len(X_val)), X_val]

        W_fold, _ = gradient_descent(X_tr, y_tr, lr, epochs_cv)
        y_val_pred = hypothesis(X_val, W_fold)
        fold_errors.append(mean_squared_error(y_val, y_val_pred))

    avg_mse = np.mean(fold_errors)
    cv_scores.append(avg_mse)
    print("Learning rate:", lr, "| Average CV MSE:", avg_mse)

best_lr = learning_rates[int(np.argmin(cv_scores))]
print("Best learning rate:", best_lr)

# 5. Final scaling: fit on full training set only
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train_raw)
X_test_scaled = scaler.transform(X_test_raw)

# Append bias (first column)
X_train = np.c_[np.ones(len(X_train_scaled)), X_train_scaled]
X_test = np.c_[np.ones(len(X_test_scaled)), X_test_scaled]

# 6. Train final model
W, loss_history = gradient_descent(
    X_train, y_train, learning_rate=best_lr, epochs=5000
)
print("\\nFinal weights:", W)
print("Final training cost:", loss_history[-1])

# 7. Test prediction and metrics
y_pred = hypothesis(X_test, W)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\\nTEST SET PERFORMANCE")
print("MSE:", mse)
print("MAE:", mae)
print("RMSE:", rmse)
print("R2 Score:", r2)

# 8. Loss curve
plt.figure(figsize=(7, 5))
plt.plot(loss_history, label="Training cost")
plt.title("Linear Regression - Loss Curve")
plt.xlabel("Epoch")
plt.ylabel("Cost (MSE/2)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 9. Actual vs predicted
plt.figure(figsize=(7, 5))
plt.scatter(y_test, y_pred, label="Predictions")
low = min(y_test.min(), y_pred.min())
high = max(y_test.max(), y_pred.max())
plt.plot([low, high], [low, high], "r--", label="Perfect prediction")
plt.title("Actual vs Predicted")
plt.xlabel("Actual values")
plt.ylabel("Predicted values")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 10. Residual plot
residuals = y_test - y_pred
plt.figure(figsize=(7, 5))
plt.scatter(y_pred, residuals, label="Residuals")
plt.axhline(0, color="red", linestyle="--", label="Zero error")
plt.title("Residual Plot")
plt.xlabel("Predicted values")
plt.ylabel("Residuals")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 11. Regression line (one feature) or regression hyperplane (2+ features)
n_features = X_train_scaled.shape[1]

if n_features == 1:
    x_line = np.linspace(X_train_scaled[:, 0].min(),
                         X_train_scaled[:, 0].max(), 100)
    y_line = W[0] + W[1] * x_line

    plt.figure(figsize=(7, 5))
    plt.scatter(X_train_scaled[:, 0], y_train, label="Training data")
    plt.plot(x_line, y_line, "r", label="Regression line")
    plt.title("Linear Regression Line")
    plt.xlabel("Feature 1 (scaled)")
    plt.ylabel("Target")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    x1 = np.linspace(X_train_scaled[:, 0].min(),
                     X_train_scaled[:, 0].max(), 30)
    x2 = np.linspace(X_train_scaled[:, 1].min(),
                     X_train_scaled[:, 1].max(), 30)
    X1, X2 = np.meshgrid(x1, x2)

    # Hold any remaining features at their training means
    grid = np.tile(np.mean(X_train_scaled, axis=0), (X1.size, 1))
    grid[:, 0] = X1.ravel()
    grid[:, 1] = X2.ravel()
    grid_bias = np.c_[np.ones(len(grid)), grid]
    Z = hypothesis(grid_bias, W).reshape(X1.shape)

    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(X_train_scaled[:, 0], X_train_scaled[:, 1],
               y_train, label="Training data")
    ax.plot_surface(X1, X2, Z, alpha=0.4)
    ax.set_title("Linear Regression Hyperplane")
    ax.set_xlabel("Feature 1 (scaled)")
    ax.set_ylabel("Feature 2 (scaled)")
    ax.set_zlabel("Target")
    ax.legend()
    plt.tight_layout()
    plt.show()

# 12. Cross-validation curve
plt.figure(figsize=(7, 5))
plt.plot(learning_rates, cv_scores, marker="o", label="5-fold CV MSE")
plt.title("Learning Rate vs Cross-Validation Error")
plt.xlabel("Learning rate")
plt.ylabel("Average validation MSE")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 13. Interpretation
print("\\nINTERPRETATION")
print("Best learning rate:", best_lr)
print("Lower MSE and MAE indicate smaller prediction errors.")
print("R2 closer to 1 indicates a better fit.")
print("Training loss should decrease during gradient descent.")
print("Residuals should be randomly distributed around zero.")
