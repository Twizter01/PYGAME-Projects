# Dexter, Pokemon Pokedex
# Loyal to the original Emerald Games, Developed By Twizter
"""
██████╗ ███████╗██╗  ██╗████████╗███████╗██████╗ 
██╔══██╗██╔════╝╚██╗██╔╝╚══██╔══╝██╔════╝██╔══██╗
██║  ██║█████╗   ╚███╔╝    ██║   █████╗  ██████╔╝
██║  ██║██╔══╝   ██╔██╗    ██║   ██╔══╝  ██╔══██╗
██████╔╝███████╗██╔╝ ██╗   ██║   ███████╗██║  ██║
╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝"""

# TODO Add env var for the API


import os
import sys
import time
import requests
from typing import Any, Callable
from assets import print_intro, DEXTER_ASCII, BYE_BYE
HAS_RICH = False

try:
    from rich.table import Table
    from rich.box import ROUNDED
    from rich.panel import Panel
    from rich.console import Console
    from rich.text import Text
    HAS_RICH = True

except ImportError:
    print("WARNING: 'rich' is not installed.")
    answer = input("Install it now? (Y/N): ").strip().upper()

    if answer == "Y":
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
            from rich.table import Table
            from rich.box import ROUNDED
            from rich.panel import Panel
            from rich.console import Console
            from rich.text import Text
            HAS_RICH = True
        except (subprocess.CalledProcessError, ImportError):
            print("Installation failed. Run: pip install rich")
    HAS_RICH = False

# === RICH OBJECTS === # 
console = Console(color_system='truecolor')

# CMD HELPER FUNCTIONS
def print_help():
    if HAS_RICH:
        with console.status("[cyan]Loading...[/cyan]"):
            # Here is where you would add your logic/code
            time.sleep(2)
        help_panel = Panel("FUNCTIONS ---------------\n" 
                          " Pokemon Lookup\n"
                          " Pokemon Strategy\n" 
                          " Pokemon Game/Generation\n"
                          " Terms & Conditions\n"
                          " quit\n"
                          " reset",
                         style='cyan')
        console.print(help_panel)
    else:
        print("FUNCTIONS ---------------" \
                          " Pokemon Lookup" \
                          " Pokemon Strategy" \
                          " Pokemon Game/Generation")

def get_pokemon_data(pokemon: requests.Response.json) -> None:
    if not pokemon:
        raise TypeError("")
    

def pokemon_lookup() -> requests.Response:
    URL: str = f"https://pokeapi.co/api/v2/"
    pokemon = input("Enter the Pokemon Name or ID: ").strip().lower()
    # Add verification logic here

    response = requests.get(f"{URL}{pokemon}")
    if response.status_code == 200:
        return response.json()
    else: print("Try Again")


def show_pokemon(pokemon: str) -> None:
    if not pokemon:
        return "I Need a Pokemon!"
    
    name = pokemon['name']
    height = pokemon['height']

    console.print(Panel(f"Name: {name} | height: {height}"))


def print_quit() -> None:
    with console.status("[dim blue]Turning off. ..[/dim blue]"):
        time.sleep(2)
    console.print(BYE_BYE, justify='center', style='dim purple')
    sys.exit()

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def print_terms_and_conditions() -> None:
    console.print("TO BE CONTINUED", end="", style='dim red')
    for _ in range(3):
        time.sleep(1)
        print(".", end="", flush=True)
    with console.status("[dim purple]Sorry[/dim purple]"):
        time.sleep(1)
    

# DISPATCH TABLE
DISPATCH_TABLE: dict[str, Callable] = {
    "help": print_help,
    "terms" : print_terms_and_conditions,
    "quit" : print_quit,
    "clean" : clear_screen,
    "pokemon lookup": pokemon_lookup
}

# USER REQUEST FLOW
def user_request() -> None | str:
    requesting: bool = True
    while requesting:
        console.print(Panel.fit("[blue]How Can I help you today: "))
        request = input("").strip()
        console.print(Panel.fit(f"User Request: {request}"), style='green')
        if request == "quit":
            DISPATCH_TABLE['quit']()
        if request not in DISPATCH_TABLE:
            console.print(Panel.fit(f"[blue]I don't know what [purple]{request}[/purple] is!, Try Again or type help to check the commands available[/blue]"))
            continue
        # elif request.lower() == "lookup pokemon":

        else:
            DISPATCH_TABLE[request]()
    
# TODO Implement an API request to POKEAPI in order to retrieve the desired information
def poke_api() -> str:
    pass



def main() -> None:
    print_intro(DEXTER_ASCII)
    # intro_table = Panel()
    console.print(Panel(user_request(), style='purple'))


if __name__ == "__main__":
    main()



