import random
import sys
import math 

max_iter = 25000

def pp(nums, P):
    n = len(nums)
    prepartitions = {i: [] for i in range(1, n + 1)}
    for i in range(n):
        prepartitions[P[i]].append(nums[i])

    s1 = []
    s2 = []
    for i, subset in prepartitions.items():
        if i % 2 == 0:
            s1.extend(subset)
        else:
            s2.extend(subset)

    return s1, s2


def Karmarkar_Karp(nums):
    s1 = nums 
    s2 = []

    # Keep subtracting the largest number from the second largest number.
    while len(s1) > 1:
        s1.sort(reverse=True)
        s2.append(s1.pop(0) - s1.pop(0))
    
    # Return the difference between the two sets.
    return abs(s1[0] - sum(s2))


# Generate a random solution
def rand_sol(n):
    return [random.randint(1, n) for _ in range(n)]


def RepeatedRandom(nums, prepartition):
    n = len(nums)
    if prepartition:
        P = rand_sol(n)
        s1, s2 = pp(nums, P)
    else:
        s1 = nums
        s2 = []

    best_diff = abs(sum(s1) - sum(s2))

    for _ in range(max_iter):
        new_P = rand_sol(n)
        temp_s1, temp_s2 = pp(nums, new_P) if prepartition else (new_P, [])
        temp_diff = abs(sum(temp_s1) - sum(temp_s2))

        if temp_diff < best_diff:
            best_diff = temp_diff
            s1, s2 = temp_s1, temp_s2

    return best_diff


# Create a random neighbor
def random_neighbor(P):
    n = len(P)
    i = random.randint(0, n - 1)
    j = random.randint(1, n)
    while P[i] == j:
        j = random.randint(1, n)
    new_P = P.copy()
    new_P[i] = j
    return new_P


def HillClimbing(nums, prepartition):
    n = len(nums)
    if prepartition:
        P = rand_sol(n)
        s1, s2 = pp(nums, P)
    else:
        s1 = nums
        s2 = []

    best_diff = abs(sum(s1) - sum(s2))

    for _ in range(max_iter):
        new_P = random_neighbor(P)
        temp_s1, temp_s2 = pp(nums, new_P) if prepartition else (new_P, [])
        temp_diff = abs(sum(temp_s1) - sum(temp_s2))

        if temp_diff < best_diff:
            best_diff = temp_diff
            s1, s2 = temp_s1, temp_s2
            P = new_P

    return best_diff


# Cooling schedule
def T(iter):
    return 10**10 * (0.8)**(iter // 300)


def SimulatedAnnealing(nums, prepartition):
    n = len(nums)
    if prepartition:
        P = rand_sol(n)
        s1, s2 = pp(nums, P)
    else:
        s1 = nums
        s2 = []

    best_diff = abs(sum(s1) - sum(s2))
    best_P = P

    for iter in range(max_iter):
        new_P = random_neighbor(P)
        temp_s1, temp_s2 = pp(nums, new_P) if prepartition else (new_P, [])
        temp_diff = abs(sum(temp_s1) - sum(temp_s2))

        if temp_diff < best_diff:
            best_diff = temp_diff
            best_P = P

        delta = temp_diff - abs(sum(s1) - sum(s2))
        if delta < 0 or random.random() < math.exp(-delta / T(iter)):
            s1, s2 = temp_s1, temp_s2
            P = new_P

    if prepartition:
        s1, s2 = pp(nums, best_P)
    else:
        s1, s2 = best_P, []

    return abs(sum(s1) - sum(s2))


"""
CODE FOR EXPERIMENTS i.e. FLAG 1
"""

def generate_instances(num_instances=50, file_prefix="instance_"):
    for i in range(num_instances):
        with open(f"{file_prefix}{i}.txt", "w") as f:
            for _ in range(100):
                f.write(f"{random.randint(1, 10**12)}\n")

def run_experiments(instances):
    algos = {
        1: RepeatedRandom,
        2: HillClimbing,
        3: SimulatedAnnealing,
        11: RepeatedRandom,
        12: HillClimbing,
        13: SimulatedAnnealing
    }
    
    results = {key: [] for key in algos.keys()}

    for instance in instances:
        for algo_code, algo_func in algos.items():
            prepartition = algo_code >= 11
            result = algo_func(instance, prepartition)
            results[algo_code].append(result)

    return results

def calculate_average_residues(results):
    average_residues = {}
    for algo_code, residues in results.items():
        average_residues[algo_code] = sum(residues) / len(residues)
    return average_residues


def main():
    # Usage: python partition.py <flag> <algorithm> <input file>

    # Get the algorithm and input file 
    flag = int(sys.argv[1])
    algo = int(sys.argv[2])

    # Read the input file
    with open(sys.argv[2], 'r') as f:
        nums = [int(line) for line in f]
    
    # Generate random numbers
    random_integers = [random.randint(1, 10**12) for _ in range(100)]

    if flag == 0:
        with open(sys.argv[3], 'r') as f:
            nums = [int(line) for line in f]    

        # Choose algorithm, args: <nums>, <prepartition>
        if algo == 0:
            print(Karmarkar_Karp(nums))
        elif algo == 1:
            print(RepeatedRandom(nums, False))
        elif algo == 2:
            print(HillClimbing(nums, False))
        elif algo == 3:
            print(SimulatedAnnealing(nums, False))
        elif algo == 11:
            print(RepeatedRandom(nums, True))
        elif algo == 12:
            print(HillClimbing(nums, True))
        elif algo == 13:
            print(SimulatedAnnealing(nums, True))

    elif flag == 1:
        instances = generate_instances()
        results = run_experiments(instances)
        average_residues = calculate_average_residues(results)
        print("Average residues:")
        for algo_code, avg_residue in average_residues.items():
            print(f"Algorithm {algo_code}: {avg_residue}")

    
if __name__ == '__main__':
    main()
