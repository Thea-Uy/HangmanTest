import sys
from enum import Enum
from dataclasses import dataclass

class Direction(Enum):
    """Movement Directions"""
    NORTH = "n"
    SOUTH = "s"
    WEST = "w"
    EAST = "e"

class SamuraiState(Enum):
    """Samurai states: stationary, charging, resting"""
    STATIONARY = "stationary"  # Can receive charging orders
    CHARGING = "charging"  # Moving state
    RESTING = "resting"  # Immune after winning duel

@dataclass
class Samurai:
    """Samurai power and state assignment"""
    power: int
    state: SamuraiState = SamuraiState.STATIONARY
    dueled_this_round: bool = False

# Default direction offset map for computations
DIRECTION_MAP: dict[Direction, tuple[int, int]] = {
    Direction.NORTH: (-1, 0),
    Direction.SOUTH: (1, 0),
    Direction.WEST: (0, -1),
    Direction.EAST: (0, 1),
}

def initial_grid(n: int) -> list[list[Samurai | None]]:
    """Create an empty n×n grid."""
    return [[None for _ in range(n)] for _ in range(n)]

def spawn_samurai(grid: list[list[Samurai | None]], n: int) -> bool:
    """Spawn power-1 samurai at rightmost empty cell of the lowest available row."""
    # Check from bottom rightmost cell first in each row
    for row in reversed(range(n)):
        for col in reversed(range(n)):
            if grid[row][col] is None:
                grid[row][col] = Samurai(power=1, state=SamuraiState.STATIONARY)
                return True
    # If field is completely full:
    return False

def charge_all(grid: list[list[Samurai | None]], direction: Direction) -> None:
    """Order all stationary samurai to charge until stationary."""
    n = len(grid)

    # Make all stationary samurai charge
    for r in range(n):
        for c in range(n):
            samurai = grid[r][c]
            if samurai:
                if samurai.state == SamuraiState.STATIONARY:
                    samurai.state = SamuraiState.CHARGING
                samurai.dueled_this_round = False

    # Continue movement until all samurai are stationary or resting
    while True:
        # Determine analysis order to avoid conflicts
        rows = list(reversed(range(n))) if direction == Direction.SOUTH else list(range(n))
        cols = list(reversed(range(n))) if direction == Direction.EAST else list(range(n))

        # Track all charging samurai
        charging_positions: list[tuple[int, int, Samurai]] = []
        for r in rows:
            for c in cols:
                samurai = grid[r][c]
                if samurai is not None and samurai.state == SamuraiState.CHARGING:
                    charging_positions.append((r, c, samurai))

        if not charging_positions:
            # No more charging samurai
            break

        any_movement = False
        for r, c, samurai in charging_positions:
            # Verify samurai is still at this position and state hasn't changed
            if (grid[r][c] is samurai and
                samurai.state == SamuraiState.CHARGING and
                not samurai.dueled_this_round):

                moved = move_samurai(grid, r, c, direction)
                any_movement = any_movement or moved
            # Else: samurai has moved or changed state, skip processing

        if not any_movement:
            # No samurai moved this iteration
            break

def get_next_position(r: int, c: int, direction: Direction) -> tuple[int, int]:
    """Return next (r, c) given direction."""
    dr, dc = DIRECTION_MAP[direction]
    return r + dr, c + dc

def move_samurai(
    grid: list[list[Samurai | None]],
    r: int,
    c: int,
    direction: Direction
) -> bool:
    """Move one charging samurai one cell and resolve collisions."""
    samurai = grid[r][c]
    if samurai is None or samurai.state != SamuraiState.CHARGING:
        return False

    new_r, new_c = get_next_position(r, c, direction)
    n = len(grid)

    if 0 <= new_r < n and 0 <= new_c < n:
        target = grid[new_r][new_c]
        if target is None:
            # Move to empty cell
            grid[new_r][new_c] = samurai
            grid[r][c] = None
            return True
        else:
            # Collision with another samurai
            return handle_collision(
                grid, samurai, target, (r, c), (new_r, new_c)
            )
    else:
        # Out of bounds (edge of field)
        samurai.state = SamuraiState.STATIONARY
        return False

def handle_collision(
    grid: list[list[Samurai | None]],
    charger: Samurai,
    target: Samurai,
    charger_pos: tuple[int, int],
    target_pos: tuple[int, int]
) -> bool:
    """Resolve collision: rest on resting, duel on equal, stop on unequal."""
    if target.state == SamuraiState.STATIONARY and charger.power == target.power:
        # Equal power collision results in duel
        charger.power += 1  # Victor becomes stronger
        charger.state = SamuraiState.RESTING  # Victor must rest after duel
        grid[target_pos[0]][target_pos[1]] = charger  # Victor occupies target's cell
        grid[charger_pos[0]][charger_pos[1]] = None  # Remove charger from original position
        charger.dueled_this_round = True  # Prevent multiple duels in same round
        return True
    else:
        # Unequal power collision stops the charger and target.state == SamuraiState.RESTING
        charger.state = SamuraiState.STATIONARY
        return False

def is_game_over(grid: list[list[Samurai | None]]) -> bool:
    """Return True if field is full and no direction can increase power."""

    # Check if field is full
    field_full = all(cell is not None for row in grid for cell in row)

    if not field_full:
        return False
    # Field is full, check if any command can increase power
    for test_dir in Direction:
        if can_increase_power(grid, test_dir):
            return False
    return True

def can_increase_power(grid: list[list[Samurai | None]], test_dir: Direction) -> bool:
    """Return True if issuing test_dir could yield any duel."""
    n = len(grid)

    for r in range(n):
        for c in range(n):
            samurai = grid[r][c]
            if samurai is not None:
                if samurai.state == SamuraiState.RESTING:
                    # Resting samurai don't participate in new charges
                    continue
                elif samurai.state == SamuraiState.STATIONARY:
                    # Test all stationary samurai in all directions
                    new_r, new_c = get_next_position(r, c, test_dir)

                    if 0 <= new_r < n and 0 <= new_c < n:
                        # Check bounds
                        target = grid[new_r][new_c]
                        if target is not None:
                            # Empty Cell
                            if (target.state != SamuraiState.RESTING and
                                samurai.power == target.power):
                                # Target can be dueled
                                return True  # Duel possible, power could increase

    return False

def print_grid(grid: list[list[Samurai | None]]) -> None:
    """Print field as <r>,<c>: <v> with row separators and round delimiter."""
    n = len(grid)
    for r in range(n):
        for c in range(n):
            cell = grid[r][c]
            power = cell.power if cell is not None else 0
            print(f"{r},{c}: {power}")

        if r < n - 1:
            # Print separator after each row except the last
            print("---")

    print("=====")

def reset_resting_samurai(grid: list[list[Samurai | None]]) -> None:
    """Set all resting samurai to stationary before a new order."""
    for row in grid:
        for samurai in row:
            if samurai is not None:
                if samurai.state == SamuraiState.RESTING:
                    samurai.state = SamuraiState.STATIONARY
                # Else: samurai is stationary or charging, no change needed

def process_valid_command(
    grid: list[list[Samurai | None]],
    user_command: str,
    n: int
) -> bool:
    """Execute a valid direction, spawn, print, and return whether game ends."""
    # Reset resting samurai
    reset_resting_samurai(grid)

    direction = Direction(user_command)
    charge_all(grid, direction)
    spawn_samurai(grid, n)
    print_grid(grid)

    # Check game over condition
    if is_game_over(grid):
        print("Game over")
        return True
    else:
        return False

def get_user_input() -> str | None:
    """Read a line; normalize to lowercase; on EOF print Done and return None."""
    try:
        return input().strip().lower()
    except EOFError:
        # Command + D
        print("Done")
        return None

def validate_arguments() -> int:
    """Parse and validate N from argv (1 ≤ N ≤ 10)."""
    if len(sys.argv) != 2:
        print("Usage: python3 lab01.py <N>", file=sys.stderr)
        sys.exit(1)
    else:
        try:
            n = int(sys.argv[1])
            if 1 <= n <= 10:
                return n
            else:
                print("Error: N must be between 1 and 10", file=sys.stderr)
                sys.exit(1)
        except ValueError:
            print("Error: N must be an integer", file=sys.stderr)
            sys.exit(1)

def main() -> None:
    """Run the main loop: init, print, read commands, update, check end."""
    n = validate_arguments()

    # Initialize field and spawn first samurai per game rules
    grid = initial_grid(n)
    spawn_samurai(grid, n)
    print_grid(grid)

    # Main game loop
    while True:
        user_command = get_user_input()

        if user_command is None:
            # EOF or interrupt encountered
            break
        elif user_command == "":
            # Empty input, continue waiting
            continue
        elif user_command in ('n', 's', 'w', 'e'):
            # Valid command
            game_ended = process_valid_command(grid, user_command, n)
            if game_ended:
                break
        else:
            # Entering anything invalid should be ignored
            continue

if __name__ == "__main__":
    main()
