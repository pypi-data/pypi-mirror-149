from . import solution1
import torch


torch.manual_seed(3244)

def generate_data(weights_true, num_samples):
    uniform = torch.distributions.uniform.Uniform(0, 5)
    normal = torch.distributions.normal.Normal(0, 1)
    inputs = torch.hstack((torch.ones(num_samples, 1), uniform.sample([num_samples, 1])))
    targets = torch.matmul(inputs, weights_true) + normal.sample([num_samples])
    return inputs, targets

def to_message(testcase_id, is_correct):
    if is_correct:
        return f"Test Case {testcase_id:02} ✓"
    return f"Test Case {testcase_id:02} ✗"

def allclose(tensor1, tensor2):
    if not(torch.is_tensor(tensor1) and torch.is_tensor(tensor2)):
        return False
    if tensor1.shape != tensor2.shape:
        return False
    return torch.allclose(tensor1, tensor2)


def grade_11_helper(testcase_id, error_gradient, weights_true, weights_current):
    inputs, targets = generate_data(weights_true, 30)
    student_output = error_gradient(weights_current.clone(), inputs.clone(), targets.clone())
    teacher_output = solution1.error_gradient(weights_current.clone(), inputs.clone(), targets.clone())
    is_correct = allclose(student_output, teacher_output)
    print(to_message(testcase_id, is_correct))

def grade_11(error_gradient):
    grade_11_helper(1, error_gradient, torch.Tensor([2.0, 3.0]), torch.Tensor([1.0, 1.0]))
    grade_11_helper(2, error_gradient, torch.Tensor([0.5, -1.0]), torch.Tensor([0.5, -1.0]))
    grade_11_helper(3, error_gradient, torch.Tensor([-1.5, 1.5]), torch.Tensor([0.0, 0.0]))


def grade_12_helper(testcase_id, gradient_descent, weights_true, weights_initial):
    inputs, targets = generate_data(weights_true, 30)
    learning_rate = 0.001
    num_iterations = 20
    student_output = gradient_descent(weights_initial.clone(), inputs.clone(), targets.clone(), learning_rate, num_iterations)
    teacher_output = solution1.gradient_descent(weights_initial.clone(), inputs.clone(), targets.clone(), learning_rate, num_iterations)
    is_correct = allclose(student_output, teacher_output)
    print(to_message(testcase_id, is_correct))

def grade_12(gradient_descent):
    grade_12_helper(1, gradient_descent, torch.Tensor([2.0, 3.0]), torch.Tensor([1.0, 1.0]))
    grade_12_helper(2, gradient_descent, torch.Tensor([0.5, -1.0]), torch.Tensor([0.5, -1.0]))
    grade_12_helper(3, gradient_descent, torch.Tensor([-1.5, 1.5]), torch.Tensor([0.0, 0.0]))


def grade_14_helper(testcase_id, gradient_descent_with_logger, weights_true, weights_initial):
    inputs, targets = generate_data(weights_true, 30)
    learning_rate = 0.001
    num_iterations = 20
    _, student_output = gradient_descent_with_logger(weights_initial.clone(), inputs.clone(), targets.clone(), learning_rate, num_iterations)
    _, teacher_output = solution1.gradient_descent_with_logger(weights_initial.clone(), inputs.clone(), targets.clone(), learning_rate, num_iterations)
    is_correct = allclose(student_output, teacher_output)
    print(to_message(testcase_id, is_correct))

def grade_14(gradient_descent_with_logger):
    grade_14_helper(1, gradient_descent_with_logger, torch.Tensor([2.0, 3.0]), torch.Tensor([1.0, 1.0]))
    grade_14_helper(2, gradient_descent_with_logger, torch.Tensor([0.5, -1.0]), torch.Tensor([0.5, -1.0]))
    grade_14_helper(3, gradient_descent_with_logger, torch.Tensor([-1.5, 1.5]), torch.Tensor([0.0, 0.0]))
