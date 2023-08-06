"""
    A main driver script for running ride automation sequences via the CLI.
"""
import typer

from ridesims.rides.Everest import main as everest
from ridesims.rides.SplashMountain import main as splashmtn


app = typer.Typer(
    help="An app for running automated ride sequences."
)

@app.command("list-rides")
def list_rides():
    """Provide a list of valid ride names that can run an automated
    sequence.
    """
    print("------------------------------------------------------\n")
    rides_list = [
        "Everest",
    ]
    coming_soon_list = [
        "SplashMountain",
    ]
    print("Available rides: \n")
    for ride in rides_list:
        typer.secho(f"- {ride}", fg="blue")

    print("\n------------------------------------------------------\n")
    print("Rides coming soon: \n")
    for ride in coming_soon_list:
        typer.secho(f"- {ride}", fg="green")

    print("------------------------------------------------------\n")


@app.command()
def run_automated(ride_name: str | None = None) -> None:
    """Run a ride sequence provided the name of the ride. """

    # [CASE] Ride name argument is NOT provided:
    if ride_name is None:
        # Prompt to the user to provide the ride name:
        ride_name = typer.prompt("\nEnter a ride name")
        
    # Match ride_name to a ride sequence:
    match ride_name.lower():
        case 'everest':
            everest.run_automated()

        case 'splashmountain':
            # splashmtn.run_automated()
            typer.secho("\nSequence not yet available. ", fg="yellow")
            typer.Exit()


        # Fallback:
        case _:
            typer.secho(
                message=f"Ride '{ride_name}' not found!",
                fg=typer.colors.RED
            )
            typer.Exit()
