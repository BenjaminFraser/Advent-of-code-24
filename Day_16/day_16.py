import heapq
import numpy as np

def read_raw_text(filename):
    """ Read entire file as a single string. """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            file_data = file.read()  
        print("File successfully read.")
    except FileNotFoundError:
        print("The specified file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return file_data


def solve_maze(maze, start, end, add_heuristic=False):
    directions = ['N', 'E', 'S', 'W']  # Cardinal directions
    dx_dy = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
    
    def turn_cost(current, new):
        current_idx = directions.index(current)
        new_idx = directions.index(new)
        return 1000 if current_idx != new_idx else 0
    
    def is_valid(x, y):
        return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != '#'
    
    def heuristic(x, y):
        return abs(end[0] - x) + abs(end[1] - y)
    
    # Priority queue for A* search
    pq = []

    # push our initial direction and location to our priority queue
    start_direction = 'E'
    heapq.heappush(pq, (0, start[0], start[1], start_direction))

    # store the parent of all of our states (to maintain route history)
    parent = {}

    # store the lowest cost at which each state was visited
    # if we resit a state with higher or equal cost, we skip (this avoids inf loops)
    visited = {}
    
    while pq:
        cost, x, y, direction = heapq.heappop(pq)
        
        if (x, y) == end:
            # get best path - go through history until we're back at start (no parent)
            path = []
            current = (x, y, direction)
            while current in parent:
                path.append(current)
                current = parent[current]

            # finally add our start state
            path.append((start[0], start[1], start_direction))

            # return cost and path (in order)
            return cost, path[::-1]

        # if we've already visited this state with lower cost, skip
        if (x, y, direction) in visited and visited[(x, y, direction)] <= cost:
            continue

        # add current state and cost
        visited[(x, y, direction)] = cost
        
        # assess movements for current position
        for new_direction in directions:
            new_cost = cost + turn_cost(direction, new_direction)
            nx, ny = x + dx_dy[new_direction][0], y + dx_dy[new_direction][1]
            
            if is_valid(nx, ny):
                new_state = (nx, ny, new_direction)
                if add_heuristic:
                    heapq.heappush(pq, (new_cost + 1 + heuristic(nx, ny), 
                                        nx, ny, new_direction))
                else:
                    heapq.heappush(pq, (new_cost + 1, nx, ny, new_direction))

                # if not already in parent, or new cost is better, add to parent dict
                if new_state not in visited or visited[new_state] > new_cost + 1:
                    parent[new_state] = (x, y, direction)

    # if no path found inf cost, empty list
    return float('inf'), []  


def find_character(grid, character):
    """ Helper function to find specific value(s) in grid. """
    array = np.array(grid).astype(str)
    location = np.where(array == character)
    return list(location[0]), list(location[1])


if __name__ == '__main__':

    print(f'{"-"*50}')
    print(f"{'#'*10} Example Input {'#'*10}")
    print(f'{"-"*50}\n')

    example_maze = read_raw_text('example_input_day_16.txt').split('\n')
    example_maze = [list(x) for x in example_maze]

    start = (13, 1)  # Coordinates of 'S'
    end = (1, 13)    # Coordinates of 'E'

    example_cost, example_route = solve_maze(example_maze, start, end)

    print(f"Final cost for example maze: {example_cost}")
    print(f'{"-"*50}\n')

    print(f'{"-"*50}')
    print(f"{'#'*10} Main Input {'#'*10}")
    print(f'{"-"*50}\n')

    # load input maze data, process, and run our min cost search
    input_maze = read_raw_text('day_16_input.txt').split('\n')
    input_maze = [list(x) for x in input_maze]

    start_x, start_y = find_character(input_maze, 'S')
    end_x, end_y = find_character(input_maze, 'E')

    input_cost, input_route = solve_maze(input_maze, (start_x[0], start_y[0]), 
                                     (end_x[0], end_y[0]))

    print(f"Final cost: {input_cost}")

    print(f'Size of maze: {len(input_maze)} x {len(input_maze[0])}')