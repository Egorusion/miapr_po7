import math
import random
import matplotlib.pyplot as plt

min_error = 1e-6
training_speed = 0.01


def func(x: float, a: int, b: int, d: float) -> float:
    return a * math.sin(b * x) + d


def my_output(
        weights: list,
        t: float,
        inputs_number: int,
        training_output: list,
        shift: int) -> float:
    output = 0
    for i in range(inputs_number):
        output += weights[i] * training_output[i + shift]
    return output - t


def training(inputs_number: int, training_number: int, training_output: list):
    weights = [random.uniform(-1, 1) for _ in range(inputs_number)]
    t = random.uniform(0.1, 1)
    data_for_drawing = ([], [])
    error = 1
    iter = 0
    while error > min_error:
        error = 0
        iter += 1
        for i in range(training_number - inputs_number):
            output_ = my_output(weights, t, inputs_number, training_output, i)
            for j in range(inputs_number):
                ideal_output = training_output[i + inputs_number]
                weights[j] -= (
                        training_speed * (output_ - ideal_output) * training_output[i + j]
                )
            t += training_speed * (output_ - ideal_output)
            error += (output_ - ideal_output) ** 2
            error /= 2
        data_for_drawing[0].append(iter)
        data_for_drawing[1].append(error)
    return weights, t, data_for_drawing, iter


def main():
    a = 1
    b = 5
    d = 0.1
    inputs_number = 3
    training_number = 33
    testing_number = 18
    step = 0.1
    training_output = [
        func(i * step, a, b, d) for i in range(training_number + inputs_number)
    ]
    testing_output = [
        func(i * step, a, b, d)
        for i in range(training_number, training_number + testing_number)
    ]

    training_weight, training_t, data_for_drawing, epochs = training(
        inputs_number, training_number, training_output
    )

    plt.plot(*data_for_drawing)
    plt.ylabel("Error")
    plt.xlabel("Iteration")
    plt.show()

    print("Результаты обучения:")
    print(f"Веса: {training_weight}, Предел: {training_t}")
    print(
        "{:<25}{:<27}{}".format("Эталонное значение", "Текущее значение", "Погрешность")
    )

    for i in range(training_number - inputs_number):
        output_ = my_output(
            training_weight, training_t, inputs_number, training_output, i
        )
        print(
            f"{training_output[i + inputs_number]:<25} {output_:<25} {(training_output[i + inputs_number] - output_)}"
        )
    print(f'Number of epochs: {epochs}')

    print("\n\nРезультаты тестирования:")
    for i in range(testing_number - inputs_number):
        output_ = my_output(
            training_weight, training_t, inputs_number, testing_output, i
        )
        print(
            f"{testing_output[i + inputs_number]:<25} {output_:<25} {(testing_output[i + inputs_number] - output_)}"
        )


if __name__ == "__main__":
    main()
