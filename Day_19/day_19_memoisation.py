from collections import defaultdict

def find_all_combinations(target, items):
    memo = {}
    n = len(target)

    # Precompute prefix map
    prefix_map = defaultdict(list)
    for item in items:
        prefix_map[item[0]].append(item)

    def backtrack(start):
        if start in memo:
            return memo[start]
        if start == n:
            return [[]]

        solutions = []
        if target[start] in prefix_map:
            for item in prefix_map[target[start]]:
                if target.startswith(item, start):
                    sub_solutions = backtrack(start + len(item))
                    for sub_solution in sub_solutions:
                        solutions.append([item] + sub_solution)

        memo[start] = solutions
        return solutions

    return backtrack(0)

# Example usage
target = 'brwrr'
items = ['r', 'wr', 'b', 'br']
solutions = find_all_combinations(target, items)
print("All solutions:")
for solution in solutions:
    print(solution)
