import multiprocessing
from multiprocessing import Manager

def run_program_with_memo(initial_a, program, memo):
    """ Optimized version of the run_program_with_memo function. """
    A, B, C = initial_a, 0, 0
    IP = 0
    output = []

    def resolve_combo_operand(operand):
        """ Optimized combo operand resolver. """
        return {
            4: A,
            5: B,
            6: C
        }.get(operand, operand)

    state_key = (A, B, C, IP)
    if state_key in memo:
        return memo[state_key]

    while IP < len(program):
        opcode = program[IP]
        operand = program[IP + 1] if IP + 1 < len(program) else 0

        try:
            if opcode == 0:  # adv
                A //= 2 ** resolve_combo_operand(operand)
            elif opcode == 1:  # bxl
                B ^= operand
            elif opcode == 2:  # bst
                B = resolve_combo_operand(operand) % 8
            elif opcode == 3:  # jnz
                if A != 0:
                    IP = operand
                    continue
            elif opcode == 4:  # bxc
                B ^= C
            elif opcode == 5:  # out
                output_value = resolve_combo_operand(operand) % 8
                if len(output) >= len(program) or output_value != program[len(output)]:
                    memo[state_key] = False
                    return False
                output.append(output_value)
            elif opcode == 6:  # bdv
                B = A // (2 ** resolve_combo_operand(operand))
            elif opcode == 7:  # cdv
                C = A // (2 ** resolve_combo_operand(operand))
            else:
                raise ValueError(f"Invalid opcode {opcode}")
        except ZeroDivisionError:
            memo[state_key] = False
            return False

        IP += 2

    result = output == program
    memo[state_key] = result
    return result


def worker(program, memo, start, step, result):
    """ Worker function to find the lowest A in a given range. """
    initial_a = start
    while True:
        if run_program_with_memo(initial_a, program, memo):
            result.put(initial_a)
            return
        initial_a += step


def find_lowest_a_with_optimizations(program):
    """ Parallelized search for the lowest A that satisfies the input program. """
    num_workers = multiprocessing.cpu_count()
    manager = Manager()
    memo = manager.dict()
    result = manager.Queue()

    processes = []
    for i in range(num_workers):
        p = multiprocessing.Process(target=worker, args=(program, memo, i + 1, num_workers, result))
        processes.append(p)
        p.start()

    # Wait for any worker to find a result
    lowest_a = result.get()
    for p in processes:
        p.terminate()  # Terminate all processes once result is found

    return lowest_a


if __name__ == "__main__":
    # Define your program input
    #program = [0,3,5,4,3,0]
    program = [2, 4, 1, 1, 7, 5, 1, 5, 4, 0, 5, 5, 0, 3, 3, 0]
    lowest_a = find_lowest_a_with_optimizations(program)
    print(f"The lowest initial A that satisfies the program is: {lowest_a}")