from Rooms.rooms import ROOMS, Room
from dataclasses import dataclass, field
from story import logo, story_intro
from typing import Any, Callable
import sys

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    print("Rich not found")

console = Console() if HAS_RICH else None

# Player Class
@dataclass
class Player:
    name: str = "Anaxamines"
    age: int = 47
    current_room: str = "cave_entrance"
    moves: int = 0
    health: float = 100.00
    win: bool = False

    def is_alive(self) -> bool:
        return self.health > 0
    
    
    def status(self) -> str:
        if HAS_RICH:
            console.print(Table(title="Player Stats"), )
        else:
            print(f'{self.name} | {self.health} | {self.current_room}')

    def move(self, direction: str) -> tuple[bool, str]:
        room = ROOMS[self.current_room]

        exits = room.get("exits", {})

        if direction not in exits:
            return False, f'You cannot move {direction} from here!'
        else:
            self.moves += 1
            new_room = exits[direction]

        self.current_room = new_room

        return True, ""

# CMD Command Functions
def print_room(player: Player) -> bool:
    room = player.current_room

    if HAS_RICH:
        console.print(Panel(
            ROOMS[room]["description"], title=room, border_style="cyan"
        ))
    else:
        print(ROOMS[room]['description'])

    return True

def print_intro(logo: str, intro_msg: str) -> str:
    if HAS_RICH:
        console.print(logo)
        console.print(intro_msg)
    else:
        print(logo)
        print(intro_msg)

def look(player: Player) -> bool:
    room = ROOMS[player.current_room]
    if HAS_RICH:
        print_room(player)
    else:
        print(room["description"])

    return True


def quit_game(player: Player) -> None:
    if HAS_RICH:
        console.print(Panel("[slate_blue3]You run towards the light and escape the cave, you live yet another day![/slate_blue3]", title="Game Over", border_style="yellow"
    ))
    else:
        print("You run towards the light and escape the cave, you live yet another day!")

    sys.exit()


# DISPATCH MAP / COMMAND TABLE
COMMANDS_MAP: dict[str, Callable[[Player], None]] = {
    'look': look,
    'escape': quit_game
}

DIRECTIONS: set[str] = {"west", "east", "south", "north", "up", "down"}



def game_loop(player: Player) -> None:
    while True:
        try:
            player_command = input(">").strip().lower()
        except(EOFError, KeyboardInterrupt):
            quit_game(player)
            sys.exit()
                
        if player_command in DIRECTIONS:
            succesful, msg = player.move(player_command)
            if succesful:
                print_room(player)
                continue
            else:
                console.print(f'[cyan]{msg}[/cyan]')

        if player_command in COMMANDS_MAP:
            COMMANDS_MAP[player_command](player)
            continue
        
        console.print(f'Unknown move, {player_command} is not recognized')

def main() -> None:
    print_intro(logo, story_intro)
    player = Player()
    print_room(player)
    game_loop(player)


if __name__ == '__main__':
    main()