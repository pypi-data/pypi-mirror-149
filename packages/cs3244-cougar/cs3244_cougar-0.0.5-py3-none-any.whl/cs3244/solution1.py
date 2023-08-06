import matplotlib.pyplot as plt
import torch


def error_gradient(weights_current, inputs, targets):
    return inputs.T @ (inputs @ weights_current - targets)

def gradient_descent(weights_initial, inputs, targets, learning_rate, num_iterations):
    weights = weights_initial
    for i in range(num_iterations):
        weights -= learning_rate * error_gradient(weights, inputs, targets)
    return weights

def visualize_model(weights, inputs, targets):
    fig, ax = plt.subplots()
    outputs = inputs @ weights
    ax.scatter(inputs[:, 1], targets, color="r")
    ax.plot(inputs[:, 1], outputs, color="g")
    return fig

def gradient_descent_with_logger(weights_initial, inputs, targets, learning_rate, num_iterations):
    weights = weights_initial
    errors = []
    for i in range(num_iterations):
        error = 0.5 * (targets - inputs @ weights).T @ (targets - inputs @ weights)
        errors.append(error.item())
        weights -= learning_rate * error_gradient(weights, inputs, targets)
    error = 0.5 * (targets - inputs @ weights).T @ (targets - inputs @ weights)
    errors.append(error.item())
    errors = torch.Tensor(errors)
    return weights, errors

def visualize_errors(initial_weights, inputs, targets, learning_rates, num_iterations):
    fig, ax = plt.subplots()
    for learning_rate in learning_rates:
        weights = initial_weights.clone()
        _, errors = gradient_descent_with_logger(weights, inputs, targets, learning_rate, num_iterations)
        ax.plot(errors, label=learning_rate)
    ax.legend()
    return fig
