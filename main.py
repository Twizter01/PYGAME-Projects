# =============================================================================
#   ██████╗██╗     ██╗     █████╗ ██████╗ ██╗   ██╗
#  ██╔════╝██║     ██║    ██╔══██╗██╔══██╗██║   ██║
#  ██║     ██║     ██║    ███████║██║  ██║██║   ██║
#  ██║     ██║     ██║    ██╔══██║██║  ██║╚██╗ ██╔╝
#  ╚██████╗███████╗██║    ██║  ██║██████╔╝ ╚████╔╝ 
#   ╚═════╝╚══════╝╚═╝    ╚═╝  ╚═╝╚═════╝   ╚═══╝  
#
#  CLI Adventure Game
#  ---------------------------------------------------------
#  Author      : Twizter
#  Version     : 1.0.0
#  License     : All Rights Reserved © 2026
#  Description : A text-based adventure forged with a hint
#                of Greek passion.
# ==============================================================================


# I. CORE COMPLIANCE (Standard Library Modules)
# ==============================================================================
from dataclasses import dataclass, field
from enum import Enum
import os
from random import choice
import time
from typing import Any, Callable
import sys

# ==============================================================================
# II. EXTERNAL FABRICATIONS (Third-Party Modules)
# ==============================================================================
try:
    import pyfiglet
    from rich.box import Box
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    HAS_RICH = True
except ImportError:
    # A silent warning to the console, preventing crash on primitive terminals
    print("Warning: 'rich' module not found. Falling back to ASCII standard.")
    HAS_RICH = False

# ==============================================================================
# III. LOCAL ARTIFACTS (Project-Specific Modules)
# ==============================================================================
from configfiles import CMD_colors
from player import Player
from Rooms.rooms import Room, ROOMS
from story import story_intro, logo

# ==============================================================================
# IV. INSTANTIATIONS (Global Artifacts)
# ==============================================================================
console = Console() if HAS_RICH else None

def print_title() -> None:
    if HAS_RICH:
        title = pyfiglet.figlet_format("OLD TIMES", font="slant")
        console.print(title, style="bold green")
        console.print("  A CLI Adventure by Twizter\n", style="dim")
    else:
        print("=== OLD TIMES ===")
        print("  A CLI Adventure by Twizter\n")

def print_room(player: Player) -> None:
    room = ROOMS[player.current_room]
    if HAS_RICH:
        console.print(Panel(
            f"[italic]{room['description']}[/italic]",
            title=f"[bold cyan]{room['name']}[/bold cyan]",
            border_style="cyan",
        ))
        # console.print(f"  [dim]{player.status()}[/dim]\n")
    else:
        print(f"\n── {room['name']} ──")
        print(room["description"])
        #print(f"\n{player.status()}\n")


# ===== CMD HELPER FUNCTIONS ===== #
def cmd_help(player: Player) -> bool:
    """Print available commands."""

    help_text = """
                             COMMANDS
  north / south / east / west / up / down   — move in a direction
  look                                      — describe the current room again
  status                                    — show your health and move count
  help                                      — show this message
  quit                                      — give up and leave the cave
"""
    if HAS_RICH:
        console.print(Panel(help_text.strip(), title="[bold]Help[/bold]", border_style="green"))
    else:
        print(help_text)
    return True  # True = keep playing


def clear_screen(player: Player) -> bool:
    os.system('cls' if os.name == 'nt' else 'clear')
    return True


def cmd_quit(player: Player):
    time.sleep(0.8)
    if HAS_RICH:
        console.print(Panel("[cyan]Bye Hero, Thank you for playing![/cyan]",title="Game Over", border_style=CMD_colors.PLAYER_STATS.value))
    else:
        print("Bye Hero, Thank you for playing!")
    sys.exit()


def look(player: Player) -> bool:
    room = ROOMS[player.current_room]
    if HAS_RICH:
        console.print(Panel(
            f"[italic]{room['description']}[/italic]", title=f"[bold cyan]{room['name']}[/bold cyan]", border_style="cyan"))
        
        # console.print(f"  [dim]{player.status()}[/dim]\n")
    else:
        print(f"\n── {room['name']} ──")
        print(room["description"])
        #print(f"\n{player.status()}\n")

    return True


def random_color(color_list: tuple[str, ...]) -> str:
    return choice(color_list)

# ==== DISPATCH MAP -> Dispatch Table ==== #
COMMAND_MAP: dict[str, Callable[[Player], None]] = {
            "help": cmd_help,
            "quit": cmd_quit,
            "look": look,
            # "pick up": "pick_up_item", TODO Add Items that be stored and add some usability
            "talk": lambda talk: print("is anyone there?"),
            "clear screen": clear_screen,
            }


DIRECTIONS = {"north", "south", "east", "west", "up", "down"}

def game_loop(player: Player) -> bool:
    """Main Game Loop"""

    if not player:
        return
    
    while True:
        try:
            raw = input(">").strip()
        except(EOFError, KeyboardInterrupt):
            print() 
            cmd_quit()
            break

        if not raw:
            continue

        if raw in DIRECTIONS:
            success, message = player.move(raw)
            if not success:
                console.log("[red]You Are Screwed, You can't Move that Way!")
                continue

            if message:
                print('message present')


            console.log(f"[slate_blue3]You have moved to {player.current_room}[/slate_blue3]")
            print_room(player)
            continue
            
        # === other commands === #
        if raw in COMMAND_MAP:
            keep_playing = COMMAND_MAP[raw](player)
            if not keep_playing:
                break
            continue
        
        console.log(f"Unknown command, I don't know what {raw} is")
        continue


def main() -> None:
    #print_title()

    time.sleep(1.5)

    if HAS_RICH:
        console.print(logo)
        console.print(Panel(story_intro.strip(), title='[bold]Prologue[/bold]', border_style=random_color(CMD_colors.ROOM_COLORS.value)))
    else: print(story_intro)
    

    player = Player()
    game_loop(player)
    
    

if __name__ == "__main__":
    main()



