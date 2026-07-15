"""Terminal display utilities using Rich."""

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

console = Console()


def create_progress() -> Progress:
    """Create a styled progress bar for batch operations."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("({task.completed}/{task.total})"),
        TimeElapsedColumn(),
        console=console,
    )


def print_success(msg: str):
    console.print(f"  [green]✓[/green] {msg}")


def print_error(msg: str):
    console.print(f"  [red]✗[/red] {msg}")


def print_warning(msg: str):
    console.print(f"  [yellow]⚠[/yellow] {msg}")


def print_header(title: str):
    console.print(f"\n[bold cyan]═══ {title} ═══[/bold cyan]\n")
