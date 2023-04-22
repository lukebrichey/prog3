import random
import sys
import math
import heapq

max_iter = 25000

# Prepartion function
def pp(nums, P):
    n = len(nums)
    prepartitions = {i: 0 for i in range(1, n + 1)}
    for i in range(n):
        prepartitions[P[i]] += nums[i]

    s1_sum = 0
    s2_sum = 0
    for i, value in prepartitions.items():
        if i % 2 == 0:
            s1_sum += value
        else:
            s2_sum += value

    return abs(s1_sum - s2_sum)

# Calculate residue 
def calc_res(nums, sol, is_pp):
    if len(nums) != len(sol):
        raise ValueError("Array sizes must match.")

    if is_pp:
        new_nums = [0] * len(nums)
        for i in range(len(nums)):
            new_nums[sol[i]] += nums[i]
        return Karmarkar_Karp(new_nums)

    else:
        res = 0
        for i in range(len(nums)):
            res += nums[i] * (1 if sol[i] % 2 == 1 else -1)
        return abs(res)



def Karmarkar_Karp(nums):
    # Check for empty list.
    if not nums:
        raise ValueError("List cannot be empty.")

    nums = [-num for num in nums]  
    heapq.heapify(nums)
    while len(nums) >= 2:
        a = -heapq.heappop(nums) 
        b = -heapq.heappop(nums) 
        heapq.heappush(nums, -(a - b))  

    return -nums[0]  # Negate back for the final result

def rand_sol(n):
    return [random.randint(1, n) for _ in range(n)]

def RepeatedRandom(nums, prepartition):
    n = len(nums)
    P = rand_sol(n)
    best_diff = calc_res(nums, P, prepartition)

    for _ in range(max_iter):
        new_P = rand_sol(n)
        temp_diff = calc_res(nums, new_P, prepartition)

        if temp_diff < best_diff:
            best_diff = temp_diff
            P = new_P

    return best_diff

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
    P = rand_sol(n)
    best_diff = calc_res(nums, P, prepartition)

    for _ in range(max_iter):
        new_P = random_neighbor(P)
        temp_diff = calc_res(nums, new_P, prepartition)

        if temp_diff < best_diff:
            best_diff = temp_diff
            P = new_P

    return best_diff


def T(iter):
    return 10**10 * (0.8)**(iter // 300)

def SimulatedAnnealing(nums, prepartition):
    n = len(nums)
    P = rand_sol(n)
    best_diff = calc_res(nums, P, prepartition)
    best_P = P

    for iter in range(max_iter):
        new_P = random_neighbor(P)
        temp_diff = calc_res(nums, new_P, prepartition)

        if temp_diff < best_diff:
            best_diff = temp_diff
            best_P = P

        delta = temp_diff - calc_res(nums, P, prepartition)
        if delta < 0 or random.random() < math.exp(-delta / T(iter)):
            P = new_P

    return best_diff


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

    flag = int(sys.argv[1])
    algo = int(sys.argv[2])

    if flag == 0:
        with open(sys.argv[3], 'r') as f:
            nums = [int(line) for line in f]

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
        # Run experiments
        instances = []
        for _ in range(50):
            instance = [random.randint(1, 10**12) for _ in range(100)]
            instances.append(instance)

        results = run_experiments(instances)
        average_residues = calculate_average_residues(results)
        print("Average residues:")
        for algo_code, avg_residue in average_residues.items():
            print(f"Algorithm {algo_code}: {avg_residue}")


if __name__ == '__main__':
    main()
