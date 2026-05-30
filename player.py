from dataclasses import dataclass, field
from Rooms.rooms import ROOMS, Room, DIRECTIONS
from typing import Callable, Any, NotRequired

try:
    from rich.panel import Panel
    from rich.console import Console
    from rich.box import Box
    from rich.table import Table
    # More Modules Here That Might Fail on Other Environments
    HAS_RICH = True
except ImportError:
    print(f'Rich Not Found')
    HAS_RICH = False

console = Console() if HAS_RICH else None

@dataclass
class Player:
    """Player Class RPG Style"""
    name: str = "Anaxamines"
    age: int = 44
    current_room: dict[str, Room] = 'cave_entrance'
    items: list[Any] = field(default_factory=list)
    moves: int = 0
    health: float = 100.00
    dead: bool = NotRequired[False]

    def is_alive(self) -> bool:
        return self.health > 0
    

    def get_stats(self) -> Table:
        table = Table(title='Stats', style="rounded", show_lines=True)
        table.add_column('Player Name', style='bold green')
        table.add_column('Age', style='cyan')
        table.add_column('Current Room', style='purple')
        table.add_row(self.name, str(self.age), self.current_room)

        console.print(table)


    def move(self, direction: str) -> tuple[bool, str]:
        """Takes in a Direction"""
        """Returns success, message """

        room = ROOMS[self.current_room]
        exits = room.get("exits", {})
            
        if direction not in exits:
            return False, f"[red]You cannot go {direction}[/red]"
        
        self.current_room = exits[direction]
        self.moves += 1

        new_room = ROOMS[self.current_room]

        return True, ""
    

    def player_status(self) -> str:
        return f"[{self.name}]  HP: {self.health:.0f}  |  Moves: {self.moves}  |  Room: {ROOMS[self.current_room]['name']}"

