"""Implementation of algorithm 1.

Reference: Lin, Shang-Chien, et al. "A Dynamic Programming Approach to
           Optimal Lane Merging of Connected and Autonomous Vehicles." 2020
           IEEE Intelligent Vehicles Symposium (IV). IEEE, 2020.
"""
import numpy as np


A = 0
B = 1
INT_MAX = np.iinfo(np.int32).max


def min_car(a_arrival_time, b_arrival_time):
    """Return the lane of the car with less earliest arrival time."""
    if a_arrival_time < b_arrival_time:
        return A
    else:
        return B


def main(ai, bi, weq, wadd):
    """Solves two-lane merging problem.
    
    Arguments:
    ai -- A sequence of earliest arrival times of cars in lane A.
    bi -- A sequence of earliest arrival times of cars in lane B.
    weq -- Waiting time for two consecutive vehicles from the same incoming
           lane.
    wadd -- Waiting time for two consecutive vehicles from different incoming
            lane.
    
    Return:
    (result, order)
    result -- Minimized entering time of the last vehicle.
    order -- A possible entering order to achieve the minimized result.
    """

    ai = np.array([0, *sorted(ai)])
    bi = np.array([0, *sorted(bi)])

    L = np.zeros((2, ai.size, bi.size))
    L_record = np.zeros((2, ai.size, bi.size))
    for i in range(2):
        for j in range(ai.size):
            for k in range(bi.size):
                L_record[i][j][k] = 10  
    L[A, 0, 0] = L[B, 0, 0] = 0
    L[A, 1, 0] = ai[1]
    L[B, 0, 1] = bi[1]
    for i in range(2, ai.size):
        L[A, i, 0] = max(ai[i], L[A, i - 1, 0] + weq)
    for j in range(2, bi.size):
        L[B, 0, j] = max(bi[j], L[B, 0, j - 1] + weq)
    for i in range(1, ai.size):
        L[B, i, 0] = INT_MAX
    for j in range(1, bi.size):
        L[A, 0, j] = INT_MAX
    
    for i in range(1, ai.size):
        for j in range(1, bi.size):
            last_a_second_last_a = max(ai[i], L[A, i - 1, j] + weq)
            last_a_second_last_b = max(ai[i], L[B, i - 1, j] + wadd)
            L[A, i, j] = min(last_a_second_last_a, last_a_second_last_b)
            if min_car(last_a_second_last_a, last_a_second_last_b) == A:
                L_record[A, i, j] = L_record[A, i - 1, j] * 10
            else:
                L_record[A, i, j] = L_record[B, i - 1, j]*10 + 1
            
            last_b_second_last_a = max(bi[j], L[A, i, j - 1] + wadd)
            last_b_second_last_b = max(bi[j], L[B, i, j - 1] + weq)
            L[B, i, j] = min(last_b_second_last_a, last_b_second_last_b)
            if min_car(last_b_second_last_a, last_b_second_last_b) == A:
                L_record[B, i, j] = L_record[A, i, j - 1] * 10
            else:
                L_record[B, i, j] = L_record[B, i, j - 1]*10 + 1
    last_a = L[A, ai.size - 1, bi.size - 1]
    last_b = L[B, ai.size - 1, bi.size - 1]
    result = min(last_a, last_b)
    if min_car(last_a, last_b) == A:
        num = int(L_record[A, ai.size - 1, bi.size - 1] * 10)
    else:
        num = int(L_record[B, ai.size - 1, bi.size - 1]*10 + 1)
    order = ''
    while num >= 10:
        if num % 10 == A:
           order = 'A' + order
        else:
           order = 'B' + order
        num //= 10
    return result, order


if __name__ == '__main__':
    """Run the algorithm using arguments given in table II."""
    ai = (1, 3)
    bi = (2, 4)
    weq = 1
    wadd = 3
    result, order = main(ai, bi, weq, wadd)
    print(f'Result: {result}')
    print(f'Order: {order}')
