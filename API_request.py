import requests
import time
import sys
from typing import Any, Optional
from rich.panel import Panel
from rich.console import Console


console = Console()
URL = f"https://pokeapi.co/api/v2/pokemon/"

"""
def pokemon_view() -> None:
    pokemon = input("Enter a pokemon name: ").lstrip().lower()
    try:
        with console.status("Loading"):
            time.sleep(2)
            response = requests.get(f"{URL}{pokemon}", timeout=5)

            response.raise_for_status()
    except requests.exceptions.Timeout:
        console.log("[yellow]Request TimedOut[/yellow]")
    except requests.exceptions.RequestException as err:
        console.log(f"[red]Request failed {err}[/red]", style='dim')
    data = response.json()
    console.print(data)
    return data

def get_pokemon_info(pokemon: Optional[str]) -> requests.Response:
    name: str = pokemon['name']
    height: int = pokemon['height']
    # print(height)
    
    if height <= 10.0:
        height = round(height * 10, 2)
        pp = Panel(f"Name: {str(name).title()} | Height: {round(height/10, 2)}m", style='cyan', padding=(1, 1))
        console.print(pp)
    else:
        pp = Panel(f"Name: {str(name).title()} | Height: {round(height/10, 2)}m", style='cyan', padding=(1, 1))
        console.print(pp)
    
pokemon_data = pokemon_view()
get_pokemon_info(pokemon_data)

"""

def request_pokemon_data(url: str) -> dict[dict[Any, Any]]:
    if not url:
        console.log(f"[yellow]No API URL Found[/yellow]")
        raise ValueError("Enter a valid URL")
    
    while True:
        try:
            pokemon: str = input('What pokemon are you looking for? : ').strip().lower()

            if not pokemon:
                console.log('[bold cyan]Please enter a pokemon[/bold cyan]')
                continue
            
            pokemon = pokemon.replace(" ", "-")
            response: requests.Response = requests.get(f"{url}{pokemon}", timeout=6)
            response.raise_for_status()

        except KeyboardInterrupt:
            sys.exit()

        except requests.HTTPError as err:
            raise requests.HTTPError(f"Error: {err}")

        except requests.exceptions.RequestException as e:
            console.log(f'[red]Network Error: {e}')
            continue

            
        return response.json()


def display_pokemon_data(pokemon: dict[Any, Any]) -> None:
    pokemon_name: str = pokemon['name']
    pokemon_height: float | int = pokemon['height']

    pokemon_abilities_list: dict[list[Any]] = [ability['ability']['name'] for ability in pokemon['abilities']]
    pokemon_abilities: str = str(", ".join(pokemon_abilities_list)).title()

    # TODO FIX PAST ABILITIES DISPLAY
    #pokemon_past_abilities_list: dict[list[Any]] = [ability['abilities']['ability'] for ability in pokemon['past_abilities']]
    # pokemon_past_abilities: str = str(", ".join(pokemon_past_abilities_list)).title()
    # pokemon_past_abilities = pokemon['past_abilities'][0]

    pokemon_type_list: dict[list[Any]] = [t['type']['name'] for t in pokemon['types']]
    pokemon_types: str = str(", ".join(pokemon_type_list).title())

    pokemon_forms_list: dict[list[Any]] = [e['name']for e in pokemon['forms']]
    pokemon_forms: str = str(", ".join(pokemon_forms_list)).title()

    pokemon_evolutions_list: dict[list[Any]] = pokemon['evolution-chain']

    poketable: Panel = Panel(f"Name: [cyan]{pokemon_name.title()} [/cyan]| Height: [green]{round(pokemon_height/10, 2)}m [/green]| Abilities: [slate_blue3]{pokemon_abilities} [/slate_blue3]\n "
                            # f"\nPast Abilities: {pokemon_past_abilities}\n"
                            f"\nWeight: [green]{pokemon['weight']}Lbs [/green]\n" 
                            f"\nTypes: [green]{pokemon_types} [/green]\n"
                            f"\nForms: [cyan]{pokemon_forms} [/cyan]"
                            f"\nEvolutions: {pokemon_evolutions_list}",
                            style='purple',
                            padding=(0, 1),
                            title=f"{pokemon_name.title()}")
    
    console.print(poketable)

def main() -> None:
    pokemon_data = request_pokemon_data(URL)
    console.print(pokemon_data, style='cyan')
    display_pokemon_data(pokemon_data)


if __name__ == "__main__":
    main()

