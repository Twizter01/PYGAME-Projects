import time
from rich.panel import Panel
from rich.console import Console
HAS_RICH = True

DEXTER_ASCII = r"""
██████╗ ███████╗██╗  ██╗████████╗███████╗██████╗ 
██╔══██╗██╔════╝╚██╗██╔╝╚══██╔══╝██╔════╝██╔══██╗
██║  ██║█████╗   ╚███╔╝    ██║   █████╗  ██████╔╝
██║  ██║██╔══╝   ██╔██╗    ██║   ██╔══╝  ██╔══██╗
██████╔╝███████╗██╔╝ ██╗   ██║   ███████╗██║  ██║
╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
"""
BYE_BYE = r"""
██████╗ ██╗   ██╗███████╗    ██████╗ ██╗   ██╗███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝    ██╔══██╗╚██╗ ██╔╝██╔════╝
██████╔╝ ╚████╔╝ █████╗      ██████╔╝ ╚████╔╝ █████╗  
██╔══██╗  ╚██╔╝  ██╔══╝      ██╔══██╗  ╚██╔╝  ██╔══╝  
██████╔╝   ██║   ███████╗    ██████╔╝   ██║   ███████╗
╚═════╝    ╚═╝   ╚══════╝    ╚═════╝    ╚═╝   ╚══════╝

"""

"""
def print_intro():
    if HAS_RICH:
        console = Console()

        console.print(f"[bold green]{DEXTER_ASCII}[/bold green]")

        console.print(Panel.fit(
            "[bold yellow]  A Pokémon Pokédex  [/bold yellow]\n"
            "[dim]Loyal to the original Emerald Games[/dim]\n"
            "[dim cyan]Developed by Twizter[/dim cyan]",
            border_style="green",
            padding=(0, 4),
        ))

        console.print(f"[green]{POKEBALL}[/green]", justify="center")

        with console.status("[bold green]Loading Pokédex data...[/bold green]", spinner="dots"):
            time.sleep(2)

        console.print("\n[bold green]✔  Pokédex Ready![/bold green]\n")

    else:
        # Fallback — no Rich
        print(DEXTER_ASCII)
        print("  A Pokemon Pokedex")
        print("  Loyal to the original Emerald Games")
        print("  Developed by Twizter\n")
        print(POKEBALL)
        print("Loading", end="")
        for _ in range(3):
            time.sleep(0.5)
            print(".", end="", flush=False)
        print("\nPokedex Ready!\n")

"""



console = Console()

def print_intro(logo: str) -> None:
    if not logo:
        raise TypeError("Logo cannot be None")
        
    if HAS_RICH:
        console.print(DEXTER_ASCII, style='purple', justify='center')
        console.print("[green]Pokedex[/green]", style='dim', justify='center')
        console.print("Developed by [purple]Twizter[/purple] Corp™. ", justify='center', style='dim')
        console.rule()

        with console.status("[green]Loading Pokedex...[/green]", spinner='aesthetic'):
            time.sleep(1)
        console.print("[bold green]✔ Pokedex Ready![/bold green]", justify='center', style='italic')

    else:
        print(logo)
        print("Pokedex")
        print("Developed by Twizter")
        print("_" * len(logo))
        print()
        print("Loading Pokedex", end="")
        for i in range(3):
            print(".", flush=True)
            time.sleep(0.33)
    
