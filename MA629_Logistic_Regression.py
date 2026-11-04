# MA629 LAB EXAM - LOGISTIC REGRESSION FROM SCRATCH
# Dataset: data_logi.csv (no header; last column is the binary target)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, roc_curve, classification_report, log_loss
)

np.random.seed(42)

# 1. LOAD AND EXPLORE DATA
data = pd.read_csv("data_logi.csv", header=None)
print("Dataset shape:", data.shape)
print(data.head())
print("Missing values:\n", data.isnull().sum())

data = data.dropna()
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

if not np.issubdtype(y.dtype, np.number):
    y = LabelEncoder().fit_transform(y)
y = y.astype(int)

classes = np.unique(y)
if len(classes) != 2:
    raise ValueError("This program expects a binary classification target.")
if not np.array_equal(classes, np.array([0, 1])):
    y = (y == classes[1]).astype(int)

print("Number of samples:", len(X))
print("Number of features:", X.shape[1])
print("Class distribution:\n", pd.Series(y).value_counts())

X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 2. LOGISTIC REGRESSION MODEL FROM SCRATCH

def sigmoid(z):
    z = np.clip(z, -500, 500)
    return 1 / (1 + np.exp(-z))

def hypothesis(X, W):
    return sigmoid(np.dot(X, W))

def cost_function(X, y, W):
    m = len(y)
    eps = 1e-15
    p = np.clip(hypothesis(X, W), eps, 1 - eps)
    return -(1 / m) * np.sum(y * np.log(p) + (1 - y) * np.log(1 - p))

def add_bias(X):
    return np.c_[np.ones((X.shape[0], 1)), X]

def gradient_descent(X, y, learning_rate, epochs):
    m, n = X.shape
    W = np.zeros(n)
    loss_history = []
    for epoch in range(epochs):
        p = hypothesis(X, W)
        gradient = (1 / m) * np.dot(X.T, (p - y))
        W = W - learning_rate * gradient
        loss_history.append(cost_function(X, y, W))
    return W, loss_history

# 3. STRATIFIED 5-FOLD CROSS-VALIDATION
# Scaling is fitted separately inside each fold to prevent data leakage.
learning_rates = [0.001, 0.01, 0.05, 0.1]
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = []

for lr in learning_rates:
    fold_losses = []
    for train_idx, val_idx in skf.split(X_train_raw, y_train):
        X_fold_train = X_train_raw[train_idx]
        X_fold_val = X_train_raw[val_idx]
        y_fold_train = y_train[train_idx]
        y_fold_val = y_train[val_idx]

        fold_scaler = StandardScaler()
        X_fold_train = fold_scaler.fit_transform(X_fold_train)
        X_fold_val = fold_scaler.transform(X_fold_val)

        X_fold_train = add_bias(X_fold_train)
        X_fold_val = add_bias(X_fold_val)

        W_fold, _ = gradient_descent(
            X_fold_train, y_fold_train, learning_rate=lr, epochs=2000
        )
        val_prob = hypothesis(X_fold_val, W_fold)
        fold_losses.append(log_loss(y_fold_val, val_prob, labels=[0, 1]))

    mean_loss = np.mean(fold_losses)
    cv_scores.append(mean_loss)
    print(f"Learning rate {lr}: mean CV log loss = {mean_loss:.4f}")

best_lr = learning_rates[int(np.argmin(cv_scores))]
print("Best learning rate:", best_lr)

# 4. FINAL TRAINING (fit scaler only on training data)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_raw)
X_test_scaled = scaler.transform(X_test_raw)

X_train = add_bias(X_train_scaled)
X_test = add_bias(X_test_scaled)

W, loss_history = gradient_descent(
    X_train, y_train, learning_rate=best_lr, epochs=3000
)
print("Learned parameters:", W)
print("Initial loss:", loss_history[0])
print("Final loss:", loss_history[-1])

# 5. TEST-SET EVALUATION
y_prob = hypothesis(X_test, W)
y_pred = (y_prob >= 0.5).astype(int)

print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, zero_division=0))
print("Recall:", recall_score(y_test, y_pred, zero_division=0))
print("F1-score:", f1_score(y_test, y_pred, zero_division=0))
print("ROC-AUC:", roc_auc_score(y_test, y_prob))
print("Classification report:\n", classification_report(y_test, y_pred, zero_division=0))

# 6. PLOTS

# Loss curve
plt.figure(figsize=(7, 4))
plt.plot(loss_history, label="Training loss")
plt.title("Logistic Regression - Loss Curve")
plt.xlabel("Epoch")
plt.ylabel("Binary Cross-Entropy Loss")
plt.legend()
plt.grid(True)
plt.show()

# ROC curve
fpr, tpr, _ = roc_curve(y_test, y_prob)
auc_value = roc_auc_score(y_test, y_prob)
plt.figure(figsize=(6, 5))
plt.plot(fpr, tpr, label=f"ROC curve (AUC = {auc_value:.3f})")
plt.plot([0, 1], [0, 1], "--", label="Random classifier")
plt.title("ROC Curve")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend()
plt.grid(True)
plt.show()

# Cross-validation curve
plt.figure(figsize=(7, 4))
plt.plot(learning_rates, cv_scores, marker="o", label="Mean 5-fold CV log loss")
plt.xscale("log")
plt.title("Cross-Validation Curve")
plt.xlabel("Learning Rate")
plt.ylabel("Mean Validation Log Loss")
plt.legend()
plt.grid(True)
plt.show()

# Decision boundary
# If there is one feature, show probability vs feature.
# If there are two or more features, plot the first two and hold others at their means.
if X.shape[1] == 1:
    order = np.argsort(X_test_scaled[:, 0])
    plt.figure(figsize=(7, 4))
    plt.scatter(X_test_scaled[:, 0], y_test, alpha=0.7, label="Actual class")
    plt.plot(X_test_scaled[order, 0], y_prob[order], color="red",
             label="Predicted probability")
    plt.axhline(0.5, linestyle="--", label="Decision threshold")
    plt.title("Logistic Regression Decision Boundary")
    plt.xlabel("Standardized feature")
    plt.ylabel("Class / Probability")
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    x_min, x_max = X_train_scaled[:, 0].min() - 1, X_train_scaled[:, 0].max() + 1
    y_min, y_max = X_train_scaled[:, 1].min() - 1, X_train_scaled[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                         np.linspace(y_min, y_max, 200))
    grid = np.tile(np.mean(X_train_scaled, axis=0), (xx.size, 1))
    grid[:, 0] = xx.ravel()
    grid[:, 1] = yy.ravel()
    probabilities = hypothesis(add_bias(grid), W).reshape(xx.shape)

    plt.figure(figsize=(7, 5))
    plt.contourf(xx, yy, probabilities, levels=[0, 0.5, 1], alpha=0.25)
    plt.contour(xx, yy, probabilities, levels=[0.5], linewidths=2)
    plt.scatter(X_train_scaled[:, 0], X_train_scaled[:, 1],
                c=y_train, edgecolors="k", label="Training samples")
    plt.title("Logistic Regression Decision Boundary")
    plt.xlabel("Feature 1 (standardized)")
    plt.ylabel("Feature 2 (standardized)")
    plt.legend()
    plt.grid(True)
    plt.show()

print("Interpretation:")
print("- The loss curve should decrease during training.")
print("- The confusion matrix shows correct and incorrect predictions.")
print("- The best learning rate is selected using the lowest mean 5-fold validation log loss.")
print("- Accuracy, precision, recall, F1-score and ROC-AUC summarize test performance.")
