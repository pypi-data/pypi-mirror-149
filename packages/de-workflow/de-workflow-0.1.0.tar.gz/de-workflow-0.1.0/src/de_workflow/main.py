from typing import Optional
import typer
from rich import print
import pathlib
from . import utils

app = typer.Typer()


@app.command()
def execute(
    file_name: pathlib.Path = typer.Argument(..., help="File to extract drugs from"),
    id_column: str = typer.Argument(
        ..., help="The column containing the id for joining"
    ),
    target_columns: tuple[str, str] = typer.Argument(..., help="The columns to search"),
    analyze: bool = typer.Option(
        False, "--analyze", help="Analyze the data. Default is False"
    ),
    live: bool = typer.Option(
        False, "--live", help="Use live data from our github repo. Default is False"
    ),
    search_file: Optional[str] = typer.Option(
        None,
        help="File containing search terms. Use if not using our sample data (i.e. live is false). Default is None",
    ),
):
    print("[cyan]Running wrapper program...")
    utils.run(file_name, id_column, target_columns, analyze, live, search_file)
    print("[green]Finished wrapper program!")
